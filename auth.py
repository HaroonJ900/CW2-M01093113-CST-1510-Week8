import bcrypt
import os 
USER_DATA_FILE = "users.txt"

with open(USER_DATA_FILE , 'a') as file:
    pass
def hash_password(plain_text_password):
    password_bytes = plain_text_password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password.decode("utf-8")

def verify_password(plain_text_password, hashed_password):
    check_password = bcrypt.checkpw(plain_text_password.encode("utf-8"), hashed_password.encode("utf-8"))
    return check_password

def register_user(username, password):
    with open(USER_DATA_FILE,"r") as file:
        for line in file:
            existing_username = line.strip().split(',')[0]
            if existing_username == username:
                print("Username already exists")
                return False   

    
    hashed_password = hash_password(password)

    with open(USER_DATA_FILE, "w") as file:
        file.write(f'{username},{hashed_password}\n')  
    print("User registered successfully!")


def user_exist(username): 
    with open(USER_DATA_FILE) as file:
        for line in file:
            username_file = line.strip().split(",")[0]
            if username_file == username:
                return True
        else:
            return False
def login_user(username, password):
        with open(USER_DATA_FILE) as file:
            for line in file:
                username_file = line.strip().split(",")[0]
                password_file = line.strip().split(",")[1]
                if username_file == username:
                    if verify_password(password, password_file):
                        print("login successful")
                    else:
                        print("incorrect password")
                else:
                    print("username was ghghjggkgjnot found")
        
        

def validate_username(username):
    if len(username) >= 4 and username.isalnum():
        return (True,"")
    else:
        return(False,"Username must be atleast 4 characters long and must only contain alphabet and numbers ")

def validate_password(password):
    if len(password) < 8:
        return (False, "Password must be at least 8 characters long.")
    if not any(c.isupper() for c in password):
        return (False, "Password must contain at least one uppercase letter.")
    if not any(c.islower() for c in password):
        return (False, "Password must contain at least one lowercase letter.")
    if not any(c.isdigit() for c in password):
        return (False, "Password must contain at least one number.")
    return (True, "")



def display_menu():
    """Displays the main menu options."""
    print("\n" + "=" * 50)
    print(" MULTI-DOMAIN INTELLIGENCE PLATFORM")
    print(" Secure Authentication System")
    print("=" * 50)
    print("\n[1] Register a new user")
    print("[2] Login")
    print("[3] Exit")
    print("-" * 50)


def main():
    """Main program loop."""
    print("\nWelcome to the Week 7 Authentication System!")
    while True:
        display_menu()
        choice = input("\nPlease select an option (1-3): ").strip()

        if choice == '1':
            # Registration flow
            print("\n--- USER REGISTRATION ---")
            username = input("Enter a username: ").strip()

            # Validate username
            is_valid, error_msg = validate_username(username)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue

            password = input("Enter a password: ").strip()

            # Validate password
            is_valid, error_msg = validate_password(password)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue

            # Confirm password
            password_confirm = input("Confirm password: ").strip()
            if password != password_confirm:
                print("Error: Passwords do not match.")
                continue

            # Register the user
            register_user(username, password)

        elif choice == '2':
            # Login flow
            print("\n--- USER LOGIN ---")
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()

            # Attempt login
            if login_user(username, password):
                print("\nYou are now logged in.")
                print("(In a real application, you would now access the domain dashboard.)")

                # Optional: Ask if they want to logout or exit
                input("\nPress Enter to return to main menu...")

        elif choice == '3':
            # Exit
            print("\nThank you for using the authentication system.")
            print("Exiting...")
            break

        else:
            print("\nError: Invalid option. Please select 1, 2, or 3.")


if __name__ == "__main__":
    main()
