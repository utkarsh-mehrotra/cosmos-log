# Cosmos Log

A living archive of the universe, updated every morning by a GitHub Actions cron job.

![Daily Cosmos Update](https://github.com/utkarsh-mehrotra/cosmos-log/actions/workflows/daily-cosmos.yml/badge.svg)

<!-- COSMOS-START -->
<!-- HEARTBEAT: 2026-04-21 07:59:19 UTC -->
## 🔭 Today's Sky — 2026-04-21
### Three Sky Arches over Snowy Alps

![Three Sky Arches over Snowy Alps](https://apod.nasa.gov/apod/image/2604/TripleArchAlps_Fux_1080.jpg)

*Why are there three arches across the sky instead of two? Last month, after being dropped off by a helicopter at a high mountain peak in the Alps near the Swiss Italian border, an adventurous astrophotographer expected two arches of our Milky Way galaxy to be visible during the n...*

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
