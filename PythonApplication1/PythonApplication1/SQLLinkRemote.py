import pyodbc

driver = 'SQL Server Native Client 11.0'  # 因版本不同而异
server = 'wkfgdbservice.chinanorth.cloudapp.chinacloudapi.cn,1433'  
user = 'sa'
password = 'rootL123456789'
database = 'test'
conn = pyodbc.connect(driver=driver, server=server, user=user, password=password, database=database)

cur = conn.cursor()
sql = 'select * from BadNames'  # 查询语句
cur.execute(sql)
rows = cur.fetchall()  # list
print(rows)
#zjn = '黑框眼镜'
#if zjn in rows:
   # print('建议击毙')
#conn.commit()
conn.close()