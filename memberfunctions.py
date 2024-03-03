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


def remove_member(member_id):
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('members.db')
        cursor = conn.cursor()

        # Check if the member with the given ID exists in the database
        cursor.execute("SELECT * FROM members WHERE id = ?", (member_id,))
        member = cursor.fetchone()
        if member is None:
            print("Member with ID", member_id, "not found.")
            return

        # Delete the member from the database
        cursor.execute("DELETE FROM members WHERE id = ?", (member_id,))
        conn.commit()
        print("Member with ID", member_id, "successfully removed from the database.")

    except sqlite3.Error as e:
        print("Error removing member:", e)

    finally:
        if conn:
            conn.close()


def search_member(last_name):
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('members.db')
        cursor = conn.cursor()

        # Search for members with the given last name
        cursor.execute("SELECT * FROM members WHERE UPPER(last_name) = UPPER(?)", (last_name,))
        members = cursor.fetchall()

        if members:
            print("Members with last name", last_name, "found:")
            for member in members:
                print("ID:", member[0])
                print("First Name:", member[1])
                print("Last Name:", member[2])
                print("Address:", member[3])
                print("City:", member[4])
                print("State:", member[5])
                print("Zipcode:", member[6])
                print("Phone Number:", member[7])
                print("Birthdate:", member[8])
                print("--------------------")
        else:
            print("No members with last name", last_name, "found.")

    except sqlite3.Error as e:
        print("Error searching member:", e)

    finally:
        if conn:
            conn.close()


def edit_member(member_id):
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('members.db')
        cursor = conn.cursor()

        # Check if the member with the given ID exists in the database
        cursor.execute("SELECT * FROM members WHERE id = ?", (member_id,))
        member = cursor.fetchone()
        if member is None:
            print("Member with ID", member_id, "not found.")
            return

        # Display the current member information
        print("Current Member Information:")
        print("ID:", member[0])
        print("First Name:", member[1])
        print("Last Name:", member[2])
        print("Address:", member[3])
        print("City:", member[4])
        print("State:", member[5])
        print("Zipcode:", member[6])
        print("Phone Number:", member[7])
        print("Birthdate:", member[8])

        # Prompt the user to enter the new member information all at once
        print("\nEnter the new member information (leave blank to keep current):")
        new_first_name = input("First Name: ").strip() or member[1]
        new_last_name = input("Last Name: ").strip() or member[2]
        new_address = input("Street Address: ").strip() or member[3]
        new_city = input("City: ").strip() or member[4]
        new_state = input("State: ").strip() or member[5]
        new_zipcode = input("Zipcode: ").strip() or member[6]
        new_phone_number = input("Phone Number: ").strip() or member[7]
        new_birthdate = input("Birthdate (dd/mm/yyyy): ").strip() or member[8]

        # Update the member information in the database
        cursor.execute("UPDATE members SET first_name = ?, last_name = ?, address = ?, city = ?, state = ?, "
                       "zipcode = ?, phone_number = ?, birthdate = ? WHERE id = ?",
                       (new_first_name, new_last_name, new_address, new_city, new_state, new_zipcode,
                        new_phone_number, new_birthdate, member_id))
        conn.commit()
        print("Member with ID", member_id, "successfully updated in the database.")

    except sqlite3.Error as e:
        print("Error editing member:", e)

    finally:
        # Close the database connection
        if conn:
            conn.close()
