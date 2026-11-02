# site

Static pages published with GitHub Pages from the `gh-pages` branch, which holds a copy of this folder.

## Publishing

After a change to `site/` is merged into `main`:

```bash
python site/build_survey_data.py --check        # must pass
git subtree push --prefix site origin gh-pages  # copies site/ to the gh-pages branch
```

GitHub Pages serves the `gh-pages` branch root (Settings → Pages → Deploy from a branch → `gh-pages`, `/ (root)`).

## survey/

The Experiment 2.5 survey page: https://devaaronjeong.github.io/continuum-protocol/survey/

- Asks the same questions, in the same words, as the Google Forms created by `examples/survey_forms.gs`, and sends the answers to those forms. Nothing else is collected and there is no analytics.
- After submitting, it shows the person where they and their job are close and far apart on each dimension. There is no overall score.
- Korean and English. Add `?lang=ko` or `?lang=en` to the link to pick one.

### When the forms are re-created

1. Run `examples/survey_forms.gs` again (see `docs/experiments/retrospective-fit-survey.md`).
2. Open the new Korean and English form links in a browser, open the developer console, and run:
   ```js
   JSON.stringify(Object.fromEntries(FB_PUBLIC_LOAD_DATA_[1][1]
     .filter(i => i[4]).map(i => [i[1], i[4][0][0]])))
   ```
   It prints each question title with its entry ID.
3. Put the new form IDs and entry IDs into `site/survey/forms.json` (keys are the question IDs from `survey_forms.gs`).
4. Run `python site/build_survey_data.py` and commit `forms.json` and `survey-data.js` together.

`python site/build_survey_data.py --check` fails if `survey-data.js` no longer matches the form script or `forms.json`. Run it before every publish.
