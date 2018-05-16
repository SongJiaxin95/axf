import random
import time

def get_ticket():
    s = 'qwertyuiopasdfghjklzxcvbnm1234567890'
    ticket = ''
    for i in range(15):
        # 获取随机的字符串
        ticket += random.choice(s)
    now_time = int(time.time())
    ticket = 'TK_' + ticket + str(now_time)
    return ticket