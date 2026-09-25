import string
import random
import Modules.utils as utils
import Modules.transaction as transaction

def acc_generator(): # can be auto generated
    return "".join(random.choices(string.digits, k=10))

def hspin_generator():
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
            utils.delete_database(a,"ALL")
        else: 
            return

    name = input("ENTER ACCOUNT HOLDER NAME : ")
    SPIN = input("CREATE 4 DIGIT STANDARD PIN : ") 
    print("GIVE ANSWERS TO 3 SECURITY QUESTIONS:")
    a1 = input(f"{utils.q1} : ")
    a2 = input(f"{utils.q2} : ")
    a3 = input(f"{utils.q3} : ")
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
    utils.query_db(q,raw_data,0)
    transaction.transaction_log(account_no,balance_initial,"SELF","ACCOUNT CREATED")      
    print(f"Account created successfully! Your Account Number is {account_no}")


def load_account_data():
    q='''select ACCOUNT_HOLDER as NAME,
        ACCOUNT_NUMBER as ACCOUNT_NO ,SPIN,"Q1: NAME OF FAVOURITE MOVIE" as a1,
        "Q2: NAME OF BIRTH CITY" as a2,"Q3: FAVOURITE COLOUR" as a3,
        HSPIN,TWPIN, AMOUNT
        from ACCOUNT
        LIMIT 1
        '''
    data=utils.query_db(q,None,1)
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
    utils.query_db(q,(new_balance,),0)