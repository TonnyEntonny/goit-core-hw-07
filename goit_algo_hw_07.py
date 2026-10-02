from collections import UserDict
from datetime import datetime, timedelta, date

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    # реалізація класу
		pass

class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Номер телефону повинен містити рівно 10 цифр")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            # Додайте перевірку коректності даних
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
    

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None


    def add_birthday(self, birthday_string):
        self.birthday = Birthday(birthday_string)



    def edit_phone(self, old_phone, new_phone):
        phone_objekt = self.find_phone(old_phone)
        if not phone_objekt:
            raise ValueError(f"Телефон {old_phone} не знайдено")
        new_phone_objekt = Phone(new_phone)
        index = self.phones.index(phone_objekt)
        self.phones[index] = new_phone_objekt


    def add_phone(self, phone_number):
        self.phones.append(Phone(phone_number))

    def remove_phone(self, phone):
        find_objekt = self.find_phone(phone)
        if find_objekt:
            self.phones.remove(find_objekt)


    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):

    def get_upcoming_birthdays(self):
        today = date.today()
        upcoming_birthdays = []
        for record in self.data.values():
            if record.birthday is None:
                continue   

            birthday_this_year = record.birthday.value.replace(year=today.year)
            
            if birthday_this_year.weekday() == 5: 
                birthday_this_year += timedelta(days=2)
            elif birthday_this_year.weekday() == 6:  
                birthday_this_year += timedelta(days=1)

            upcoming_birthdays.append({
                        "name": record.name.value,
                        "congratulation_date": birthday_this_year.strftime("%d.%m.%Y")
                    })
                
        return upcoming_birthdays
            

    def add_record(self, record):
                self.data[record.name.value] = record

    
    def find(self, name):
        return self.data.get(name)


    def delete(self, name):
        if name in self.data: 
            del self.data[name]



def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, IndexError) as e:
            return str(e) or "Give me correct arguments please."
    return inner

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def add_contact(args, contacts):
    name, phone = args
    contacts[name] = phone
    return "Contact added."
def change_contact(args, contacts):
    name, phone = args
    contacts[name] = phone
    return "change_contact"


def show_phone(args, contacts):
    name = args[0]
    return contacts[name]


def show_all(contacts):
    return contacts
        


@input_error
def add_birthday(args, book: AddressBook):
    name, birthday_string, *_ = args
    record = book.find(name)
    if record is None:
        return "Contact not found."
    record.add_birthday(birthday_string)
    return "Birthday added."


@input_error
def show_birthday(args, book):
    name, *_ = args
    record = book.find(name)
    if record is None:
        return "Contact not found."
    if record.birthday is None:
        return "Birthday not set for this contact."
    return record.birthday.value.strftime("%d.%m.%Y")


@input_error
def birthdays(args, book):
    all_birthdays = []
    upcoming_birthdays = book.get_upcoming_birthdays()
    for birt_name in upcoming_birthdays:
        if birt_name is None:
            return "Birthday not set for this contact."
        all_birthdays.append(f"{birt_name['name']}: {birt_name['congratulation_date']}")
    return "\n".join(all_birthdays)




def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")

        
        if not user_input.strip():
            continue
            
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
                     print(show_all(book))
        elif command == "change":
             print(change_contact(args, book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")
        
        
if __name__ == "__main__":
    main()
