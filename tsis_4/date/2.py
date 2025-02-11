from datetime import datetime, timedelta

today = datetime.now()
print("Today:", today.strftime("%Y-%m-%d"))

yesterday = today - timedelta(days=1)
print("Yesterday:", yesterday.strftime("%Y-%m-%d"))

tomorrow = today + timedelta(days=1)
print("Tomorrow:", tomorrow.strftime("%Y-%m-%d"))