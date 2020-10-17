from datetime import datetime, timedelta
t = ["월", "화", "수", "목", "금", "토", "일"]
r = datetime.today().weekday()
print(t[r])
# print(type(dasl_time))