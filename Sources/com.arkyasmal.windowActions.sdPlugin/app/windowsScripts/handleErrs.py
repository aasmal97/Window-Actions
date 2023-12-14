import os
dataDirectory = os.environ['APPDATA']
filePath = os.path.join(dataDirectory, r"Elgato\StreamDeck\logs\com.arkyasmal.windowActions.txt")
def err_log(message):
    with open(filePath, "a+") as file:
        file.write(message + "\n")