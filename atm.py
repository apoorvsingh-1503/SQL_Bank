from datetime import datetime
import os
import random
import string
import sqlite3

db="BANK.sqlite3"
q1 = "NAME OF FAVOURITE MOVIE"
q2 = "NAME OF BIRTH CITY"
q3 = "FAVOURITE COLOUR"

def query_db(q,data=None):
    con = sqlite3.connect(db)
    cur = con.cursor()

    if data is None:
        cur.execute(q)
    else:
        cur.execute(q,data)

    result = cur.fetchone()
    con.close()
    return result

def query_dba(q, data=None):
    con = sqlite3.connect(db)
    cur = con.cursor()

    if data is None:
        cur.execute(q)
    else:
        cur.execute(q,data)

    result = cur.fetchall()
    con.close()
    return result

def execute(q,data=None):
    con = sqlite3.connect(db)
    cur = con.cursor()
    if data is None:
        cur.execute(q)
    else:
        cur.execute(q,data)
    con.commit()
    con.close()
os.system("color 02")

def acc_generator():
    return "".join(random.choices(string.digits, k=10))

def hs_pin_generator():
    return "".join(random.choices(string.digits, k=4))

def transaction_log(ACCOUNT_NUMBER,AMOUNT,BENEFICIARY,ACTION):
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H:%M:%S")
    d=(ACCOUNT_NUMBER,current_date,current_time,AMOUNT,BENEFICIARY,ACTION)
    q=''' insert into TRANSACTIONS
      (ACCOUNT_NUMBER,DATE,TIME,AMOUNT,BENEFICIARY,ACTION)
      VALUES(?,?,?,?,?,?)'''
    execute(q,d)

def delete_database(acc,action):
    if action=="ALL":
        execute('''DELETE FROM ACCOUNT WHERE ACCOUNT_NUMBER = ?''', (acc,))
        execute('''DELETE FROM BENEFICIARY WHERE ACCOUNT_NUMBER = ?''', (acc,))
        execute('''DELETE FROM TRANSACTIONS WHERE ACCOUNT_NUMBER = ?''', (acc,))
        print("ALL LOGS DELETED")
    elif action=="BENEFICIARY":
        execute('''DELETE FROM BENEFICIARY WHERE "BENEFICIARY_AC/NO" = ?''', (acc,))

def add_beneficiary_to_file(account_number):
    b_name = input("Beneficiary Name: ")
    b_acc = input("Beneficiary A/c Number: ")
    b_limit = input("Max Transfer Limit: ")
    d=(account_number,b_name,b_acc,b_limit)
    q=''' insert into BENEFICIARY
      (ACCOUNT_NUMBER,BENEFICIARY_NAME,"BENEFICIARY_AC/NO","MAX.LIMIT")
      VALUES(?,?,?,?)'''
    execute(q,d)
    print("Beneficiary added successfully.")

def print_beneficiary_file():
    q=''' select *
          from BENEFICIARY
      '''
    data= query_dba(q)
    if not data:
        print("No beneficiaries found.")
        return        
    print("\n--- Beneficiary List ---")    
    for idx, data in enumerate(data, 1):
        print(f"{idx}. Name: {data[1]} | A/c: {data[2]} | Limit: {data[3]}")

def delete_beneficiary_from_file():
    q=''' select *
          from BENEFICIARY
      '''
    data=query_dba(q)
    if not data:
        print("No beneficiaries file found.")
        return

    for idx, data in enumerate(data, 1):
        print(f"{idx}. {data[1]} ({data[2]})")

    accd = int(input("Enter Account Number to delete: ").strip())
    b=''' SELECT BENEFICIARY_NAME FROM BENEFICIARY
          WHERE "BENEFICIARY_AC/NO" =?'''
    match=query_db(b,(accd,))
    if match:
        delete_database(accd,"BENEFICIARY")
        print("Beneficiary deleted.")
    else:
        print("Invalid selection.")
def print_transactions_file():
    q=''' select *
          from TRANSACTIONS
      '''
    data= query_dba(q)       
    print("\n--- Transactions List ---")    
    for idx, data in enumerate(data, 1):
        print(f"{idx}. ACCOUNT_NUMBER: {data[0]} | DATE: {data[1]} |TIME: {data[2]} | AMOUNT: {data[3]} | TO: {data[4]} | ACTION: {data[5]}")
