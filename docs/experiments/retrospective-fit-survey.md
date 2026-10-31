# Experiment 2.5: Retrospective Fit Survey

> **Status:** Planned. This plan was written and committed before any data was collected (November 2026).
>
> Questionnaire: [retrospective-fit-survey-questions.md](retrospective-fit-survey-questions.md) · Forms: [`examples/survey_forms.gs`](../../examples/survey_forms.gs) · Analysis: [`examples/survey_analysis.py`](../../examples/survey_analysis.py)

---

## What this checks

The engine assumes that fit is about **matching intensity** ("walking at the same speed"). That's why it uses weighted Manhattan distance instead of cosine ([technical-philosophy.md](../technical-philosophy.md), [metric-analysis.md](../metric-analysis.md)).

This survey checks that assumption against people's own experience of real jobs. It doesn't try to "solve" fit or predict anyone. It asks one thing: when people describe themselves and jobs they've had, does the engine's alignment score line up with how well they say those jobs fit?

Because this is an assumption check, the rules for reading the result are fixed **here, before any data comes in**, so the result can't be read to match what we hoped.

---

## Schedule

| Date (2026) | Step |
|---|---|
| Nov 2 | Create the forms by running `examples/survey_forms.gs` in Google Apps Script |
| Nov 2–4 | Pre-check with about 5 people: are the questions clear, and does it take about 10 minutes? Their answers are not analyzed. |
| Nov 5 | Last changes to the questions. After this, nothing in this plan, the forms, or the analysis script changes. |
| **Nov 6** | **Survey opens** |
| Nov 20 | Mid-point check on the **number** of responses only (see Stopping) |
| **Nov 30** | **Survey closes** at the latest |
| After closing | Analysis runs once; results are published, whatever they show |

---

## Who takes part, and what that means

- **Who:** adults who have worked at least one job (part-time and freelance count) for 3 months or more.
- **How they're reached (all free):** shared by friends and their friends, GitHub Discussions, Korean online communities (where their rules allow surveys), [SurveyCircle](https://www.surveycircle.com), and Reddit r/SampleSize. Korean and English versions.
- **Target:** 100 complete responses.

**Who this really describes.** People who choose to answer a survey about whether their work fits them are likely to have strong feelings about it, often because it doesn't. Paid survey panels have their own lean as well. So the result describes **people who sought out a survey like this**, not workers in general. That is close to the people this protocol is meant for: people looking for work that fits better. Results will be written up with that scope.

**What protects the check from this.** The check compares two scores on the same people, so a lean in who answers affects both equally. The bigger risk is that everyone describes only jobs that didn't fit. So each person describes their current or most recent job, then is asked for a **contrasting job**: one that fit better if the first didn't, or worse if it did. That way each person can contribute both ends.

---

## Design

- **What they answer:** their own rhythm on the engine's 5 dimensions; their current or most recent job (3+ months) on the same dimensions, plus how well it fit (1–7) and how much they had to adjust themselves (0–10); optionally a contrasting second job, the same way.
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

**On sample size:** Manhattan and cosine scores are strongly related, so separating them takes data. In made-up data where fit really follows Manhattan and each person describes one job, 100 people found the basic relationship 93–100% of the time but separated Manhattan from cosine only 27–50% of the time, depending on how noisy the answers are (200 people: 40–80%). Second jobs add pairs and help. "Can't tell" is a real possibility, and it would still be published.

---

## Secondary checks

These are reported, but they don't change the reading above.

1. **Adjustment effort:** correlation between alignment and how much people had to adjust (expected to be negative), for both metrics.
2. **Within-person:** for people who described two jobs with different fit ratings, how often does the job with the higher alignment score also get the higher fit rating? Compared for each metric. This sidesteps differences in how people use rating scales.
3. **By channel:** the primary correlations computed separately for people reached through friends and people reached online (only for groups with 15 or more pairs). A big difference would mean the channel matters and is reported as such.
4. **Other metrics:** centered cosine, Euclidean, and Chebyshev (largest single gap), computed the same way.

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

A second job is used only if all of its required answers are present. Pre-check answers (Nov 2–4) are not analyzed. There are no other exclusions. The number excluded for each reason is reported.

## Stopping

- The survey closes at **100 complete responses or on November 30, 2026, whichever comes first.**
- Until it closes, only the **number** of responses is checked, never the answers.
- **Mid-point, November 20:** if there are fewer than 30 responses, the maintainer decides whether to add a paid panel (Opensurvey, about ₩165,000 including VAT for 100 people, using a shorter version with Parts 1–2 only). Whatever is decided is recorded in this file before closing, and any panel responses are reported as their own channel.
- The analysis runs once, after closing, using the script as committed before opening.

---

## Data handling

- No names, emails, employers, or job titles are collected. The forms are created with email collection and sign-in turned off.
- Responses stay in the maintainer's Google account. Raw exports never go on GitHub: keep them in `data/`, which git ignores.
- What gets published: summary numbers, the analysis output, and the code. Free-text answers are only published as summarized themes, never quoted in a way that could identify someone.
- Deletion: respondents can submit their code word through the separate deletion form. Matching responses are removed, and the analysis is re-run if it has already been done.
- Raw data is deleted 12 months after the results are published.

## Known limitations

- **Who answers:** see "Who this really describes" above.
- **Memory:** past jobs are described from memory, and how a job ended can color how people remember it. Starting from the current or most recent job limits this.
- **Same person on both sides:** each person rates themselves, the job, and the fit, so their general mood can tie the answers together.
- **Scales mean different things to different people:** "7 out of 10" isn't the same for everyone. The within-person check partly addresses this.

---

## Creating the forms

1. Go to [script.google.com](https://script.google.com) and click **New project**.
2. Delete the sample code, paste all of [`examples/survey_forms.gs`](../../examples/survey_forms.gs), and save.
3. Choose `createSurveyForms` and click **Run**. Allow Google to create forms in your Drive.
4. Open the **Execution log**. It lists the links to the Korean survey, the English survey, and the deletion form.
5. For SurveyCircle, add the survey code they give you to the end of the English form's confirmation message (Settings → Presentation).

## Running the analysis

1. In each form, open **Responses → ⋮ → Download responses (.csv)**.
2. Save them as `data/survey_ko.csv` and `data/survey_en.csv`. The `data/` folder is ignored by git. No renaming is needed: the script recognizes the question titles in either language.
3. Run:
   ```bash
   python examples/survey_analysis.py data/survey_ko.csv data/survey_en.csv
   ```

To see what the output looks like first, run it on made-up data:

```bash
python examples/survey_analysis.py --demo            # fit follows Manhattan
python examples/survey_analysis.py --demo none       # fit is random
python examples/survey_analysis.py --test            # unit tests
```
