class InputContact:
    def __init__(self, phone, identifier):
        self.phone = phone
        self.identifier = identifier


class InputMessage:
    def __init__(self, data: str=None, text: str=None, contact: InputContact=None):
        self.data = data
        self.text = text
        self.contact = contact


