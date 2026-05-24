import csv
import os
from database import get_connection


def import_func(folder_name):
    conn = get_connection()
    cursor = conn.cursor()

    # Delete in reverse order of foreign key dependencies
    try:
        delete_statements = [
            "DELETE FROM Approval",
            "DELETE FROM Hosting",
            "DELETE FROM Slot",
            "DELETE FROM OffCampus",
            "DELETE FROM OnCampus",
            "DELETE FROM Event",
            "DELETE FROM Administrator",
            "DELETE FROM Participant",
            "DELETE FROM Organizer",
            "DELETE FROM User",
            "DELETE FROM Venue",
        ]

        for statement in delete_statements:
            cursor.execute(statement)
        conn.commit()

        # define CSV file mappings and table insert statements:
        csv_configs = {
            "User.csv": {
                "table": "User",
                "columns": ["uid", "email", "username", "joined"],
                "insert_sql": "INSERT INTO User (uid, email, username, joined) VALUES (%s, %s, %s, %s)",
            },
            "Organizer.csv": {
                "table": "Organizer",
                "columns": ["uid", "department", "experience"],
                "insert_sql": "INSERT INTO Organizer (uid, department, experience) VALUES (%s, %s, %s)",
            },
            "Participant.csv": {
                "table": "Participant",
                "columns": ["uid", "type"],
                "insert_sql": "INSERT INTO Participant (uid, type) VALUES (%s, %s)",
            },
            "Administrator.csv": {
                "table": "Administrator",
                "columns": ["uid", "firstname", "lastname"],
                "insert_sql": "INSERT INTO Administrator (uid, firstname, lastname) VALUES (%s, %s, %s)",
            },
            "Event.csv": {
                "table": "Event",
                "columns": ["eid", "creator_uid", "title", "type", "datetime"],
                "insert_sql": "INSERT INTO Event (eid, creator_uid, title, type, datetime) VALUES (%s, %s, %s, %s, %s)",
            },
            "Slot.csv": {
                "table": "Slot",
                "columns": ["eid", "snum", "is_reserved", "uid"],
                "insert_sql": "INSERT INTO Slot (eid, snum, is_reserved, uid) VALUES (%s, %s, %s, %s)",
            },
            "Venue.csv": {
                "table": "Venue",
                "columns": ["vid", "street", "city", "state", "zip"],
                "insert_sql": "INSERT INTO Venue (vid, street, city, state, zip) VALUES (%s, %s, %s, %s, %s)",
            },
            "OnCampus.csv": {
                "table": "OnCampus",
                "columns": ["vid", "code"],
                "insert_sql": "INSERT INTO OnCampus (vid, code) VALUES (%s, %s)",
            },
            "OffCampus.csv": {
                "table": "OffCampus",
                "columns": ["vid", "distance"],
                "insert_sql": "INSERT INTO OffCampus (vid, distance) VALUES (%s, %s)",
            },
            "Hosting.csv": {
                "table": "Hosting",
                "columns": ["eid", "vid", "is_primary"],
                "insert_sql": "INSERT INTO Hosting (eid, vid, is_primary) VALUES (%s, %s, %s)",
            },
            "Approval.csv": {
                "table": "Approval",
                "columns": ["uid", "vid", "valid_from", "valid_until"],
                "insert_sql": "INSERT INTO Approval (uid, vid, valid_from, valid_until) VALUES (%s, %s, %s, %s)",
            },
        }

        # Read each CSV file and insert data
        for csv_file, config in csv_configs.items():
            file_path = os.path.join(folder_name, csv_file)

            # check if the file exists
            if not os.path.exists(file_path):
                print(f"Warning: {csv_file} not found in {folder_name}")
                continue

            # Read CSV and insert rows
            with open(file_path, "r") as f:
                csv_reader = csv.reader(f)
                for row in csv_reader:
                    # skip empty rows
                    if not row or all(cell.strip() == "" for cell in row):
                        continue

                    # convert values as needed
                    converted_row = []
                    for i, cell in enumerate(row):
                        cell = cell.strip()

                        # handle NULL values
                        if cell.upper() == "NULL" or cell == "":
                            converted_row.append(None)
                        # convert boolean values
                        elif cell.lower() in ["true", "false"]:
                            converted_row.append(cell.lower() == "true")
                        # convert integer values (for uid, eid, vid, snum, experience, distance)
                        elif config["columns"][i] in [
                            "uid",
                            "eid",
                            "vid",
                            "snum",
                            "experience",
                            "distance",
                        ]:
                            try:
                                converted_row.append(int(cell))
                            except ValueError:
                                converted_row.append(cell)
                        else:
                            converted_row.append(cell)

                    # insert row into database
                    cursor.execute(config["insert_sql"], converted_row)
            conn.commit()

        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error during import: {e}")
        cursor.close()
        conn.close()
        return False
