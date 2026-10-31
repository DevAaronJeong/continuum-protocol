# Experiment 2.5: Retrospective Fit Survey

> **Status:** Planned. This plan was written and committed before any data was collected (November 2026).
>
> Questionnaire: [retrospective-fit-survey-questions.md](retrospective-fit-survey-questions.md) · Analysis: [`examples/survey_analysis.py`](../../examples/survey_analysis.py)

---

## What this checks

The engine assumes that fit is about **matching intensity** ("walking at the same speed"). That's why it uses weighted Manhattan distance instead of cosine ([technical-philosophy.md](../technical-philosophy.md), [metric-analysis.md](../metric-analysis.md)).

This survey checks that assumption against people's own experience of real jobs. It doesn't try to "solve" fit or predict anyone. It asks one thing: when people describe themselves and a job they've had, does the engine's alignment score line up with how well they say that job fit?

Because this is an assumption check, the rules for reading the result are fixed **here, before any data comes in**, so the result can't be read to match what we hoped.

---

## Design

- **Who:** 20–30 adults who have worked at least one job for 3 months or more. A convenience sample: personal networks, GitHub Discussions, and a few communities.
- **What they answer:** their own rhythm on the engine's 5 dimensions, then 1–2 jobs on the same dimensions, plus how well each job fit (1–7) and how much they had to adjust themselves (0–10).
- **Unit of analysis:** one person–job pair. Each person contributes 1 or 2 pairs.
- **Encoding:** the engine's own. Energy rhythm uses the codes in `src/alignment_engine.py`, 0–10 answers are divided by 10, and the engine's default weights are used. **No weights are tuned on this data.**

---

## Primary check

For every pair, compute alignment with **weighted Manhattan** (the current engine) and **cosine** (the removed engine), from the same vectors and weights. Then compute the Spearman correlation between each score and the fit rating.

- `ρ_M` = correlation between Manhattan alignment and fit
- `d = ρ_M − ρ_cosine`
- 95% intervals for `ρ_M` and `d` come from a bootstrap that resamples **people**, not pairs (5,000 resamples, seed 2026).

### How the result will be read

| Result | Reading |
|---|---|
| The interval for `ρ_M` includes 0 | **The basic assumption doesn't hold here:** the alignment score doesn't track reported fit. This is reported first, whatever `d` says. |
| `d > 0` and its interval excludes 0 | Consistent with the "same speed" assumption: Manhattan tracks fit better than cosine. |
| `d < 0` and its interval excludes 0 | Inconsistent with it: cosine tracks fit better. We revisit the metric choice. |
| The interval for `d` includes 0 | Can't tell the two apart with this sample. |

**On sample size:** Manhattan and cosine scores are strongly related, so separating them takes data. In a made-up scenario where fit really follows Manhattan with fairly little noise, 30 people separated them about 80% of the time, and 60 people about 96%. Real answers will be noisier, so "can't tell" is a real possibility with 20–30 people. It would still be published.

---

## Secondary checks

These are reported, but they don't change the reading above.

1. **Adjustment effort:** correlation between alignment and how much people had to adjust (expected to be negative), for both metrics.
2. **Within-person:** for people who described two jobs with different fit ratings, how often does the job with the higher alignment score also get the higher fit rating? Compared for each metric. This sidesteps differences in how people use rating scales.
3. **Other metrics:** centered cosine, Euclidean, and Chebyshev (largest single gap), computed the same way.

## Exploratory

Labelled as exploratory in the results, with no conclusions drawn:

- Which single dimension's gap relates most to fit
- Asymmetry: does a job that's more intense than you hurt fit more than one that's less intense?
- Free-text answers, summarized by theme

---

## Exclusions

A response is excluded if:

- consent isn't given
- any Part 1 or Part 2 required answer is missing
- the attention item (`a_check`) isn't 4
- every 0–10 answer in the response is the same number

A second job is used only if all of its required answers are present. There are no other exclusions. The number excluded for each reason is reported.

## Stopping

The survey closes at **30 complete responses or 4 weeks after it opens, whichever comes first.** Nobody looks at the results before it closes. The analysis runs once, after closing, using the script as committed before opening.

---

## Data handling

- No names, emails, employers, or job titles are collected. No form setting that records who answered is turned on.
- Raw exports never go on GitHub. Keep them in `data/`, which git ignores.
- What gets published: summary numbers, the analysis output, and the code. Free-text answers are only published as summarized themes, never quoted in a way that could identify someone.
- Deletion: respondents can submit their code word through a separate deletion form. Matching responses are removed, and the analysis is re-run if it has already been done.
- Raw data is deleted 12 months after the results are published.

## Known limitations

- **Memory:** jobs are described from memory, and how a job ended can color how people remember it.
- **Same person on both sides:** each person rates themselves, the job, and the fit, so their general mood can tie the answers together.
- **Small convenience sample:** the result describes these respondents, not people in general.
- **Scales mean different things to different people:** "7 out of 10" isn't the same for everyone. The within-person check partly addresses this.

---

## Running the analysis

1. Export the responses as CSV from the form tool.
2. Rename the columns to the IDs below. Energy answers can stay as text, in English or Korean.
3. Save the file as `data/survey_responses.csv` and run:
   ```bash
   python examples/survey_analysis.py data/survey_responses.csv
   ```

To see what the output looks like first, run it on made-up data:

```bash
python examples/survey_analysis.py --demo            # fit follows Manhattan
python examples/survey_analysis.py --demo none       # fit is random
python examples/survey_analysis.py --test            # unit tests
```

### CSV columns

| Column | Values | Required |
|---|---|---|
| `consent` | any "yes" value (`true`, `yes`, `동의`, a checked box) | yes |
| `self_energy`, `a_energy`, `b_energy` | morning / afternoon / evening / varies (English or Korean labels from the questionnaire) | self, a |
| `self_flex`, `self_people`, `self_change`, `self_pace` | 0–10 | yes |
| `a_flex`, `a_people`, `a_change`, `a_pace` | 0–10 | yes |
| `a_fit` | 1–7 | yes |
| `a_adjust` | 0–10 | yes |
| `a_check` | 1–7 (must be 4) | yes |
| `a_current`, `a_duration`, `a_note` | as asked | no |
| `b_*` | same as `a_*`, without `b_check` | no |
| `work_type`, `region`, `code_word` | as asked | no |
