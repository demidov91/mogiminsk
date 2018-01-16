class InputContact:
    def __init__(self, phone: str, is_user_phone: bool):
        self.phone = phone
        self.is_user_phone = is_user_phone


class InputMessage:
    def __init__(self, data: str=None, text: str=None, contact: InputContact=None):
        self.data = data
        self.text = text
        self.contact = contact
