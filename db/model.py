

class Manager:
    def __init__(self, chat_id, first_name, last_name=None, phone_number=None, username=None):
        self.chat_id = chat_id
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.username = username

    def __repr__(self):
        return (f"{self.__class__.__name__}(chat_id={self.chat_id}, first_name='{self.first_name}', "
                f"last_name='{self.last_name}', phone_number='{self.phone_number}', username='{self.username}')")


from manager import Manager

class Customer(Manager):
    def __init__(self, chat_id, first_name, last_name=None, phone_number=None, username=None, company=None, address=None):
        super().__init__(chat_id, first_name, last_name, phone_number, username)
        self.company = company
        self.address = address

    def __repr__(self):
        return (f"{super().__repr__()}, company='{self.company}', address='{self.address}'")