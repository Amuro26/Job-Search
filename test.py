

from datetime import datetime


class Time():
    s = str(datetime.utcnow())
    num = s[6] + s[8] + s[9] + s[11] + s[12] + s[14] + s[15] + s[17] + s[18]


print(int(Time.num))


