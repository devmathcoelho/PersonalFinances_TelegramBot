class Category:
    def __init__(self, name: str, value: float, month: int, userId: int):
        self.name = name
        self.value = value
        self.month = month
        self.userId = userId

    def to_dict(self):
        return {
            "name": self.name,
            "value": self.value,
            "month": self.month,
            "userId": self.userId
        }