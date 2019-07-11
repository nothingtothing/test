# -*- coding: utf-8 -*-

from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
from chineseYeahYeah import jiebaclearText
import re
import poplib

# 输入邮件地址, 口令和POP3服务器地址:
email = '1678120695@qq.com'
password = 'oxlxnspfguthdajc'
pop3_server = 'pop.qq.com'

def guess_charset(msg):
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset

def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value


list1 = [0,0,0,0,0,0]
def print_info(msg, indent=0): 
    if indent == 0:
        i=0
        for header in ['From', 'To', 'Subject']:
            value = msg.get(header, '')
            if value:
                if header=='Subject':
                    value = decode_str(value)
                else:
                    hdr, addr = parseaddr(value)
                    name = decode_str(hdr)
                    value = u'%s <%s>' % (name, addr)
            #print('%s%s: %s' % ('  ' * indent, header, value))
            list1[i]=value
            i+=1

    if (msg.is_multipart()):
        parts = msg.get_payload()
        for n, part in enumerate(parts):
            print('%spart %s' % ('  ' * indent, n))
            print('%s--------------------' % ('  ' * indent))
            print_info(part, indent + 1)
    else:
        content_type = msg.get_content_type()
        if content_type=='text/plain' or content_type=='text/html':
            content = msg.get_payload(decode=True)
            charset = guess_charset(msg)
            if charset:
                content = content.decode(charset)
            print('%sText: %s' % ('  ' * indent, content))
            list1[3]=content
            list1[5]='2'
        else:#存在附件
            print('%sAttachment: %s' % ('  ' * indent, content_type))
            list1[5]='0'

    list1[3] = list1[3].replace(',',' ')
    list1[3] = re.sub(r'<.*?>','',list1[3])
    list1[3] = list1[3].replace('\n','')
    list1[2] = list1[2].replace(',',' ')
    mail = ''.join(list1[0])+','+''.join(list1[1])+','+''.join(list1[2])+','+''.join(list1[3])+','+''.join(list1[5])+'\n'
    return mail

# 连接到POP3服务器:
server = poplib.POP3(pop3_server)
# 可以打开或关闭调试信息:
server.set_debuglevel(1)
# 可选:打印POP3服务器的欢迎文字:
#print(server.getwelcome().decode('utf-8'))
# 身份认证:
server.user(email)
server.pass_(password)
# stat()返回邮件数量和占用空间:
print('Messages: %s. Size: %s' % server.stat())
# list()返回所有邮件的编号:
resp, mails, octets = server.list()
# 可以查看返回的列表类似[b'1 82923', b'2 2184', ...]
print(mails)

#获取所有邮件, 注意索引号从1开始:

index = len(mails)
for i in range(1,index+1):
    resp, lines, octets = server.retr(i)
    # lines存储了邮件的原始文本的每一行,
    # 可以获得整个邮件的原始文本:
    msg_content = b'\r\n'.join(lines).decode('utf-8')
    # 稍后解析出邮件:
    msg = Parser().parsestr(msg_content)
    #print_info(msg)
    text = print_info(msg)
    with open('mail%s'%i,encoding='utf-8',mode='w') as file:
        file.write(text)

with open('email','w',encoding='utf-8') as file:
    for i in range(1,index):
        with open('mail%s'%i,'r',encoding='utf-8') as f1:
            line = f1.read()
            #for linelist in line:
                #line_new = linelist.replace('[','')
                #line_new = line_new.replace(']','')
            file.write(line)

# 关闭连接:
server.quit()
