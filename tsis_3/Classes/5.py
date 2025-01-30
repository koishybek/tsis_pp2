class Account:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance
    def deposit(self, amount):
        self.balance += amount
        print("Deposit of", amount, "accepted. New balance:", self.balance)
    def withdraw(self, amount):
        if amount > self.balance:
            print("Funds Unavailable!")
        else:
            self.balance -= amount
            print("Withdrawal of", amount, "accepted. New balance:", self.balance)
account = Account("Olzhas", 100)
print(account.owner)
print(account.balance)
account.deposit(50)
account.deposit(25)
account.withdraw(60)
account.withdraw(200)
print(account.balance)
