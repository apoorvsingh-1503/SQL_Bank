from datetime import datetime
import random
import string
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

def acc_generator(): # can be auto generated
    return "".join(random.choices(string.digits, k=10))

def hspin_generator():
    return "".join(random.choices(string.digits, k=4))

def transaction_log(ACCOUNT_NUMBER,AMOUNT,BENEFICIARY,ACTION):
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H:%M:%S")
    d=(ACCOUNT_NUMBER,current_date,current_time,AMOUNT,BENEFICIARY,ACTION)
    q=''' insert into TRANSACTIONS
      (ACCOUNT_NUMBER,DATE,TIME,AMOUNT,BENEFICIARY,ACTION)
      VALUES(?,?,?,?,?,?)'''
    query_db(q,d,0)

def delete_database(acc,action):
    if action=="ALL":
        query_db('''DELETE FROM ACCOUNT WHERE ACCOUNT_NUMBER = ?''', (acc,),0)
        query_db('''DELETE FROM BENEFICIARY WHERE ACCOUNT_NUMBER = ?''', (acc,),0)
        query_db('''DELETE FROM TRANSACTIONS WHERE ACCOUNT_NUMBER = ?''', (acc,),0)
        print("ALL LOGS DELETED")
    elif action=="BENEFICIARY":
        query_db('''DELETE FROM BENEFICIARY WHERE "BENEFICIARY_AC/NO" = ?''', (acc,))

def add_beneficiary_to_file(account_number):
    b_name = input("Beneficiary Name: ")
    b_acc = input("Beneficiary A/c Number: ")
    b_limit = input("Max Transfer Limit: ")
    d=(account_number,b_name,b_acc,b_limit)
    q=''' insert into BENEFICIARY
      (ACCOUNT_NUMBER,BENEFICIARY_NAME,"BENEFICIARY_AC/NO","MAX.LIMIT")
      VALUES(?,?,?,?)'''
    query_db(q,d,0)
    print("Beneficiary added successfully.")

def print_beneficiary():
    q='select * from BENEFICIARY'
    data = query_db(q, a=2)
    if not data:
        print("No beneficiaries found.")
        return []       
    print("\n--- Beneficiary List ---")    
    for idx, r in enumerate(data, 1):
        print(f"{idx}. Name: {r[1]} | A/c: {r[2]} | Limit: {r[3]}")
    return data

def print_transactions_file():
    q=''' select *
          from TRANSACTIONS
      '''
    data= query_db(q,None,2)       
    print("\n--- Transactions List ---")    
    for idx, data in enumerate(data, 1):
        print(f"{idx}. ACCOUNT_NUMBER: {data[0]} | DATE: {data[1]} |TIME: {data[2]} | AMOUNT: {data[3]} | TO: {data[4]} | ACTION: {data[5]}")

def account_creation():
    q=''' select count(*)
          from ACCOUNT
      '''
    c=query_db(q,None,1)[0]
    if c>0:
        print("Account Already Exists")
        ch = input("Do you want to continue (1) or Create a new account (2)? ")
        if ch == "2":
            q=''' Select ACCOUNT_NUMBER 
                  FROM ACCOUNT
                  limit 1
                '''
            a=query_db(q,None,1)[0]
            delete_database(a,"ALL")
        else: 
            return

    name = input("ENTER ACCOUNT HOLDER NAME : ")
    SPIN = input("CREATE 4 DIGIT STANDARD PIN : ") 
    print("GIVE ANSWERS TO 3 SECURITY QUESTIONS:")
    a1 = input(f"{q1} : ")
    a2 = input(f"{q2} : ")
    a3 = input(f"{q3} : ")
    account_no = acc_generator()    
    HSPIN = hspin_generator()
    TWPIN = input("Create a TRANSACTION-WITHDRAWL PIN "
                                      "(Transfer/Withdrawal PIN): ")
    balance_initial = 2500.0
    print("\n\n\n")
    print("ACCOUNT DETAILS------------")
    print("ACCOUNT NUMBER :",account_no)
    print("STANDARD PIN :",SPIN)
    print("TWPIN PIN :",TWPIN)
    print("HIGH SEQURITY PIN :",HSPIN)
    print(f"ANSWERS TO ALL SEQURITY QUESTIONS\n :{a1}\n{a2}\n{a3}")

    raw_data = (name,account_no, SPIN,a1,a2,a3,HSPIN,
                TWPIN,balance_initial)

    q=''' insert into ACCOUNT 
          (ACCOUNT_HOLDER,ACCOUNT_NUMBER,SPIN,"Q1: NAME OF FAVOURITE MOVIE",
           "Q2: NAME OF BIRTH CITY","Q3: FAVOURITE COLOUR",HSPIN,TWPIN,AMOUNT)
          VALUES(?,?,?,?,?,?,?,?,?)'''
    query_db(q,raw_data,0)
    transaction_log(account_no,balance_initial,"SELF","ACCOUNT CREATED")      
    print(f"Account created successfully! Your Account Number is {account_no}")

def load_account_data():
    q='''select ACCOUNT_HOLDER as NAME,
        ACCOUNT_NUMBER as ACCOUNT_NO ,SPIN,"Q1: NAME OF FAVOURITE MOVIE" as a1,
        "Q2: NAME OF BIRTH CITY" as a2,"Q3: FAVOURITE COLOUR" as a3,
        HSPIN,TWPIN, AMOUNT
        from ACCOUNT
        LIMIT 1
        '''
    data=query_db(q,None,1)
    if not data:
        return None
    return {
        "NAME" : data[0],
        "ACCOUNT_NO" : data[1],
        "SPIN" : data[2],
        "a1": data[3],
        "a2": data[4],
        "a3": data[5],
        "HSPIN" : data[6],
        "TWPIN" : data[7],
        "AMOUNT" : data[8]
    }

