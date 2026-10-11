# LLMs / neural models for annotating math problems and assessing student solutions (2023–2026)

## 1. Automatic knowledge-component (KC) / skill tagging of math problems with LLMs

### Takeaway
LLMs can propose KC tags, but exact agreement with expert tags is modest (one peer-reviewed study: 35–56% top-1 match with GPT-4), even though evaluators often *prefer* LLM-written KC labels. Tagging works best as "verify a candidate tag from a fixed list" (binary match task with retrieved examples), not open generation — so a hand-curated, explicitly defined skill list plus a few hundred hand-tagged items is exactly what later machine tagging needs.

### Cited Findings
- Moore, Schmucker, Mitchell, Stamper (ACM L@S 2024, DOI 10.1145/3657604.3662030; arXiv 2405.20526): GPT-4 generated/tagged KCs for multiple-choice questions; best strategy matched human-assigned KCs on 56% of Chemistry MCQs and 35% of E-Learning MCQs (higher when top-5 suggestions counted, number not in abstract). Three domain experts per domain preferred LLM-generated KCs over human ones ~2/3 of the time (statistically significant). Also an unsupervised clustering of questions by KC (no numbers in abstract). Not math-specific. — [arXiv 2405.20526](https://arxiv.org/abs/2405.20526v1)
- Li, Xu, Tang, Wen (Squirrel AI / MSU, arXiv 2406.13885, preprint): frame math knowledge tagging as binary judgment "does knowledge definition k match question q" with a flexible demonstration retriever (in-context examples), on an expert-annotated K-12 dataset "MathKnowCT". Accuracy figures not retrievable from the fetched text. — [arXiv 2406.13885](https://arxiv.org/html/2406.13885v1)
- Further related work found but not read in full: "Towards Scalable Annotation of Math Word Problems: KC Tagging via LLMs and Sentence Embeddings" (ICCE, APSCE) — [ICCE](https://library.apsce.net/index.php/ICCE/article/view/5574); "Leveraging LLMs for Identifying Knowledge Components" (arXiv 2511.09935) — [arXiv](https://arxiv.org/pdf/2511.09935); KC generation + knowledge tracing for coding problems (arXiv 2502.18632, Fernandez et al.) — [arXiv](https://arxiv.org/html/2502.18632v3).

### Inferences
- The tagging task the literature makes tractable is "pick from a defined list with definitions", so the bank should store each skill/method as an ID **with a one-paragraph textual definition and 2–3 canonical example problems** — these are exactly what retrieval-augmented taggers consume.
- 35–56% top-1 agreement means machine tags must stay "suggestions with human confirmation"; storing who assigned each tag (teacher vs model, with confidence) keeps future training data clean.
- Expert disagreement is a known ceiling; recording a second annotator on a small subset (e.g. an assistant) gives an inter-rater baseline against which any machine tagger can be judged.

### Gaps
- No math-specific, peer-reviewed number for LLM KC tagging accuracy on olympiad/discrete-math style problems (combinatorics, invariants, parity, etc.) was found. All found numbers are for K-12 word problems or non-math MCQs.
- Q-matrix construction with LLMs: not specifically searched due to budget; no numbers collected.

## 2. LLM difficulty estimation for items (brief)

### Takeaway
Zero-shot LLM difficulty estimates correlate weakly with empirical difficulty (Spearman ≲0.45 even on SAT Math); bigger models are not better. Real response data (attempts, correctness) remain necessary.

### Cited Findings
- Li et al. (UMD/CMU/Buffalo, arXiv 2512.18880, preprint): on SAT Math (1,385 items) Spearman ρ≈0.41 between LLM-predicted and empirical difficulty; GPT-4.1 ρ=0.44, GPT-5 ρ=0.34 (rising to 0.47 with ensembling over simulated proficiency levels, attributed to noise averaging). Average below 0.50 across four domains; USMLE ρ≈0.13. "Curse of knowledge": strong solvers fail to simulate student struggle; models predict their own failures at AUROC ~0.50–0.60. — [alphaXiv overview 2512.18880](https://alphaxiv.org/overview/2512.18880v1)
- Other 2025–26 work exists (EDM 2026 poster on difficulty estimation; Stanford EDS project on synthetic student responses + LLM-extracted features for IRT difficulty) — not read. — [EDM 2026](https://educationaldatamining.org/edm2026/proceedings/2026.EDM.poster-demo-papers.425/index.html); [Stanford EDS](https://ed.stanford.edu/eds/project/synthetic-student-responses-llm-extracted-features-irt-difficulty-parameter-estimation)

### Inferences
- The teacher's hand-assigned level is a prior; it should be stored separately from an empirical difficulty field computed later from attempts (solve rate, time, hints used).

### Gaps
- No numbers for LLM difficulty estimates on small, non-standard (olympiad-style) problem banks.

## 3. Grading handwritten math solutions from photos; proof grading; risks

### Takeaway
For computational/short-answer university work with a rubric, vision LLMs now reach ~90–95% rubric-item agreement with instructors; the dominant error source is transcription of the photo (blur, rotation, nested fractions, crossed-out work, diagrams), not the math judgment. Without a reference solution and rubric, LLM graders systematically over-credit ("leniency"), and for proofs even the best setup is ~1 point off on a 0–7 scale. Accepting wrong-but-polished work is the main documented risk.

### Cited Findings
- Caraeni, Scarlatos, Lan (LAK 2025; arXiv 2411.05231): GPT-4o graded scanned handwritten probability-course exams (18 students × 5 questions = 90 samples). Best prompt (response + correct answer + rubric): exact-score accuracy 0.467, Pearson 0.617, MAE 0.077 (normalized). Without reference, model overestimates; without rubric, underestimates (rarely gives partial credit). Gave full marks to faulty Chebyshev-inequality solutions; struggles to judge justifications. Small sample. — [arXiv 2411.05231](https://arxiv.org/html/2411.05231v2)
- Yu et al. (UC Irvine, arXiv 2603.00895, preprint, 2026): ~3,900 handwritten calculus quiz responses; GPT-4.1-mini for OCR+grading (o3-mini for hard items). AI scored on average 0.40 points below TAs; quiz-level MAE 0.5–1.06 points; within-1-point 68–86%. Independent reviewers: 79.8% evaluations fully correct, 9.6% acceptable, 10.7% incorrect. OCR: ~88% transcriptions acceptable; on a 171-solution subset GPT-4.1-mini 84% vs Mathpix 55%. Failure modes: nested fractions, crossed-out work, diagrams not reconstructed, autocorrection of student errors (<2%), hallucinated solutions in blank boxes. Error patterns: over-penalizing valid methods not in rubric, and leniency toward "rubric-shaped" explanations with wrong reasoning. Students: ~60% found feedback accurate; 52–53% preferred TA. — [arXiv 2603.00895](https://arxiv.org/pdf/2603.00895)
- Levine, Aenlle, Zilles, West, Silva (UIUC, arXiv 2605.19043, preprint, 2026): numerical methods + dynamics courses (55–242 submissions/question); rubric-item accuracy vs instructor: Gemini-3-flash 89–99% (~95% overall), GPT-5-mini 89–98%, GPT-5.1 87–95%. False-positive rate (rubric items credited by AI but not human) 0–9%; Gemini errors skew to false positives ~2.5:1. Transcription errors caused 87% of disagreements for the best model; hallucinated text on blurry/rotated photos sometimes resembled the reference solution and inflated scores. Recommendations: invest in image capture (preview transcription to student, reject rotated/blurry), use for low-stakes formative practice. — [arXiv 2605.19043](https://arxiv.org/pdf/2605.19043)
- Proof grading — Ma et al., "Reliable Fine-Grained Evaluation of Natural Language Math Proofs" (NeurIPS 2025 workshop / ICLR 2026; arXiv 2510.13888): ProofBench = 145 olympiad problems (APMO, EGMO, IMO, USA TST, Putnam, USAMO 2022–25), 435 expert-graded proofs on 0–7. Best grader (o3 + reference solution + marking scheme, median of 5 runs) MAE 0.926, Kendall τ ≈ 0.54–0.58. Without context, RMSE rose 1.273→1.901 and low-quality proofs (0–2) were over-scored by ~1.7 points (rewards polished but flawed write-ups). The marking scheme gave most of the gain; graders are sensitive to the specific rubric. When the grader cannot solve the problem itself, it credits partial progress badly. Self-family bias observed. — [arXiv 2510.13888](https://arxiv.org/html/2510.13888v1); [ICLR 2026](https://iclr.cc/virtual/2026/poster/10007732)
- Related, not read: RefGrader (agentic grading of competition proofs, NeurIPS 2025) — [NeurIPS](https://neurips.cc/virtual/2025/131062); DeepMind IMO-ProofBench — [alphaXiv](https://www.alphaxiv.org/benchmarks/google-deepmind/proofbench); MathArena human grading of USAMO/IMO model proofs — [MathArena](https://matharena.ai/imo/).
- Step-level verification: in ProcessBench, ~52% of Omni-MATH (olympiad-level) model solutions with a *correct final answer* still contained a process error — final-answer checking alone is unsafe for hard problems. — [arXiv 2412.06559](https://arxiv.org/pdf/2412.06559)

### Inferences
- For a bank, the highest-value fields for future auto-grading are: (a) reference solution(s), one per method; (b) an explicit marking scheme/rubric with partial-credit items (e.g. "found the invariant: +2"); (c) a list of known wrong approaches/typical errors. All three studies show grading quality collapses without (a)+(b).
- Multiple solutions per problem directly address the documented failure "over-penalizing valid methods not in the rubric".
- Seventh-grade discrete-math solutions are largely verbal arguments/case analyses — closer to proof grading (MAE ~1/7 with best setup) than to calculus computation (~95% rubric items). Realistic use: machine pre-check + flag, human final verdict; never auto-accept.
- The Telegram bot should keep the original photo, the machine transcription, and the human verdict side by side — that triple is the training/eval set for any future grader and lets one measure OCR error separately from judgment error.

### Gaps
- No study found on grading handwritten solutions of middle-school (grade 6–8) students, or in Russian handwriting/language.
- No study found reporting false-acceptance rates specifically on combinatorics/olympiad solutions by children.

## 4. Misconception / error diagnosis datasets and their labels

### Takeaway
Two Eedi Kaggle competitions define the de-facto schema: per multiple-choice distractor a misconception ID from a fixed bank (2024: 2,587 misconceptions, MAP@25, winners ~retrieve-then-rerank with Qwen + synthetic data); per student explanation a category + misconception (2025 MAP: MAP@3 >0.94 but only 15 questions, so generalization untested). Step-level work (ProcessBench) labels only "index of first wrong step". Generalizing to unseen misconceptions/questions is the open problem.

### Cited Findings
- Eedi "Mining Misconceptions in Mathematics" (Kaggle 2024): bank of 2,587 fine-grained math misconceptions; metric MAP@25; a silver-medal solution scored 0.50 private LB (retriever alone 0.42 MAP@25 on held-out fold). — [GitHub silver solution](https://github.com/DaoyuanLi2816/Kaggle-Eedi-Mining-Misconceptions-in-Mathematics-Silver-Medal)
- Same competition, winners (per Eedi): 1st — two-stage retrieve + rerank on Qwen with LoRA/contrastive learning on 10k synthetic + 1.8k real examples, reranking with Claude-generated student rationales; 2nd — CoT with Qwen2.5 + listwise rerank of top-25; 3rd — Qwen2.5-14B embeddings + 32B reranker with a scaling factor for unseen misconceptions; efficiency prize won by a 22.7M-parameter MiniLM without fine-tuning, gains from better queries + LLM-written misconception explanations. Key challenge: many test misconceptions unseen in training. Eedi's aim: help teachers tag misconceptions faster. — [Eedi blog](https://www.eedi.com/news/from-wrong-answers-to-real-insights-how-we-used-a-kaggle-challenge-to-map-student-misconceptions)
- "MAP – Charting Student Math Misunderstandings" (Kaggle 2025, Learning Agency + Eedi): inputs = question, chosen MC answer, student's free-text explanation; labels = correctness + category + misconception (taxonomy separates procedural vs conceptual errors, grades 4–8). Metric MAP@3; top >0.948 vs 0.75 baseline; top 1,000 teams all >0.941. Train/public/private shared the same 15 questions → generalization to new questions untested (flag: leaderboard numbers overstate real-world ability). Winners: suffix classification with shared-prefix attention; ~80k synthetic examples; 72B models run only on low-confidence cases. — [Learning Agency case study](https://the-learning-agency.com/the-cutting-ed/article/case-study-math-misconceptions-competition)
- MathDial (Macina et al., Findings of EMNLP 2023): ~3,000 one-to-one tutoring dialogues; human teachers tutor an LLM simulating a student with common errors on multi-step word problems; teacher turns annotated with a taxonomy of teacher moves (scaffolding etc.). Finding: LLMs solve well but tutor poorly — incorrect feedback and revealing solutions too early; fine-tuning on MathDial helps. — [ACL Anthology](https://preview.aclanthology.org/new-sigs/2023.findings-emnlp.372/)
- ProcessBench (Zheng et al., Qwen team, arXiv 2412.06559; ACL 2025): 3,400 cases (GSM8K 400, MATH 1,000, OlympiadBench 1,000, Omni-MATH 1,000); label = 0-indexed earliest erroneous step or −1; PhD-level annotators, 3–5 per item, ~30% discarded for disagreement. Average F1: best PRM 56.5 (Qwen2.5-Math-7B-PRM800K), GPT-4o 61.9, QwQ-32B 71.5, o1-mini 87.9; PRMs degrade sharply on harder problems. — [arXiv 2412.06559](https://arxiv.org/pdf/2412.06559)

### Inferences
- Misconception labels are useful only against a **closed, curated bank with text descriptions** — the same pattern as KC tagging. For a small class, a bank of typical errors per problem (e.g. "counted ordered pairs as unordered", "missed a case") is the right granularity.
- "First wrong step" is a cheap, well-defined step label that a teacher can record when checking; it is the one step-level schema with a public benchmark.
- Even MAP@3 = 0.95 came with only 15 questions; for a novel bank of hundreds of distinct problems, expect far weaker automatic misconception detection.

### Gaps
- Exact column names of the Eedi 2024 data (fields like ConstructName/SubjectName/AnswerText/MisconceptionId) not confirmed from a primary source in this session; winners' MAP@25 scores not retrieved.
- No public misconception dataset for discrete math/combinatorics at middle-school level found.

## 5. Data schemas a small bank should mirror (per problem / per attempt / per step)

### Takeaway
Across the datasets above, the recurring fields are: problem text + ID; skill/construct tags from a defined list; reference answer; reference solution(s); rubric/marking scheme; distractors or typical errors linked to misconception IDs; per attempt — student ID, problem ID, timestamp, raw response (image/text), correctness, score, misconception/error label, grader identity; per step — first-error index.

### Cited Findings
- Eedi/MAP 2025 data: "student IDs, problem IDs and text, the content of the response, and metadata such as misconception tags and correctness labels"; MC question with one correct answer + three distractors + optional written explanation. — [Learning Agency](https://the-learning-agency.com/the-cutting-ed/article/case-study-math-misconceptions-competition)
- Eedi 2024: per-distractor link to a misconception from a 2,587-item bank. — [GitHub](https://github.com/DaoyuanLi2816/Kaggle-Eedi-Mining-Misconceptions-in-Mathematics-Silver-Medal)
- ProofBench: per problem reference solution + marking scheme; per proof 0–7 expert score; 40% double-graded. — [arXiv 2510.13888](https://arxiv.org/html/2510.13888v1)
- ProcessBench: per solution step-segmented text + earliest-error index. — [arXiv 2412.06559](https://arxiv.org/pdf/2412.06559)
- Handwriting studies: grading inputs = image + rubric + reference; outputs = per-rubric-item selections, enabling FP/FN analysis per rubric item. — [arXiv 2605.19043](https://arxiv.org/pdf/2605.19043)

### Inferences
- Minimal machine-usable schema for the bank (inference, not a published standard):
  - problem: id, text (LaTeX/markdown), source, answer, solutions[] (each with method tag), skills[] (IDs from a defined dictionary with definitions), level (teacher prior), rubric items with points, typical_errors[] (IDs from an error dictionary), version.
  - attempt: attempt_id, student_id (pseudonymous), problem_id, problem_version, timestamp, photo, transcription (+ who/what produced it), verdict/score per rubric item, error IDs, first_error_step (optional), grader (teacher/assistant/model + model version), hint used, time-on-task if known.
- Rubric-item-level verdicts (not just total score) are what allow measuring machine false acceptance later.

### Gaps
- No single interoperable standard (e.g. xAPI/QTI-for-proofs) was found in use across these datasets; schema convergence is an inference.

## 6. LLM tutoring evidence from RCTs 2024–2026 (next-problem selection, explanations)

### Takeaway
Evidence is positive but modest and use-dependent: a teacher-in-the-loop copilot (+4 pp mastery, +9 pp for weaker tutors), guided classroom chatbot in Nigeria (0.31 SD overall, 0.23 SD English; working paper), meta-analytic mean ~0.18 SD across 13 experiments. Unrestricted answer-giving access can harm learning (−0.19 SD on later unassisted exam). No RCT found isolating LLM-driven next-problem selection.

### Cited Findings
- Tutor CoPilot (Wang et al., Stanford/NSSA, 2024–25 working paper): >700 tutors, ~1,000 students (secondary sources give 900/1,800 — conflicting); students 4 pp more likely to master topics (p<0.01), +9 pp for lower-rated tutors; ~$20 per tutor per year (one outlet says per pupil — conflicting). — [NSSA](https://nssa.stanford.edu/studies/tutor-copilot-human-ai-approach-scaling-real-time-expertise)
- Nigeria (De Simone et al., World Bank Policy Research Working Paper, May 2025): six-week RCT, first-year senior secondary; 0.31 SD overall, 0.23 SD on English. Not math. — [ibl.ai summary of WB paper](https://ibl.ai/blog/world-bank-group-from-chalkboard-to-chatbots-evaluating-the-impact-of-generative-ai-on-learning-outcomes-in-nigeria.md); [World Bank PDF](https://openknowledge.worldbank.org/bitstreams/cd9cca5b-2ffd-4be1-8313-0f4d2ed6ef4f/download)
- Bastani et al. ("Generative AI can harm learning", high-school math, Turkey): GPT-4 base access → −0.19 SD on later unassisted exam despite more practice problems solved (as summarized in Contractor & Reyes). — [arXiv 2607.08849](https://arxiv.org/pdf/2607.08849); [Stanford SCALE repository](https://scale.stanford.edu/ai/repository/generative-ai-can-harm-learning)
- Contractor & Reyes (Middlebury, arXiv 2607.08849, preprint July 2026): own RCT 211 undergraduates, +0.27 SD immediate test, similar retention; random-effects mean over 13 experiments/22 estimates = 0.18 SD; effect tracks how AI is used during practice (augmentation vs substitution). Mentions Chung et al. 2026 (AI tutor adapting order/difficulty of problems) and Kim et al. 2025 (AI only after attempting) without effect sizes. — [arXiv 2607.08849](https://arxiv.org/pdf/2607.08849)
- MathDial: LLM tutors reveal solutions too early and give incorrect feedback. — [ACL Anthology](https://preview.aclanthology.org/new-sigs/2023.findings-emnlp.372/)

### Inferences
- The strongest evidence supports "AI assists the human teacher" and "AI after the student's own attempt", which fits a bot that collects attempts and a teacher who verifies.
- Adaptivity claims from startups should be judged against the absence of RCT evidence for LLM-based next-problem selection specifically (flag hype).

### Gaps
- No Khanmigo RCT with published effect sizes was found in this session.
- No RCT isolating next-problem selection by LLM (vs classical knowledge-tracing/IRT) was found.
