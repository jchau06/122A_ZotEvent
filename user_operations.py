from database import get_connection

def insertAdmin(uid, email, username, joined, firstname, lastname):
    """Insert a new user and administrator into the related tables."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        #changes id to int for inserting
        new_uid = int(uid)
        #sql statements to actually insert
        cursor.execute("INSERT INTO User(uid, email, username, joined)" \
                        " VALUES (%s,%s,%s,%s)", (new_uid, email, username, joined))
        
        cursor.execute("INSERT INTO Administrator(uid, firstname, lastname)" \
                        " VALUES (%s,%s,%s)", (new_uid, firstname, lastname))
        conn.commit()

        cursor.close()
        conn.close()
        return True
    except Exception:
        return False


def deleteOrganizer(uid):
    """Delete an organizer from the database."""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM Organizer WHERE uid = %s", (uid,))
        conn.commit()

        cursor.close()
        conn.close()
        return True
    except Exception:
        return False