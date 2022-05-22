from werkzeug.security import generate_password_hash
from getpass import getpass

def main():
    print("This tool will create a hash for the emergency key for a system enviroment")
    passw = getpass("Password: ")
    print(generate_password_hash(passw))

if __name__ == "__main__":
    main()