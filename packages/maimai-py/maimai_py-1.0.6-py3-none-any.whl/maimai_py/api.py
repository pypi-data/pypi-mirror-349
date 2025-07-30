import asyncio
from dataclasses import dataclass
from importlib.util import find_spec
from typing import Annotated, Callable, Literal

from maimai_py import ArcadeProvider, DivingFishProvider, LXNSProvider, MaimaiClient, MaimaiSongs
from maimai_py.exceptions import MaimaiPyError
from maimai_py.maimai import MaimaiPlates, MaimaiScores
from maimai_py.models import *

router = None
asgi_app = None
local_lxns_token = None
local_divingfish_token = None
local_arcade_proxy = None
maimai_client = MaimaiClient()


@dataclass(slots=True)
class ScorePublic(Score):
    song_name: str
    level_value: float


@dataclass(slots=True)
class PlayerBests:
    rating: int
    rating_b35: int
    rating_b15: int
    scores_b35: list[ScorePublic]
    scores_b15: list[ScorePublic]


def pagination(page_size, page, data):
    total_pages = (len(data) + page_size - 1) // page_size
    if page < 1 or page > total_pages:
        return []

    start = (page - 1) * page_size
    end = page * page_size
    return data[start:end]


def xstr(s: str | None) -> str:
    return "" if s is None else str(s).lower()


def istr(i: list | None) -> str:
    return "" if i is None else "".join(i).lower()


def get_filters(functions: dict[Any, Callable[..., bool]]):
    union = [flag for cond, flag in functions.items() if cond is not None]
    filter = lambda obj: all([flag(obj) for flag in union])
    return filter


@staticmethod
async def ser_score(score: Score, songs: dict[int, Song]) -> ScorePublic | None:
    if (song := songs.get(score.id)) and (diff := song.get_difficulty(score.type, score.level_index)):
        return ScorePublic(
            id=score.id,
            song_name=song.title,
            level=score.level,
            level_index=score.level_index,
            level_value=diff.level_value,
            achievements=score.achievements,
            fc=score.fc,
            fs=score.fs,
            dx_score=score.dx_score,
            dx_rating=score.dx_rating,
            rate=score.rate,
            type=score.type,
        )


@staticmethod
async def ser_bests(maimai_scores: MaimaiScores, maimai_songs: MaimaiSongs) -> PlayerBests:
    song_ids = [score.id for score in maimai_scores.scores_b35 + maimai_scores.scores_b15]
    songs: list[Song] = await maimai_songs.get_batch(song_ids) if len(song_ids) > 0 else []
    required_songs: dict[int, Song] = {song.id: song for song in songs}
    async with asyncio.TaskGroup() as tg:
        b35_tasks = [tg.create_task(ser_score(score, required_songs)) for score in maimai_scores.scores_b35]
        b15_tasks = [tg.create_task(ser_score(score, required_songs)) for score in maimai_scores.scores_b15]
    scores_b35, scores_b15 = [v for task in b35_tasks if (v := task.result())], [v for task in b15_tasks if (v := task.result())]
    return PlayerBests(
        rating=maimai_scores.rating,
        rating_b35=maimai_scores.rating_b35,
        rating_b15=maimai_scores.rating_b15,
        scores_b35=scores_b35,
        scores_b15=scores_b15,
    )


