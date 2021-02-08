import sqlite3

con=sqlite3.connect('FollowUp.db')
con.execute('create table if not exists Student (enquiryid TEXT primary key,StudentName text,class text,dob text,mob1 TEXT,email TEXT,schoolname text,address text,reminder TEXT,remindernext TEXT,remark TEXT,imgname TEXT,fname TEXT,mob2 TEXT,foccupation TEXT,mname TEXT,mob3 TEXT,paddress TEXT,added TEXT,updated TEXT)')
con.execute('create table if not exists Login (Username text,password text,ms_password text,login_created_date TEXT,login_update_date TEXT)')
con.execute('insert into login values ("ashu","ashu1234","ashu1234","","")')
#cur=con.cursor()
#cur.execute("select * from student")
#print(cur.fetchall())

con.commit()
con.close()