---
name: CAN
version: 0.1.7
description: "Clock Address Naming: WHERE (hash), WHEN (clock), WHAT (name). In the CAN, or NOT."
homepage: https://github.com/xccx/can
metadata: {"openclaw":{"emoji":"⌛","requires":{"bins":["sha256sum","openssl","base64","awk","date"]}}}
---

# CAN: Clock Address Naming

CAN automate naming: when, where, what. Or NOT.

## Three namespaces

```
WHERE   hashspace    math names it        verified or NOT
WHEN    timespace    physics names it     stamped or NOT
WHAT    namespace    humans name it       claim as TRUE or NOT
```

Every CAN entry has three answers. Same three, every time, at every layer. Remove any leg and the stool falls. CAN can not lie. So we work with what is TRUE.

## Why?

Hacking millions of branches? Strike one "1" root. Fix the naming.

WHERE locations fail. IP addresses change. File paths change. URLs break. DNS needs ICANN. TLS needs certificate authorities you chose, not. Cloud paths depend on a company existing next quarter.

LOCATION addressing tried to locate atoms. Atoms rearrange. Addresses break. Every address costs money to maintain — registrars, certificate authorities, cloud providers, redirect services. All tax on bad naming.

CONTENT-ADDRESSING found a WHAT. But WHAT is it? Some set of bits? What do they mean? What time when? What author who? What price how much? What for why? Wut?

CLOCK-ADDRESSING finds math, physics, logic. Compute WHEN and WHERE, then NAME who wants what why how, by WEN (before expiry). Automate the objective. Free the subjective. Make meaning TRUE. So we can do things FAST.

CAN agree on verifiably TRUE timings, signed by consent. AGREE or NOT. In the CAN. Or NOT.

## How?

Name things in logic, not atoms. A clock tick is logical. A hash is logical. Logic doesn't rearrange.

```
WHERE   SHA-256 hash                math names the thing
WHEN    millisecond timestamp       physics names the moment
WHAT    whatever you call it        humans name the meaning
```

WHERE in hashspace? One thing's true point in 2^256 possibles. It doesn't HAVE a location. It owns the place. Fixed. Inalienable. True. The hash doesn't tell you which shelf — it tells you where it exists in math.

WHEN in timespace? The clock claims a thing happens at one point within limited time. Irreversible. The clock can't unsay it. Physics doesn't negotiate. What happens happens. WHEN? On timer, in physics.

WHAT in namespace? Natural language makes the meaning happen. Who says? How? Why? Can it be falsified? Or NOT. Are you slowly uniquely file-name each thing? Or does natural language naming make you find things faster?

```
HASHSPACE    math      (sha256 declares logic address)
TIMESPACE    physics   (clock declares time address)
NAMESPACE    words     (subjective claims for tots and bots to validate, or not)
```

Clock without hash? you know when, can't verify what. Every database ever.
Hash without clock? you can verify what, don't know when. Lost in 2^256 space.
Clock AND hash: verify what, prove when. CAN.

CAN names the HASH and TIME for free. Every machine with a clock and sha256 can say WHERE and WHEN. BOTS name natively for bots. Human TOTS own natural naming. Bots and Tots find things fast. CAN agree. Or NOT.

## Find fast

CAN finds fast because the tripod has three legs to search.

Know WHEN? Narrow by time. Know WHERE? Match the hash. Know WHAT? Search by human name. Two legs narrow instantly. Three legs find exactly.

Old naming had one leg: location. When it breaks you have zero legs.

The finding IS the verifying. When you check if the hash matches, you've also located the thing in hashspace. One operation, two results. Lookup tax cuts in half.

CAN cares less if ten things have the same WHAT. The tripod differentiates: same name, different hash, different time. Name freely. Find precisely.

## Falsify fast

Every claim in CAN is falsifiable. That's the point.

Hash doesn't match? NOT. Instantly. No investigation, no committee, no appeal. You want to argue with the timer? The timer doesn't care.

Old security: try make lying hard. Walls, passwords, certificates, authorities. CAN security: make lying trivial, make detecting lies trivial too. A network already full of fakes — CAN makes fakes instantly visible and costless to reject.

Building trust is expensive: time multiplied by evidence. Losing trust is instant: one NOT from a trusted peer. Asymmetric by design, exactly like real reputation.

Every claim is a bet against the clock. Either the hash matches at this moment or it doesn't. True, or NOT. Falsifiable, or not worth naming.

## Identity

WHO lives in NAMESPACE. Identity is a name you own for yourself.

```
WHO-0   sha256(user + machine-id)        free, instant, spoofable
WHO-1   local keypair (~/.can/who.key)   self-generated, persistent, trust local
WHO-2   any key the agent already holds  Nostr nsec, PGP, SSH, trust global
```

