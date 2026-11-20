export interface Native {
  readonly symbol: string;
  readonly decimals: number;
  readonly price: string | null;
}

export interface Chain {
  readonly slug: string;
  readonly name: string;
  readonly chainId: number | null;
  readonly aliases: readonly string[];
  readonly explorer: string | null;
  /** "{}" is the transaction hash. */
  readonly txUrl: string | null;
  readonly llama: string | null;
  readonly native: Native | null;
  readonly status: "live" | "retired";
  readonly retired: boolean;
  readonly retiredSource: string | null;
  readonly retiredNote: string | null;
}

export declare const CHAINS: readonly Chain[];
export declare const RETIRED_CHAIN_IDS: ReadonlySet<number>;
export declare const RETIRED_CHAIN_NAMES: ReadonlySet<string>;
export declare function byId(chainId: number | string | null | undefined): Chain | null;
export declare function byName(value: string | null | undefined): Chain | null;
export declare function isRetired(chain?: string | null, chainId?: number | string | null): boolean;
export declare function normalize(value: unknown): string;
