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
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False


def popularEventTypes(N):
    """For each event type, compute the total number of reserved slots."""
    # TODO: Implement in queries.py
    return []


def participantSchedule(uid):
    """Given a participant ID, list all events for which the participant has reserved a slot."""
    # TODO: Implement in queries.py
    return []


def organizerStats(N):
    """List organizers who have created at least N events."""
    # TODO: Implement in queries.py
    return []


def venueEvents(vid):
    """Given a venue ID, list all events hosted at that venue."""
    # TODO: Implement in queries.py
    return []