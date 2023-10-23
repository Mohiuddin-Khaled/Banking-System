from abc import ABC, abstractmethod


class Bank(ABC):
    @abstractmethod
    def onOffLoan(self, status):
        pass


class User(Bank):
    def __init__(self, name, email, address, account_type):
        self.name = name
        self.email = email
        self.address = address
        self.account_type = account_type
        self.balance = 0
        self.transaction = []
        self.loans_taken = 0

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.transaction.append(f"Deposit: +${amount}")
        else:
            print("Invalid amount for deposit.")

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            self.transaction.append(f"Withdraw: -${amount}")
        else:
            print("Invalid amount for withdrawal.")

    def transfer(self, recipient, amount):
        if recipient:
            if amount <= self.balance:
                self.balance -= amount
                recipient.balance += amount
                self.transaction.append(f"Transfer to {recipient.name}: -${amount}")
                recipient.transaction.append(f"Transfer from {self.name}: +${amount}")
            else:
                print("Invalid amount for the transfer.")
        else:
            print("account does not exist.")

    def take_loan(self, amount):
        if self.loans_taken < 2:
            self.balance += amount
            self.transaction.append(f"Loan: +${amount}")
            self.loans_taken += 1
        else:
            print("You have already taken the maximum number of loans.")

    def onOffLoan(self, status):
        print("Users are not allowed to on/off the loan feature.")


class Admin(Bank):
    def __init__(self):
        self.users = []

    def create_account(self, name, email, address, account_type):
        user = User(name, email, address, account_type)
        self.users.append(user)

    def delete_account(self, user):
        self.users.remove(user)

    def list_accounts(self):
        for user in self.users:
            print(
                f"Name: {user.name}, Email: {user.email}, Account Type: {user.account_type}"
            )

    def total_balance(self):
        total = sum(user.balance for user in self.users)
        return total

    def total_loan_amount(self):
        total = sum(user.balance for user in self.users if user.loans_taken > 0)
        return total

    def onOffLoan(self, status):
        if status:
            print("Loan feature on.")
        else:
            print("Loan feature off.")


def main():
    admin = Admin()

    while True:
        print("\nanking Management System")
        print("1. Admin")
        print("2. User")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            # Admin Menu
            while True:
                print("\nAdmin Menu:")
                print("1. Create Account")
                print("2. Delete Account")
                print("3. List Accounts")
                print("4. Total Available Balance")
                print("5. Total Loan Amount")
                print("6. On/Off Loan Feature")
                print("7. Main Menu")
                admin_choice = input("Enter your choice: ")

                if admin_choice == "1":
                    name = input("Enter user's name: ")
                    email = input("Enter user's email: ")
                    address = input("Enter user's address: ")
                    account_type = input("Enter account type (Savings/Current): ")
                    admin.create_account(name, email, address, account_type)
                    print(f"{name}'s account has been created.")
                elif admin_choice == "2":
                    print("List of accounts:")
                    admin.list_accounts()
                    account_name = input("Enter the name of the account to delete: ")
                    account_to_delete = None
                    for user in admin.users:
                        if user.name == account_name:
                            account_to_delete = user
                            break
                    if account_to_delete:
                        admin.delete_account(account_to_delete)
                        print(f"{account_name}'s account has been deleted.")
                    else:
                        print(f"Account with name {account_name} not found.")
                elif admin_choice == "3":
                    admin.list_accounts()
                elif admin_choice == "4":
                    total_balance = admin.total_balance()
                    print(f"Total Available Balance: ${total_balance}")
                elif admin_choice == "5":
                    total_loan_amount = admin.total_loan_amount()
                    print(f"Total Loan Amount: ${total_loan_amount}")
                elif admin_choice == "6":
                    status = input("Enter 'on'/'off' the loan feature: ")
                    admin.onOffLoan(status.lower() == "on")
                elif admin_choice == "7":
                    break
                else:
                    print("Invalid choice.")
        elif choice == "2":
            # User Menu
            while True:
                print("\nUser Menu:")
                print("1. Deposit")
                print("2. Withdraw")
                print("3. Transfer")
                print("4. Take Loan")
                print("5. Transaction History")
                print("6. Main Menu")
                user_choice = input("Enter your choice: ")

                if user_choice == "1":
                    account_name = input("Enter your account name: ")
                    user = None
                    for u in admin.users:
                        if u.name == account_name:
                            user = u
                            break
                    if user:
                        amount = int(input("Enter the amount to deposit: $"))
                        user.deposit(amount)
                        print(f"Deposited ${amount} into {account_name}'s account.")
                    else:
                        print(f"Account with name {account_name} not found.")
                elif user_choice == "2":
                    account_name = input("Enter your account name: ")
                    user = None
                    for u in admin.users:
                        if u.name == account_name:
                            user = u
                            break
                    if user:
                        amount = int(input("Enter the amount to withdraw: $"))
                        user.withdraw(amount)
                    else:
                        print(f"Account with name {account_name} not found.")
                elif user_choice == "3":
                    account_name = input("Enter your account name: ")
                    recipient_name = input("Enter recipient's account name: ")
                    user = None
                    recipient = None
                    for u in admin.users:
                        if u.name == account_name:
                            user = u
                        if u.name == recipient_name:
                            recipient = u
                    if user:
                        amount = int(input("Enter the amount to transfer: $"))
                        user.transfer(recipient, amount)
                    else:
                        print(f"Account with name {account_name} not found.")
                elif user_choice == "4":
                    account_name = input("Enter your account name: ")
                    user = None
                    for u in admin.users:
                        if u.name == account_name:
                            user = u
                            break
                    if user:
                        amount = int(input("Enter the amount to take as a loan: $"))
                        user.take_loan(amount)
                        print(
                            f"Received a loan of ${amount} from {account_name}'s account."
                        )
                    else:
                        print(f"Account with name {account_name} not found.")
                elif user_choice == "5":
                    account_name = input("Enter your account name: ")
                    user = None
                    for u in admin.users:
                        if u.name == account_name:
                            user = u
                            break
                    if user:
                        print(f"Transaction History for {account_name}:")
                        for transaction in user.transaction:
                            print(transaction)
                    else:
                        print(f"Account with name {account_name} not found.")
                elif user_choice == "6":
                    break
                else:
                    print("Invalid choice.")
        elif choice == "3":
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
