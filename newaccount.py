class Newaccounts:
    def __init__(self,first_name,last_name,account_name,password):
        self.first_name = first_name
        self.last_name = last_name
        self.account_name=account_name
        self.password = password

    user_accounts = []

    def keep_account(self):
        Newaccounts.user_accounts.append(self)

    @classmethod
    def find_by_account_name(cls, account_name):
       
        for account in cls.user_accounts:
            if account.account_name == account_name:
                return account 
    @classmethod
    def check_account(cls, account_name):
        
        for account in cls.user_accounts:
            if account.account_name == account_name:
                return True
        return False

    @classmethod
    def display_accounts(cls):
        return cls.user_accounts           