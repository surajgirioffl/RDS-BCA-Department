"""
    @file: menu.py
    @author: Suraj Kumar Giri
    @init-date: 29th Dec 2022
    @last-modified: 29th Dec 2022
    
    @description:
        * Module to display menu and handle user input.
        
    @functions:
        * displayMenu()
            - To display menu and handle user input after displaying menu.
"""
from time import sleep
from os import system

__author__ = 'Suraj Kumar Giri'
__email__ = 'surajgirioffl@gmail.com'

username = 'rdsbca'


def __ipMenu() -> str:
    """
        Description:
            - To display menu and handle user input after displaying menu
        
        Returns:
            * str:
                - User's choice
    """
    print(
        f"""
        \033[2J;\033[H
        =================== PythonAnyWhere API Menu ===================
        00. To exit.
        01. Change username (selected username is {username}).
        Console:
            02. List all your consoles [GET].
            03. Get information about specific console [GET].
            04. Get latest output from console [GET].
            05. Send input to console [POST].
        CPU:
            06. Get CPU usage information [GET].
        Files:
            07. Get a file [GET].
            08. Upload file to the specified path [POST].
            09. Delete file at the specified path [DELETE].
            10. Start sharing a file [POST].
            11. Check sharing status for a path [GET].
            12. Stop sharing a path [DELETE].
            13. See directory tree [GET].
        Schedule:
            14: List all your schedule tasks [GET].
            15. Create new schedule task [POST].
            16. Get information about schedule task [GET].
            17. Delete a schedule task [DELETE]. 
            18. Endpoint for schedule task [PUT].
            19. Endpoint for schedule task [PATCH].
        Students:
            20. Get list of students [GET].
            21. Delete a student [DELETE].
        WebApp:
            22. List all web apps [GET].
            23. Get information about a web app configuration [GET].
            24. Disable the web app [POST].
            25. Enable the web app [POST].
            26. Reload the web app [POST].
        StaticFiles:
            27. List all static files mapping for domain.
        """
    )

    choice = input("\nWrite your choice: ")
    return choice


def displayMenu() -> tuple[int, str]:
    """
        Description:
            To display menu and handle user input after displaying menu.
        Returns:
            * tuple[int,str]:
                - int: user's choice
                - str: selected username
        
    """
    global username

    while True:
        try:
            choice = int(__ipMenu())
        except Exception as e:
            print(e)
            print("Invalid input. Try again.")
            sleep(1)
            continue
        else:
            if choice not in range(0, 28):
                print("Invalid input. Try again.")
                sleep(1)
                continue

        if choice == 0:
            exit(0)
        elif choice == 1:
            print("""
                  1. rdsbca
                  2. surajgiridev
                  """)
            selection = input("select username: ")
            if selection == '1':
                username = 'rdsbca'
            elif selection == '2':
                username = 'surajgiridev'
            else:
                print("Invalid selection. Try again.")
                sleep(1)
        else:
            return choice, username


if __name__ == '__main__':
    print(displayMenu())
