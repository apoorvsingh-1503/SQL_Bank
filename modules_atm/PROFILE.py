import string
import random
import utils
import PRINT_DEL as pd
import loads

q1 = "NAME OF FAVOURITE MOVIE"
q2 = "NAME OF BIRTH CITY"
q3 = "FAVOURITE COLOUR"


def acc_generator(): # can be auto generated
    return "".join(random.choices(string.digits, k=10))

def hs_pin_generator():
    return "".join(random.choices(string.digits, k=4))

def account_creation():
    q=''' select count(*)
          from ACCOUNT
      '''
    c=utils.query_db(q,None,1)[0]
    if c>0:
        print("Account Already Exists")
        ch = input("Do you want to continue (1) or Create a new account (2)? ")
        if ch == "2":
            q=''' Select ACCOUNT_NUMBER 
                  FROM ACCOUNT
                  limit 1
                '''
            a=utils.query_db(q,None,1)[0]
            pd.delete_database(a,"ALL")
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
    TRANSACTION_WITHDRAWL_PIN = input("Create a TRANSACTION-WITHDRAWL PIN "
                                      "(Transfer/Withdrawal PIN): ")
    balance_initial = 2500.0

    raw_data = (name,account_no, pin,a1,a2,a3,HIGH_SEQURITY_PIN,
                TRANSACTION_WITHDRAWL_PIN,balance_initial)

    q=''' insert into ACCOUNT 
          (ACCOUNT_HOLDER,ACCOUNT_NUMBER,SPIN,"Q1: NAME OF FAVOURITE MOVIE",
           "Q2: NAME OF BIRTH CITY","Q3: FAVOURITE COLOUR",HSPIN,TWPIN,AMOUNT)
          VALUES(?,?,?,?,?,?,?,?,?)'''
    utils.query_db(q,raw_data,0)
    pd.transaction_log(account_no,balance_initial,"SELF","ACCOUNT CREATED")      
    print(f"Account created successfully! Your Account Number is {account_no}")

def check_balance():
    current_data =loads.dla()
    print(f"Total Balance: {current_data['AMOUNT']}")

def change_pin():
    print("PIN CHANGE OPTIONS-------")
    print("1.STANDARD PIN | 2. HIGH-SEQURITY PIN | 3.TRANSACTION WITHDRAWL PIN")
    ch=int(input("ENTER CHOICE(1-3) : "))           
    ans1 = input(f"Answer Q1 {q1}): ")
    ans2 = input(f"Answer Q2 {q2}): ")
    ans3 = input(f"Answer Q3 {q3}): ")
    a1c=utils.authentication(ans1,"QUESTION_1")
    a2c=utils.authentication(ans2,"QUESTION_2")
    a3c=utils.authentication(ans3,"QUESTION_3")
    if ch==1:
        entered_hs = int(input("Enter High-Security PIN: "))
        hc=utils.authentication(entered_hs,"HSPIN")
        if a1c and a2c and a3c and hc:
            new_pin = input("Enter new standard PIN: ")
            loads.dla["PIN"] = new_pin
            d=(new_pin,loads.dla["ACCOUNT_NO"])
            q=''' update ACCOUNT
                  set spin =?
                  WHERE ACCOUNT_NUMBER=?'''
            utils.query_db(q,d,0)
            print("PIN changed successfully.")
        else:
            print("Verification failed.")
    elif ch==2:
        entered_spin = int(input("Enter STANDARD PIN: "))
        sp=utils.authentication(entered_spin,"TWPIN")
        if a1c and a2c and a3c and sp:
            new_pin = input("Enter new High-Security PIN: ")
            loads.dla["HIGH-SEQURITY PIN"] = new_pin
            d=(new_pin,loads.dla["ACCOUNT_NO"])
            q=''' update ACCOUNT
                  set hspin =?
                  WHERE ACCOUNT_NUMBER=?'''
            utils.query_db(q,d,0)
            print("PIN changed successfully.")
        else:
            print("Verification failed.")
    elif ch==3:
        entered_spin = int(input("Enter STANDARD PIN: "))
        entered_hs = int(input("Enter High-Security PIN: "))
        hc=utils.authentication(entered_hs,"HSPIN")
        sp=utils.authentication(entered_spin,"TWPIN")
        if a1c and a2c and a3c and sp and hc:
            new_pin = input("Enter new High-Security PIN: ")
            loads.dla["TRANSACTION-WITHDRAWL PIN"] = new_pin
            d=(new_pin,loads.dla["ACCOUNT_NO"])
            q=''' update ACCOUNT
                  set twpin =?
                  WHERE ACCOUNT_NUMBER=?'''
            utils.query_db(q,d,0)
            print("PIN changed successfully.")
        else:
            print("Verification failed.")
    else:
        print("INVALID CHOICE")
