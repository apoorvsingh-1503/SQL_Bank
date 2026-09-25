import sqlite3

db="bank.sqlite3"
q1 = "NAME OF FAVOURITE MOVIE"
q2 = "NAME OF BIRTH CITY"
q3 = "FAVOURITE COLOUR"

def query_db(q, data=None,a=0):
    con = sqlite3.connect(db)
    cur = con.cursor()

    if data is None:
        cur.execute(q)
    else: cur.execute(q,data)
    result=None
    if a==1:
        result=cur.fetchone()
    elif a==2:
        result = cur.fetchall()
    con.commit()
    con.close()
    return result

def authenticate(d, pins):
    pinss={"SPIN":"STANDARD PIN","TWPIN":"TRANSACTION-WITHDRAWL PIN","HSPIN":"HIGH SEQURITY PIN"}
    for pin in pins:
        tp=int(input(f"ENTER {pinss.get(pin,pin)} :  "))
        if pin=="SPIN" and tp!=d['SPIN']:
            return False
        elif pin=="TWPIN" and tp!=d["TWPIN"]:
            return False
        elif pin=="HSPIN" and tp!= d["HSPIN"]:
            return False
        elif pin=="QUESTIONS":
            ans1 = input(f"Answer Q1 {q1}: ")
            ans2 = input(f"Answer Q2 {q2}: ")
            ans3 = input(f"Answer Q3 {q3}: ")
            if ans1!=d["a1"] and ans2!=d["a2"] and ans3!=d["a3"]:
                return False

    return True

def delete_database(acc,action):
    if action=="ALL":
        query_db('''DELETE FROM ACCOUNT WHERE ACCOUNT_NUMBER = ?''', (acc,),0)
        query_db('''DELETE FROM BENEFICIARY WHERE ACCOUNT_NUMBER = ?''', (acc,),0)
        query_db('''DELETE FROM TRANSACTIONS WHERE ACCOUNT_NUMBER = ?''', (acc,),0)
        print("ALL LOGS DELETED")
    elif action=="BENEFICIARY":
        query_db('''DELETE FROM BENEFICIARY WHERE "BENEFICIARY_AC/NO" = ?''', (acc,))