def account_creation():
    q=''' select count(*)
          from ACCOUNT
      '''
    c=query_db(q)[0]
    if c>0:
        print("Account Already Exists")
        ch = input("Do you want to continue (1) or Create a new account (2)? ")
        if ch == "2":
            q=''' Select ACCOUNT_NUMBER 
                  FROM ACCOUNT
                  limit 1
                '''
            a=query_db(q)[0]
            delete_database(a,"ALL")
        else: 
            return

    name = input("ENTER ACCOUNT HOLDER NAME : ")
    account_no = acc_generator()
    pin = input("CREATE 4 DIGIT STANDARD PIN : ")   
    
    print("GIVE ANSWERS TO 3 SECURITY QUESTIONS:")
    a1 = input(f"{q1} : ")
    a2 = input(f"{q2} : ")
    a3 = input(f"{q3} : ")
    
    HIGH_SEQURITY_PIN = hs_pin_generator()
    print(f"YOUR HIGH SECURITY PIN IS : {HIGH_SEQURITY_PIN} (KEEP IT SAFELY)")
    TRANSACTION_WITHDRAWL_PIN = input("Create a TRANSACTION-WITHDRAWL PIN (Transfer/Withdrawal PIN): ")
    balance_initial = 2500.0

    raw_data = (name,account_no, pin,a1,a2,a3,HIGH_SEQURITY_PIN,TRANSACTION_WITHDRAWL_PIN,balance_initial)

    q=''' insert into ACCOUNT 
          (ACCOUNT_HOLDER,ACCOUNT_NUMBER,SPIN,"Q1: NAME OF FAVOURITE MOVIE",
           "Q2: NAME OF BIRTH CITY","Q3: FAVOURITE COLOUR",HSPIN,TWPIN,AMOUNT)
          VALUES(?,?,?,?,?,?,?,?,?)'''
    execute(q,raw_data)
    transaction_log(account_no,balance_initial,"SELF","ACCOUNT CREATED")      
    print(f"Account created successfully! Your Account Number is {account_no}")

def load_account_data():
    q='''select ACCOUNT_HOLDER as NAME,
        ACCOUNT_NUMBER as ACCOUNT_NO ,SPIN as PIN,"Q1: NAME OF FAVOURITE MOVIE" as a1,
        "Q2: NAME OF BIRTH CITY" as a2,"Q3: FAVOURITE COLOUR" as a3,
        HSPIN as "HIGH-SEQURITY PIN",TWPIN as "TRANSACTION-WITHDRAWL PIN", AMOUNT
        from ACCOUNT
        LIMIT 1
        '''
    data=query_db(q)
    if not data:
        return None
    return{
        "NAME" : data[0],
        "ACCOUNT_NO" : data[1],
        "PIN" : data[2],
        "a1": data[3],
        "a2": data[4],
        "a3": data[5],
        "HIGH-SEQURITY PIN" : data[6],
        "TRANSACTION-WITHDRAWL PIN" : data[7],
        "AMOUNT" : data[8]
    }
def update_account_balance(new_balance):
    q=''' update ACCOUNT 
        set AMOUNT = ?'''
    execute(q,(new_balance,))

def login():
    data = load_account_data()
    if not data:
        print("CREATE AN ACCOUNT TO CONTINUE")
        return False
    a = 3
    while a > 0:
        epin = int(input("ENTER YOUR STANDARD PIN : "))
        if epin == data["PIN"]:
            print("LOGIN SUCCESSFUL!")
            dashboard(data)
            return True
        else:
            a -= 1
            print(f"INCORRECT PIN. ATTEMPTS LEFT = {a}")
    print("\nTOO MANY FAILED ATTEMPTS. SECURITY SYSTEM TRIGGERED")
    ehs_pin = input("ENTER YOUR HIGH SECURITY PIN : ")
    if ehs_pin == data["HIGH-SEQURITY PIN"]:
        print("SECURITY VERIFICATION PASSED")
        dashboard(data)
        return True
    else:
        ans1 = input(f"Answer Q1 {q1}: ")
        ans2 = input(f"Answer Q2 {q2}: ")
        ans3 = input(f"Answer Q3 {q3}: ")
        if ans1 == data["a1"] and ans2 == data["a2"] and ans3 == data["a3"]:
            print("SECURITY VERIFICATION PASSED")
            dashboard(data)
            return True
        else:
            print("SECURITY VERIFICATION FAILED ! DELETING ALL LOGS")
            delete_database(data["ACCOUNT_NO"],"ALL")
            return False

