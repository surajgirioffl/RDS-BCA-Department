
def menu() -> int:
    print("""
          Basics:
                01. Write content and upload in a file (Press anything except 2).
          Advanced:
                02. Upload an existing file from local directory.
          """)
    choice = input("Write your choice: ")
    if choice == "2":
        return 2
    return 1


def userInputUpload() -> dict:
    fileName = input(
        "Enter the file name with extension that will be created or updated in PythonAnywhere: ")
    content = input("Enter the content that will be written in the file: ")
    return {"fileName": fileName, "content": content}
