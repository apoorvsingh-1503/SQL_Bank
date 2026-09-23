import utils
import loads
import PRINT_DEL as pd

def add_beneficiary():
    hs = int(input("ENTER HIGH SECURITY PIN : "))
    auth=utils.authentication(hs,"HSPIN")
    if auth:
        a=loads.dla["ACCOUNT_NO"]
        pd.add_beneficiary_to_file(a)
    else:
        print("INCORRECT HIGH SECURITY PIN ENTERED")

def print_beneficiary():
    pd.print_beneficiary_file()

def delete_beneficiary():
    tp = int(input("Enter TPIN: "))
    hs = int(input("Enter High-Security PIN: "))
    auth1=utils.authentication(tp,"TWPIN")
    auth2=utils.authentication(hs,"HSPIN")
    if auth1 and auth2:
        pd.delete_beneficiary_from_file()
    else:
        print("Incorrect credentials.")