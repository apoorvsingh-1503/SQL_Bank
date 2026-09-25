import Modules.accounts as accounts
import Modules.beneficiary as beneficiary
import Modules.transaction as transaction
import Modules.utils as utils

def login():
    data = accounts.load_account_data()
    if not data:
        print("CREATE AN ACCOUNT TO CONTINUE")
        return False
    a = 3
    while a > 0:
        passed= utils.authenticate(data,['SPIN'])
        if passed:
            print("LOGIN SUCCESSFUL!")
            dashboard(data)
            return True
        else:
            a -= 1
            print(f"INCORRECT PIN. ATTEMPTS LEFT = {a}")
    print("\nTOO MANY FAILED ATTEMPTS. SECURITY SYSTEM TRIGGERED")
    passed= utils.authenticate(data,['HSPIN'])
    if passed:
        print("SECURITY VERIFICATION PASSED")
        dashboard(data)
        return True
    else:
        p=utils.authenticate(data,["QUESTIONS"])
        if p:
            print("SECURITY VERIFICATION PASSED")
            dashboard(data)
            return True
        else:
            print("SECURITY VERIFICATION FAILED ! DELETING ALL LOGS")
            utils.delete_database(data["ACCOUNT_NO"],"ALL")
            return False

def pin_change(data):
    passed=utils.authenticate(data,['HSPIN',"QUESTIONS"])
    if passed:
        new_pin = input("Enter new standard PIN: ")
        data["SPIN"] = new_pin
        d=(new_pin,data["ACCOUNT_NO"])
        q=''' update ACCOUNT
              set spin =?
              WHERE ACCOUNT_NUMBER=?'''
        utils.query_db(q,d,0)
        print("PIN changed successfully.")
    else:
        print("Verification failed.")



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
        if   c == 1: beneficiary.add_beneficiary(data)
        elif c == 2: beneficiary.print_beneficiary()
        elif c == 3: beneficiary.beneficiary_delete(data)
        elif c == 4: beneficiary.tranfer_beneficiary(data)
        elif c == 5: transaction.withdraw()
        elif c == 6: transaction.deposit()
        elif c == 7: transaction.print_transactions_file()
        elif c == 8: transaction.check_balance()
        elif c == 9: pin_change(data)

def main():
    while True:
        print(f"=== WELCOME TO APOORV BANKING SYSTEM ===")
        print("(a) Already having an account")
        print("(b) Create an account")
        choice = input("Select option (a/b or 'q' to quit): ").lower()
        
        if choice == 'b':
            accounts.account_creation()
        elif choice == 'a':
            login()
        elif choice == 'q':
            break

if __name__ == "__main__":
    main()