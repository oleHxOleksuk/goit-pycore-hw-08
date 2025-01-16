from record import Record
from address_book import AddressBook
import re
from colorama import Back, Fore, Style

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except KeyError as e:
            return Fore.RED + f"Contact {e} not found." + Style.RESET_ALL
        except IndexError:
            return Fore.RED + "Invalid number of arguments." + Style.RESET_ALL
        except Exception as e:
            return Fore.RED + f"An error occurred: {e}" + Style.RESET_ALL
    return inner

@input_error
def add_contact(args, book):
    if len(args) != 2:
        raise ValueError(Fore.RED + "Give me name and phone please." + Style.RESET_ALL)
    name, phone = args
    record = book.find(name)
    if record:
        record.add_phone(phone)
        return Fore.GREEN + "Phone added." + Style.RESET_ALL
    else:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
        return Fore.GREEN + "Contact added." + Style.RESET_ALL

@input_error
def change_contact(args, book):
    if len(args) != 3:
        raise ValueError(Fore.RED + "Give me name, old phone and new phone please." + Style.RESET_ALL)
    name, old_phone, new_phone = args
    record = book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return Fore.GREEN + "Phone updated." + Style.RESET_ALL
    else:
        raise Fore.RED + KeyError(name) + Style.RESET_ALL

@input_error
def show_phone(args, book):
    if len(args) != 1:
        raise ValueError(Fore.RED + "Enter user name" + Style.RESET_ALL)
    name = args[0]
    record = book.find(name)
    if record:
        return '; '.join(phone.value for phone in record.phones)
    else:
        raise Fore.RED + KeyError(name) + Style.RESET_ALL

@input_error
def show_all(book):
    return '\n'.join(str(record) for record in book.values())

@input_error
def add_birthday(args, book):
    if len(args) != 2:
        raise ValueError(Fore.RED + "Give me name and birthday please." + Style.RESET_ALL)
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return Fore.GREEN + "Birthday added." + Style.RESET_ALL
    else:
        raise Fore.RED + KeyError(name) + Style.RESET_ALL

@input_error
def show_birthday(args, book):
    if len(args) != 1:
        raise ValueError(Fore.RED + "Enter user name" + Style.RESET_ALL) 
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        return f"{name}'s birthday: {record.birthday.value}"
    elif record:
        return f"{name} has no birthday set."
    else:
        raise Fore.RED + KeyError(name) + Style.RESET_ALL

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
    print(Fore.GREEN + "Welcome to the assistant bot!" + Style.RESET_ALL)
    while True:
        user_input = input(Back.BLUE + "Enter a command: " + Style.RESET_ALL)
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print(Fore.YELLOW + "Good bye!" + Style.RESET_ALL)
            break
        elif command == "hello":
            print(Fore.YELLOW + "How can I help you?" + Style.RESET_ALL)
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
            print(Fore.RED + "Invalid command." + Style.RESET_ALL)

if __name__ == "__main__":
    main()