"""Shared chain registry: one ``chains.json`` for every saulcapital repo.

Each chain has a canonical ``slug``, display ``name``, EVM ``chain_id`` (``None``
for non-EVM chains), extra ``aliases``, explorer/tx URLs, DefiLlama slug,
native token, and a ``status``. A ``retired`` chain has shut down (``source``
links the official notice): consumers keep its name for labels and history
but must not poll it.

Name lookups normalize case, spaces, ``-`` and ``_`` (``"Fantom Opera"`` and
``"fantom_opera"`` both match ``fantomopera``).
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources
from typing import Any

__all__ = [
    "CHAINS",
    "Chain",
    "Native",
    "RETIRED_CHAIN_IDS",
    "RETIRED_CHAIN_NAMES",
    "by_id",
    "by_name",
    "is_retired",
    "normalize",
]


@dataclass(frozen=True)
class Native:
    symbol: str
    decimals: int
    price: str | None  # price key, e.g. "coingecko:ethereum"


@dataclass(frozen=True)
class Chain:
    slug: str
    name: str
    chain_id: int | None
    aliases: tuple[str, ...]
    explorer: str | None
    tx_url: str | None  # "{}" is the transaction hash
    llama: str | None
    native: Native | None
    status: str  # "live" | "retired"
    retired_source: str | None
    retired_note: str | None

    @property
    def retired(self) -> bool:
        return self.status == "retired"

    def names(self) -> frozenset[str]:
        """Every normalized name this chain answers to."""
        return frozenset(normalize(v) for v in (self.slug, self.name, *self.aliases))


def normalize(value: Any) -> str:
    return str(value or "").strip().casefold().replace("-", "").replace("_", "").replace(" ", "")


def _chain(row: dict[str, Any]) -> Chain:
    native = row.get("native")
    retired = row.get("retired") or {}
    return Chain(
        slug=row["slug"],
        name=row["name"],
        chain_id=row.get("chain_id"),
        aliases=tuple(row.get("aliases") or ()),
        explorer=row.get("explorer"),
        tx_url=row.get("tx_url"),
        llama=row.get("llama"),
        native=Native(native["symbol"], native["decimals"], native.get("price")) if native else None,
        status=row["status"],
        retired_source=retired.get("source"),
        retired_note=retired.get("note"),
    )


def _load() -> tuple[Chain, ...]:
    text = resources.files(__name__).joinpath("chains.json").read_text(encoding="utf-8")
    return tuple(_chain(row) for row in json.loads(text)["chains"])


CHAINS: tuple[Chain, ...] = _load()
_BY_ID = {chain.chain_id: chain for chain in CHAINS if chain.chain_id is not None}
_BY_NAME = {name: chain for chain in CHAINS for name in chain.names()}
RETIRED_CHAIN_IDS: frozenset[int] = frozenset(
    chain.chain_id for chain in CHAINS if chain.retired and chain.chain_id is not None
)
RETIRED_CHAIN_NAMES: frozenset[str] = frozenset(
    name for chain in CHAINS if chain.retired for name in chain.names()
)


def by_id(chain_id: Any) -> Chain | None:
    try:
        return _BY_ID.get(int(str(chain_id).strip()))
    except (TypeError, ValueError):
        return None


def by_name(value: Any) -> Chain | None:
    """Chain by slug, display name or alias."""
    return _BY_NAME.get(normalize(value))


def is_retired(chain: Any = None, chain_id: Any = None) -> bool:
    """Whether a chain name/slug or EVM id (int or decimal string) is retired."""
    for value in (chain_id, chain):
        text = normalize(value)
        if text in RETIRED_CHAIN_NAMES or (text.isdecimal() and int(text) in RETIRED_CHAIN_IDS):
            return True
    return False
