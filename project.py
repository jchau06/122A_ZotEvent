import sys
from import_data import import_func
from user_operations import insertAdmin, deleteOrganizer
from event_operations import addVenue, updateEvent
from slot_operations import cancelReservation, reserveSlot
from queries import availableEvents, popularEventTypes, participantSchedule, organizerStats, venueEvents

# entry point - parses through CLI arguments and routes to functions
# Expected format: python3 project.py <function_name> [param1] [param2] ...
def main():
    # check if function name was provided
    if len(sys.argv) < 2:
        print("Error: No function name provided")
        return
    
    func_name = sys.argv[1]
    args = sys.argv[2:]
    
    result = None
    
    try:
        
        if func_name == "import":
            # python3 project.py import [folderName]
            result = import_func(args[0])

        elif func_name == "insertAdmin":
            #python3 project.py insertAdmin [uid] [email] [username] [joined] [firstname] [lastname]
            result = insertAdmin(int(args[0]), args[1], args[2], args[3], args[4], args[5])

        elif func_name == "deleteOrganizer":
            #python3 project.py deleteOrganizer [uid:int]
            result = deleteOrganizer(int(args[0]))

        elif func_name == "reserveSlot":
            #python3 project.py reserveSlot [eid:int] [snum:int] [uid:int]
            result = reserveSlot(int(args[0]), int(args[1]), int(args[2]))

        elif func_name == "cancelReservation":
            #python3 project.py cancelReservation [eid] [snum] [uid]
            result = cancelReservation(int(args[0]), int(args[1]), int(args[2]))

        elif func_name == "addVenue":
            result = addVenue(int(args[0]), int(args[1]), args[2].lower() == 'true')
        
        elif func_name == "updateEvent":
            result = updateEvent(int(args[0]), args[1], args[2])
        
        elif func_name == "availableEvents":
            #python3 project.py availableEvents [date:date]
            result = availableEvents(args[0])
        
        elif func_name == "popularEventTypes":
            #python3 project.py popularEventTypes [N:int]
            result = popularEventTypes(int(args[0]))

        # branches for other functions need to be added. 
        else:
            print(f"Error: Unknown function '{func_name}'")
            return
        
        # format and print results
        if result is None:
            return
        
        elif isinstance(result, bool):
            # boolean result - print "Success" or "Fail"
            print("Success" if result else "Fail")
        
        else:
            # Table result - print as comma-separated values
            # result should be a list of tuples
            for row in result:
                # Convert all values to strings and join with commas
                print(",".join(str(value) for value in row))
    
    except IndexError:
        print(f"Error: Missing required arguments for function '{func_name}'")
    except ValueError as e:
        print(f"Error: Invalid argument type - {e}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()