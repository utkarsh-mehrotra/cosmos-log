import random

def pick_time_of_day():
    """Returns (hour, minute) in UTC, weighted toward evening IST hours with
    a long tail, so commit times don't cluster around a single fixed hour."""
    bucket = random.choices(
        ["evening", "afternoon", "late_morning", "late_night"],
        weights=[55, 20, 15, 10],
    )[0]
    if bucket == "evening":
        hour = random.randint(13, 18)
    elif bucket == "afternoon":
        hour = random.randint(9, 12)
    elif bucket == "late_morning":
        hour = random.randint(4, 7)
    else:
        hour = random.choice([19, 20, 21, 22, 23, 0, 1])
    minute = random.randint(0, 59)
    return hour, minute
