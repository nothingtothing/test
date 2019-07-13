#by 李星星

import poplib
import html
import time
import DBaction
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr

#判断邮箱和授权码是否正确
def judgePass(E,P):
    try:
        server=poplib.POP3_SSL('pop.qq.com')
        server.user(E)
        server.pass_(P)
        server.quit()
    except:
        return False
    else:
        return True
