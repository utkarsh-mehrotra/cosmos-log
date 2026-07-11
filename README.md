# Cosmos Log

A living archive of the universe, updated every morning by a GitHub Actions cron job.

![Daily Cosmos Update](https://github.com/utkarsh-mehrotra/cosmos-log/actions/workflows/daily-cosmos.yml/badge.svg)

<!-- COSMOS-START -->
<!-- HEARTBEAT: 2026-07-11 08:00:37 UTC -->
## 🔭 Today's Sky — 2026-07-11
### Messier 24: Sagittarius Star Cloud

![Messier 24: Sagittarius Star Cloud](./assets/2026-07-11.jpg)

*Unlike most entries in Charles Messier's famous catalog of deep sky objects, M24 is not a bright galaxy, star cluster, or nebula. It's a gap in nearby, obscuring interstellar dust clouds that allows a view of the distant stars in the Sagittarius spiral arm of our Milky Way galaxy...*

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