if find_spec("fastapi"):
    from fastapi import APIRouter, Depends, FastAPI, Header, Query, Request
    from fastapi.openapi.utils import get_openapi
    from fastapi.responses import JSONResponse

    asgi_app = FastAPI()
    router = APIRouter()

    def dep_lxns(token_lxns: Annotated[str | None, Header()] = None):
        return LXNSProvider(token_lxns or local_lxns_token)

    def dep_diving(token_divingfish: Annotated[str | None, Header()] = None):
        return DivingFishProvider(token_divingfish or local_divingfish_token)

    def dep_arcade():
        return ArcadeProvider(http_proxy=local_arcade_proxy)

    def dep_lxns_player(friend_code: int | None = None, qq: int | None = None):
        return PlayerIdentifier(qq=qq, friend_code=friend_code)

    def dep_diving_player(username: str | None = None, qq: int | None = None):
        return PlayerIdentifier(qq=qq, username=username)

    def dep_arcade_player(credentials: str):
        return PlayerIdentifier(credentials=credentials)

    @asgi_app.exception_handler(MaimaiPyError)
    async def exception_handler(request: Request, exc: MaimaiPyError):
        return JSONResponse(
            status_code=400,
            content={"message": f"Oops! There goes a maimai.py error {exc}.", "details": repr(exc)},
        )

    @router.get(
        "/songs",
        response_model=list[Song],
        tags=["base"],
        description="Get songs by various filters, filters are combined by AND",
    )
    async def get_songs(
        id: int | None = None,
        title: str | None = None,
        artist: str | None = None,
        genre: Genre | None = None,
        bpm: int | None = None,
        map: str | None = None,
        version: int | None = None,
        type: SongType | None = None,
        level: str | None = None,
        versions: Version | None = None,
        keywords: str | None = None,
        page: int = Query(1, ge=1),
        page_size: int = Query(100, ge=1, le=1000),
    ):
        songs: MaimaiSongs = await maimai_client.songs(curve_provider=None)
        type_func: Callable[[Song], bool] = lambda song: song.difficulties._get_children(type) != []  # type: ignore
        level_func: Callable[[Song], bool] = lambda song: any([diff.level == level for diff in song.difficulties._get_children()])
        versions_func: Callable[[Song], bool] = lambda song: versions.value <= song.version < all_versions[all_versions.index(versions) + 1].value  # type: ignore
        keywords_func: Callable[[Song], bool] = lambda song: xstr(keywords) in xstr(song.title) + xstr(song.artist) + istr(song.aliases)
        filters = get_filters({type: type_func, level: level_func, versions: versions_func, keywords: keywords_func})
        results = [x async for x in songs.filter(id=id, title=title, artist=artist, genre=genre, bpm=bpm, map=map, version=version) if filters(x)]
        return pagination(page_size, page, results)

    @router.get(
        "/icons",
        response_model=list[PlayerIcon],
        tags=["base"],
        description="Get player icons by various filters, filters are combined by AND",
    )
    async def get_icons(
        id: int | None = None,
        name: str | None = None,
        description: str | None = None,
        genre: str | None = None,
        keywords: str | None = None,
        page: int = Query(1, ge=1),
        page_size: int = Query(100, ge=1, le=1000),
    ):
        items = await maimai_client.items(PlayerIcon)
        if id is not None:
            return [item] if (item := items.by_id(id)) else []
        keyword_func: Callable[[PlayerIcon], bool] = lambda icon: xstr(keywords) in (xstr(icon.name) + xstr(icon.description) + xstr(icon.genre))
        filters = get_filters({keywords: keyword_func})
        results = [x async for x in items.filter(name=name, description=description, genre=genre) if filters(x)]
        return pagination(page_size, page, results)

    @router.get(
        "/nameplates",
        response_model=list[PlayerNamePlate],
        tags=["base"],
        description="Get player nameplates by various filters, filters are combined by AND",
    )
    async def get_nameplates(
        id: int | None = None,
        name: str | None = None,
        description: str | None = None,
        genre: str | None = None,
        keywords: str | None = None,
        page: int = Query(1, ge=1),
        page_size: int = Query(100, ge=1, le=1000),
    ):
        items = await maimai_client.items(PlayerNamePlate)
        if id is not None:
            return [item] if (item := items.by_id(id)) else []
        keyword_func: Callable[[PlayerNamePlate], bool] = lambda icon: xstr(keywords) in (xstr(icon.name) + xstr(icon.description) + xstr(icon.genre))
        filters = get_filters({keywords: keyword_func})
        results = [x async for x in items.filter(name=name, description=description, genre=genre) if filters(x)]
        return pagination(page_size, page, results)

    @router.get(
        "/frames",
        response_model=list[PlayerFrame],
        tags=["base"],
        description="Get player frames by various filters, filters are combined by AND",
    )
    async def get_frames(
        id: int | None = None,
        name: str | None = None,
        description: str | None = None,
        genre: str | None = None,
        keywords: str | None = None,
        page: int = Query(1, ge=1),
        page_size: int = Query(100, ge=1, le=1000),
    ):
        items = await maimai_client.items(PlayerFrame)
        if id is not None:
            return [item] if (item := items.by_id(id)) else []
        keyword_func: Callable[[PlayerFrame], bool] = lambda icon: xstr(keywords) in (xstr(icon.name) + xstr(icon.description) + xstr(icon.genre))
        filters = get_filters({keywords: keyword_func})
        results = [x async for x in items.filter(name=name, description=description, genre=genre) if filters(x)]
        return pagination(page_size, page, results)

    @router.get(
        "/trophies",
        response_model=list[PlayerTrophy],
        tags=["base"],
        description="Get player trophies by various filters, filters are combined by AND",
    )
    async def get_trophies(
        id: int | None = None,
        name: str | None = None,
        color: str | None = None,
        keywords: str | None = None,
        page: int = Query(1, ge=1),
        page_size: int = Query(100, ge=1, le=1000),
    ):
        items = await maimai_client.items(PlayerTrophy)
        if id is not None:
            return [item] if (item := items.by_id(id)) else []
        keyword_func: Callable[[PlayerTrophy], bool] = lambda icon: xstr(keywords) in (xstr(icon.name) + xstr(icon.color))
        filters = get_filters({keywords: keyword_func})
        results = [x async for x in items.filter(name=name, color=color) if filters(x)]
        return pagination(page_size, page, results)

    @router.get(
        "/charas",
        response_model=list[PlayerChara],
        tags=["base"],
        description="Get player charas by various filters, filters are combined by AND",
    )
    async def get_charas(
        id: int | None = None,
        name: str | None = None,
        keywords: str | None = None,
        page: int = Query(1, ge=1),
        page_size: int = Query(100, ge=1, le=1000),
    ):
        items = await maimai_client.items(PlayerChara)
        if id is not None:
            return [item] if (item := items.by_id(id)) else []
        results = items.filter(name=name or keywords)
        return pagination(page_size, page, results)

    @router.get(
        "/partners",
        response_model=list[PlayerPartner],
        tags=["base"],
        description="Get player partners by various filters, filters are combined by AND",
    )
    async def get_partners(
        id: int | None = None,
        name: str | None = None,
        keywords: str | None = None,
        page: int = Query(1, ge=1),
        page_size: int = Query(100, ge=1, le=1000),
    ):
        items = await maimai_client.items(PlayerPartner)
        if id is not None:
            return [item] if (item := items.by_id(id)) else []
        results = items.filter(name=name or keywords)
        return pagination(page_size, page, results)

    @router.get(
        "/areas",
        response_model=list[Area],
        tags=["base"],
        description="Get areas",
    )
    async def get_areas(
        lang: Literal["ja", "zh"] = "ja",
        id: str | None = None,
        name: str | None = None,
        page: int = Query(1, ge=1),
        page_size: int = Query(100, ge=1, le=1000),
    ):
        areas = await maimai_client.areas(lang)
        if id is not None:
            return [area] if (area := await areas.by_id(id)) else []
        if name is not None:
            return [area] if (area := await areas.by_name(name)) else []
        return pagination(page_size, page, await areas.get_all())

    @router.get(
        "/lxns/players",
        response_model=LXNSPlayer,
        tags=["lxns"],
        description="Get player info from LXNS",
    )
    async def get_player_lxns(
        player: PlayerIdentifier = Depends(dep_lxns_player),
        provider: LXNSProvider = Depends(dep_lxns),
    ):
        return await maimai_client.players(player, provider)

    @router.get(
        "/divingfish/players",
        response_model=DivingFishPlayer,
        tags=["divingfish"],
        description="Get player info from Diving Fish",
    )
    async def get_player_diving(
        player: PlayerIdentifier = Depends(dep_diving_player),
        provider: DivingFishProvider = Depends(dep_diving),
    ):
        return await maimai_client.players(player, provider)

    @router.get(
        "/arcade/players",
        response_model=ArcadePlayer,
        tags=["arcade"],
        description="Get player info from Arcade",
    )
    async def get_player_arcade(
        player: PlayerIdentifier = Depends(dep_arcade_player),
        provider: ArcadeProvider = Depends(dep_arcade),
    ):
        return await maimai_client.players(player, provider)

    @router.get(
        "/lxns/scores",
        response_model=list[Score],
        tags=["lxns"],
        description="Get player ALL scores from LXNS",
    )
    async def get_scores_lxns(
        player: PlayerIdentifier = Depends(dep_lxns_player),
        provider: LXNSProvider = Depends(dep_lxns),
    ):
        scores = await maimai_client.scores(player, provider=provider)
        return scores.scores  # no pagination because it costs more

    @router.get(
        "/divingfish/scores",
        response_model=list[Score],
        tags=["divingfish"],
        description="Get player ALL scores from Diving Fish",
    )
    async def get_scores_diving(
        player: PlayerIdentifier = Depends(dep_diving_player),
        provider: DivingFishProvider = Depends(dep_diving),
    ):
        scores = await maimai_client.scores(player, provider=provider)
        return scores.scores  # no pagination because it costs more

    @router.get(
        "/arcade/scores",
        response_model=list[Score],
        tags=["arcade"],
        description="Get player ALL scores from Arcade",
    )
    async def get_scores_arcade(
        player: PlayerIdentifier = Depends(dep_arcade_player),
        provider: ArcadeProvider = Depends(dep_arcade),
    ):
        scores = await maimai_client.scores(player, provider=provider)
        return scores.scores  # no pagination because it costs more

    @router.post(
        "/lxns/scores",
        tags=["lxns"],
        description="Update player scores to LXNS",
    )
    async def update_scores_lxns(
        scores: list[Score],
        player: PlayerIdentifier = Depends(dep_lxns_player),
        provider: LXNSProvider = Depends(dep_lxns),
    ):
        await maimai_client.updates(player, scores, provider=provider)

    @router.post(
        "/divingfish/scores",
        tags=["divingfish"],
        description="Update player scores to Diving Fish, should provide the user's username and password, or import token as credentials.",
    )
    async def update_scores_diving(
        scores: list[Score],
        username: str | None = None,
        credentials: str | None = None,
    ):
        player = PlayerIdentifier(username=username, credentials=credentials)
        await maimai_client.updates(player, scores, provider=DivingFishProvider())

    @router.get(
        "/lxns/bests",
        response_model=PlayerBests,
        tags=["lxns"],
        description="Get player b50 scores from LXNS",
    )
    async def get_bests_lxns(
        player: PlayerIdentifier = Depends(dep_lxns_player),
        provider: LXNSProvider = Depends(dep_lxns),
    ):
        songs, scores = await asyncio.gather(maimai_client.songs(), maimai_client.scores(player, provider=provider))
        return await ser_bests(scores, songs)

    @router.get(
        "/divingfish/bests",
        response_model=PlayerBests,
        tags=["divingfish"],
        description="Get player b50 scores from Diving Fish",
    )
    async def get_bests_diving(
        player: PlayerIdentifier = Depends(dep_diving_player),
        provider: DivingFishProvider = Depends(dep_diving),
    ):
        songs, scores = await asyncio.gather(maimai_client.songs(), maimai_client.scores(player, provider=provider))
        return await ser_bests(scores, songs)

    @router.get(
        "/arcade/bests",
        response_model=PlayerBests,
        tags=["arcade"],
        description="Get player b50 scores from Arcade",
    )
    async def get_bests_arcade(
        player: PlayerIdentifier = Depends(dep_arcade_player),
        provider: ArcadeProvider = Depends(dep_arcade),
    ):
        songs, scores = await asyncio.gather(maimai_client.songs(), maimai_client.scores(player, provider=provider))
        return await ser_bests(scores, songs)

    @router.get("/lxns/plates", response_model=list[PlateObject], tags=["lxns"], description="Get player plates from LXNS")
    async def get_plate_lxns(
        plate: str,
        attr: Literal["remained", "cleared", "played", "all"] = "remained",
        player: PlayerIdentifier = Depends(dep_lxns_player),
        provider: LXNSProvider = Depends(dep_lxns),
    ):
        plates: MaimaiPlates = await maimai_client.plates(player, plate, provider=provider)
        return await getattr(plates, f"get_{attr}")()

    @router.get("/divingfish/plates", response_model=list[PlateObject], tags=["divingfish"], description="Get player plates from Diving Fish")
    async def get_plate_diving(
        plate: str,
        attr: Literal["remained", "cleared", "played", "all"] = "remained",
        player: PlayerIdentifier = Depends(dep_diving_player),
        provider: DivingFishProvider = Depends(dep_diving),
    ):
        plates: MaimaiPlates = await maimai_client.plates(player, plate, provider=provider)
        return await getattr(plates, f"get_{attr}")()

    @router.get("/arcade/plates", response_model=list[PlateObject], tags=["arcade"], description="Get player plates from Arcade")
    async def get_plate_arcade(
        plate: str,
        attr: Literal["remained", "cleared", "played", "all"] = "remained",
        player: PlayerIdentifier = Depends(dep_arcade_player),
        provider: ArcadeProvider = Depends(dep_arcade),
    ):
        plates: MaimaiPlates = await maimai_client.plates(player, plate, provider=provider)
        return await getattr(plates, f"get_{attr}")()

    @router.get("/arcade/regions", response_model=list[PlayerRegion], tags=["arcade"], description="Get player regions from Arcade")
    async def get_region(
        player: PlayerIdentifier = Depends(dep_arcade_player),
        provider: ArcadeProvider = Depends(dep_arcade),
    ):
        return await maimai_client.regions(player, provider=provider)

    @router.get("/arcade/qrcode", tags=["arcade"], description="Get encrypted player credentials from QR code")
    async def parse_qrcode(qrcode: str):
        identifier = await maimai_client.qrcode(qrcode, http_proxy=local_arcade_proxy)
        return {"credentials": identifier.credentials}

    @asgi_app.get("/", include_in_schema=False)
    async def root():
        return {"message": "Hello, maimai.py! Check /docs for more information."}

    asgi_app.include_router(router)

    def openapi():
        if asgi_app is not None:
            specs = get_openapi(
                title=asgi_app.title,
                version=asgi_app.version,
                openapi_version=asgi_app.openapi_version,
                description=asgi_app.description,
                routes=asgi_app.routes,
            )
            with open(f"openapi.json", "w") as f:
                json.dump(specs, f)


