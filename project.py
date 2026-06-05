import sys
from import_data import import_func
from user_operations import *

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
            result = insertAdmin(args[0], args[1], args[2], args[3], args[4], args[5]);
            
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