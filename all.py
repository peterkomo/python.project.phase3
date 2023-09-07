from newaccount import Newaccounts
from password import Password

def create_account(first_name, last_name, account_name, password):
    accounts = Newaccounts(first_name, last_name, account_name, password)
    return accounts
def save_account(accounts):
    accounts.save_account()
def find_accounts(account_name):
    return Newaccounts.find_by_user_name(account_name)
def isexist_accounts(account_name):
    return Newaccounts.account_exists(account_name)
def display_accounts():
    return Newaccounts.display_accounts()
def create_page(page, password):
    passwords = Password(page, password)
    return passwords
def save_page(passwords):
    passwords.save_page()
def find_page(pager):
    return Password.find_by_page(pager)
def isexist_page(pager):
    return Password.page_exists(pager)
def display_pages():
    return Password.display_page()
def main():
    print("WELCOME TO UNCLE PETE'S GROSSARY SHOP")
    print('HEY CONTIUE WALKING WITH US, PICK ACCORDING TO YOUR')
    while True:

        print(" 1) LOGIN \n 2) SIGN UP \n  4) DISPLAY ACCOUNTS \n 5) SIGN OUT")
        choice = int(input())
        if choice == 1:
            print('Enter Account name')
            username = input()
            print('Enter passoword')
            password = input()
            account = find_accounts(username)
            if account.account_name == username and account.password == password:
                print('logged in ')
                while True:
                       print(
                        f'Welcome {username}, Use the following numbers to select their relating ideas')

                       print(
                        ' 1) Save new password \n  2) Display saved passwords \n 3) Log out ')
                       log_choice = int(input())
                if log_choice == 1:
                    print('New page')
                    print('*'*100)

                    print('Page name')
                    page = input()

                    print('password')
                    password = input()

                    # created and saved page
                    save_page(create_page(page, password))
if __name__ == '__main__':
    main()