if find_spec("uvicorn") and __name__ == "__main__":
    from urllib.parse import unquote, urlparse

    import typer
    import uvicorn
    from aiocache import RedisCache
    from aiocache.serializers import PickleSerializer

    def main(
        host: Annotated[str, typer.Option(help="The host address to bind to.")] = "127.0.0.1",
        port: Annotated[int, typer.Option(help="The port number to bind to.")] = 8000,
        redis: Annotated[str | None, typer.Option(help="Redis server address, for example: redis://localhost:6379/0.")] = None,
    ):
        redis_backend = UNSET
        if redis:
            redis_url = urlparse(redis)
            redis_backend = RedisCache(
                serializer=PickleSerializer(),
                endpoint=unquote(redis_url.hostname or "localhost"),
                port=redis_url.port or 6379,
                password=redis_url.password,
                db=int(unquote(redis_url.path).replace("/", "")),
            )
        global maimai_client
        maimai_client = MaimaiClient(cache=redis_backend)

        if asgi_app is not None:
            uvicorn.run(asgi_app, host=host, port=port)

    typer.run(main)


if find_spec("maimai_ffi") and find_spec("nuitka"):
    import json

    import cryptography
    import cryptography.fernet
    import cryptography.hazmat.backends
    import cryptography.hazmat.primitives.ciphers
    import maimai_ffi
    import maimai_ffi.model
    import maimai_ffi.request
    import redis
