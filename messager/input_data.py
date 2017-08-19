class Contact:
    def __init__(self, phone, identifier):
        self.phone = phone
        self.identifier = identifier


class Message:
    def __init__(self, data: str=None, text: str=None, contact: Contact=None):
        self.data = data
        self.text = text
        self.contact = contact


