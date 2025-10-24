#step1- import driver module of database
import pymysql

#step2 - make connection with database
conobj=pymysql.connect(user="root",password="root",host="localhost",database="230pm")

#step3 - create cursor object from connection
curobj=conobj.cursor()

#step4 - execute(DQL/DDL-it directly execute no need of commit)/
# store(DML-it get store into cursor object and need to commit for execution)
#  query on cursor object and collect the result
insert_count=curobj.execute("insert into emp values(203,'kapil',100000,'manager')")
delete_count=curobj.execute("delete from emp where esal is null")
update_count=curobj.execute("update emp set esal=esal+1000")

#step5- execute all queries in same order
conobj.commit()

#step6-close the connection
conobj.close()