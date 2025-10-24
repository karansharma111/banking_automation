import sqlite3
def generate():

    conobj=sqlite3.connect(database="bank.sqlite")
    curobj=conobj.cursor()
    query='''create table if not exists accounts(
    acn_acno integer primary key autoincrement,
    acn_name text,
    acn_pass text,
    acn_email text,
    acn_mob text,
    acn_adhar text,
    acn_adrs text,
    acn_dob text,
    acn_bal float,
    acn_opendate text
    )
    '''
    curobj.execute(query)
    conobj.close()

