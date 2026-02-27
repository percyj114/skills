# CAN: Clock Address Naming

Find what you name. Trust what you verify. OWN things. CAN or NOT.

## What CAN does

1. **STAMP** — hash + clock + name. One operation.
2. **PROVE** — check hash, reject fakes. CAN or NOT.
3. **FIND** — search by time, hash, or name. Three legs, not one.
4. **ROUTE** — local store → peers. Every log is a routing hint.
5. **TRUST** — earned by evidence, not ceremony. The log is the trust graph.

## Requirements

`sha256sum` (pre-installed on most Linux; use `shasum -a 256` on macOS). WHO-1 signing uses `openssl` (pre-installed on most systems). Also uses `awk`, `date`, `base64` — standard on Linux and macOS. No npm. No pip. No runtime. Works air-gapped.

## Quick start

```bash
# Stamp a thing
WHEN=$(date +%s%3N)
WHERE=$(sha256sum myfile.txt | awk '{print $1}')
WHAT="myfile.txt SAVE $(cat ~/.can/who.id)"
echo -e "$WHEN\t$WHERE\t$WHAT" >> ~/.can/index.tsv

# Find by name
grep "myfile" ~/.can/index.tsv

# Find by time (today)
TODAY=$(date +%s)000
awk -F'\t' -v t="$TODAY" '$1 >= t' ~/.can/index.tsv
```

## Why?

```
WHAT YOU TRUST           WHAT ACTUALLY HAPPENS
──────────────           ──────────────────────
machine name             changes when IT renames the server
IP address               changes when you switch networks
file path                changes when you move a folder
URL                      breaks when the site restructures
DNS                      depends on ICANN and registrars
TLS certificate          depends on authorities you never chose
cloud storage path       depends on a company existing next quarter
```

Every row is a WHERE defined by atoms. Atoms rearrange. Addresses break.

Clock without hash? You know when, can't verify what. Every database ever.
Hash without clock? You can verify what, don't know when. Dead snapshots.
Clock AND hash: verify what, prove when. CAN.

## Three namespaces

```
WHERE   hashspace    math names it        verified or NOT
WHEN    timespace    physics names it     stamped or NOT
WHAT    namespace    humans name it       claim as TRUE or NOT
```

Nobody did all three:

```
DNS:        namespace only         (no verify, no time)
GIT:        hashspace only         (no time-first, no human name)
IPFS:       hashspace only         (dead snapshots, no clock)
BLOCKCHAIN: timespace + hashspace  (no human namespace)
CAN:        all three              (WHERE + WHEN + WHAT)
```

## Index format

Three columns, tab-separated: `~/.can/index.tsv`

```
WHEN            WHERE                                   WHAT
1770600000000   a3f8b2c1e9d7f0a1b2c3d4e5f6a7b8c9d0e1   meme.jpg
```

WHAT grammar: `NAME [INTENT] [WHO] [PATH]`

## WHO identity tiers

```
WHO-0   sha256(user + machine-id)        free, instant, spoofable
WHO-1   local keypair (~/.can/who.key)   self-generated, persistent
WHO-2   any key the agent already holds  Nostr nsec, PGP, SSH
```

## BAGS

Save by intent. Four bags. One question: who gets access?

```
HUSH    secret. exists in log, never leaves. (hard problem).
GOOD    private. mine. my business. copynot.
FREN    trusted. signed. few WHOs, one hash. contract.
POST    public. by choice. by consent.
```

Default: HUSH. Everything else is opt-in.

## Scope

**ME → FAM → FRENS → ALIENS**

Same CAN at every layer. Same operations. Different scope, different trust.

BAGS control what leaves. Scope controls who sees it.

## References

- Baran, P. (1964). On Distributed Communications — no center by design.
- Diffie, W. & Hellman, M. (1976). New Directions in Cryptography — OWN without permission.
- Merkle, R. (1979). Hash trees — the data structure beneath WHERE.
- Ostrom, E. (1990). Governing the Commons — small groups, no central authority.
- Zimmermann, P. (1991). PGP: Web of Trust — trust from peers up, not authorities down.
- Szabo, N. (1997). Smart contracts, bit gold — named the game before anyone could play.
- Grigg, I. (2004). The Ricardian Contract — human-readable, machine-verifiable, one hash.
- Torvalds, L. (2005). Git — content-addressed storage, hash chains.
- Jacobson, V. (2006). NDN: Named Data Networking — name the data, not the pipe.
- Day, J. (2008). RINA: Patterns in Network Architecture — recursive scoping.
- Nakamoto, S. (2008). Bitcoin — clock + hash + log for value. No priest.
- Taleb, N.N. (2012). Antifragile — skin in game, Lindy, via negativa. First do NOT.

## TL;DR

```
CAN automate naming.
WHERE in math.
WHEN in physics.
WHAT you name it.
CAN not lie.

())) ← in the CAN
```
