import json
from collections import Counter
from pathlib import Path

import saul_chains as sc

ROWS = json.loads((Path(sc.__file__).parent / "chains.json").read_text())["chains"]


def test_slugs_ids_and_names_are_unique():
    assert not [s for s, n in Counter(r["slug"] for r in ROWS).items() if n > 1]
    ids = [r["chain_id"] for r in ROWS if r["chain_id"] is not None]
    assert not [i for i, n in Counter(ids).items() if n > 1]
    owners: dict[str, str] = {}
    for chain in sc.CHAINS:
        for name in chain.names():
            assert owners.setdefault(name, chain.slug) == chain.slug, f"{name} names {owners[name]} and {chain.slug}"


def test_rows_are_well_formed():
    for row in ROWS:
        assert row["status"] in {"live", "retired"}, row["slug"]
        assert (row["status"] == "retired") == bool(row.get("retired")), row["slug"]
        if row["status"] == "retired":
            assert row["retired"]["source"].startswith("https://"), row["slug"]
        if row.get("tx_url"):
            assert "{}" in row["tx_url"], row["slug"]
        assert row["slug"] == row["slug"].strip().lower(), row["slug"]


def test_is_retired_matches_ids_and_name_variants():
    fantom = sc.by_id(250)
    assert fantom is not None and fantom.retired
    assert sc.is_retired(chain_id=250) and sc.is_retired(chain_id="250")
    assert sc.is_retired("Fantom Opera") and sc.is_retired("fantom_opera") and sc.is_retired("FANTOM")
    assert not sc.is_retired("ethereum") and not sc.is_retired(chain_id=1)
    assert not sc.is_retired() and not sc.is_retired("", "")
    assert sc.by_name("Polygon zkEVM") is sc.by_id(1101)


def test_retired_sets_cover_every_retired_row():
    retired = [c for c in sc.CHAINS if c.retired]
    assert {c.chain_id for c in retired if c.chain_id is not None} == set(sc.RETIRED_CHAIN_IDS)
    assert all(c.names() <= sc.RETIRED_CHAIN_NAMES for c in retired)
    assert not any(c.names() & sc.RETIRED_CHAIN_NAMES for c in sc.CHAINS if not c.retired)
