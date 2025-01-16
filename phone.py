from field import Field

class Phone(Field):
    def __init__(self, value):
        if not self.validate(value):
            raise ValueError("Invalid phone number format. Should start from 0 and be 10 digits")
        super().__init__(value)

    def validate(self, value):
        # Validating phone number and raising exception if number is not 10 digits
        return len(value) == 10 and value.isdigit() 