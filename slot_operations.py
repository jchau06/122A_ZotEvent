from database import get_connection

def cancelReservation(eid, snum, uid):
    """Cancel a participant's reservation for a specific event slot."""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("UPDATE Slot SET is_reserved = FALSE, uid = NULL "
                       "WHERE eid = %s AND snum= %s AND uid = %s AND is_reserved = TRUE",
                        (eid, snum, uid))

        conn.commit()
        success = cursor.rowcount > 0
        cursor.close()
        conn.close()
        return success
        
    except Exception:
        return False


def reserveSlot(eid, snum, uid):
    """Reserve a specific slot for a participant."""
    # TODO: Implement in slot_operations.py
    try:
        conn = get_connection()
        cursor = conn.cursor()
        #sql statements to actually insert into slots table
        cursor.execute("UPDATE Slot SET is_reserved = TRUE, uid = %s "
                       "WHERE eid = %s AND snum = %s AND is_reserved = FALSE",
                        (uid, eid, snum))
        conn.commit()
        if cursor.rowcount == 0:
            cursor.close()
            conn.close()
            return False
        cursor.close()
        conn.close()
        return True
    except Exception:
        return False