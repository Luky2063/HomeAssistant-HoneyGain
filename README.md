# HomeAssistant-HoneyGain

Installation :
Ajouter les fichiers dans \config\custom_components\apiHoneyGain
Redémarrer HomeAssistant
Ajouter dans le fichier de configuration.yaml :
  - platform: apiHoneyGain
    token: !secret honeygain_token
    scan_interval: 120
Le Token se trouve à la connexion sur le dashboard HoneyGain (Voir les outils développeur)

Basé sur https://pypi.org/project/pyHoneygain/ pour l'API HoneyGain et sur https://github.com/saniho/apiEarnApp pour la structure du programme.