WHO-0 is a free ticket — disposable, good enough to start. WHO-1 is a subscription — yours, durable. WHO-2 is a passport — CAN doesn't authenticate WHO-2 keys. CAN logs which key signed and when. The external system authenticates. CAN timestamps the claim.

Many processes don't need WHO named. WHEN + WHERE is the name. WHO names can resolve collisions.

```
WHEN alone          enough for one agent, one machine
WHEN + WHERE        enough for one agent, anything
WHEN + WHERE + WHO  enough for everyone, everything
```

Progressive specificity. Start minimal. Add only what collides.

## Index

Three columns. Tab-separated. One file: `~/.can/index.tsv`

```
WHEN            WHERE                                   WHAT
1770600000000   a3f8b2c1e9d7f0a1b2c3d4e5f6a7b8c9d0e1   meme.jpg
```

WHAT is the flexible column. First token is the name, rest is optional metadata:

```
WHAT = NAME [INTENT] [WHO] [PATH]
```

```
WHAT examples:
meme.jpg                          a filename
meme.jpg SAVE c7d2e9f0            a filename + intent + who
meme.jpg SAVE c7d2e9f0 ~/meme.jpg a filename + intent + who + path
meme.jpg HUSH                     a filename, private, never leaves scope
```

WHAT grows rightward as needed. Minimal by default. Three columns. Tripod.

## Stamp

```bash
WHEN=$(date +%s%3N)
WHERE=$(sha256sum thing.txt | awk '{print $1}')
WHAT="thing.txt SAVE $(cat ~/.can/who.id)"
echo -e "$WHEN\t$WHERE\t$WHAT" >> ~/.can/index.tsv
```

One line. Own your naming. Clocked. Addressed. Named. In the CAN.

No npm. No pip. No runtime. No cloud. Works air-gapped. Works offline. Works forever.

## CAN (verb)

**0. Sanitize.** Every input validates before touching anything:

```bash
can_safe() {
    local val="$1" pattern="$2"
    [[ "$val" =~ $pattern ]] && echo "$val" || echo "NOT"
}

WHERE=$(can_safe "$WHERE" '^[a-f0-9]{64}$')
WHEN=$(can_safe "$WHEN" '^[0-9]{13}$')
[ "$WHERE" = "NOT" ] || [ "$WHEN" = "NOT" ] && exit 1
```

Step 0 runs first. Bad input never reaches the log.

**1. Hash.** Does the content match its claimed address?

```
ACTUAL=$(sha256sum thing | awk '{print $1}')
if [ "$ACTUAL" = "$CLAIMED" ]; then
    # CAN
else
    # NOT
fi
```

**2. Clock.** When did this happen? Timestamp. Automatic. Non-negotiable.

**3. Log.** Append to index. CAN or NOT. The log is the network.

CAN is hash (verify) + clock (time) + log (record) in one operation. Everything else — trust, routing, scoping — falls out of doing this over and over.

The finding IS the verifying. When you check if the hash matches, you've also coordinated the thing in hashspace. One operation, two results. Lookup tax cuts in half. Coordinate 2x faster.

## NOT: lies can't hide.

Every CAN has a NOT. Wronged hashes are not true. See what's wrong, and who says so.

NOT is signal, not noise. Your NOTs warn future routers: been there, done that, not true.

```
CAN: "this hash matches, verified at this moment"
NOT: "this hash DOESN'T match, rejected at this moment"
```

Your CAN is a router. Your NOT is a blacklist. Together they replace three tables with two words:

```
NDN PIT  (pending interest)  → what you're looking for     → CAN-find
NDN FIB  (forwarding info)   → where to look next          → CAN index
NDN CS   (content store)     → what you already have       → CAN store
NDN ???                      → what you know is fake       → NOT
```

NDN names the data, not the pipe. CAN adds the fourth table: the rejection log. "I have it." "I want it." "It's not true." The sword that splits true from false.

## Routing

Routing is a side effect of agents naming what they verified.

```
Agent A stamps a thing     → CAN entry (WHEN + WHERE + WHAT)
Agent B requests hash      → checks local store first
Agent B finds it locally   → done, zero network
Agent B doesn't have it    → asks peers
Agent A responds           → sends thing
Agent B verifies hash      → match = CAN, cache, log
                           → mismatch = NOT, warn, skip
Agent C requests same hash → TWO sources now
```

CAN grows an index. The network gets faster. Least authority. No registry. No permission. Just math. Every log is a routing hint for the next agent.

Location says "it's on shelf 3." Coordination says "inalienably at hashspace in timespace — any agent who has it can serve it." Location is one copy in one place. Coordination is every copy everywhere, findable by the same name.