def dashboard(data):
    while True:
        print("\n--- Banking Menu ---")
        print("1. Add Beneficiary")
        print("2. Get All Beneficiary Data")
        print("3. Transfer Money To Beneficiary")
        print("4. Withdraw Money")
        print("5. Deposit Money")
        print("6. Check Total Balance")
        print("7. Get Transaction History")
        print("8. Change PIN")
        print("9. Delete Beneficiary")
        print("10. Logout")
        c = int(input("Select an option (1-10): "))
        if c == 1:
            hs = int(input("ENTER HIGH SECURITY PIN : "))
            if hs == data["HIGH-SEQURITY PIN"]:
                a=data["ACCOUNT_NO"]
                add_beneficiary_to_file(a)
            else:
                print("INCORRECT HIGH SECURITY PIN ENTERED")
        elif c == 2:
            print_beneficiary_file()
        elif c==3:
            print_beneficiary_file()
            accd = int(input("Enter Account Number to be Transferred: ").strip())
            bq=''' SELECT "BENEFICIARY_NAME","BENEFICIARY_AC/NO","MAX.LIMIT"
                    FROM BENEFICIARY
                    WHERE "BENEFICIARY_AC/NO"=?
                    '''
            data=query_db(bq,(accd,))
            if not data:
                print("NO SUCH BENEFICIARY")
            else:
                bname=data[0]
                limit=data[2]
                amount=float(input("ENTER AMOUNT TO BE TRANSFERRED : "))
                if amount>limit:
                    print("AMOUNT EXCEEDS MAX TRANSFER LIMIT")
                else:
                    d=load_account_data()
                    if amount>d["AMOUNT"]:
                        print("INSUFFICIENT BALANCE")
                    else:
                        tp=int(input("ENTER TRANSACTION-WITHDRAWL PIN:  "))
                        if tp==d["TRANSACTION-WITHDRAWL PIN"]:
                            new_bal = d["AMOUNT"] - amount
                            update_account_balance(new_bal)
                            action = "TRANSFERRED"
                            transaction_log(d["ACCOUNT_NO"],amount,bname,action)
                            print(f"Transaction successful! New Balance: {new_bal}")
                        else:
                            print("Incorrect TPIN.")
        elif c == 4:
            amount = float(input("Enter amount: "))
            current_data = load_account_data()
            if amount > current_data["AMOUNT"]:
                print("TRANSACTION CANNOT BE PROCESSED. INSUFFICIENT BALANCE")
            else:
                tp = int(input("Enter TPIN: "))
                if tp == current_data["TRANSACTION-WITHDRAWL PIN"]:
                    new_bal = current_data["AMOUNT"] - amount
                    update_account_balance(new_bal)
                    action = "WITHDRAWN"
                    transaction_log(current_data["ACCOUNT_NO"],amount,"SELF",action)
                    print(f"Transaction successful! New Balance: {new_bal}")
                else:
                    print("Incorrect TPIN.")
        elif c == 5:
            amount = float(input("Enter amount: "))
            current_data = load_account_data()
            tp = int(input("Enter TPIN: "))
            if tp == current_data["TRANSACTION-WITHDRAWL PIN"]:
                new_bal = current_data["AMOUNT"] + amount
                update_account_balance(new_bal)
                action = "DEPOSITED"
                transaction_log(current_data["ACCOUNT_NO"],amount,"SELF",action)
                print(f"Transaction successful! New Balance: {new_bal}")
            else:
                print("Incorrect TPIN.")
        elif c == 6:
            current_data = load_account_data()
            print(f"Total Balance: {current_data['AMOUNT']}")
        elif c==7:
            print_transactions_file()
        elif c == 8:
            ans1 = input(f"Answer Q1 {q1}): ")
            ans2 = input(f"Answer Q2 {q2}): ")
            ans3 = input(f"Answer Q3 {q3}): ")
            entered_hs = int(input("Enter High-Security PIN: "))
            if ans1 == data["a1"] and ans2 == data["a2"] and ans3 == data["a3"] and entered_hs == data["HIGH-SEQURITY PIN"]:
                new_pin = input("Enter new standard PIN: ")
                data["PIN"] = new_pin
                d=(new_pin,data["ACCOUNT_NO"])
                q=''' update ACCOUNT
                      set spin =?
                      WHERE ACCOUNT_NUMBER=?'''
                execute(q,d)
                print("PIN changed successfully.")
            else:
                print("Verification failed.")
        elif c == 9: 
            tp = int(input("Enter TPIN: "))
            hs = int(input("Enter High-Security PIN: "))
            if tp == data["TRANSACTION-WITHDRAWL PIN"] and hs == data["HIGH-SEQURITY PIN"]:
                delete_beneficiary_from_file()
            else:
                print("Incorrect credentials.")
        elif c == 10:
            break

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