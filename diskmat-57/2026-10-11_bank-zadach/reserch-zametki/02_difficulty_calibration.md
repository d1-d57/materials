# Estimating and parameterizing math problem difficulty with tiny samples (cold start, n≈30)

Note on sourcing: items marked [fetched] were read during this session. Items marked [known, not re-fetched] are well-known publications cited from prior knowledge, with a canonical URL or DOI. The report writer should treat their exact numbers as needing verification. Every other claim has an inline source.

## 1. How accurate are expert (teacher) judgments of item difficulty, and what improves them?

### Takeaway
Teachers rank *students* fairly well (meta-analytic r≈.6). They are much worse at giving *absolute* item difficulty (p-values) and show systematic biases that depend on their own class level. Comparative (relative) judgements of items work noticeably better than absolute ratings. Even the best feature- or judgement-based approaches historically explain only a modest share of difficulty variance.

### Cited Findings
- Südkamp, Kaiser & Möller (2012, J. Educ. Psychol. 104(3), 743–762) meta-analysed 75 studies of teachers' judgements of student achievement. The mean judgement–achievement correlation was ≈ .63, and it was higher when teachers were informed about the test or judged task-specifically. This is about judging students, not items. [known, not re-fetched] — [DOI 10.1037/a0027697](https://doi.org/10.1037/a0027697)
- Güzel & Başokçu (2023, *Metacognition and Learning* 18, 295–312) studied 38 teachers, 86 classes and 2,608 sixth-graders on a PISA-equivalent math test, with item-by-item and overall estimates:
  - Item-by-item estimates fell below actual performance; overall estimates did not.
  - Teachers of low-performing classes were less accurate and underestimated easy items.
  - Teachers of high-performing classes overestimated performance on difficult items.
  - The authors' interpretation is that teachers anchor on their perception of the class (a mnemonic cue) rather than on features of the item. — [Springer](https://link.springer.com/article/10.1007/s11409-023-09333-2) [fetched]
