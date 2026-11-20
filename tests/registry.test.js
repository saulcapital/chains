"use strict";
const test = require("node:test");
const assert = require("node:assert/strict");
const chains = require("..");

test("isRetired matches ids and name variants like the Python helper", () => {
  assert.equal(chains.isRetired(null, 250), true);
  assert.equal(chains.isRetired(null, "250"), true);
  assert.equal(chains.isRetired("Fantom Opera"), true);
  assert.equal(chains.isRetired("fantom_opera"), true);
  assert.equal(chains.isRetired("ethereum"), false);
  assert.equal(chains.isRetired(null, 1), false);
  assert.equal(chains.isRetired(), false);
});

test("lookups resolve ids, slugs, names and aliases", () => {
  assert.equal(chains.byId(1).slug, "ethereum");
  assert.equal(chains.byId("1").slug, "ethereum");
  assert.equal(chains.byName("Polygon zkEVM"), chains.byId(1101));
  assert.equal(chains.byId("nope"), null);
});

test("retired sets cover exactly the retired rows", () => {
  const retired = chains.CHAINS.filter((c) => c.retired);
  assert.deepEqual(
    [...chains.RETIRED_CHAIN_IDS].sort((a, b) => a - b),
    retired.filter((c) => c.chainId !== null).map((c) => c.chainId).sort((a, b) => a - b),
  );
  for (const c of chains.CHAINS.filter((x) => !x.retired)) {
    for (const n of [c.slug, c.name, ...c.aliases]) {
      assert.equal(chains.RETIRED_CHAIN_NAMES.has(chains.normalize(n)), false, `${c.slug}: ${n}`);
    }
  }
});
