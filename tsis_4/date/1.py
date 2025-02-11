from datetime import datetime, timedelta

today = datetime.now()
print("Current Date:", today.strftime("%Y-%m-%d"))

new_date = today - timedelta(days=5)
print("Date After Subtracting 5 Days:", new_date.strftime("%Y-%m-%d"))
