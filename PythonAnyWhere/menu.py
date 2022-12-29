"""
    @file: credentials.py
    @author: Suraj Kumar Giri
    @init-date: 29th Dec 2022
    @last-modified: 29th Dec 2022
    
    @description:
        * Module to display menu and handle user input.
        
    @functions:
        * 
"""

__author__ = 'Suraj Kumar Giri'
__email__ = 'surajgirioffl@gmail.com'

username = 'rdsbca'


def __ipMenu():
    print(
        """
        \033[2J\033[H
        01. Change username (default is rdsbca).
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


if __name__ == '__main__':
    __ipMenu()
