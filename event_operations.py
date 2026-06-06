from database import get_connection

def addVenue(eid, vid, is_primary):
    """Add a venue to an existing event by inserting it into the Hosting relationship."""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        if is_primary is True:
            # run query to see if another primary venue exists 
            cursor.execute(
                "SELECT COUNT(*) FROM Hosting WHERE eid = %s AND is_primary = TRUE",
                (eid,))
            result = cursor.fetchone()  # fetch if there are any results
            count = result[0]

            if count > 0:
                # return False if there exists another primary venue with the same eid
                return False
        cursor.execute("INSERT INTO Hosting (eid, vid, is_primary) VALUES (%s,%s,%s)", (eid, vid, is_primary))
        conn.commit()
        return True

    except Exception:
        return False
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


def updateEvent(eid, title, datetime):
    """Update the title and the datetime of an event."""
    # TODO: Implement in event_operations.py
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
                "UPDATE Event SET title = %s, datetime = %s WHERE eid = %s",
                (title, datetime, eid))
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
