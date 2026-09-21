from datetime import datetime
import os
import random
import string

os.system("color 02")

# FILES 
File_Account = "data_account.txt"
File_Transaction = "data_transaction.txt"
File_Beneficiary = "data_beneficiary.txt"

def acc_generator():
    return "".join(random.choices(string.digits, k=10))

def hs_pin_generator():
    return "".join(random.choices(string.digits, k=4))

def transaction_log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}]\n\t {message}\n"
    with open(File_Transaction, "a") as f:
        f.write(log_entry)

def file_delete():
    for file in [File_Transaction, File_Account, File_Beneficiary]:
        if os.path.exists(file):
            os.remove(file)
    print("ALL LOGS AND FILES DELETED")

def add_beneficiary_to_file():
    b_name = input("Beneficiary Name: ")
    b_acc = input("Beneficiary A/c Number: ")
    b_limit = input("Max Transfer Limit: ")
    plain_text = f"{b_name}\t{b_acc}\t{b_limit}\n"
    with open(File_Beneficiary, "a") as f:
        f.write(plain_text)
    print("Beneficiary added successfully.")

def print_beneficiary_file():
    if not os.path.exists(File_Beneficiary):
        print("No beneficiaries found.")
        return        
    print("\n--- Beneficiary List ---")    
    with open(File_Beneficiary, "r") as f:
        i = 1
        for line in f:
            if line.strip():
                parts = line.strip().split("\t")
                name = parts[0]
                acct = parts[1]
                limit = parts[2]
                print(f"{i}. Name: {name} | A/c: {acct} | Limit: {limit}")
                i += 1

def delete_beneficiary_from_file():
    if not os.path.exists(File_Beneficiary):
        print("No beneficiaries file found.")
        return

    with open(File_Beneficiary, "r") as f:
        lines = f.readlines()
    
    beneficiaries = [l.strip() for l in lines if l.strip()]   

    if not beneficiaries:
        print("No beneficiaries to delete.")
        return

    for idx, b in enumerate(beneficiaries, 1):
        name, acct, *_ = b.strip().split("\t")
        print(f"{idx}. {name} ({acct})")
        
    choice = input("Enter serial number to delete: ")
    del_idx = int(choice) - 1

    if 0 <= del_idx < len(beneficiaries):
        beneficiaries.pop(del_idx)
        with open(File_Beneficiary, "w") as f:
            for b in beneficiaries:
                f.write((b if b.endswith('\n') else b + '\n'))
        print("Beneficiary deleted.")
    else:
        print("Invalid selection.")

def account_creation():
    if os.path.exists(File_Account):
        print("Account Already Exists")
        ch = input("Do you want to continue (1) or Create a new account (2)? ")
        if ch == "2":
            file_delete()
        else: 
            return

    name = input("ENTER ACCOUNT HOLDER NAME : ")
    account_no = acc_generator()
    pin = input("CREATE 4 DIGIT STANDARD PIN : ")
    
    q1 = "NAME OF FAVOURITE MOVIE"
    q2 = "NAME OF BIRTH CITY"
    q3 = "FAVOURITE COLOUR"
    
    print("GIVE ANSWERS TO 3 SECURITY QUESTIONS:")
    a1 = input(f"{q1} : ")
    a2 = input(f"{q2} : ")
    a3 = input(f"{q3} : ")
    
    hs_pin = hs_pin_generator()
    print(f"YOUR HIGH SECURITY PIN IS : {hs_pin} (KEEP IT SAFELY)")
    twpin = input("Create a TWPIN (Transfer/Withdrawal PIN): ")
    balance_initial = 2500.0

    raw_data = f"{name}\n{account_no}\n{pin}\n{q1}:{a1}\n{q2}:{a2}\n{q3}:{a3}\n{hs_pin}\n{twpin}\n{balance_initial}\n"
    
    with open(File_Account, "w") as f:
        f.write(raw_data)

    with open(File_Transaction, "w") as f:
        initial_log = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Account Created.\n"
        f.write(initial_log)
        
    print(f"Account created successfully! Your Account Number is {account_no}")

def load_account_data():
    if not os.path.exists(File_Account):
        return None

    with open(File_Account, "r") as f:
        content = f.read()

    lines = [line.strip() for line in content.split("\n") if line.strip()]

    if len(lines) < 9:
        return None

    data = {}
    data["name"] = lines[0]
    data["acc_no"] = lines[1]
    data["pin"] = lines[2]

    data["q1"], data["a1"] = lines[3].split(":")
    data["q2"], data["a2"] = lines[4].split(":")
    data["q3"], data["a3"] = lines[5].split(":")

    data["hs_pin"] = lines[6]
    data["t_pin"] = lines[7]
    data["balance"] = float(lines[8])
    return data

