class Expense:
    def __init__(self, name: str, value: float, category: str, userId: int, date: str = None):
        self.name = name
        self.value = value
        self.category = category
        self.date = date
        self.userId = userId

    def __str__(self):
        return f"\nName: {self.name} \
                 \nValue: {self.value} \
                 \nCategory: {self.category} \
                 \nDate: {self.date}"
    
    def to_dict(self):
        # convert the expense object to a dictionary to the API
        return {
            "name": self.name,
            "value": self.value,
            "category": self.category,
            "date": self.date,
            "userId": self.userId
        }
