# Experiment 2.7: Want vs. Have in Public Survey Data

> **Status:** Planned. This plan was written and committed before the data was downloaded (November 2026). The maintainer has read the questionnaire but not the data.
>
> Data: [ISSP 2015 "Work Orientations IV"](https://www.gesis.org/en/issp/data-and-documentation/work-orientations/2015) (GESIS ZA6770, DOI [10.4232/1.12848](https://doi.org/10.4232/1.12848)) · [Work Orientations I–IV cumulation, 1989–2015](https://www.gesis.org/en/issp/data-and-documentation/work-orientations/cumulation) (ZA8797) · [Work Orientations V, 2025](https://www.gesis.org/en/issp/data-and-documentation/work-orientations/2025) (data expected April 2027) · Analysis: `examples/issp_fit_analysis.py` (committed before the data is downloaded)

---

## What this checks

The engine scores fit by how far a person's preferences are from what a job offers, using Manhattan distance ([technical-philosophy.md](../technical-philosophy.md), [metric-analysis.md](../metric-analysis.md)). Experiment 2.5 checks that with a new survey, but its results won't exist before April 2027.

The International Social Survey Programme (ISSP) already asked tens of thousands of working people the two halves of that question:

- **Want:** how important each feature of a job is to them
- **Have:** whether their own job has it

So this experiment asks, on existing data and without recruiting anyone:

1. Does the distance between what people want and what their job gives them track how satisfied they are with the job?
2. Does Manhattan distance track it better than cosine?
3. Has that relationship stayed the same from 1989 to 2015, and does it hold in the 2025 data?

As in Experiment 2.5, the rules for reading the result are fixed **here, before the data is downloaded**.

---

## Data

| Dataset | What it adds | Access |
|---|---|---|
| ISSP 2015, Work Orientations IV (ZA6770) | Primary analysis. About 51,700 respondents in 37 countries (Japan, China and Taiwan included; South Korea not) | Free registration at GESIS |
| ISSP 1989–2015 cumulation (ZA8797) | Stability over 26 years, using the item pairs asked in all four waves (South Korea took part in 1989 only) | Free registration at GESIS |
| ISSP 2025, Work Orientations V | Repeat of the primary analysis on current data, when released (preliminary April 2027, final August 2027) | Free registration at GESIS |

The data is used under GESIS's terms of use. It is never committed to this repository: it stays in `data/`, which git ignores. Only code and aggregate results are published, with the dataset citations above.

---

## Item pairs (2015 questionnaire)

| Feature | Want: "How important is…" | Have: "For each statement about your (main) job…" |
|---|---|---|
| Security | Q2a job security | Q12a My job is secure |
| Income | Q2b high income | Q12b My income is high |
| Advancement | Q2c good opportunities for advancement | Q12c My opportunities for advancement are high |
| Interest | Q2d an interesting job | Q12d My job is interesting |
| Independence | Q2e a job that allows someone to work independently | Q12e I can work independently |
| Helping others | Q2f a job that allows someone to help other people | Q12f In my job I can help other people |
| Usefulness | Q2g a job that is useful to society | Q12g My job is useful to society |
| Contact with people | Q2i a job that involves personal contact with other people | Q12h In my job, I have personal contact with other people |
| Control over working times | Q2h a job that allows someone to decide their times or days of work | Q15 how starting and finishing times are decided |

**Rhythm subset:** independence, contact with people, and control over working times. These are the closest to the engine's own dimensions (working with others, schedule flexibility). The other six are about what a job gives, not its rhythm, and are included because they are what the survey asked.

**Scaling (fixed before seeing the data):**
- Want: importance mapped to 0–1, "very important" = 1, "not important at all" = 0, evenly spaced.
- Have: agreement mapped to 0–1, "strongly agree" = 1, "strongly disagree" = 0, evenly spaced.
- Control over working times (Q15): employer decides and I can't change it = 0, I can decide within limits = 0.5, entirely free = 1.
- "Can't choose" and similar answers count as missing.
- All features get equal weight. **No weights are tuned on this data.**

The exact variable names and codes are taken from the GESIS variable report and listed in the analysis script. Mapping them doesn't change anything in this plan.

---

## Who is analyzed

- Respondents currently in paid work who answered the own-job items
- With all nine pairs (all three for the rhythm-subset check) and job satisfaction present
- Countries with at least 200 such respondents. Smaller countries are listed with their counts but left out of the averages.

Answers are analyzed unweighted. The question is whether a relationship exists among working people, not how common something is in a population.

---

## Primary check

For every respondent, compute an alignment score between their want and have vectors with **Manhattan** distance (the engine) and **cosine** similarity (the removed engine). Alignment is oriented so that higher means closer: 1 minus the mean absolute gap for Manhattan, the cosine itself for cosine.

Job satisfaction (Q23, seven points) is recoded so that higher means more satisfied.

Within each country, compute the Spearman correlation between each alignment score and satisfaction. Then average across countries, each country counting equally.

- `ρ_M` = average correlation between Manhattan alignment and satisfaction
- `d = ρ_M − ρ_cosine`
- 95% intervals come from a bootstrap that resamples **countries** (5,000 resamples, seed 2026).

### How the result will be read

| Result | Reading |
|---|---|
| The interval for `ρ_M` includes 0 | **The basic assumption doesn't hold here:** closeness between want and have doesn't track satisfaction. Reported first, whatever `d` says. |
| `d ≥ 0.02` and its interval excludes 0 | Consistent with the engine's choice: Manhattan tracks satisfaction better than cosine. |
| `d ≤ −0.02` and its interval excludes 0 | Inconsistent with it: cosine tracks satisfaction better. We revisit the metric choice. |
| Otherwise | No difference that matters between the two in this data. |

With tens of thousands of respondents, even tiny differences can have narrow intervals. That's why a difference smaller than 0.02 in correlation is read as "no difference that matters", whatever its interval.

---

## Stability, 1989–2015

Using the cumulation, run the primary check separately for each wave on the item pairs asked in all four waves. Which pairs those are is taken from the cumulation's documentation before the analysis and listed in the script.

| Result | Reading |
|---|---|
| `ρ_M` is positive with an interval excluding 0 in all four waves, and the largest minus the smallest is less than 0.10 | **Stable:** the relationship held across 26 years. |
| Otherwise | **Changed:** reported with its direction (stronger or weaker over time). |

A stable relationship across 1989–2015 is the main argument for expecting it to hold today. The 2025 data then tests that expectation directly.

## Repeat on the 2025 data

When the 2025 wave is released, run the primary check again on whichever of the nine pairs it repeats, with the same code. The only change allowed is the variable-name mapping.

| Result | Reading |
|---|---|
| `ρ_M` is positive with an interval excluding 0, and within 0.10 of the 2015 value on the same pairs | **Holds in 2025.** |
| Otherwise | **Different in 2025**, reported with its direction. |

The Manhattan-versus-cosine reading is repeated the same way.

---

## Countries not in the data

The 2015 data has no South Korea, and today's economies aren't the same as in 2015. To say anything about a country that isn't in the data, it is matched to the surveyed countries it most resembles.

- **Indicators**, for every country with data: share of employment in services, share in industry, self-employment as a share of employment, and average annual hours actually worked per worker (ILO and OECD public statistics), plus average days worked from home per week where available (Global Survey of Working Arrangements, 2024–25). Surveyed countries use their 2015 values; the target country uses its latest values.
- **Method:** standardize each indicator across all countries, compute Euclidean distances, and list the three nearest surveyed countries for each target.
- **Reading:** results for a target country are reported as "approximated by its three nearest surveyed countries", with their names and distances. If even the nearest is farther than three quarters of all country pairs, the target is reported as having no close match, and nothing is said about it.
- Sources and years are recorded in the script before the analysis.

This transfers the **relationship** (does distance track satisfaction), not **levels** (how many people work flexible hours). Levels have changed since 2015, most visibly in working from home.

---

## Secondary checks

Reported, but they don't change the readings above.

1. **Other outcomes:** work stress (Q13b) and work interfering with family life (Q19a), recoded so that higher means more. Expected to fall as alignment rises.
2. **Rhythm subset:** the primary check on independence, contact with people, and control over working times only.
3. **Shortfall only:** distance counting only features where people have less than they want. Having more of a wanted feature than needed is rarely a problem, while the engine's distance treats both directions the same.
4. **Other metrics:** Euclidean, Chebyshev (largest single gap), and centered cosine (measured from the scale midpoint), computed the same way.

## Exploratory

Labelled as exploratory in the results, with no conclusions drawn:

- Which single feature's gap relates most to satisfaction
- How the correlation varies across countries

---

## Known limitations

- **Different dimensions:** only two of the engine's five dimensions have a counterpart here (working with others, schedule flexibility). There are no items on energy timing, amount of change, or pace.
- **Importance is not the same as preferred level:** "how important is it that a job lets you work independently" and "I can work independently" are answered on different scales. Differences between such scores are a long-debated way to measure fit. They're used here because that's what the engine does, and the shortfall-only check gives a second view.
- **One moment, one person:** everything is self-reported at one time, so a person's general mood can tie their answers together.
- **Age of the data:** 2015 is before the shift to working from home. The 2025 repeat and the stability check are there for this.
- **Countries outside the data** are approximations, as described above.

---

## Running the analysis

```bash
python examples/issp_fit_analysis.py --test           # unit tests
python examples/issp_fit_analysis.py --demo           # made-up data with the same columns
python examples/issp_fit_analysis.py data/ZA6770.dta  # the real data, after downloading it from GESIS
```

The script is committed before the data is downloaded. The analysis runs once on the 2015 data and once on the cumulation, and once more when the 2025 data is released. All results are published, whatever they show.
