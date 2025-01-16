from record import Record
from address_book import AddressBook
import re

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except KeyError as e:
            return f"Contact {e} not found."
        except IndexError:
            return "Invalid number of arguments."
        except Exception as e:
            return f"An error occurred: {e}"
    return inner

@input_error
def add_contact(args, book):
    if len(args) != 2:
        raise ValueError("Give me name and phone please.")
    name, phone = args
    record = book.find(name)
    if record:
        record.add_phone(phone)
        return "Phone added."
    else:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
        return "Contact added."

@input_error
def change_contact(args, book):
    if len(args) != 3:
        raise ValueError("Give me name, old phone and new phone please.")
    name, old_phone, new_phone = args
    record = book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return "Phone updated."
    else:
        raise KeyError(name)

@input_error
def show_phone(args, book):
    if len(args) != 1:
        raise ValueError("Enter user name")
    name = args[0]
    record = book.find(name)
    if record:
        return '; '.join(phone.value for phone in record.phones)
    else:
        raise KeyError(name)

@input_error
def show_all(book):
    return '\n'.join(str(record) for record in book.values())

@input_error
def add_birthday(args, book):
    if len(args) != 2:
        raise ValueError("Give me name and birthday please.")
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return "Birthday added."
    else:
        raise KeyError(name)

@input_error
def show_birthday(args, book):
    if len(args) != 1:
        raise ValueError("Enter user name")
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        return f"{name}'s birthday: {record.birthday.value}"
    elif record:
        return f"{name} has no birthday set."
    else:
        raise KeyError(name)

@input_error
def birthdays(book):
    upcoming = book.get_upcoming_birthdays()
    if upcoming:
        return '\n'.join(f"{b['name']}: {b['congratulation_date']}" for b in upcoming)
    else:
        return "No upcoming birthdays in the next week."

def parse_input(user_input):
    cmd, *args = re.findall(r'\S+', user_input)
    cmd = cmd.strip().lower()
    return cmd, args

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(book))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()