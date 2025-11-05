class User:
    def __init__(self, id: int, name: str, userstate: str,
                  Categories: list, Expenses: list, Bills: list, 
                  TotalRevenue: float, TotalExpense: float, TotalBalance: float, CreatedAt: str):
        self.id = id
        self.name = name
        self.userstate = userstate
        self.categories = Categories
        self.expenses = Expenses
        self.Bills = Bills
        self.TotalRevenue = TotalRevenue
        self.TotalExpense = TotalExpense
        self.TotalBalance = TotalBalance
        self.CreatedAt = CreatedAt

    def __str__(self):
        return f"User: {self.name} \
        \nID: {self.id} \
        \nState: {self.userstate} \
        \nBalance: {self.TotalBalance} \
        \nTotal Expenses: {self.TotalExpense} \
        \nTotal Revenue: {self.TotalRevenue} \
        \nCategories: {self.Categories} \
        \nExpenses: {self.Expenses} \
        \nBills: {self.Bills} \
        \nCreated: {self.CreatedAt}"