def update_account_balance(new_balance):
    data = load_account_data()

    if data:
        raw_data = (
            f"{data['name']}\n"
            f"{data['acc_no']}\n"
            f"{data['pin']}\n"
            f"{data['q1']}:{data['a1']}\n"
            f"{data['q2']}:{data['a2']}\n"
            f"{data['q3']}:{data['a3']}\n"
            f"{data['hs_pin']}\n"
            f"{data['t_pin']}\n"
            f"{new_balance}\n"
        )

        with open(File_Account, "w") as f:
            f.write(raw_data)

def login():
    data = load_account_data()
    if not data:
        print("CREATE AN ACCOUNT TO CONTINUE")
        return False
    a = 3
    while a > 0:
        epin = input("ENTER YOUR STANDARD PIN : ")
        if epin == data["pin"]:
            print("LOGIN SUCCESSFUL!")
            dashboard(data)
            return True
        else:
            a -= 1
            print(f"INCORRECT PIN. ATTEMPTS LEFT = {a}")
    print("\nTOO MANY FAILED ATTEMPTS. SECURITY SYSTEM TRIGGERED")
    ehs_pin = input("ENTER YOUR HIGH SECURITY PIN : ")
    if ehs_pin == data["hs_pin"]:
        print("SECURITY VERIFICATION PASSED")
        dashboard(data)
        return True
    else:
        ans1 = input(f"Answer Q1 ({data['q1']}): ")
        ans2 = input(f"Answer Q2 ({data['q2']}): ")
        ans3 = input(f"Answer Q3 ({data['q3']}): ")
        if ans1 == data["a1"] and ans2 == data["a2"] and ans3 == data["a3"]:
            print("SECURITY VERIFICATION PASSED")
            dashboard(data)
            return True
        else:
            print("SECURITY VERIFICATION FAILED ! DELETING ALL LOGS")
            file_delete()
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
            hs = input("ENTER HIGH SECURITY PIN : ")
            if hs == data["hs_pin"]:
                add_beneficiary_to_file()
            else:
                print("INCORRECT HIGH SECURITY PIN ENTERED")
        elif c == 2:
            print_beneficiary_file()
        elif c == 3:  # CHANGES TO BE MADE HERE
            amount = float(input("Enter amount: "))
            current_data = load_account_data()
            if amount > current_data["balance"]:
                print("TRANSACTION CANNOT BE PROCESSED. INSUFFICIENT BALANCE")
            else:
                tp = input("Enter TPIN: ")
                if tp == current_data["t_pin"]:
                    new_bal = current_data["balance"] - amount
                    update_account_balance(new_bal)
                    action = "Withdrawn"
                    transaction_log(f"{action} amount: {amount}.\n\t New Balance: {new_bal}")
                    print(f"Transaction successful! New Balance: {new_bal}")
                else:
                    print("Incorrect TPIN.")
        elif c == 4:
            amount = float(input("Enter amount: "))
            current_data = load_account_data()
            if amount > current_data["balance"]:
                print("TRANSACTION CANNOT BE PROCESSED. INSUFFICIENT BALANCE")
            else:
                tp = input("Enter TPIN: ")
                if tp == current_data["t_pin"]:
                    new_bal = current_data["balance"] - amount
                    update_account_balance(new_bal)
                    action = "Withdrawn"
                    transaction_log(f"{action} amount: {amount}.\n\t New Balance: {new_bal}")
                    print(f"Transaction successful! New Balance: {new_bal}")
                else:
                    print("Incorrect TPIN.")
        elif c == 5:
            amount = float(input("Enter amount: "))
            current_data = load_account_data()
            tp = input("Enter TPIN: ")
            if tp == current_data["t_pin"]:
                new_bal = current_data["balance"] + amount
                update_account_balance(new_bal)
                action = "Deposited"
                transaction_log(f"{action} amount: {amount}.\n\t New Balance: {new_bal}")
                print(f"Transaction successful! New Balance: {new_bal}")
            else:
                print("Incorrect TPIN.")
        elif c == 6:
            current_data = load_account_data()
            print(f"Total Balance: {current_data['balance']}")
        elif c == 7:
            if os.path.exists(File_Transaction):
                print("\n--- Transaction History ---")
                with open(File_Transaction, "r") as f:
                    for line in f:
                        if line.strip():
                            print(line.strip())
            else:
                print("No history found.")
        elif c == 8:
            ans1 = input(f"Answer Q1 ({data['q1']}): ")
            ans2 = input(f"Answer Q2 ({data['q2']}): ")
            ans3 = input(f"Answer Q3 ({data['q3']}): ")
            entered_hs = input("Enter High-Security PIN: ")
            if ans1 == data["a1"] and ans2 == data["a2"] and ans3 == data["a3"] and entered_hs == data["hs_pin"]:
                new_pin = input("Enter new standard PIN: ")
                data["pin"] = new_pin
                update_account_balance(data["balance"])
                print("PIN changed successfully.")
            else:
                print("Verification failed.")
        elif c == 9:
            tp = input("Enter TPIN: ")
            hs = input("Enter High-Security PIN: ")
            if tp == data["t_pin"] and hs == data["hs_pin"]:
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