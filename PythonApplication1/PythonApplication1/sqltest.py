import pymssql #引入pymssql模块

def conn():
    connect = pymssql.connect('LAPTOP-LDUC71HB', 'sa', 'root', 'GymMsystem') #服务器名,账户,密码,数据库名
    if connect:
        print("连接成功!")
    return connect

if __name__ == '__main__':
    connect = conn()
    cursor = connect.cursor()   #创建一个游标对象,python里的sql语句都要通过cursor来执行
    cursor.execute("create table C_test02(id varchar(20))")   #执行sql语句
    connect.commit()  #提交
    cursor.close()   #关闭游标
    connect.close()  #关闭连接