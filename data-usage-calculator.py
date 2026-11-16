# Day 41: Data Usage Calculator - 2026-11-16
# What it does: Helps you plan your mobile/Wi-Fi data pack - converts between
# data units (MB, GB), works out how long a data pack will last at your daily
# usage, and how much data you need for a trip or a month.
# Useful for: Anyone on a limited mobile data pack who wants to avoid running
# out of data mid-month, or to pick the right pack size before recharging.

def convert_data(amount, from_unit, to_unit):
    """Convert a data amount between B, KB, MB, GB and TB.

    Example: convert_data(2, "GB", "MB") -> 2048.0
    """
    units = {"B": 0, "KB": 1, "MB": 2, "GB": 3, "TB": 4}
    from_unit = from_unit.upper()
    to_unit = to_unit.upper()
    if from_unit not in units or to_unit not in units:
        raise ValueError("Unit must be one of B, KB, MB, GB, TB.")
    if amount < 0:
        raise ValueError("Amount cannot be negative.")
    bytes_amount = amount * (1024 ** units[from_unit])
    return round(bytes_amount / (1024 ** units[to_unit]), 2)


def days_pack_will_last(pack_gb, daily_usage_mb):
    """How many days a data pack lasts at your average daily usage.

    Example: days_pack_will_last(30, 1000) -> 30 days (30 GB at 1 GB/day).
    Returns 0 when daily usage is 0 or the pack is empty.
    """
    if pack_gb <= 0 or daily_usage_mb <= 0:
        return 0
    total_mb = pack_gb * 1024
    return int(total_mb // daily_usage_mb)


def data_needed(days, daily_usage_mb):
    """How much data (in GB) you need for a number of days.

    Example: data_needed(30, 1500) -> 43.95 GB for a month at 1.5 GB/day.
    """
    if days <= 0 or daily_usage_mb < 0:
        raise ValueError("Days must be positive and usage cannot be negative.")
    return round((days * daily_usage_mb) / 1024, 2)


def daily_allowance(pack_gb, days_left):
    """Your daily data budget (in MB) so the pack lasts until it expires.

    Example: daily_allowance(20, 10) -> 2048 MB/day for 10 days left.
    """
    if pack_gb <= 0 or days_left <= 0:
        raise ValueError("Pack size and days left must both be positive.")
    return round((pack_gb * 1024) / days_left, 2)


def pack_status(pack_gb, used_gb, days_left):
    """A quick summary: how much is left, what percent is used, and whether
    your remaining data fits the days left at your current pace.

    Returns a dict with remaining GB, used percent and a plain advice string.
    """
    if pack_gb <= 0 or used_gb < 0 or used_gb > pack_gb or days_left < 0:
        raise ValueError("Check your numbers: 0 <= used <= pack, days left >= 0.")
    remaining_gb = round(pack_gb - used_gb, 2)
    used_percent = round((used_gb / pack_gb) * 100, 1)
    if days_left == 0:
        advice = "Pack expires today - use the remaining data or it is lost."
    elif remaining_gb == 0:
        advice = "Data finished! Recharge a new pack."
    else:
        daily_budget = daily_allowance(remaining_gb, days_left)
        advice = (f"You have {remaining_gb} GB left for {days_left} days - "
                  f"use up to {daily_budget} MB per day to make it last.")
    return {
        "remaining_gb": remaining_gb,
        "used_percent": used_percent,
        "advice": advice,
    }


if __name__ == "__main__":
    # Example 1: You bought a 30 GB pack and use about 1 GB a day.
    print("30 GB pack at 1 GB/day lasts:",
          days_pack_will_last(30, 1024), "days")

    # Example 2: A 15-day trip, using 2 GB a day - how big a pack do you need?
    print("Data needed for a 15-day trip at 2 GB/day:",
          data_needed(15, 2048), "GB")

    # Example 3: 20 GB pack, 12 GB used, 10 days left - what is the situation?
    status = pack_status(20, 12, 10)
    print("Remaining:", status["remaining_gb"], "GB | Used:",
          status["used_percent"], "%")
    print(status["advice"])

    # Bonus: unit conversion - 2.5 GB in MB.
    print("2.5 GB =", convert_data(2.5, "GB", "MB"), "MB")
