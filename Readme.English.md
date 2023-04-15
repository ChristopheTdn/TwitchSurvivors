# Twitch Survivors

![Twitch Survivors Logo](TBoT-PZ/TwitchSurvivors/Contents/mods/TwitchSurvivors/logo.png?raw=true)

Click here for [FRENCH VERSION](README.md)

Interaction system between TWITCH and PROJECT ZOMBOID through a game where viewers assume the role of survivors and can help the streamer by performing RAIDs and regrouping to survive as long as possible.

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

 Sur le site [https://twitchtokengenerator.com/](https://twitchtokengenerator.com/)

- generer un bot tchat token
- sélectionner l'ensemble des autorisations  (Bouton select all tout en bas).
- cliquer sur generate token.
- Entrer les informations dans le fichier `Configuration/Secret/config_Token_Client.json` :
- exemple

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

### Integrer les overlays dans OBS :

 Afin de visualiser les commandes et leurs effets, il est necessaire d ajouter 2 overlay à  votre scene OBS.

- TBoT_Overlay/html/chat.html : taille 1000 x 2000, Rafraichissement lorsque le fichier devient actif.
- TBoT_Overlay/html/cars.html : taille 1920 x 200, Rafraichissement lorsque le fichier devient actif.

## Configuration

### sur votre chaine TWITCH :

Ajouter 3 recompenses de point de chaine. Respecter la dénomination :

- "Acheter 300 crédits"
- "Acheter 2000 crédits"
- "Acheter 5000 crédits"

Chaque récompenses doit déduire le nombre correspondant de points de chaine.

### parametrer le fonctionnement du script

- Entrer les informations dans le fichier `Configuration/config.json`
- Dans la pratique, seul le nom du streamer est a fournir à la première ligne

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

## Lancer le programme :

pour lancer le script à la racine du projet :

```
TWITCH SURVIVOR.ps1
```

*clic droit* et *Executer avec powershell*

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
