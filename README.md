# Golemio Kniznice
## Golemio Prague Municipal Libraries Data

This project fetches and processes data on municipal libraries in Prague using the Golemio API.
The data is extracted, transformed, and saved into a CSV file using a scheduled GitHub Actions workflow.

## What it does

- Connects to the Golemio API to access municipal libraries data.
- Extracts following information:
  - ID knižnice, Názov knižnice (Library name), Ulica (Address), PSČ (ZIP code), Mesto (City), District, Krajina (Country), Zemepisná šírka (Latitude), Zemepisná dĺžka (Longitude), Čas otvorenia (Opening Hours - default schedule only)
- Saves the cleaned data as a CSV file.
- Runs **automatically every day at 7:00 AM Prague Summer time**.
- Also allows manual run via GitHub Actions.

## Tech used

- Python (requests + pandas)
- GitHub Actions (for automation)
- CSV (output format)

## Output

The resulting `libraries.csv` file is saved as an **artifact** of each workflow run. You can download it by going to the **Actions** tab, clicking the latest successful run, and finding the file under **Artifacts**.

## API Key

The Golemio API requires an access token, which is stored securely as a repository secret (`GOLEMIO_API_KEY`).

## Notes

You don’t have to wait until the scheduled time – you can also manually trigger the workflow anytime from the **Actions** tab on GitHub by selecting the workflow and clicking **Run workflow**.
