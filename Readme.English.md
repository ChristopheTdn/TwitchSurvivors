# Twitch Survivors

![Twitch Survivors Logo](TBoT-PZ/TwitchSurvivors/Contents/mods/TwitchSurvivors/logo.png?raw=true)

Click here for [FRENCH VERSION](README.md)

Interaction system between TWITCH and PROJECT ZOMBOID through a game where viewers assume the role of survivors and can help the streamer by performing RAIDs and regrouping to survive as long as possible.

You can read the [game manual](manual/fr/manual_fr.md) (french only at this time) based on the [TancredTerror twitch server](https://www.twitch.tv/tancredterror)

## PRE REQUIS

### subscribe to the Steam mod TWITCH SURVIVORS :

- In Project Zomboid's Steam Workshop subscribe to [TWITCH SURVIVORS](https://steamcommunity.com/sharedfiles/filedetails/?id=2948924574&searchtext=twitch+survivors)

### Install python

- python v3.11  minimum (install via [Microsoft windows store](https://apps.microsoft.com/store/detail/python-311/9NRWMJP3717K) )

### Know your Twitch ID number

- Get your [Twitch ID number](https://streamscharts.com/tools/convert-username)

### Autoriser l'exécution de scripts PowerShell

- Start Windows PowerShell with the "Run as Administrator" option. Only members of the Administrators group on the computer can change the execution policy.
- Enable running unsigned scripts by entering:

```csharp
set-executionpolicy remotesigned
```

```bash
 Set-ExecutionPolicy RemoteSigned
```

- Confirm (press Y)

## Installation

### Get last release :

[Releases · ChristopheTdn/TwitchSurvivors (github.com)](https://github.com/ChristopheTdn/TwitchSurvivors/releases)

### Setting Python virtual environment :

At the root of the project, right click on the file **settingENV.ps1** and Run with powershell

### Get necessary tokens to validate communication between the python script and  TWITCH

 go to the site [https://twitchtokengenerator.com/](https://twitchtokengenerator.com/)

- generate a bot chat token
- select all permissions (Select all button at the bottom).
- Click on Generate Token.
- Put informations in the file `Configuration/Secret/config_Token_Client.json` :
- "USER_ID" is the [Twitch ID number](https://streamscharts.com/tools/convert-username).
- sample :

```json
{
    "USERNAME":"gtof_",
    "TOKEN":"mjklgfdg54fdg524fgdfdg456fd4g415",
    "REFRESH":"fgd6541d23g45632d1fgd63521g3fd2",
    "ID":"gp762nuuoqcoxypju8c569th9wz7q5",
    "USER_ID" : 123456,
    "NICK":"GToF_",
    "PREFIX":"!",
    "CHANNEL":"GToF_"
}
```

### Integrate overlays in OBS :

 In order to visualize the controls and their effects, it is necessary to add 2 overlays to your OBS scene.

- TBoT_Overlay/html/chat.html : size 1000 x 2000, Refresh when the file becomes active.
- TBoT_Overlay/html/cars.html : size 1920 x 200, Refresh when the file becomes active.

## Configuration

### sur votre chaine TWITCH :

Add 3 chain point rewards. Respect the name :

- "Get 300 credits"
- "Get 2000 credits"
- "Get 5000 credits"

Each reward must deduct the corresponding number of chain points.

### Configure how the script works

- Enter information in the file  `Configuration/config.json`

```json
{
    "MOD_STEAM" : true,
    "STEAM_MOD_NAME" : "TwitchSurvivors",
    "STEAM_MOD_ID" : "2948924574",
    "MOD_PATH" : "",
    "DEBUG" : false,
    "TIMING"  : 60,
    "LANGUE" : "french",
    "COUT_REVIVE" : 2000,
    "COUT_MSG_RADIO" : 50,
    "AJOUT_CREDIT" : 5000,
    "TARIF_UPGRADE" : [0,1000,2500,6000,13000],
    "MAX_TIME_RENFORT" : 5,
    "PLAY_SOUND" : true,
    "VOLUME" : 0.5,
    "KILL_THEM_ALL" : true,
    "RESET_PRESTIGE_AFTER_DEATH" : true,
    "ASSISTANT_BOOST" : true,
    "GEAR_BOOST" : 66,
    "MAX_VISI" : 5,
    "TIME_VISI" :5,
    "BASE_READY" : false
}
```

## Launch the program: :

to run the script. At the root of the project:

```
TWITCH SURVIVOR.ps1
```

*right-click* and *Run with powershell*

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[GNU AGPLv3](https://choosealicense.com/licenses/agpl-3.0/)

## Auteurs :

- **TancredTerror** : Concepteur du projet
- **GToF_** : codage
- **Masoht_** : interface Overlay
- **Perralto** : Test et relecture du code

## Contribution :

- **Dane** : relecture/Debuggage LUA.
