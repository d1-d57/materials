# Skill tagging of problems: knowledge components, Q-matrix, granularity

Labels used in this file: **[measured]** means an empirical finding with data. **[design]** means a practitioner or author opinion or design rule. **[model]** means a modelling assumption.

## 1. KLI framework: what a knowledge component is, its types, and how granularity is chosen

### Takeaway
In the KLI framework (Koedinger, Corbett, Perfetti, *Cognitive Science* 2012), a KC is defined by performance: an acquired unit of cognition that is *inferred from performance on a set of related tasks*. The grain is set at "the level at which the novice makes errors", and everything below it is treated as atomic. A KC is therefore a hypothesis to be tested against data, not a label the author fixes by fiat.

### Cited Findings
- Definition: a KC is "an acquired unit of cognitive function or structure that can be inferred from performance on a set of related tasks". The term deliberately covers production rules, schemas, misconceptions, facets, concepts, principles, facts and skills. Many KCs operate at the unit-task level (~10 s, the application of a single operator). [design/theory] — [KLI paper v5 (Koedinger, Corbett, Perfetti; published 2012)](https://home.cs.colorado.edu/~mozer/Teaching/syllabi/TopicsInCognitiveScienceFall2011/KLI-paper-v5.00.pdf); [CMU KiltHub record](https://kilthub.cmu.edu/articles/journal_contribution/The_knowledge-learning-instruction_framework_bridging_the_science-practice_chasm_to_enhance_robust_student_learning_/6470522)
- The taxonomy has four dimensions:
  - Condition: constant or variable.
  - Response: constant or variable.
  - Verbal or non-verbal.
  - With or without rationale.

  These give three basic kinds. Constant–constant is a fact. Variable–constant is a category or concept. Variable–variable is a rule, schema or formula. Non-verbal KCs, such as many procedures and perceptual categories, cannot readily be articulated. — [KLI paper](https://home.cs.colorado.edu/~mozer/Teaching/syllabi/TopicsInCognitiveScienceFall2011/KLI-paper-v5.00.pdf)
- Granularity rule: focus on "the component level at which the novice student makes errors". Lower levels are treated as atomic on the empirical assumption that the population has mastered them. Because KCs are hierarchical, a course analysis can target only the level just above what novices already have. [design] — [KLI paper](https://home.cs.colorado.edu/~mozer/Teaching/syllabi/TopicsInCognitiveScienceFall2011/KLI-paper-v5.00.pdf)
- Typical times to apply a KC correctly [measured, illustrative]: Chinese vocabulary ~3–6 s, English articles ~6–10 s, geometry area ~10–14 s. KC description length grows with KC type: 6–9 words for constant–constant, 10–12 for variable–constant, 12–21 for variable–variable. Accuracy alone does not show fluency; timing data are needed. — [KLI paper](https://home.cs.colorado.edu/~mozer/Teaching/syllabi/TopicsInCognitiveScienceFall2011/KLI-paper-v5.00.pdf)
- Hidden or integrative KCs are inferred by contrasting task types, for example a hard composite task against its easier parts. One "subtraction logic" heuristic: P(integrative KC) ≈ success on the hard task ÷ success on the easier task, assuming independence. [model] — [KLI paper](https://home.cs.colorado.edu/~mozer/Teaching/syllabi/TopicsInCognitiveScienceFall2011/KLI-paper-v5.00.pdf)
- Difficulty Factors Assessment is named alongside think-alouds as a cheap empirical cognitive task analysis method. It works by systematically varying one feature of matched problems and comparing success rates. — [KLI paper](https://home.cs.colorado.edu/~mozer/Teaching/syllabi/TopicsInCognitiveScienceFall2011/KLI-paper-v5.00.pdf)

### Inferences
- The local definition, a skill as "an action the child performs", fits KLI well. In KLI terms most such skills are variable–variable rules or schemas, plus some non-verbal "noticing" KCs (for example, recognising that a set should be split by cases). The KLI test for a candidate skill is operational: do children who fail on it fail *together*, and do they improve with practice on it?
- "Level at which novices make errors" gives a usable stopping rule for a 7th-grade discrete-maths class. Do not tag skills that every child in the class already has, such as arithmetic. Do split a skill when children visibly succeed on one sub-case and fail on another.

### Gaps
- KLI gives no numeric granularity rule, such as a target number of KCs per hour of instruction.

## 2. The Q-matrix and cognitive diagnostic models: multiple skills per item, conjunctive vs compensatory

### Takeaway
A Q-matrix is a binary items × attributes table: 1 if the attribute is required for the item. The models that use it differ in how several required skills combine:
- **DINA** is conjunctive ("noisy AND": all required skills are needed).
- **DINO** is disjunctive ("noisy OR": any one is enough).
- **G-DINA** is the general form.

Multiple solution strategies need either one Q-matrix per strategy (MS-DINA) or a mixture model. All of these need hundreds of students to estimate. At N≈30 not all attribute patterns can even be observed.

### Cited Findings
- Q-matrix (Tatsuoka): q_kj = 1 if attribute k is required to answer item j correctly. "The rows represent attributes and the columns represent items." Each item also carries a slip parameter s_j and a guess parameter g_j. [model] — [Wang et al. 2020, Frontiers in Psychology 11:2120](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2020.02120/pdf)
- DINA = "noisy AND": a correct answer (apart from slips and guesses) requires mastery of all required attributes. DINO = "noisy OR": one required attribute is enough. [model] — [Wang et al. 2020](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2020.02120/pdf)
- Misspecifying the Q-matrix "can seriously affect the accuracy of the classification of examinees" and biases item parameters. In one revision on real data, an item's guess estimate went from 0.10 to 0.48 after its Q-row was corrected. On the classic fraction-subtraction data (536 examinees, 20 items), data-driven Q-entries agreed with the expert Q-matrix 84% of the time for the 10 items analysed. [measured] — [Wang et al. 2020](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2020.02120/pdf)
- Sample size: simulations ran N = 30…300. At N = 30 "not all attribute patterns can be observed", which lowered recovery. At N = 300, mean correct recovery of Q-entries was 0.79–0.86 depending on design. [measured, simulation] — [Wang et al. 2020](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2020.02120/pdf)
- Multiple strategies: most CDMs assume one solution method. MS-DINA (de la Torre & Douglas 2008) gives each strategy its own Q-matrix, and an examinee succeeds by having all attributes for *at least one* strategy. In the fraction example 4 4/12 − 2 7/12, strategy 1 needs attributes {a, b, c, d} and strategy 2 needs {a, b, f}. [model] — [Zhang et al. 2021, Frontiers in Psychology 12:568348](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2021.568348/pdf)
- Measured strategy split: of 528 students on 15 fraction-subtraction items, ~81.8% were classified as using strategy 1 throughout and ~18.2% strategy 2. In the same paper, information-criterion fit favoured plain DINA over the multi-strategy models on this dataset. **Caveat:** the paper is internally inconsistent about the ranking. [measured] — [Zhang et al. 2021](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2021.568348/pdf)
- Pelánek's practitioner survey: Q-matrices with N:M item–KC mappings suffer from the "credit/blame assignment problem". Research also "does not address how a Q-matrix should guide adaptive behaviour". [design] — [Pelánek, "Managing items and knowledge components: domain modeling in practice", ETR&D (~2019/2020)](https://www.fi.muni.cz/~xpelanek/publications/domain-modeling.pdf)

### Inferences
- With 28 students, no CDM can be fitted; DINA-type estimation needs hundreds. The *Q-matrix as a data structure* is still useful as the bank's "required skills" column. Its semantics should be explicitly conjunctive: the problem needs all listed skills.
- For problems with several genuinely different solution routes (common in olympiad-style combinatorics), the literature's answer is a *separate skill set per method* (per-strategy Q-rows). That maps directly onto the bank having "method" records under a problem, each with its own skill list, and on the "required skills" field being the intersection or the cheapest route.

### Gaps
- No source found on CDMs or Q-matrices for olympiad-style or proof-type problems; the literature is dominated by fraction arithmetic and test items.

## 3. Refining expert KC models with data: LFA, DataShop, learning curves, expert blind spot

### Takeaway
**[measured]** across many datasets: expert or textbook KC models are almost always improvable. The typical fix is *splitting* an over-general KC that hides a skill experts did not count, such as "decompose the figure yourself" or "work the formula backward". The diagnostic is the learning curve per KC (error rate against opportunity number):
- **Smooth and decreasing** means the KC is coherent.
- **Flat** means no learning, or a KC that is too broad or already mastered.
- **Blips or spikes** mean a mixture of items with different hidden demands.

The expert blind spot is itself documented. Teachers predicted symbolic equations would be easier than story problems; students showed the opposite (42% vs 70% correct).

### Cited Findings
- **LFA** (Cen, Koedinger, Junker, ~2005/2006) has three parts:
  - A statistical model: AFM, a logistic regression with a student intercept, a KC intercept (difficulty) and a KC slope × opportunity count (learning rate).
  - Expert-supplied "difficulty factors".
  - A search (A*, scored by AIC/BIC) that splits KCs by factor values.

  Data: Geometry Tutor area unit, 24 students, 4,102 data points, 115 steps, 15 initial skills. The best BIC model cut BIC by 37 and AIC by 62, and MAD fell from 0.083 to 0.071. Example: compose-by-multiplication split into an area version (final P≈0.96) and a segment version (initial 0.32, final 0.60). The merged skill had looked mastered (0.92) while one subskill was weak, so knowledge tracing on the coarse KC would miss it. [measured] — [Cen, Koedinger, Junker, LFA paper](https://www.ml.cmu.edu/research/dap-papers/cen_kddpaper2.pdf)
- A "blip" in a learning curve signals a hidden KC. Example: Declare-Parameter split into Declare-First-Parameter and Declare-Second-Parameter, which gave smoother curves. [measured] — [LFA paper](https://www.ml.cmu.edu/research/dap-papers/cen_kddpaper2.pdf)
- **DataShop case study** (Koedinger, geometry), with learning curves read as described in the Takeaway. Compose-by-addition showed error rates around 27–30%, with a ~50% peak at opportunity 12. Inspection showed some problems required the student to *generate the sub-goal decomposition* while others supplied it. The KC was split into "Decompose" (4 problems) and "Compose-by-addition". Peaks disappeared, all points fell below 30%, and AIC/BIC improved even after penalising the extra KC. The KC model was edited as a spreadsheet and re-imported. [measured] — [DataShop case study](https://pslcdatashop.web.cmu.edu/about/case-studies/koedinger-geometry-script-for-web.htm)
- Liu, Koedinger, McLaughlin (EDM 2014): automated LFA search improved on the best human KC models in **all 11** DataShop datasets by cross-validation. The gains were small in RMSE; in one case 0.403 vs 0.406. Hidden KC found: circle area *backward* (radius from area) vs *forward*, interpreted as "knowing when to apply a square root". The interpretation was confirmed on a new dataset of 82 students and 72,404 steps. Recommended cycle:
  1. Use the algorithm's output to find candidate splits.
  2. Inspect the data for where the split does and does not appear.
  3. Develop a cognitive interpretation.
  4. Test it on new data with different task types.
  5. Compare candidate models by AIC/BIC/cross-validation and learning-curve slopes.
  6. Redesign instruction and test whether learning improves.

  [measured + design] — [Liu, Koedinger, McLaughlin, EDM 2014](https://educationaldatamining.org/EDM2014/uploads/procs2014/long%20papers/107_EDM-2014-Full.pdf)
- **Counter-evidence:** van de Sande (Pearson, EDM 2016) studied 62,000 expert-tagged exercises from 10 college textbooks (~12 KCs per chapter, mean 3.84 practice opportunities per KC). Most per-KC learning curves were *not* monotone decreasing. *Problem* difficulty varied more than KC difficulty (SD 1.15 for problem difficulty vs 1.02 for student skill), and problem difficulty explained performance better than KC mastery did. Coarse expert tagging plus few opportunities per KC yields KC models with little predictive value. [measured] — [van de Sande, EDM 2016](https://www.educationaldatamining.org/EDM2016/proceedings/paper_127.pdf)
- **Expert blind spot** (Koedinger & Nathan 2004, *J. Learning Sciences*):
  - Percent correct by representation:

    | Study | Story problems | Word equations | Symbolic equations |
    |---|---|---|---|
    | DFA1 (n = 76) | 66% | 62% | 43% |
    | DFA2 (n = 171) | 70% | 61% | 42% |

  - No-response rate: 26% on equations vs 8% on verbal forms.
  - Students on story problems mostly used informal strategies: "unwind" 50% and guess-and-test, with 69–71% accuracy, against 51% for symbol manipulation.
  - Most of 67 high-school maths teachers and a majority of 35 maths-education researchers predicted the reverse difficulty order.

  [measured] — [Koedinger & Nathan 2004](https://www.stat.cmu.edu/~brian/PIER-methods/For%202013-03-04/Data/Koedinger-Nathan-LS04.pdf)
- In a survey of 105 teachers, high-school teachers held the "symbol precedence" view most often and predicted student difficulty *worst*; middle-school teachers predicted best. [measured] — [Nathan & Koedinger 2000 summary](https://mathed.net/wiki/Nathan_%26_Koedinger_(2000)_C%26I)
- Koedinger et al. (PNAS 2023), via a secondary summary: across >6,000 students, KC-level learning curves fitted with AFM-style models showed:
  - Prior knowledge averaged ~65% correct, ~55% for weaker students and ~75% for stronger.
  - Learning per opportunity was nearly uniform, ~2.5 percentage points.
  - Reaching 80% took ~4 opportunities for strong students, >13 for weak ones, ~7 on average.

  [measured; secondary source] — [Scott Young summary of Koedinger et al. 2023](https://www.scotthyoung.com/blog/2024/02/06/learning-rate-paper/). A 2026 re-analysis questions the sensitivity of these rate estimates to sequence length — [arXiv 2605.01690 listing](https://fugumt.com/fugumt/paper_check/2605.01690v1) (not read in full).

### Inferences
- With 28 students and ~170 marked items, formal LFA/AFM fits will be very noisy; the original LFA demo used 24 students but ~4,000 step-level observations. The *qualitative* method transfers, though:
  - Tag by expert judgement.
  - Look per skill for items where the class did unexpectedly worse.
  - Ask what that item demands that the others do not.
  - Split the skill or add a hidden skill.
- Hidden skills most likely in this domain, by analogy with "Decompose" and "backward" (these are inferences, not findings):
  - The child chooses the case split themselves vs is given it.
  - The child must invent the enumeration order vs is given it (already in the local skill list).
  - Translating a word statement into a combinatorial object.
  - Working backward from an answer or invariant.
  - Recognising that a parity or invariant argument applies at all.
- The ~7 opportunities per KC to mastery figure implies a fine-grained skill needs ~7+ items in the bank *at the right level*, or the tutor cannot run a practice cycle on it.

### Gaps
- No primary access to the PNAS 2023 paper text; numbers come from a secondary summary.
- No found studies of learning-curve KC refinement at N≈30 class scale.

## 4. Skill vs method vs strategy vs misconception

### Takeaway
The literature separates these only partly:
- KLI puts misconceptions under "KC", as buggy KCs.
- CDMs model strategies as alternative Q-rows.
- Student-modelling surveys describe strategy and misconception tagging as additions on top of KC mapping.

There is no consensus schema. The standard practical move is to tag the *required* skills of the intended or most common solution, and to record the method actually used separately at the attempt level.

### Cited Findings
- KLI explicitly includes misconceptions (buggy KCs) and "facets" within the KC notion; the KC concept is not limited to correct skills. — [KLI paper](https://home.cs.colorado.edu/~mozer/Teaching/syllabi/TopicsInCognitiveScienceFall2011/KLI-paper-v5.00.pdf)
- Strategies as separate Q-matrices (MS-DINA), and mixtures estimating each student's strategy (MMS-DINA). The MS-DINA restriction of identical item parameters across strategies is "too restrictive", since strategies differ in difficulty. [model] — [Zhang et al. 2021](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2021.568348/pdf)
- Strategy is observable and changes difficulty, measured on start-unknown algebra problems:
  - Strategy chosen depends on representation. On story problems: unwind 50%, guess-and-test 7%, symbol manipulation 5%. On symbolic equations: unwind 13%, guess-and-test 14%, symbol manipulation 22%.
  - Success differs by strategy: 69% for unwind vs 51% for symbol manipulation.

  [measured] — [Koedinger & Nathan 2004](https://www.stat.cmu.edu/~brian/PIER-methods/For%202013-03-04/Data/Koedinger-Nathan-LS04.pdf)
- Wrong answers are highly skewed: a few common errors dominate. For example, 12 − 6 + 4 → common wrong answer 2. Pelánek recommends collecting them from constructed-response items and reusing them, as distractors and as misconception signals. [measured, informal + design] — [Pelánek, domain modeling](https://www.fi.muni.cz/~xpelanek/publications/domain-modeling.pdf)

### Inferences
- For the bank, a clean split consistent with the literature:
  - **Problem level:** required skills (conjunctive) for the reference solution, plus optional alternative methods, each with its own skill list (per-strategy Q-rows).
  - **Attempt level:** the method the child actually used, and the error type or misconception. Teacher markings ("+", "±", "−") get richer if they carry a method or error code.
- Strategies differ in difficulty, so difficulty belongs to the method too, not only to the problem. A problem solvable by brute force at level "easy" and by a bijection at level "hard" is effectively two practice opportunities for different skills.

### Gaps
- No systematic empirical work found on how ITSs (ASSISTments, Khan Academy) treat open problems with several valid methods. Step-based tutors such as Cognitive Tutors handle it via multiple production-rule paths, but no concrete source was retrieved here.

## 5. Practical granularity: KCs per item, ASSISTments WPI models, Math Academy and Khan knowledge graphs

### Takeaway
Measured, ASSISTments: finer hand-tagged skill models predicted state-test outcomes better than coarse ones. The ladder was 1 skill (WPI-1), 5 skills (WPI-5), 39 skills (WPI-39), and 78 skills (WPI-78, the used part of the 106 coded). Raters agreed poorly at fine grain. Items were capped at ≤3 skills and averaged 1.44; scaffold sub-steps averaged 1.03.

Practitioner advice:
- Pelánek: one KC per item, a tree of KCs, three difficulty levels, and ≥15–40 items per KC.
- Math Academy: thousands of fine "topics", each a single problem-solving skill. A prerequisite DAG and a separate manually weighted "encompassing" graph let practice on an advanced topic count as implicit review of simpler ones.

### Cited Findings
- **ASSISTments WPI models** (Feng, Heffernan et al., ~2006–2008), as described in the Takeaway. In 2006 (474 students), WPI-78 was reliably better than WPI-39, WPI-5 and WPI-1 (p < .001); in 2005 (447 students) WPI-78 and WPI-39 tied. [measured]

  | Model | % error predicting state score, 2005 | 2006 |
  |---|---|---|
  | WPI-1 | 13.00% | 19.37% |
  | WPI-5 | 12.85% | 19.14% |
  | WPI-39 | 12.41% | 15.10% |
  | WPI-78 | 12.09% | 14.70% |
  | IRT (Rasch) | 12.82% | 13.70% |

  The source's text conflicts with its own table on the IRT vs WPI-78 comparison; rely on the table. — [Feng et al., "Using mixed-effects modeling to analyze different grain-sized skill models"](https://web.cs.wpi.edu/~mfeng/pub/IEEE_feng.pdf); [SRI publication page](https://www.sri.com/publication/education-learning-pubs/analyzing-fine-grained-skill-models-using-bayesian-and-mixed-effect-methods/)
- How WPI-106 was built: one subject expert, about 300 released 8th-grade MCAS items, about 7 hours (April 2005). The coding was cognitive task analysis using piles of printed items. The cap was "no one item would be tagged with more than 3 skills". An earlier uncapped session produced items with up to **9** skills, which the authors judged unworkable. Main questions averaged **1.44** skills; scaffolding sub-questions averaged **1.03**. [measured/design] — [Feng et al.](https://web.cs.wpi.edu/~mfeng/pub/IEEE_feng.pdf)
- Inter-rater reliability of fine tagging, on 50 items with two teachers vs the expert: full agreement 22%, partial 56%, disagreement 22%. At the skill level raters disagreed more than they agreed: teacher A 38 agreements vs 54 disagreements, teacher B 37 vs 71. [measured] — [Feng et al.](https://web.cs.wpi.edu/~mfeng/pub/IEEE_feng.pdf)
- **Pelánek's practical rules** [design, from experience running adaptive systems]:
  - Map each item to **one** KC (1:N). For cross-KC items, either create an integrative KC or duplicate the item into each KC.
  - A tree or taxonomy of KCs is usually enough; avoid Bayesian networks, full ontologies and knowledge-space theory for systems with hundreds of KCs.
  - Soft prerequisite and "follow-up" links are useful for recommendation.
  - **Three difficulty levels** within a KC are sufficient; choose randomly within a level.
  - For a few-minute session without repeats, a KC needs at least about **40 items** if items are simple (<10 s) and about **15** if complex.
  - Coarse KCs with narrow coverage are useless, and fine KCs with broad coverage are unmanageable.
  - Fine KCs suit BKT, intermediate ones suit AFM, very coarse ones suit IRT.
  - Keep KCs homogeneous in type: fact, concept or rule.
  - Heavily used KCs deserve manual refinement.
  - Do not split difficulty mechanically if that reinforces a wrong heuristic.

  — [Pelánek, domain modeling in practice](https://www.fi.muni.cz/~xpelanek/publications/domain-modeling.pdf)
- **Math Academy** (Skycak, *The Math Academy Way*, working draft 2023–2024):
  - A topic is "a problem-solving skill", for example multiplying a 2-digit number by a 1-digit number.
  - Topics are learned only after prerequisites; a new topic starts with a lesson of ~10 questions, and later reviews are 3–5 questions.
  - *Encompassing* is a separate relation from prerequisite. Topic A encompasses B when practising A also practises B; the 2×1-digit multiplication example encompasses 1-digit multiplication and adding 1-digit to 2-digit numbers.
  - Partial encompassings get manual weights in [0, 1], interpreted as "the probability that a random advanced problem encompasses a random simpler problem". Weights are usually set only on direct or key-prerequisite edges, and can be 0 for a prerequisite needed only conceptually.
  - Credit flows down (passing an advanced review credits simpler topics) and penalties flow up. Review selection picks tasks that knock out several due reviews at once ("repetition compression").
  - The whole graph has "thousands" of topics. AP Calculus BC has 300+ topics and takes ~6,000 min, i.e. ~20 min per topic.

  [design; vendor self-description] — [Skycak, "Optimized, individualized spaced repetition in hierarchical knowledge structures" (archived)](https://gwern.net/doc/www/www.justinmath.com/9af2ce40376e836660c237a0e971d1896a163eee.html); [The Math Academy Way PDF](https://www.justinmath.com/files/the-math-academy-way.pdf); [Hecker's summary, 2025](https://frankhecker.com/2025/02/10/math-academy-part-3/)
- Math Academy's claimed 4× acceleration is the vendor's own claim and not independently verified. — [Hecker 2025](https://frankhecker.com/2025/02/10/math-academy-part-3/)

### Inferences
- The defaults best supported by evidence and practice for a small hand-tagged bank:
  - 1–3 required skills per problem, with an average around 1.5.
  - One "primary" skill per problem, used for selection and progress, plus optional secondary skills.
  - A shallow tree of skills with a few soft prerequisite links.
  - 3 difficulty levels.
- At ~20 min per Math Academy topic, versus a 90-min weekly pair, a 7th-grade year of ~30 pairs supports something like 30–80 fine skills taught explicitly. This is a back-of-envelope estimate, not a finding.
- The 22% full inter-rater agreement is a strong argument for *operational definitions* of each skill, including what counts and what does not, with 1–2 anchor problems per skill. The local "action the child performs" definitions are the right direction.
- The *encompassing* relation is exactly what a tutor needs to decide "what next" in a spiral course. A hard problem using "sum rule" + "case split" counts as partial practice of both. It is cheap to add as an optional weighted link at skill level, not at problem level.

### Gaps
- **Khan Academy:** no primary source was retrieved on its current skill or "mastery" model and exercise–skill mapping, so no claims are made here.
- No retrieved study gives an optimal number of KCs per item for open-ended olympiad-style problems.

## 6. Item families, isomorphs, variants: one item or several?

### Takeaway
Variants from one template or "isomorphs" are standardly grouped as one family or KC unit. Measured and documented variation shows they are *not* reliably equal in difficulty, so they should be treated as one *problem* (shared skills, shared solution idea) but as separate *items* for logging outcomes and difficulty. The ETS item-model literature exists specifically to test "how isomorphic" family members really are.

### Cited Findings
- Template-generated items in maths can differ widely in difficulty. 1/2 vs 2/10 is much easier than 4/6 vs 5/8, and templates usually ignore this. Pelánek recommends a hybrid: generate from templates, then fix by hand. Use similarity measures to find duplicates and outliers, and avoid presenting near-identical items back to back. [measured informally + design] — [Pelánek, domain modeling](https://www.fi.muni.cz/~xpelanek/publications/domain-modeling.pdf)
- Pelánek: items solvable by a heuristic such as "compare numerators" are systematically easier. Grouping by surface difficulty can reward a wrong heuristic, so variants that break the heuristic are needed. [design] — [Pelánek](https://www.fi.muni.cz/~xpelanek/publications/domain-modeling.pdf)
- ETS (Sinharay & Johnson 2005, RR-05-06) proposes "a rigorous statistical diagnostic to assess the extent of isomorphicity" for item models (families) and notes scoring with item-model data needs more research. Only the abstract was accessed. — [ETS RR-05-06](https://www.ets.org/research/policy_research_reports/publications/report/2005/hyxs.html)
- The LFA results show that seemingly same-skill items (circle area forward vs backward; compose with vs without given sub-goals) differ by a hidden KC, so "variant" status must be checked against which actions the child performs. [measured] — [Liu et al. 2014](https://educationaldatamining.org/EDM2014/uploads/procs2014/long%20papers/107_EDM-2014-Full.pdf); [DataShop case](https://pslcdatashop.web.cmu.edu/about/case-studies/koedinger-geometry-script-for-web.htm)

### Inferences
- Recommended structure, an inference from the above:
  - **One problem record** holds the shared skills, the idea and the solutions.
  - **Variants A/B** are child items, each with its own answer and outcome log, and an optional "difficulty delta" or flag "differs in an action".
  - If a variant changes *what the child does* (backward vs forward, case split given vs self-chosen, enumeration order given vs not), it is not a variant but a different item with an extra skill.
  - Variants are where cheap Difficulty-Factors-style contrasts come from: change one feature, compare success.
- For 28 children, variants A/B given to halves of the class are the only realistic way to collect contrast data on hidden skills.

### Gaps
- The classic Tower-of-Hanoi isomorph results (Kotovsky, Hayes & Simon 1985) are widely cited as showing large difficulty differences between formally identical problems. The exact figures were not verified from a primary source in this session, so no number is given.
- No found empirical study on A/B parallel variants in small-classroom problem banks.
