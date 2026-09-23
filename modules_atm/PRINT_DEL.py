import utils
from datetime import datetime

def add_beneficiary_to_file(account_number):
    b_name = input("Beneficiary Name: ")
    b_acc = input("Beneficiary A/c Number: ")
    b_limit = input("Max Transfer Limit: ")
    d=(account_number,b_name,b_acc,b_limit)
    q=''' insert into BENEFICIARY
      (ACCOUNT_NUMBER,BENEFICIARY_NAME,"BENEFICIARY_AC/NO","MAX.LIMIT")
      VALUES(?,?,?,?)'''
    utils.query_db(q,d,0)
    print("Beneficiary added successfully.")

def print_beneficiary_file():
    q='select * from BENEFICIARY'
    dd= utils.query_db(q,a=2)
    if not dd:
        print("No beneficiaries found.")
        return        
    print("\n--- Beneficiary List ---")    
    for idx, dd in enumerate(dd, 1):
        print(f"{idx}. Name: {dd[1]} | A/c: {dd[2]} | Limit: {dd[3]}")

def delete_beneficiary_from_file():
    print_beneficiary_file()
    accd = int(input("Enter Account Number to delete: ").strip())
    b=''' SELECT BENEFICIARY_NAME FROM BENEFICIARY
          WHERE "BENEFICIARY_AC/NO" =?'''
    match=utils.query_db(b,(accd,),1)
    if match:
        utils.delete_database(accd,"BENEFICIARY")
        print("Beneficiary deleted.")
    else:
        print("Invalid selection.")

def print_transactions_file():
    q=''' select *
          from TRANSACTIONS
      '''
    data= utils.query_db(q,None,2)       
    print("\n--- Transactions List ---")    
    for idx, data in enumerate(data, 1):
        print(f"{idx}. ACCOUNT_NUMBER: {data[0]} | DATE: {data[1]} |TIME: {data[2]} | AMOUNT: {data[3]} | TO: {data[4]} | ACTION: {data[5]}")

def transaction_log(ACCOUNT_NUMBER,AMOUNT,BENEFICIARY,ACTION):
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H:%M:%S")
    d=(ACCOUNT_NUMBER,current_date,current_time,AMOUNT,BENEFICIARY,ACTION)
    q=''' insert into TRANSACTIONS
      (ACCOUNT_NUMBER,DATE,TIME,AMOUNT,BENEFICIARY,ACTION)
      VALUES(?,?,?,?,?,?)'''
    utils.query_db(q,d,0)