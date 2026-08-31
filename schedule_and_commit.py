import glob
import os
import random
import subprocess
from datetime import datetime, timedelta

from cosmos_timing import pick_time_of_day
from update_log import fetch_and_log

MAX_CATCHUP_LOOKBACK_DAYS = 5
MAX_CATCHUP_PER_RUN = 2
WEEKEND_SKIP_PROBABILITY = 0.4
SPLIT_COMMIT_PROBABILITY = 0.15


def has_metadata(date_str):
    return os.path.exists(os.path.join("metadata", f"{date_str}.json"))


def find_catchup_dates(today):
    missing = []
    for i in range(1, MAX_CATCHUP_LOOKBACK_DAYS + 1):
        d = today - timedelta(days=i)
        d_str = d.strftime("%Y-%m-%d")
        if not has_metadata(d_str):
            missing.append(d_str)
        if len(missing) >= MAX_CATCHUP_PER_RUN:
            break
    missing.reverse()  # oldest first, so log prepend order stays newest-first
    return missing


def run_git(args, env=None):
    subprocess.run(["git"] + args, check=True, env=env)


def commit_paths(paths, message, commit_dt):
    existing_paths = [p for p in paths if os.path.exists(p)]
    if not existing_paths:
        return False

    run_git(["add"] + existing_paths)

    status = subprocess.run(["git", "diff", "--cached", "--quiet"])
    if status.returncode == 0:
        return False  # nothing staged for these paths

    date_str = commit_dt.strftime("%Y-%m-%dT%H:%M:%S+00:00")
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = date_str
    env["GIT_COMMITTER_DATE"] = date_str
    run_git(["commit", "-m", message], env=env)
    return True


def main():
    today_dt = datetime.utcnow()
    today = today_dt.date()
    today_str = today.strftime("%Y-%m-%d")
    is_weekend = today.weekday() >= 5

    skip_today = is_weekend and random.random() < WEEKEND_SKIP_PROBABILITY
    catchup_dates = find_catchup_dates(today)
    dates_to_process = catchup_dates + ([] if skip_today else [today_str])

    if not dates_to_process:
        print("No dates to process today (weekend skip, nothing to catch up on).")
        return

    hour, minute = pick_time_of_day()
    clock = datetime(today.year, today.month, today.day, hour, minute)
    if clock > today_dt:
        clock = today_dt - timedelta(minutes=random.randint(5, 60))

    processed = []
    for date_str in dates_to_process:
        is_today = date_str == today_str
        result = fetch_and_log(date_override=None if is_today else date_str)
        if result is None:
            print(f"Skipping {date_str}: fetch failed.")
            continue

        actual_date = result["date"]
        if is_today and actual_date != today_str:
            # NASA hasn't published today's APOD yet - this just re-fetched
            # an already-logged date. Nothing new to commit.
            print(f"NASA's 'today' still resolves to {actual_date}; nothing new yet.")
            continue

        clock = min(clock + timedelta(minutes=random.randint(3, 25)), today_dt)

        asset_paths = glob.glob(os.path.join("assets", f"{actual_date}.*"))
        metadata_paths = [os.path.join("metadata", f"{actual_date}.json")]
        log_month = actual_date[:7]
        log_paths = [os.path.join("log", f"{log_month}.md"), "README.md"]

        date_str = actual_date
        label = "" if is_today else " (catch-up)"

        if random.random() < SPLIT_COMMIT_PROBABILITY:
            commit_paths(
                asset_paths + metadata_paths,
                f"🌌 {date_str}: {result['title']}{label}",
                clock,
            )
            clock = min(clock + timedelta(minutes=random.randint(2, 12)), today_dt)
            commit_paths(
                log_paths,
                f"📝 {date_str}: log + summary update",
                clock,
            )
        else:
            commit_paths(
                asset_paths + metadata_paths + log_paths,
                f"🌌 {date_str}: {result['title']}{label}",
                clock,
            )

        processed.append(date_str)

    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        with open(summary_path, "a", encoding="utf-8") as f:
            f.write("### Cosmos Run Summary 🌌\n")
            if processed:
                f.write(f"- Processed: {', '.join(processed)}\n")
            else:
                f.write("- Nothing processed\n")
            if skip_today:
                f.write("- Today skipped (weekend pattern)\n")


if __name__ == "__main__":
    main()
