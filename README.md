# Cosmos Log

A living archive of the universe, updated every morning by a GitHub Actions cron job.

![Daily Cosmos Update](https://github.com/utkarsh-mehrotra/cosmos-log/actions/workflows/daily-cosmos.yml/badge.svg)

<!-- COSMOS-START -->
<!-- HEARTBEAT: 2026-04-18 18:02:07 UTC -->
## 🔭 Today's Sky — 2026-04-18
### PanSTARRS and Planets

![PanSTARRS and Planets](https://apod.nasa.gov/apod/image/2604/PanstarrsPlanetsPerrotLab1024.jpg)

*Near the eastern horizon before sunrise, Comet C/2025 R3 PanSTARRS is getting brighter. Readily visible in binoculars and small telescopes, the comet may be just on the verge of naked-eye visibility from dark sky sites. Though it was not quite apparent to the eye, PanSTARRS is st...*

📂 [Full archive in /log](./log/)
<!-- COSMOS-END -->

## How it works

1. **Scheduled Run**: A GitHub Actions workflow runs every day at 6 AM UTC (or manually via workflow_dispatch).
2. **Fetch Data**: A Python script runs to fetch the latest Astronomy Picture of the Day from NASA's API.
3. **Format & Commit**: The script updates this README, creates or updates a monthly log file in the `/log` directory, and pushes the latest entry directly to the repository.

## Setup

1. Push these files to a new GitHub repository called `cosmos-log`.
2. Go to your repository's **Settings → Secrets and variables → Actions**.
3. Create a new repository secret named `NASA_API_KEY` and paste your NASA API key. (You can register for a free key at [api.nasa.gov](https://api.nasa.gov/)). Alternatively, it will use the `DEMO_KEY` with strict rate limits.
