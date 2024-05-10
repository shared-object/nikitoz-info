import asyncio
from typing import Any, AsyncGenerator

from aiohttp import ClientSession
from loguru import logger
from pyrogram.client import Client

from .settings import Settings
from .types import Pair, PairsResponse


async def get_pairs(nikitoz_addr: str) -> PairsResponse:
    async with ClientSession("https://api.dexscreener.com") as session:
        async with session.get(f"/latest/dex/pairs/ton/{nikitoz_addr}") as response:
            return PairsResponse.model_validate(await response.json())


async def poll_nikitoz(settings: Settings) -> AsyncGenerator[Any, PairsResponse]:
    while True:
        try:
            yield await get_pairs(settings.nikitoz_address)
        except Exception:
            logger.exception("Polling error")
            continue


def format_info(
    coin: str,
    price_change_24h: str,
    volume_24h: float,
    buys_24h: int,
    sells_24h: int,
    liquidity_usd: float,
    last_price: str,
    price_usd: str,
):

    return (
        f"24H: **{coin}** / {price_change_24h}%\n\n"
        f"**24H Volume**: ${volume_24h}\n"
        f"**24H Buys**: {buys_24h}\n"
        f"**24H Sells**: {sells_24h}\n\n"
        f"**Liquidity**: ${liquidity_usd}\n\n"
        f"${last_price} -> ${price_usd}"
    )


async def main(settings: Settings):
    app = Client("nikitoz", settings.app_id, settings.app_hash)

    last_pairs = (await get_pairs(settings.nikitoz_address)).pairs

    async with app:
        logger.info("Ninfo bot started")

        async for pairs in poll_nikitoz(settings):
            await asyncio.sleep(0.5)

            try:
                pair: Pair = pairs.pairs[0] if pairs.pairs else None  # type: ignore

                if pair is None:
                    continue

                last_price = last_pairs[0].priceUsd if last_pairs else "0"
                
                if last_price == pair.priceUsd:
                    continue

                coin = "$" + pair.baseToken.symbol
                volume_24h = pair.volume.h24
                price_change_24h = str(pair.priceChange.h24)
                buys_24h = pair.txns.h24.buys
                sells_24h = pair.txns.h24.sells
                liquidity_usd = pair.liquidity.usd if pair.liquidity else 0.0
                price_usd = pair.priceUsd

                await app.send_message(
                    settings.chat_id,
                    format_info(
                        coin,
                        price_change_24h,
                        volume_24h,
                        buys_24h,
                        sells_24h,
                        liquidity_usd,  # type: ignore
                        last_price,  # type: ignore
                        price_usd,  # type: ignore
                    ),
                )

                last_pairs = pairs.pairs
            except Exception:
                logger.exception("bot err")
