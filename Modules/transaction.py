from datetime import datetime 
import Modules.utils as utils
import Modules.accounts as accounts

def transaction_log(ACCOUNT_NUMBER,AMOUNT,BENEFICIARY,ACTION):
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H:%M:%S")
    d=(ACCOUNT_NUMBER,current_date,current_time,AMOUNT,BENEFICIARY,ACTION)
    q=''' insert into TRANSACTIONS
      (ACCOUNT_NUMBER,DATE,TIME,AMOUNT,BENEFICIARY,ACTION)
      VALUES(?,?,?,?,?,?)'''
    utils.query_db(q,d,0)

def print_transactions_file():
    q=''' select *
          from TRANSACTIONS
      '''
    data= utils.query_db(q,None,2)       
    print("\n--- Transactions List ---")    
    for idx, data in enumerate(data, 1):
        print(f"{idx}. ACCOUNT_NUMBER: {data[0]} | DATE: {data[1]} |TIME: {data[2]} | AMOUNT: {data[3]} | TO: {data[4]} | ACTION: {data[5]}")

def withdraw(data):
    amount = float(input("Enter amount: "))
    if amount > data["AMOUNT"]:
        print("TRANSACTION CANNOT BE PROCESSED. INSUFFICIENT BALANCE")
        return
    if  not utils.authenticate(data,['TWPIN']):
        print("Incorrect TWPIN.")
        return
    new_bal = data["AMOUNT"] - amount
    accounts.update_account_balance(new_bal)
    action = "WITHDRAWN"
    transaction_log(data["ACCOUNT_NO"],amount,"SELF",action)
    print(f"Transaction successful! New Balance: {new_bal}")

def deposit(data):
    amount = float(input("Enter amount: "))
    if not utils.authenticate(data,['TWPIN']):
        print("Incorrect TWPIN.")
        return
    new_bal = data["AMOUNT"] + amount
    accounts.update_account_balance(new_bal)
    action = "DEPOSITED"
    transaction_log(data["ACCOUNT_NO"],amount,"SELF",action)
    print(f"Transaction successful! New Balance: {new_bal}")  

def check_balance():
    current_data = utils.load_account_data()
    print(f"Total Balance: {current_data['AMOUNT']}")

