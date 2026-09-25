import Modules.utils as utils
import Modules.accounts as accounts
import Modules.transaction as transaction

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

def print_beneficiary():
    q='select * from BENEFICIARY'
    data = utils.query_db(q, a=2)
    if not data:
        print("No beneficiaries found.")
        return []       
    print("\n--- Beneficiary List ---")    
    for idx, r in enumerate(data, 1):
        print(f"{idx}. Name: {r[1]} | A/c: {r[2]} | Limit: {r[3]}")
    return data

def add_beneficiary(data):
    if utils.authenticate(data, ['HSPIN']):
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
    if  not utils.authenticate(data,['TWPIN']):
        print("Incorrect TWPIN.")
        return
    new_bal = data["AMOUNT"] - amount
    accounts.update_account_balance(new_bal)
    action = "TRANSFERRED"
    transaction.transaction_log(data["ACCOUNT_NO"],amount,bname,action)
    print(f"Transaction successful! New Balance: {new_bal}")

def beneficiary_delete(data):
    if not utils.authenticate(data, ['TWPIN', 'HSPIN']): return
    bfcs = print_beneficiary()
    if bfcs==[]: return
    i = int(input("Enter Index to delete: ").strip())
    if i<1 or i>len(bfcs):
        print("Invalid selection.")
        return
    accd = bfcs[i-1][2]
    utils.delete_database(accd,"BENEFICIARY")
    print("Beneficiary deleted.")
