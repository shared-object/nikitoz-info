from typing import List, Optional

from pydantic import BaseModel

class TxnsData(BaseModel):
    buys: int
    sells: int


class Txns(BaseModel):
    m5: TxnsData
    h1: TxnsData
    h6: TxnsData
    h24: TxnsData


class Volume(BaseModel):
    m5: float = 0.0
    h1: float = 0.0
    h6: float = 0.0
    h24: float = 0.0


class PriceChange(BaseModel):
    m5: float = 0.0
    h1: float = 0.0
    h6: float = 0.0
    h24: float = 0.0


class Liquidity(BaseModel):
    usd: Optional[float] = None
    base: float = 0.0
    quote: float = 0.0


class BaseToken(BaseModel):
    address: str
    name: str
    symbol: str


class QuoteToken(BaseModel):
    symbol: str


class Pair(BaseModel):
    chainId: str
    dexId: str
    url: str
    pairAddress: str
    baseToken: BaseToken
    quoteToken: QuoteToken
    priceNative: str
    priceUsd: Optional[str] = None
    txns: Txns
    volume: Volume
    priceChange: PriceChange
    liquidity: Optional[Liquidity] = None
    fdv: Optional[float] = None
    pairCreatedAt: Optional[int] = None


class PairsResponse(BaseModel):
    schemaVersion: str
    pair: Optional[Pair] = None
    pairs: Optional[List[Pair]] = None

    # @deprecated
    # def use_pairs(self):
    #     if self.pair:
    #         return [self.pair]
    #     return self.pairs