def update_account_balance(new_balance):
    q=''' update ACCOUNT 
        set AMOUNT = ?'''
    query_db(q,(new_balance,),0)

def login():
    data = load_account_data()
    if not data:
        print("CREATE AN ACCOUNT TO CONTINUE")
        return False
    a = 3
    while a > 0:
        passed= authenticate(data,['SPIN'])
        if passed:
            print("LOGIN SUCCESSFUL!")
            dashboard(data)
            return True
        else:
            a -= 1
            print(f"INCORRECT PIN. ATTEMPTS LEFT = {a}")
    print("\nTOO MANY FAILED ATTEMPTS. SECURITY SYSTEM TRIGGERED")
    passed= authenticate(data,['HSPIN'])
    if passed:
        print("SECURITY VERIFICATION PASSED")
        dashboard(data)
        return True
    else:
        p=authenticate(data,["QUESTIONS"])
        if p:
            print("SECURITY VERIFICATION PASSED")
            dashboard(data)
            return True
        else:
            print("SECURITY VERIFICATION FAILED ! DELETING ALL LOGS")
            delete_database(data["ACCOUNT_NO"],"ALL")
            return False

def add_beneficiary(data):
    if authenticate(data, ['HSPIN']):
        a=data["ACCOUNT_NO"]
        add_beneficiary_to_file(a)
    else:
        print("INCORRECT HIGH SECURITY PIN ENTERED")

def tranfer_beneficiary(data):
    bfcs = print_beneficiary()
    if bfcs==[]: return
    i = int(input("Enter Index to delete: ").strip())
    if i<1 or i>len(bfcs):
        print("Invalid selection.")
        return
    bname=bfcs[i-1][1]
    limit=bfcs[i-1][3]
    amount=float(input("ENTER AMOUNT TO BE TRANSFERRED : "))
    if amount>limit:
        print("AMOUNT EXCEEDS MAX TRANSFER LIMIT")
        return
    if amount>data["AMOUNT"]:
        print("INSUFFICIENT BALANCE")
        return
    if  not authenticate(data,['TWPIN']):
        print("Incorrect TWPIN.")
        return
    new_bal = data["AMOUNT"] - amount
    update_account_balance(new_bal)
    action = "TRANSFERRED"
    transaction_log(data["ACCOUNT_NO"],amount,bname,action)
    print(f"Transaction successful! New Balance: {new_bal}")
            
def withdraw(data):
    amount = float(input("Enter amount: "))
    if amount > data["AMOUNT"]:
        print("TRANSACTION CANNOT BE PROCESSED. INSUFFICIENT BALANCE")
        return
    if  not authenticate(data,['TWPIN']):
        print("Incorrect TWPIN.")
        return
    new_bal = data["AMOUNT"] - amount
    update_account_balance(new_bal)
    action = "WITHDRAWN"
    transaction_log(data["ACCOUNT_NO"],amount,"SELF",action)
    print(f"Transaction successful! New Balance: {new_bal}")

def deposit(data):
    amount = float(input("Enter amount: "))
    data = load_account_data()
    if not authenticate(data,['TWPIN']):
        print("Incorrect TWPIN.")
        return
    new_bal = data["AMOUNT"] + amount
    update_account_balance(new_bal)
    action = "DEPOSITED"
    transaction_log(data["ACCOUNT_NO"],amount,"SELF",action)
    print(f"Transaction successful! New Balance: {new_bal}")       

def check_balance():
    current_data = load_account_data()
    print(f"Total Balance: {current_data['AMOUNT']}")

def pin_change(data):
    passed=authenticate(data,['HSPIN',"QUESTIONS"])
    if passed:
        new_pin = input("Enter new standard PIN: ")
        data["SPIN"] = new_pin
        d=(new_pin,data["ACCOUNT_NO"])
        q=''' update ACCOUNT
              set spin =?
              WHERE ACCOUNT_NUMBER=?'''
        query_db(q,d,0)
        print("PIN changed successfully.")
    else:
        print("Verification failed.")

def beneficiary_delete(data):
    if not authenticate(data, ['TWPIN', 'HSPIN']): return
    bfcs = print_beneficiary()
    if bfcs==[]: return
    i = int(input("Enter Index to delete: ").strip())
    if i<1 or i>len(bfcs):
        print("Invalid selection.")
        return
    accd = bfcs[i-1][2]
    delete_database(accd,"BENEFICIARY")
    print("Beneficiary deleted.")


def dashboard(data):
    c=0
    while c!=10:
        print("\n--- Banking Menu ---")
        print("1. Add Beneficiary")
        print("2. Get All Beneficiary Data")
        print("3. Delete Beneficiary")
        print("4. Transfer Money To Beneficiary")
        print("5. Withdraw Money")
        print("6. Deposit Money")
        print("7. Get Transaction History")
        print("8. Check Total Balance")
        print("9. Change PIN")
        print("10. Logout")
        c = int(input("Select an option (1-10): ")) # change conditions
        if   c == 1: add_beneficiary(data)
        elif c == 2: print_beneficiary()
        elif c == 3: beneficiary_delete(data)
        elif c == 4: tranfer_beneficiary(data)
        elif c == 5: withdraw()
        elif c == 6: deposit()
        elif c == 7: print_transactions_file()
        elif c == 8: check_balance()
        elif c == 9: pin_change(data)

def main():
    while True:
        print(f"=== WELCOME TO APOORV BANKING SYSTEM ===")
        print("(a) Already having an account")
        print("(b) Create an account")
        choice = input("Select option (a/b or 'q' to quit): ").lower()
        
        if choice == 'b':
            account_creation()
        elif choice == 'a':
            login()
        elif choice == 'q':
            break

if __name__ == "__main__":
    main()