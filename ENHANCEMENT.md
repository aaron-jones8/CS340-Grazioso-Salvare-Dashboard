# CS 499 Milestone Four — Enhancement Three: Databases

The `enhanced/` folder contains the CS 499 capstone enhancement of this artifact (original: `CRUD_Python_Module.py`, `ProjectTwoDashboard.ipynb` at the repo root).

## Summary of the enhancement

- **Credentials externalized.** `AnimalShelter` now reads credentials from the `AAC_MONGO_USERNAME` / `AAC_MONGO_PASSWORD` environment variables (or explicit constructor arguments) instead of hardcoded defaults. Missing credentials raise a clear `ValueError` immediately rather than silently falling back to a default account baked into the source file.
- **Completed the CRUD module.** The original only implemented Create and Read despite being named a "CRUD" module. Added `update()` and `delete()`, both of which reject an empty query rather than silently acting on the entire collection.
- **Added a compound index** on `animal_type`, `breed`, `sex_upon_outcome`, and `age_upon_outcome_in_weeks` — the exact fields every rescue-type filter in the dashboard queries together.

## Bugs fixed

1. **Authentication failures were never actually caught.** `MongoClient()` connects lazily in PyMongo, so the original `try/except` around just that call never caught a bad username/password. Fixed by forcing a `client.admin.command("ping")` inside the try block.
2. **Unescaped credentials in the connection URI.** Fixed with `urllib.parse.quote_plus()`.
3. **No error handling on the logo image load.** Fixed to catch `FileNotFoundError` and run without the logo instead.

## Environment note (not a defect in the original artifact)

The original notebook used the `jupyter_dash` package, incompatible with current Jupyter/`ipykernel` versions. The enhanced version replaces `JupyterDash` with plain `dash.Dash` and `app.run(debug=True)`.

## Testing

Verified with `mongomock` (17 checks, including the real 10,000-record shelter dataset) and then against a real local MongoDB instance: the cleaned dataset was imported with `mongoimport`, a matching MongoDB user was created, and the dashboard ran successfully end to end with the real credential-handling and forced-ping authentication check.

Full narrative: see `Jones_Aaron_Milestone_Four_Narrative.pdf` on the [ePortfolio site](https://aaron-jones8.github.io/).

## Running the enhanced project

Requires Python 3, MongoDB running locally, and `dash`, `dash-leaflet`, `plotly`, `pandas`, `numpy`, `matplotlib`, `pymongo`, `jupyter`.

```
mongoimport --db aac --collection animals --type csv --headerline --file aac_shelter_outcomes_clean.csv
```
