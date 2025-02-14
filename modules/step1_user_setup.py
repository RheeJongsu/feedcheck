# step1_user_setup.py
import os

def create_user(username: str, password: str):
    """
    Creates a system user and sets up their environment.
    
    Args:
        username (str): The name of the user to create.
        password (str): The password for the new user.
    """
    print("Creating User and Setting it up")
    
    try:
        # Create a new user
        os.system(f"useradd -m {username}")
        
        # Add the user to the sudo group
        os.system(f"adduser {username} sudo")
        
        # Set the password for the user
        os.system(f"echo '{username}:{password}' | sudo chpasswd")
        
        # Change the user's default shell to bash
        os.system("sed -i 's/\\/bin\\/sh/\\/bin\\/bash/g' /etc/passwd")
        
        print(f"User '{username}' created and configured successfully!")
    except Exception as e:
        print(f"An error occurred during user setup: {e}")
