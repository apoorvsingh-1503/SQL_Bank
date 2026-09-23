import utils
import PRINT_DEL as pd
import loads

def update_account_balance(new_balance):
    q=''' update ACCOUNT 
        set AMOUNT = ?'''
    utils.query_db(q,(new_balance,),0)


def transfer_beneficiary():
    pd.print_beneficiary_file()
    accd = int(input("Enter Account Number to be Transferred: ").strip())
    bq=''' SELECT "BENEFICIARY_NAME","BENEFICIARY_AC/NO","MAX.LIMIT"
                            FROM BENEFICIARY
                            WHERE "BENEFICIARY_AC/NO"=?
                            '''
    ds=utils.query_db(bq,(accd,),1)
    if not ds:
        print("NO SUCH BENEFICIARY")
    else:
        bname=ds[0]
        limit=ds[2]
        amount=float(input("ENTER AMOUNT TO BE TRANSFERRED : "))
        if amount>limit:
            print("AMOUNT EXCEEDS MAX TRANSFER LIMIT")
        else:
            d=loads.dla()
            if amount>d["AMOUNT"]:
                print("INSUFFICIENT BALANCE")
            else:
                tp=int(input("ENTER TRANSACTION-WITHDRAWL PIN:  "))
                auth=utils.authentication(tp,"TWPIN")
                if auth:
                    new_bal = d["AMOUNT"] - amount
                    update_account_balance(new_bal)
                    action = "TRANSFERRED"
                    pd.transaction_log(d["ACCOUNT_NO"],amount,bname,action)
                    print(f"Transaction successful! New Balance: {new_bal}")
                else:
                    print("Incorrect TPIN.")

def withdraw():
    amount = float(input("Enter amount: "))
    current_data = loads.dla()
    if amount > current_data["AMOUNT"]:
        print("TRANSACTION CANNOT BE PROCESSED. INSUFFICIENT BALANCE")
    else:
        tp = int(input("Enter TPIN: "))
        auth=utils.authentication(tp,"TWPIN")
        if auth:
            new_bal = current_data["AMOUNT"] - amount
            update_account_balance(new_bal)
            action = "WITHDRAWN"
            pd.transaction_log(current_data["ACCOUNT_NO"],amount,"SELF",action)
            print(f"Transaction successful! New Balance: {new_bal}")
        else:
            print("Incorrect TPIN.")

def deposit():
    amount = float(input("Enter amount: "))
    current_data = loads.dla()
    tp = int(input("Enter TPIN: "))
    auth=utils.authentication(tp,"TWPIN")
    if auth:
        new_bal = current_data["AMOUNT"] + amount
        update_account_balance(new_bal)
        action = "DEPOSITED"
        pd.transaction_log(current_data["ACCOUNT_NO"],amount,"SELF",action)
        print(f"Transaction successful! New Balance: {new_bal}")
    else:
        print("Incorrect TPIN.")

def history():
    pd.print_transactions_file()