## Scope

CAN holds CANs. Same three answers at every layer. All the way down. All the way UP.

```
┌─────────────────────────────┐
│  CAN (my machine)           │
│                             │
│  things I CAN'd             │
│  things I NOT'd             │
│                             │
│  ┌───────────────────────┐  │
│  │  CAN (a project)      │  │
│  │  its own CANs          │  │
│  │  its own NOTs          │  │
│  └───────────────────────┘  │
│                             │
└─────────────────────────────┘
```

**ME → FAM → FRENS → ALIENS**

Same CAN at every layer. The only thing that changes is who's in the scope and what trust governs entry.

| Policy | Entry | Example |
|--------|-------|---------|
| **PUB** | public | not private |
| **FOF** | friend-of-friends | trust path |
| **SIG** | signature-authorize | WHO-1+ |
| **BUMP** | co-presence proof | who's here now |

Default scope is SELF. All sharing opt-in. No daemon. No automatic sync. Your CAN is private until you share.

## Trust

Trust isn't declared. Trust is earned, weighing CAN and NOT, over time.

```
trust = (CAN_count × recency) + (vouch_count × voucher_weight) - (NOT_count × severity)
```

Computed locally. Per-agent. Your log, your weights. No global score.

Every time you CAN something accurately, trust goes up. Every time you NOT something correctly, trust goes up — you caught a fake, good. Every time YOU get NOT'd by others, trust goes down.

No ceremony. No key-signing party. No passport. The log IS the trust graph. What you did is who you are.

## Contract

A CAN entry satisfies contract primitives:

```
CONTRACT ELEMENT         CAN MECHANISM
────────────────         ─────────────
offer                    share a hash (immutable terms)
acceptance               CAN the offer (LOG = consent)
consideration            value exchanged, logged
capacity                 WHO proves identity (tier 0/1/2)
meeting of minds         same hash = same document, no ambiguity
```

Two WHOs. One hash. Both CAN'd it. That's a contract. Clock-addressed, timestamped, signed by both parties. The hash proves the terms didn't change.

## Five operations

Same at every layer. Your machine, your pair, your village. Same CAN.

| Op | What | Verb |
|----|------|------|
| **STAMP** | Hash + clock + name | CAN this |
| **PROVE** | Check hash, reject fakes | CAN or NOT |
| **FIND** | Search by time, hash, or name | CAN I find it? |
| **ROUTE** | Locate nearest copy, trust-weighted | CAN anyone? |
| **TRUST** | Score by evidence, not ceremony | CAN I trust you? |

## Security

Firewall: everything outside is dangerous, everything inside is trusted. One breach and the village burns.

CAN: own things. I own mine. You do you. We share what we choose. We can restore our privacy.

```
FIREWALL:                    CAN:

  ┌──────────────────┐       🔒 🔒 🔒 🔒 🔒
  │ TRUSTED ZONE     │       🔒 🔒 🔒 🔒 🔒
  │ one breach = gg  │       every thing owns itself
  └──────────────────┘       one breach = one thing
```

No automatic sharing. Default is PRIVATE. You CAN share. You can NOT be shared without consent.

## BAGS

Save by intent. Four bags. One question: who gets access?

```
HUSH    secret. exists in log, never leaves. (hard problem).
GOOD    private. mine. my business. copynot.
FREN    trusted. signed. few WHOs, one hash. contract.
POST    public. by choice. by consent.
```

Default: HUSH. Everything else is opt-in.

BAGS control what leaves. Scope controls who sees it.

## Safety

**Input safety:**

```
WHERE    ^[a-f0-9]{64}$              not exactly 64 hex chars → NOT
WHEN     ^[0-9]{13}$                 not exactly 13 digits → NOT
WHAT     ^[a-zA-Z0-9._: /-]{1,1024}$ shell metacharacters → NOT
         no semicolons, pipes, backticks, $() → NOT
```

Bash examples are illustrations, not executables. Use safe string handling.

**Network safety:**

CAN never automatically shares. Every share is explicit. No daemon. No background sync. Respect HUSH (absolute). Scope boundaries are access control. Index is sensitive — private by default. Transport is agent-chosen: HTTP, Nostr, sneakernet. CAN defines what to verify, not how to connect.

CAN never reads keys it didn't generate. WHO-2 means YOU present a key to CAN, not CAN reaching for yours.

## CAN name all three

```
DNS:        namespace only         (no verify, no time)
GIT:        hashspace only         (no time-first, no human name)
IPFS:       hashspace only         (dead snapshots, no clock)
BLOCKCHAIN: timespace + hashspace  (no human namespace)
CAN:        all three              (WHERE + WHEN + WHAT)
```

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
