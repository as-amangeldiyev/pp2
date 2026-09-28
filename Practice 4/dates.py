from datetime import date, datetime, timedelta, timezone


def main():
    today = date.today()
    now = datetime.now()
    print("Today:", today)
    print("Current local date and time:", now)

    birthday = date(2000, 1, 1)
    print("Created date object:", birthday)
    print("Formatted date:", now.strftime("%A, %d %B %Y at %H:%M"))

    target = date(today.year + 1, 1, 1)
    print("Days until next January 1:", (target - today).days)
    later = now + timedelta(days=7, hours=2)
    print("One week and two hours later:", later)

    # A timezone-aware datetime uses an explicit UTC offset.
    utc_now = datetime.now(timezone.utc)
    almaty = timezone(timedelta(hours=5), name="UTC+05:00 (Almaty)")
    print("Current UTC time:", utc_now.isoformat())
    print("Same instant at UTC+05:00:", utc_now.astimezone(almaty).isoformat())


if __name__ == "__main__":
    main()
