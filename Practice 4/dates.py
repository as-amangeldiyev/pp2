from datetime import date, datetime, timedelta

# Subtract five days from today's date.
today = date.today()
print("Five days ago:", today - timedelta(days=5))

# Print yesterday, today, and tomorrow.
print("Yesterday:", today - timedelta(days=1))
print("Today:", today)
print("Tomorrow:", today + timedelta(days=1))

# Remove microseconds from the current time.
now = datetime.now().replace(microsecond=0)
print("Current time without microseconds:", now)

# Find the difference between two dates in seconds.
first_date = datetime.strptime(input("Enter the first date (YYYY-MM-DD): "), "%Y-%m-%d")
second_date = datetime.strptime(input("Enter the second date (YYYY-MM-DD): "), "%Y-%m-%d")
print("Difference in seconds:", abs((second_date - first_date).total_seconds()))
