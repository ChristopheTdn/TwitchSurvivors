# Twitch Survivors

Click here for [ENGLISH VERSION](Readme.English.md)

systeme d interraction entre TWITCH et PROJECT ZOMBOID au travers d'un jeu ou les viewers assure le role de survivants et peuvent apporter leur aide au streamer en realisant des RAIDs et en se regroupant pour survivre le plus longtemps possible.

## PRE REQUIS

### s'abonner au  mod Steam TWITCH SURVIVORS :
-Dans le Workshop Steam de Project Zomboid s'abonner à [TWITCH SURVIVORS](https://steamcommunity.com/sharedfiles/filedetails/?id=2948924574&searchtext=twitch+survivors)

### Installer python 
- python v3.11  minimum (installation via [Microsoft windows store](https://apps.microsoft.com/store/detail/python-311/9NRWMJP3717K) )

### Connaitre son ID Twitch
- connaitre son [n° identifiant Twitch](https://streamscharts.com/tools/convert-username)

### Autoriser l'exécution de scripts PowerShell
- Cliquer sur le bouton Démarrer, sur Tous les programmes, sur Accessoires, sur Windows PowerShell.
- Cliquer avec le bouton droit de la souris sur Windows PowerShell puis cliquez sur Exécuter en tant qu'administrateur.
- Dans la fenêtre qui s'ouvre, saisissez la commande :
 ```bash
 Set-ExecutionPolicy RemoteSigned
 ```
 - Confirmer en appuyant sur O

## Installation

### Cloner le depot sur votre disque local

### executer le script settingENV.ps1
- A la racine du projet, clique droit sur le fichier settingENV.ps1 et Executer avec powershell
- 
### fournir les tokens necessaires a la communication entre le script et le stream TWITCH
 Sur le site [https://twitchtokengenerator.com/](https://twitchtokengenerator.com/) 
 - generer un bot tchat token
 - selectionner l ensemble des autorisations  (Bouton select all tout en bas).
 - cliquer sur generate token.
 - Entrer les informations dans le fichier config_Token_Client.json :
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
 


## Configuration

```python
import foobar

# returns 'words'
foobar.pluralize('word')

# returns 'geese'
foobar.pluralize('goose')

# returns 'phenomenon'
foobar.singularize('phenomena')
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)





1 - Environnement de developpement : 

 GESTION wingetUI :
    winget install -e --id SomePythonThings.WingetUIStore

- PYTHON 3.11 
- GIT
- GITHUB DESKTOP
- Link Shell Extension

2- connaitre son n° identifiant :
https://streamscharts.com/tools/convert-username

3- Generer un token :
https://twitchtokengenerator.com/ avec tous les droits


pour permettre une utilisation sereine du MODS et un suivi des mises a jours, je vous invite a faire appel aux lien symbolique.

https://www.lecoindunet.com/lien-symbolique-windows-10#Creer_un_lien_symbolique_avec_un_logiciel

Installez le logiciel linkshellextension : https://schinagl.priv.at/nt/hardlinkshellext/linkshellextension.html

Pointez le repertoire 

1- Install environnement PYTHON : 
    En cours de redaction

. pip install -r /path/to/requirements.txt

2- Install MODS PROJECT Zomboid
    En cours de redaction
