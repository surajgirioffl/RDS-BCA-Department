"""
    @file: drive-direct-download-link.py
    @author: Suraj Kumar Giri
    @init-date: 4th Jan 2023
    @last-modified: 4th Jan 2023

    @description:
        * This script will convert the view link of a files of Google Drive to direct download link.

    @functions:
        * convertToDownloadLink():
            - This function will convert the view link of a files of Google Drive to direct download link.
        * checkLink():
            - This function will check that the link is valid or not means is it a view link of a file of Google Drive or not.
        * pause():
            - This function will pause the execution of the script until user press any key and display a message "Press any key to continue...".
        * menu():
            - This function will display the menu and take input from user and manage all issues related to input. And returns the link and method required in conversion.        
"""

import win32clipboard as clipboard
from sys import platform
from msvcrt import getch

"""
    ** How link looks like **

    * View link of file: https://drive.google.com/file/d/1oRuyF-EKZDV7z8D_REpyLugzf5HPmCee/view?usp=share_link
    * Download link of file:
                    * 1) https://drive.google.com/uc?export=download&id=1oRuyF-EKZDV7z8D_REpyLugzf5HPmCee
                    * 2) https://drive.google.com/uc?id=1oRuyF-EKZDV7z8D_REpyLugzf5HPmCee&export=download
"""


def convertToDownloadLink(viewLink: str, method: int = 1) -> str:
    """
        Description:
            - To convert the view link of a files of Google Drive to direct download link.

        Args:
            * viewLink (str):
                - View link. The link to be converted.
            * method (int, optional): 
                - Method of conversion. (Only two methods are available.)
                - 1 for first method and any other number for second method. (see option 4 of main menu for details).
                - Defaults to 1.

        Returns:
            * str:
                - Direct download link.
    """
    # if method will be 1 then it will use first method otherwise it will use second method.
    if method == 1:
        viewLink = viewLink.removesuffix("/view?usp=share_link")
        viewLink = viewLink.replace("file/d/", "uc?export=download&id=")
        return viewLink

    viewLink = viewLink.replace("file/d/", "uc?id=")
    viewLink = viewLink.replace("/view?usp=share_link", "&export=download")
    return viewLink


def checkLink(link: str) -> bool:
    """
        Description:
            - To check the link is valid or not means is it a view link of a file of Google Drive or not.

        Args:
            * link (str):
                - Link to be checked.

        Returns:
            * True:
                - If link is valid.
            * False:
                - If link is invalid.
    """
    if link.startswith("https://drive.google.com/file/d/") and link.endswith("/view?usp=share_link"):
        return True
    return False


def pause() -> None:
    """
        Description:
            - To pause the execution of the script until user press any key and display a message "Press any key to continue...".
    """
    print("Press any key to continue...", end="")
    getch()
    print()  # for new line


def menu() -> tuple[str, int]:
    """
        Description:
            - To display the menu and take input from user and manage all issues related to input. And returns the link and method required in conversion.

        Returns:
            * tuple[str, int]:
                - str: Link to be converted.
                - int: Method of conversion.
    """

    method = 1
    while True:
        print(f"""
              \033[2J\033[H
    	==============> Generate download link for Google Drive file <==============
    	              1. Copy link from clipboard (Default. Press Enter)
    	              2. Input link manually
    	              3. Change method of link conversion (Default: {method})
    	              4. Details about the methods of link conversion
    	              5. Exit
    	    """)

        choice = input("Enter your choice: ")
        print()
        if choice == "" or choice == "1":
            if platform != "win32":
                print("Warning: This feature is only available on Windows...")
                pause()
                continue
            clipboard.OpenClipboard()
            link = clipboard.GetClipboardData()
            clipboard.CloseClipboard()
            if link == "":
                print("Clipboard is empty...")
                print("Please copy the link and try again or enter link manually...")
                pause()
                continue
            print(f"Fetched link from clipboard: {link}")
            if checkLink(link):
                print("Link is valid...")
                pause()
                return link, method
            print("Invalid link...")
            print("Please copy the link and try again or enter link manually...")
            pause()
            continue  # this is not necessary because the loop will continue anyway because there is no break statement in below executable area. But it is added for better understanding and also control don't need to go to the end of the loop.

        elif choice == "2":
            while True:
                link = input("Enter the link (press @ for main menu): ")
                if link == "":
                    print("Link can't be empty...")
                    pause()
                    continue  # continue to inner loop
                elif link == "@":
                    break  # break from inner loop
                elif checkLink(link):
                    print("Link is valid...")
                    return link, method
                print("Invalid link...")
                pause()
                continue  # continue to inner loop
            continue  # continue to outer loop

        elif choice == "3":
            try:
                method = int(input("Enter the method number: "))
            except Exception as e:
                method = 1
                print(e)
            else:
                print("Method changed successfully...")
            finally:
                pause()
                continue

        elif choice == "4":
            print("""
                  =============> Details about the methods link conversion<===========
                  There are only two methods to convert the view link to download link.
                  See example:
                    * View link of file: 
                        - https://drive.google.com/file/d/1oRuyF-EKZDV7z8D_REpyLugzf5HPmCee/view?usp=share_link
                    * Download link of file:
                        - 1) https://drive.google.com/uc?export=download&id=1oRuyF-EKZDV7z8D_REpyLugzf5HPmCee
                        - 2) https://drive.google.com/uc?id=1oRuyF-EKZDV7z8D_REpyLugzf5HPmCee&export=download
                  
                  Method 1 is default method. If you want to change the method, then enter 3 in main menu.
                  If you select anything other than 1 then method 2 will be used.
                  It is recommended to use method 1 because
                        - file id is one side (right) and other side is the query parameters for download(left).
                        - It is easy to understand.
                        
                  """)
            pause()

        elif choice == "5":
            print("Exited successfully...")
            exit(0)

        else:
            print("Invalid choice...")
            pause()


def main() -> None:
    """
        Description:
            - Main function to execute the script.
            
        Returns: 
            * None
    """
    link, method = menu()
    print("Download Link:", convertToDownloadLink(link, method))


if __name__ == '__main__':
    main()
