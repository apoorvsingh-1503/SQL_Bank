import loads
import PROFILE as prof
import TRANSACTIONS as txn
import BENEFICIARY as ben
import PRINT_DEL as pd

q1 = "NAME OF FAVOURITE MOVIE"
q2 = "NAME OF BIRTH CITY"
q3 = "FAVOURITE COLOUR"

def login():
    data =loads.dla()
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
            pd.delete_database(data["ACCOUNT_NO"],"ALL")
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
        if c==1:
            ben.add_beneficiary()
        elif c == 2:
            ben.print_beneficiary()
        elif c == 3:
            txn.transfer_beneficiary()
        elif c == 4:
            txn.withdraw()
        elif c == 5:
            txn.deposit()
        elif c == 6:
            prof.check_balance()
        elif c == 7:
            txn.history()
        elif c == 8:
            prof.change_pin()
        elif c == 9:
            ben.delete_beneficiary()
        elif c == 10:
            break

def main():
    while True:
        print(f"=== WELCOME TO APOORV BANKING SYSTEM ===")
        print("(a) Already having an account")
        print("(b) Create an account")
        choice = input("Select option (a/b or 'q' to quit): ").lower()
        
        if choice == 'b':
            prof.account_creation()
        elif choice == 'a':
            login()
        elif choice == 'q':
            break

if __name__ == "__main__":
    main()