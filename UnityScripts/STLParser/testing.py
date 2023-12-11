import sys


if __name__ == "__main__":
    script_name = sys.argv[0]
    arguments = sys.argv[1:]
    if len(arguments) > 1:
        sys.exit(
            "Expect 1 command line argument of type string but received 2")
    path = arguments[0]
    if type(path) == str and path.split('.')[-1] == "json":
        print(True)
