import sqlite3

db="BANK.sqlite3"

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

def authentication(val,action1):
    import loads
    data=loads.dla()
    if action1=="HSPIN":
        return val == data["HIGH-SEQURITY PIN"]
    elif action1 == "TWPIN":
        return val == data["TRANSACTION-WITHDRAWL PIN"]
    elif action1=="QUESTION_1":
        return val==data["a1"]
    elif action1=="QUESTION_2":
        return val==data["a2"]
    elif action1=="QUESTION_3":
        return val==data["a3"]    
    else:
        return False

def delete_database(acc,action):
    if action=="ALL":
        query_db('''DELETE FROM ACCOUNT WHERE ACCOUNT_NUMBER = ?''', (acc,),0)
        query_db('''DELETE FROM BENEFICIARY WHERE ACCOUNT_NUMBER = ?''', (acc,),0)
        query_db('''DELETE FROM TRANSACTIONS WHERE ACCOUNT_NUMBER = ?''', (acc,),0)
        print("ALL LOGS DELETED")
    elif action=="BENEFICIARY":
        query_db('''DELETE FROM BENEFICIARY WHERE "BENEFICIARY_AC/NO" = ?''', (acc,))