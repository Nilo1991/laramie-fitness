import re
import sqlite3
from classes import Member


def create_new_member():
    # Function to create new member and save to db
    def save_to_database(member):
        # Create SQLite connection
        conn = sqlite3.connect('members.db')
        cursor = conn.cursor()

        # Create table if it doesn't exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS members (
                            id INTEGER PRIMARY KEY,
                            first_name TEXT,
                            last_name TEXT,
                            address TEXT,
                            city TEXT,
                            state TEXT,
                            zipcode TEXT,
                            phone_number TEXT,
                            birthdate TEXT
                        )''')
        # Add new member info to db
        cursor.execute('''INSERT INTO members (first_name, last_name, address, city, state, zipcode, phone_number, birthdate)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                       (new_member.first_name, new_member.last_name, new_member.address,
                        new_member.city, new_member.state, new_member.zipcode,
                        new_member.phone_number, new_member.birthdate))
        # Commit & Close
        conn.commit()
        conn.close()


    first_name = input("First Name: ")
    last_name = input("Last Name: ")
    address = input("Street Address: ")
    city = input("City: ")
    state = input("State: ")
    zipcode = input("Zipcode: ")
    phone_number = input("Phone Number: ")
    while True:
        birthdate = input("Birthdate (dd/mm/yyyy): ")
        # validate birthdate format
        if re.match(r'^\d{2}/\d{2}/\d{4}$', birthdate):
            break

        else:
            print("Invalid birthdate. Please use format dd/mm/yyyy.")
    # Create new member instance
    new_member = Member(first_name, last_name, address, city, state, zipcode, phone_number, birthdate)

    # Save new member to db
    save_to_database(new_member)

    print("New member added successfully!")
