from rHoodFuncsStock import *
import mysql.connector
import time, os

os.environ['TZ'] = 'EST+05EDT,M4.1.0,M10.5.0'
time.tzset()

conn = mysql.connector.connect(host='localhost', database='RHood', user='root', password='')
cursor = conn.cursor(buffered=True)
cursor.execute('select * from stocks_enabled')
stocks_enabled = cursor.fetchall()
login()
for _id, stock in stocks_enabled:
    price = get_price(stock)
    s = f'insert into stock_data (stock_id,price,time,time_str) values ({_id}, {price}, {time.time()}, "{time.ctime(time.time())}")'
    cursor.execute(s)
    conn.commit()

