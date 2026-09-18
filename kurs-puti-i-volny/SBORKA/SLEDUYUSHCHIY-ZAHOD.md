---
opisanie: Program and calendar for the next executor's work on course corpus organization
sloj: 4
status: zhivoy
---

# Context for Next Executor: Q1 and Ongoing

Written after completing descriptions and cartoteka links for the course corpus (September 2026).

## Calendar Reality

First quarter (I) has **6 lectures**, fitting exactly into available slots:
1. 2026-09-19 (Sat)
2. 2026-09-26
3. 2026-10-03
4. 2026-10-10
5. 2026-10-17
6. 2026-10-24

**Year structure:** Q1=6, Q2=8, Q3=9, Q4=10 lectures total; 33 slots available, 32 topics needed.

## Course Shape (Owner Decision 2026-09-19)

**First lecture:** Line with `q` OFF (only combinatorics weight, no $q$-parameter)

**Quarter 1 emphasis:** Lines with `q` ON
- Young diagrams and Gaussian binomials
- Partitions generating function
- Foundation before moving to walls and weight

**Topics 5–6 moved to club:** Euler pentagonal theorem and Franklin involution defer to extracurricular club schedule; Q1 focuses on Young diagrams and generating functions.

**Analysis postponed:** No analytic methods (asymptotic, spectral) in first half — only combinatorial counting and bijections.

## Lecture-by-Lecture Plan (Q1, from `kurs-puti-i-volny/plan/src/karkas.md`)

### Block 1: Warm-up (1 lecture)
**Lecture 1. Paths and Binomial Coefficients**
- Object: $\binom{n}{k}$ as number of lattice paths
- Vandermonde identity, sum of squares by double counting
- Return to zero: probability $\sim 1/\sqrt{\pi n}$

### Block 2: Line with weight — Partitions (5 lectures, fills rest of Q1)

**Lecture 2. Young Diagrams**
- Partition = diagram; conjugation symmetry
- Partitions into distinct vs. odd parts: bijection via "double and divide"
- Area under path = Young diagram

**Lecture 3. Gaussian Binomial Coefficients**
- Object: $\binom{n}{k}_q$; partitions in a box
- Two Pascal rules via diagram dissection; palindromicity
- At $q=2$: equals number of 2D subspaces in $\mathbb{F}_2^4$

**Lecture 4. Partition Generating Function**
- Object: $\prod_{i \geq 1} \frac{1}{1-q^i}$
- Why product form; partitions with restricted parts
- First object with NO closed formula or bijection — signals need for new language

**Lecture 5. Pentagonal Numbers (Brief Version)**
- Object: $\prod_{i \geq 1} (1-q^i)$
- Why: infinite product collapses to series with only isolated nonzero terms
- Surviving exponents: $1, 2, 5, 7, 12, 15, 22, 26, \ldots$
- ⚠️ Full pentagonal theorem (Franklin involution) deferred to club

**Lecture 6. Franklin Involution (Adapted)**
- Sign-canceling involution on diagrams (partial version for Q1 review)
- Leads to recursion for $p(100) = 190,569,292$ hand calculation
- Technique: pair and cancel, answer is what survives

## Files Next Executor Must Read

**Main reference:** `kurs-puti-i-volny/plan/src/karkas.md` — complete lecture plan with central object per lecture.

**Calendar constraints:** `kurs-puti-i-volny/proverki/kalendar_goda.py` — check it to confirm slot counts.

**Status reference:** `kurs-puti-i-volny/SBORKA/REESTR-tekstov.md` sections A (ready), B (awaiting verdict), C (rejected) — understand which texts are live vs. archived.

**Course intent:** `kurs-puti-i-volny/ZAMYSEL.md` — why course exists, owner's design intent, decisions made 2026-09-02.

**Skeleton structure:** `obzory/funkciya-putey-i-ee-uravneniya/SKELET.md` — how all topics interconnect (both halves).

## Insights from This Work

### On Cartoteka Links
24 cartoteka cards exist (`catalan/kartoteka/KARTA-OBLASTI.md`); this round added ~10 new links to corpus files. Most are used in second half (weights, spectra, Franklin's involution). **First quarter has minimal cartoteka coverage** — Q1 stays in pure combinatorics.

### On Descriptions and Sloj
Files were assigned `sloj: 0–5` (intent → language → math → structure → pipeline → output). Most course texts landed in **sloj 0–2** (foundational design, not mechanistic).

### On Status: "Забракован" Does Not Mean Dead
Several "rejected" texts (`C1–C7` in registry) contain working material but were rejected as *full documents* — their components live in newer versions. `C4` "LEKCIYA/" marked "ЦЕЛЬ, НЕ ТЕКСТ" is deliberately left as a template showing what empty skeleton looks like.

### What's Missing for Next Round
1. **Q2–Q4 content:** Only Q1 is settled; next executor will add lecture files / syllabi for remaining quarters.
2. **Classroom exercises:** `kurs-puti-i-volny/tools/DOLG-bez-opisaniya.txt` mentioned that **problem sheets for each block are not written yet** — next work.
3. **Second pentagonal theorem proof:** Owner moved Euler pentagonal and Franklin to club; if Q1 lecture 5 needs its proof, it must come from club materials.
4. **Analysis section (Q2 onward):** Asymptotic behavior, spectral formulas, continuous limit — these require coordinate system and $m$ parameter; see `SKELET.md` part 2.

## For This Executor's Handoff

All 69 files in corpus now have YAML headers with `opisanie:`, `sloj:`, `status:` fields.
Cartoteka links added where corpus discusses topics matching card content.
`indeks.py` runs clean: `без описания: 0`, `✅ гейт зелёный`.

Next: verify this file is registered in `_studio/docs/KARTA.md`.