- El Masri (Oxford, 2016 project, page published 2019) ran a systematic review of judging demands and predicting task difficulty since 1980. It says predicting item difficulty "remains a major challenge" for teachers and test designers, and that "empirical attempts have not yet exceeded 25% of variance explained." — [Oxford Dept. of Education](https://www.education.ox.ac.uk/project/judging-demands-and-predicting-task-difficulty-a-systematic-review-of-the-literature/) [fetched]
- Attali, Saldivia, Jackson, Schuppan & Wanamaker (2014, ETS RR-14-39) had judges rank-order SAT math items in sets of 7. Judges ordered items "reasonably well", with little variation across judges or content areas. Simulations showed high true–estimated difficulty correlations with relatively few comparisons. The authors argue comparative judgement beats the noncomparative ratings of earlier studies, which had "disappointing results." — [ETS](https://www.ets.org/research/policy_research_reports/publications/report/2014/jtmq.html) [fetched; no coefficients on the abstract page]
- Benton (2020, *Research Matters*, Cambridge Assessment) reviewed evidence on whether experts' comparative judgements of item difficulty predict empirical difficulty, and proposed a CJ-based test-equating method. The figures were not visible on the landing page. — [Cambridge repository](https://www.repository.cam.ac.uk/items/01dff77d-441f-4d99-9a55-9ce3937c988f)
- Ofqual / MEI evaluated "expected item difficulty" for reformed A level and GCSE maths, using expert judgements of item difficulty compared against empirical data. These are relevant UK math-specific evaluations but were not read in detail. — [DERA A-level report](https://dera.ioe.ac.uk/id/eprint/31018/1/A_level_and_AS_mathematics_An_evaluation_of_the_expected_item_difficulty.pdf), [MEI GCSE](https://mei.org.uk/app/uploads/2021/08/MEI-App-4-Maths-GCSE-post161.pdf)
- Impara & Plake (1998, JEM) found that teachers estimated item p-values for the total group better than for "borderline" students. Absolute p-value estimates were poor, which is the standard criticism of Angoff standard setting. [known, not re-fetched]

### Inferences
- For a teacher of a single class, the observed biases suggest that *relative* placement ("harder than X, easier than Y" against already-calibrated anchors) is more trustworthy than an absolute guess such as "60% will solve it."
- The bias pattern (underestimating what kids can do on easy items, overestimating on hard ones) maps onto the teacher's two failure modes: a trivial problem everyone solved and an impossible problem nobody solved. Expect both errors at the tails.
- Practical improvements supported by the evidence: switch to comparative format (Attali 2014); give judges task-specific information (Südkamp moderators); give feedback against observed data. That last one is an inference from the "informed judgement" moderator, not a direct item-level finding.

### Gaps
- No meta-analysis specifically of teacher accuracy on *item* difficulty (as opposed to student achievement) was found. Coefficients for Attali 2014 and Benton 2020 were not extracted because the full PDFs were not read.
- No study found on olympiad-style or proof problems for 12–13-year-olds. All the evidence concerns standardized multiple-choice or short-answer items.

## 2. Comparative judgement (pairwise "which is harder", Bradley–Terry) with few judges

### Takeaway
CJ reliability is driven mainly by the number of comparisons per object, not by the number of judges. About 10 comparisons per item gives a scale separation reliability (SSR) of about .8. Ranking 100 problems therefore costs roughly 500 pairwise judgements, which is feasible for one teacher plus 4 assistants.

### Cited Findings
- Kinnear, Jones & Davies (2025, *Behavior Research Methods* 57:222) meta-analysed 101 CJ sessions. Their reliability measures are SSR, the internal scale separation reliability, and SHR, split-half inter-rater reliability.
  - Number of comparisons per representation was the only characteristic that remained a significant predictor in the final model. Number of assessors dropped out once it was controlled for.
  - SSR was ≥ .7 in 96 of 101 sessions; SHR was ≥ .7 in 68 of 101.
  - SSR and SHR correlated at r = .86.
  - Adaptive pairing inflates SSR: mean .92 vs .85.
  - Recommendations: aim for SSR ≥ .8 rather than .7; use ≥ 10 comparisons per representation (each item appears in ≥ 20 judgements as N_CR is defined); avoid adaptive pairing if SSR is to be interpreted.
  - Earlier guidance they cite: Wheadon 2015, ≥ 5 comparisons per representation; Bisson et al. 2016, ≥ 10 comparisons and ≥ 10 judges; Verhavert et al. 2019, ≥ 5 for .7 and ≥ 13 for .9; Crompvoets et al. 2021, N_CR ≥ 41. — [Springer, BRM 2025](https://link.springer.com/article/10.3758/s13428-025-02744-w) [fetched]
- Verhavert et al. (2019) is the original meta-analysis on CJ reliability. — [VU research portal](https://research.vu.nl/en/publications/a-meta-analysis-on-the-reliability-of-comparative-judgement/)
- Attali et al. (2014) used CJ specifically for *item difficulty*, with SAT math items ranked in sets of 7 (see section 1). Ranking k items at once yields k(k−1)/2 implied pairs per judgement, which is cheaper than strict pairs. — [ETS](https://www.ets.org/research/policy_research_reports/publications/report/2014/jtmq.html)
- Reference-based adaptive selection algorithms for CJ have been studied for efficiency, and they warn about inflated reliability. — [Frontiers in Education 2021](https://www.frontiersin.org/journals/education/articles/10.3389/feduc.2021.785919/pdf)

### Inferences
- CJ can be applied in two ways here:
  - (a) Rank problems by difficulty, using the teacher and assistants as judges, before use.
  - (b) Rank written solutions or photos by quality, which goes beyond solved/not solved. This is No More Marking-style use, and the literature mostly covers this case (essays and proofs).
- The resulting Bradley–Terry logits sit on a logit scale that can directly serve as a Rasch/Elo prior for item difficulty, up to a linear rescaling fitted once real response data arrive.
- The rank-in-sets format (Attali) suits sorting a sheet: "order these 7 problems by difficulty."

### Gaps
- No quantitative study was found that compares CJ-of-item-difficulty accuracy against empirical difficulty for small classes or for proof/olympiad problems.

## 3. IRT/Rasch with small samples, Bayesian priors, and Elo-style online ratings

### Takeaway
With 30 respondents, a Rasch item difficulty is only known to about ±1 logit (95% confidence). Elo-style updating with a decreasing K (uncertainty function) is the standard practical tool for cold start and gives JMLE-like estimates. Even so, item estimates need on the order of 100+ answers to be good. The data must therefore be pooled across years and classes, and expert/CJ priors are what make the first 30 answers informative.

### Cited Findings
- Pelánek (2016, *Computers & Education*, DOI 10.1016/j.compedu.2016.03.017), "Applications of the Elo rating system in adaptive educational systems":
  - Model: P(correct) = 1/(1+e^−(θs−di)); θs ← θs + K(correct − P); di ← di + K(P − correct).
  - Guessing variant: P = 1/k + (1−1/k)·logistic.
  - A constant K = 0.4 was used in earlier work. The uncertainty function U(n) = a/(1+bn) with a = 1, b = 0.05 is recommended from the geography system, and many a, b values give similar results.
  - Use separate uncertainty functions for items and students.
  - In simulation (150 items, 200 students), 10 answers per student gave a skill-estimate correlation of about 0.8 with ground truth. Item difficulty needs "at least 100 students" for good estimates.
  - Under adaptive item selection, raw proportion-correct gives biased difficulty estimates that do not improve with more data, while Elo stays close to JMLE.
  - Cold start: a new item starts at d = 0, or better at a prior, with large uncertainty.
  - Elo extends to response time (log-time) and to asymmetric updates for correct and wrong answers. — [Pelánek accepted manuscript](https://www.fi.muni.cz/~xpelanek/publications/CAE-elo.pdf) [fetched]
- A 2025 paper, "Keeping Elo alive: evaluating and improving measurement properties of learning systems based on Elo ratings" (Tilburg/KU Leuven/imec), examines the measurement properties of Elo-based systems. Full text was blocked, so no numbers were extracted. — [Tilburg](https://research.tilburguniversity.edu/en/publications/keeping-elo-alive-evaluating-and-improving-measurement-properties/), [PMC](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12784335/)
- Linacre (1994, *Rasch Measurement Transactions* 7:4) gives the Rasch rule of thumb: about 30 well-targeted persons calibrate an item to ±1 logit at 95% confidence, and about 100 persons give ±0.5 logit. [known, not re-fetched] — [rasch.org/rmt/rmt74m.htm](https://www.rasch.org/rmt/rmt74m.htm)
- Wauters, Desmet & Van den Noortgate (2012, *Computers & Education*), "Item difficulty estimation: an auspicious collaboration between data and judgment", compared proportion correct, IRT, Elo, learner feedback, expert ratings and paired comparisons as difficulty estimators. Pelánek cites them with 200 students. [known, not re-fetched; exact results not verified]

### Inferences
- Arithmetic for the teacher's metric (computed, binomial, independent solvers):
  - With true solve rate p and 28 kids, P(nobody solves) = (1−p)^28. At p = .10 this is ≈ .05; at p = .05 it is ≈ .24.
  - "Nobody solved it" is therefore strong evidence that p ≲ 10%, while "everybody solved it" implies p ≳ 90% with similar strength.
  - The standard error of an observed p-value at n = 28 is √(p(1−p)/28) ≈ .09 at p = .5, so the 95% interval is about ±.18. Differences smaller than about 0.2 in solve rate between two problems on one sheet are noise.
- Recommended cold-start pipeline (an inference that combines the sources):
  1. Seed each item's difficulty from a teacher or CJ logit, with large uncertainty.
  2. Update by Elo/Rasch with U(n) decreasing.
  3. Shrink toward the ○/△ track mean. This is hierarchical Rasch: a track or topic is an item family with a shared mean.
  4. Report a credible interval, not a point estimate.
  - The Bayesian version is a Rasch model with a N(prior_from_expert, σ²) prior on b_i. With n = 28 responses the posterior is roughly a precision-weighted blend of the prior and the data, so the expert prior dominates when σ_prior is below about 1 logit.
- Student ability can be estimated faster than item difficulty here, because each child answers many items.
- Not-attempted vs failed: the "solved / not solved" coding mixes "did not reach the problem" with "tried and failed". This biases difficulty upward for late problems on a sheet. A "not attempted" code is worth recording separately.

### Gaps
- Not found: a peer-reviewed study directly evaluating Bayesian Rasch with expert-informed priors at n≈30 for math items. That literature exists (e.g., Bayesian small-sample IRT), but no specific source was retrieved this session.
- The quantitative results of the 2025 "Keeping Elo alive" paper were not extracted.

## 4. Feature-based difficulty prediction: what properties of a math problem predict difficulty

### Takeaway
Text and feature models historically explain at most about 25% of difficulty variance in broad settings. Within well-defined item families (isomorphs differing in controlled "radicals"), designed features explain much more. The most transferable math features are: number of solution steps, cognitive complexity or demand, required method/concept, potential misconceptions, and linguistic load of the wording. Recent LLM-extracted versions of these features reach r ≈ .78 with IRT difficulty on large math datasets.

### Cited Findings
- El Masri's review: empirical feature-based predictions have "not yet exceeded 25% of variance explained." — [Oxford](https://www.education.ox.ac.uk/project/judging-demands-and-predicting-task-difficulty-a-systematic-review-of-the-literature/) [fetched]
- Hoyl (arXiv, Jan 2026) trained on more than 250k student responses to math questions. A neural net uses linguistic features plus LLM-extracted pedagogical features (solution step count, cognitive complexity, potential misconceptions) to simulate responses, from which IRT difficulty is derived. Pearson r ≈ .78 with actual IRT difficulty on unseen questions. Preprint, no baseline comparison in the abstract. — [arXiv 2602.00034](https://arxiv.org/abs/2602.00034) [fetched]
- AlKhuzaey et al. published a systematic review of text-based question difficulty prediction in *IJAIED* (2023/24). Benedetto et al. (2023, *ACM Computing Surveys*) surveyed question difficulty estimation from text. Both catalogue feature families: linguistic/readability, semantic, syntactic, cognitive level such as Bloom, and domain-knowledge features. — [Springer IJAIED](https://link.springer.com/article/10.1007/s40593-023-00362-1), [Liverpool repository](https://livrepository.liverpool.ac.uk/3172298/)
- A machine-learning difficulty-level estimation of mathematics problems was done at Mahidol (Thailand). Not read. — [Mahidol](https://repository.li.mahidol.ac.th/handle/123456789/84285)
- Background frameworks [known, not re-fetched]:
  - Item models / automatic item generation (Gierl & Lai; Irvine 2002): "radicals" are features that change difficulty or the cognitive process, while "incidentals" are surface features that should not. Isomorphs and item families share radicals.
  - Enright, Morley & Sheehan (2002, *Applied Measurement in Education* 15(1)), "Items by design", systematically varied features of GRE quantitative word problems and showed that the designed features accounted for a large part of difficulty variance.
  - Daroczy et al. (2015, *Frontiers in Psychology*) reviewed linguistic and numerical factors in word-problem difficulty.

### Inferences
- For a hand-tagged combinatorics/logic bank, candidate tag fields that the literature supports as difficulty predictors:
  - Number of reasoning steps or nested cases.
  - Need for an "idea" (a non-routine insight) versus routine application. This is cognitive demand, akin to Smith & Stein's levels of demand.
  - Method required, such as casework, bijection, invariant or pigeonhole, and whether it has already been taught.
  - Size of the search space (for enumeration).
  - Presence of a known misconception trap.
  - Wording length and complexity, and whether a picture is given.
- Tagging which features are radicals versus incidentals turns the bank into item families. Calibrating one member then gives a prior for its isomorphs, which is the main lever for reuse at n≈30.
- Data on the teacher's own tags (teacher-predicted ○/△ vs observed solve rate) can be fitted with a tiny regression, with 3–5 features over a few hundred item administrations across the year. This shows which tags actually carry signal in this class.

### Gaps
- Not found: feature-based difficulty studies specifically for olympiad-style combinatorics or logic problems.

## 5. LLM-based difficulty estimation: BEA 2024 shared task and 2024–2026 follow-ups

### Takeaway
On the BEA 2024 task (medical MCQs, 466 training items), almost all systems barely beat a predict-the-mean baseline: best RMSE 0.299 vs 0.311. Direct "LLM, rate this difficulty" prompting is weak. Simulating a classroom of LLM "students" and fitting IRT works much better for school math, with r ≈ .75–.82 against NAEP. These are research prototypes on standardized multiple-choice items, not olympiad problems.

### Cited Findings
- BEA 2024 shared task, as described in a participant paper (British Council): 667 retired USMLE MCQs (466 train, 201 test).
  - The DummyRegressor (mean) baseline RMSE was 0.311; the best run (EduTec "electra") was 0.299.
  - Only about 35% of submitted systems beat the baseline.
  - Feature-based linear regression was competitive with fine-tuned transformers on the small dataset.
  - Predictions were worst for very difficult items, and the small training set was a key limitation. — [ACL Anthology 2024.bea-1.42](https://aclanthology.org/2024.bea-1.42.pdf) [fetched]
- Another BEA 2024 paper presented an LLM-based pipeline for item difficulty and response time estimation (UCLA, Balaji Shankar, Alwan et al.). — [ACL Anthology 2024.bea-1.49](https://aclanthology.org/2024.bea-1.49/)
- Acquaye, Huang, Carpuat & Rudinger (arXiv 2601.09953, Jan 2026, v2 Apr 2026), "Take Out Your Calculators":
  - Abstract: LLMs are "poor direct judges of problem difficulty".
  - Open-source LLMs role-playing grade 4/8/12 classrooms at varied proficiency, with IRT fitted to the simulated responses, reached correlations of up to .75 (grade 4), .76 (grade 8) and .82 (grade 12) with NAEP math item correctness rates.
  - Larger simulated classes help. Named, demographically stratified personas beat ID-only personas.
  - The weaker-at-math Gemma predicted real difficulty better than stronger Llama and Qwen models, which suggests that strong solvers find everything easy. — [arXiv](https://arxiv.org/abs/2601.09953) [fetched; abstract-level]
- More 2026 work appears in AIME-Con 2026 main and work-in-progress papers on LLM difficulty estimation, and in an EDM 2026 poster. These were found by search but not read. — [AIME-Con 2026 main.42](https://aclanthology.org/2026.aimecon-main.42.pdf), [AIME-Con 2026 wip.24](https://aclanthology.org/2026.aimecon-wip.24/), [EDM 2026 poster](https://educationaldatamining.org/edm2026/proceedings/2026.EDM.poster-demo-papers.425/index.html), [arXiv 2504.08804](https://arxiv.org/abs/2504.08804)

### Inferences
- For this setting, an LLM is more useful as:
  - (a) an extractor of tag features (step count, required method, misconceptions), following Hoyl 2026;
  - (b) a generator of a "simulated class" prior, to be overwritten quickly by real data;
  - (c) one more judge in CJ.
  It is less useful as an oracle for absolute difficulty.
- The "weak model predicts better" result suggests prompting for typical 7th-grader errors, rather than asking a strong solver whether it can solve the problem.

### Gaps
- No study was found on LLM difficulty estimation for proof-based or olympiad combinatorics at middle-school level. All math results are on NAEP-style MCQs or large online platforms.
- The official BEA 2024 overview paper (organizers' findings) was not retrieved. Figures come from a participant paper.

## 6. Which per-attempt data are worth collecting

### Takeaway
In intelligent tutoring systems, "assistance" data (hints requested, number of attempts, time) predict outcomes better than correctness alone. First-attempt correctness is the standard binary signal. Response time can be folded into Elo/IRT. Pelánek's Elo framework already handles time and asymmetric right/wrong updates.

### Cited Findings
- Feng, Heffernan & Koedinger (2006, ITS conference, pp. 31–40), "Predicting state test scores better with intelligent tutoring systems: developing metrics to measure assistance required", logged hints requested and attempts made. Models using these assistance metrics predicted state test (MCAS) scores better than correctness-only models. The abstract reports "positive evidence"; no numbers were on the landing page. — [SRI](https://www.sri.com/publication/education-learning-pubs/digital-learning-pubs/predicting-state-test-scores-better-with-intelligent-tutoring-systems-developing-metrics-to-measure-assistance-required/) [fetched]
- The follow-up "Addressing the assessment challenge in an online system that tutors as it assesses" (Feng, Heffernan & Koedinger, 2009, UMUAI) is the extended version of the dynamic-assessment result. — [SRI](https://sri.com/?p=12263); [EDM08 paper PDF](https://web.cs.wpi.edu/~mfeng/pub/EDM08-prediction-final.pdf)
- Pelánek (2016) gives Elo variants for response time: log-time with expected time E = d_p − θ_s. The Math Garden "high speed, high stakes" score is S = (2·correct−1)(a·d − a·t). The same paper gives asymmetric correct/incorrect updates. — [Pelánek 2016](https://www.fi.muni.cz/~xpelanek/publications/CAE-elo.pdf) [fetched]

### Inferences
Priority list for the Telegram bot, ranked by information per unit of collection cost (inference):
1. First-attempt outcome, coded as one of: solved / wrong / not attempted / ran out of time.
2. Number of attempts until accepted.
3. Hint used (and which hint).
4. Error-type tag at acceptance, chosen from a short fixed list per problem. This builds the misconception features from section 4.
5. Time from opening the problem to first submission, logged and used as a secondary signal. For proof problems done on paper, timing is noisy.
6. Optional child self-rating ("hard / ok / easy"). Wauters 2012 included learner feedback as an estimator.

Partial credit (0/½/1, or a "+ / ± / ∓ / −" scale typical in Russian circles) supports a graded-response or partial-credit Rasch model. This extracts more information per child than binary scoring, an inference from standard IRT.

### Gaps
- Not extracted: quantitative effect sizes from Feng et al., such as the reduction in prediction error, and evidence that time data help item calibration in non-timed proof tasks.

## 7. Item statistics useful for a teacher: p-value, discrimination, sheet-level spread

### Takeaway
At n≈28, the p-value (solve rate) is the only robust per-item statistic, with an SE of about .09. Discrimination (point-biserial or item–rest correlation) has an SE of about .19 and is only indicative within one sheet. It becomes usable when pooled over sheets or years, or estimated in a Rasch/Elo model where ability comes from all problems. Sheet-level spread is best checked as the coverage of the class's ability range by item difficulties (a Wright map).

### Cited Findings
- Pelánek (2016): under adaptive or selective assignment, raw proportion-correct is biased, while model-based (Elo/JMLE) estimates are not. This matters if children choose problems or have different numbers of △ problems. — [Pelánek 2016](https://www.fi.muni.cz/~xpelanek/publications/CAE-elo.pdf)
- Linacre's rule of thumb: about 30 persons give ±1 logit. [known, not re-fetched] — [rasch.org](https://www.rasch.org/rmt/rmt74m.htm)

### Inferences
Computed statistics:
- SE(p) = √(p(1−p)/n), which is .095 at p = .5 and n = 28.
- SE of a correlation near 0 ≈ 1/√(n−1), which is about .19 at n = 28. A point-biserial of .3 on one sheet is therefore not distinguishable from 0.

Practical dashboard per sheet:
- Solve rate per problem, with a CI or flag. Flag p = 0 (true p ≲ .1, too hard) and p = 1 (true p ≳ .9, too easy), matching the teacher's success criteria.
- Item–rest correlation, flagged only when negative and the item is not "genius". A negative value is a hint of an ambiguous statement or a guessing artefact.
- Wright-map style plot of item difficulties against student abilities, to check spread. For the target "each child solves something, nobody solves everything", the item difficulties should span roughly the 10th–90th percentile of class ability.
- Per-track ○/△ mean and SD.
- Hidden "genius" problems are designed to have p ≈ 0–2/28. Exclude them from the "no problem nobody solved" metric or track them separately, since their p-value carries almost no information on 28 kids.

### Gaps
- No peer-reviewed source was retrieved that is specifically on classroom-scale (n<50) classical item analysis guidance. The recommendations above rest on standard sampling theory.
