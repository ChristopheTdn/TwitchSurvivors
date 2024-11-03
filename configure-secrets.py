import json

def ask(msg, type = str):
    while True:
        try:
            return type(input(f"{msg}: "))
        except ValueError:
            print("Wrong type")
            pass

new_config = {
    "USERNAME": ask("Username"),
    "TOKEN": ask("Access token"),
    "REFRESH": ask("Refresh token"),
    "ID": ask("Client ID"),
    "USER_ID": ask("User ID", int),
    "NICK": ask("Nickname"),
    "PREFIX": ask("Prefix"),
    "CHANNEL": ask("Channel"),
}

with open("./Configuration/Secret/config_Token_Client.json", "w") as file:
    file.write(json.dumps(new_config, indent=4))

print("New secret configuration written successfully")
