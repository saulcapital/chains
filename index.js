"use strict";
// Shared chain registry; same data and semantics as the Python saul_chains package.
const data = require("./saul_chains/chains.json");

function normalize(value) {
  return String(value ?? "").trim().toLowerCase().replace(/[-_ ]/g, "");
}

const CHAINS = Object.freeze(data.chains.map((row) => Object.freeze({
  slug: row.slug,
  name: row.name,
  chainId: row.chain_id ?? null,
  aliases: Object.freeze([...(row.aliases ?? [])]),
  explorer: row.explorer ?? null,
  txUrl: row.tx_url ?? null,
  llama: row.llama ?? null,
  native: row.native ? Object.freeze({ ...row.native }) : null,
  status: row.status,
  retired: row.status === "retired",
  retiredSource: row.retired?.source ?? null,
  retiredNote: row.retired?.note ?? null,
})));

const namesOf = (chain) => new Set([chain.slug, chain.name, ...chain.aliases].map(normalize));
const BY_ID = new Map(CHAINS.filter((c) => c.chainId !== null).map((c) => [c.chainId, c]));
const BY_NAME = new Map(CHAINS.flatMap((c) => [...namesOf(c)].map((n) => [n, c])));
const RETIRED_CHAIN_IDS = Object.freeze(new Set(CHAINS.filter((c) => c.retired && c.chainId !== null).map((c) => c.chainId)));
const RETIRED_CHAIN_NAMES = Object.freeze(new Set(CHAINS.filter((c) => c.retired).flatMap((c) => [...namesOf(c)])));

function byId(chainId) {
  const id = Number(String(chainId ?? "").trim());
  return Number.isInteger(id) ? BY_ID.get(id) ?? null : null;
}

function byName(value) {
  return BY_NAME.get(normalize(value)) ?? null;
}

function isRetired(chain, chainId) {
  for (const value of [chainId, chain]) {
    const text = normalize(value);
    if (RETIRED_CHAIN_NAMES.has(text) || (/^\d+$/.test(text) && RETIRED_CHAIN_IDS.has(Number(text)))) return true;
  }
  return false;
}

module.exports = { CHAINS, RETIRED_CHAIN_IDS, RETIRED_CHAIN_NAMES, byId, byName, isRetired, normalize };
