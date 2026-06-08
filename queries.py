from database import get_connection

def availableEvents(date):
    """List all future events that still have at least one unreserved slot."""
    # TODO: Implement in queries.py
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT e.eid, e.title, e.type, e.datetime, COUNT(*) AS avaliableSlots "
                       "FROM Event e "
                       "INNER JOIN Slot s on e.eid = s.eid "
                       "WHERE s.is_reserved = FALSE "
                       "AND e.datetime > %s "
                       "GROUP BY e.eid "
                       "ORDER BY e.datetime ASC, e.eid ASC ",
                       (date,))
        for eid, title, type, datetime, availiable in cursor.fetchall():
            print(f"{eid},{title},{type},{datetime},{availiable}")
        cursor.close()
        conn.close()
        #TODO: subject to removal bc idk if we need to return the boolean
        return True
    except Exception as e:
        print(f"Error: {e}")
        #TODO: subject to removal bc idk if we need to return the boolean
        return False


def popularEventTypes(N):
    """For each event type, compute the total number of reserved slots."""
    # TODO: Implement in queries.py
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT e.type, COUNT(*) AS reservedCount "
                       "FROM Event e "
                       "INNER JOIN Slot s on e.eid = s.eid "
                       "WHERE s.is_reserved = TRUE "
                       "GROUP BY e.type "
                       "HAVING COUNT(*) >= %s "
                       "ORDER BY reservedCount DESC, e.type ASC",
                       (int(N),))
        for type, reservedCount in cursor.fetchall():
            print(f"{type},{reservedCount}")
        cursor.close()
        conn.close()
        #TODO: subject to removal bc idk if we need to return the boolean
        return True
    except Exception as e:
        print(f"Error: {e}")
        #TODO: subject to removal bc idk if we need to return the boolean
        return False


def participantSchedule(uid):
    """Given a participant ID, list all events for which the participant has reserved a slot."""
    # TODO: Implement in queries.py
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                e.eid,
                e.title,
                e.type,
                e.datetime,
                s.snum,
                v.vid,
                v.street,
                v.city,
                v.state,
                v.zip
            FROM Slot s
            JOIN Event e ON s.eid = e.eid
            LEFT JOIN Hosting h 
                ON e.eid = h.eid AND h.is_primary = TRUE
            LEFT JOIN Venue v 
                ON h.vid = v.vid
            WHERE s.uid = %s
              AND s.is_reserved = TRUE
            ORDER BY e.datetime ASC
        """, (int(uid),))

        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return rows

    except Exception:
        return []


def organizerStats(N):
    """List organizers who have created at least N events."""
    # TODO: Implement in queries.py
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                o.uid,
                u.username,
                o.department,
                COUNT(e.eid) AS eventCount
            FROM Organizer o
            JOIN User u ON o.uid = u.uid
            JOIN Event e ON o.uid = e.creator_uid
            GROUP BY o.uid, u.username, o.department
            HAVING COUNT(e.eid) >= %s
            ORDER BY eventCount DESC, o.uid ASC
        """, (int(N),))

        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return rows

    except Exception:
        return []


def venueEvents(vid):
    """Given a venue ID, list all events hosted at that venue."""
    # TODO: Implement in queries.py
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                e.eid,
                e.title,
                e.type,
                e.datetime,
                h.is_primary
            FROM Hosting h
            JOIN Event e ON h.eid = e.eid
            WHERE h.vid = %s
            ORDER BY e.datetime ASC, e.eid ASC
        """, (int(vid),))

        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return rows

    except Exception:
        return []

