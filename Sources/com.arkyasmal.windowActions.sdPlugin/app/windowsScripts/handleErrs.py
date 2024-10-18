import os
dataDirectory = os.environ['APPDATA']
filePath = os.path.join(dataDirectory, r"Elgato\StreamDeck\logs\com.arkyasmal.windowActions\error.txt")
# def err_log(message):
#     with open(filePath, "a+") as file:
#         file.write(message + "\n")
def write_to_file(message):
     with open(filePath, "a+") as file:
            file.write(message + "\n")
def err_log(message):
    try:
        write_to_file(message)
    except FileNotFoundError as e:
        create_file_with_directories(filePath)
        write_to_file(message)

def create_file_with_directories(path):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        file = open(path, "w")
        file.close()
    except Exception as e:
        print(str(e))
