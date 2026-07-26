# Cosmos Log

A living archive of the universe, updated every morning by a GitHub Actions cron job.

![Daily Cosmos Update](https://github.com/utkarsh-mehrotra/cosmos-log/actions/workflows/daily-cosmos.yml/badge.svg)

<!-- COSMOS-START -->
<!-- HEARTBEAT: 2026-07-22 08:33:16 UTC -->
## 🔭 Today's Sky — 2026-07-22
### The Corona Australis Molecular Cloud and the Chandelier Cluster

![The Corona Australis Molecular Cloud and the Chandelier Cluster](./assets/2026-07-22.jpg)

*The Southern Crown (Corona Australis) dazzles with young and ancient celestial jewels. The Corona Australis Cloud is a collage of reflection and emission nebulae on the left of today’s image. At 430 light years away, this cloud is one of the closest star-forming regions to Earth....*

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
