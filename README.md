# chains

One chain registry for every saulcapital repo: EVM ids, slugs, names, aliases,
explorers, native tokens, and which chains have shut down. Edit
`saul_chains/chains.json`; the Python and JS helpers read that one file.

## Install

Python (pin a tag):

```
saul-chains @ git+https://github.com/saulcapital/chains@v0.1.0
```

Node / TypeScript:

```
npm install github:saulcapital/chains#v0.1.0
```

## Use

```python
from saul_chains import is_retired, by_id, by_name, RETIRED_CHAIN_IDS

is_retired("Fantom Opera")      # True; names normalize case, spaces, "-" and "_"
is_retired(chain_id="250")      # True; ints or decimal strings
by_id(1).explorer               # "https://etherscan.io"
```

```js
const { isRetired, byId, byName } = require("@saulcapital/chains");
isRetired(null, 250);           // true
```

## Retired chains

`status: "retired"` means the chain has an official shutdown, wind-down or
migration notice, linked in `retired.source`. Consumers keep the chain's name
for labels and history but must not poll its RPCs or crawl its routes;
recovery that runs entirely on Ethereum stays allowed. A migration, rebrand
or low activity alone is not a retirement.

To retire a chain: set `status` to `"retired"`, add `retired.source` (and
`retired.note` when it retires ahead of the announced date), add any extra
names to `aliases`, bump the version in `pyproject.toml` and `package.json`,
tag `vX.Y.Z`, then bump the pin in each consumer.

## Consumers

- yamDiscBot (`bot/services/chain_support.py`)
- shared-labels (`code/evm_rpc.py`, `code/evm_rpc_pool.py`, `code/evm_address_history.py`, `code/hypersync_transfers.py`, Across/Hop/Superform loops)

## Test

```
pip install . pytest && pytest -q
npm test
```
