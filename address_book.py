from collections import UserDict
from datetime import datetime, timedelta


class AddressBook(UserDict):

    # Adds new record to the address book
    def add_record(self, record):
        self.data[record.name.value] = record

    # Seaches for phone using name
    def find(self, name):
        return self.data.get(name, None)

    # Deletes phone
    def delete(self, name):
        if name in self.data:
            del self.data[name]

    # Check birthdays
    def get_upcoming_birthdays(self):
        today = datetime.now().date()
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday:
                birthday_date = datetime.strptime(record.birthday.value, "%d.%m.%Y").date()
                birthday_this_year = birthday_date.replace(year=today.year)

                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)

                days_until_birthday = (birthday_this_year - today).days

                if 0 <= days_until_birthday <= 7:
                    congratulation_date = birthday_this_year

                    if congratulation_date.weekday() >= 5:  # Saturday or Sunday
                        congratulation_date += timedelta(days=(7 - congratulation_date.weekday()))

                    upcoming_birthdays.append({
                        "name": record.name.value,
                        "congratulation_date": congratulation_date.strftime("%Y.%m.%d")
                    })

        return upcoming_birthdays