# PiSense 

## Sensor multiple à base de raspberry pi
Le but du projet, utiliser une raspberry pi zero et des petit capteurs qui dialoguent en I2C ou SPI pour permettre de faire des capteurs riches en profitant de la discrétion d'une raspberry (notamment une piZeroW).

## Coté hardware
Ce projet a pour but de mettre à disposition des scripts de notification de mesures à un serveur Domoticz.

Ce capteur se compose des capteurs suivants :
* Capteur température/humidité/pression atmosphérique [BME 280
](https://www.amazon.fr/GY-BME280-Pr%C3%A9cision-Num%C3%A9rique-Barom%C3%A9trique-Temp%C3%A9rature/dp/B0799FH5PG/ref=sr_1_3?adgrpid=61886146291&gclid=CjwKCAjw8qjnBRA-EiwAaNvhwDATlijXdqymDr0VeDMKIAiONZ3i_0DGXfpgGNqr5Itiktv3yCTCChoCVVQQAvD_BwE&hvadid=275352305011&hvdev=c&hvlocphy=9055562&hvnetw=g&hvpos=1t1&hvqmt=e&hvrand=6352208228668978622&hvtargid=kwd-366977058887&hydadcr=7434_1743189&keywords=bme280&qid=1558873450&s=gateway&sr=8-3-spell)
* Capteur d'intensité lumineuse [TSL2561](https://www.amazon.fr/gp/product/B06XGWVW31/)
* Capteur de mouvement [HR-SC501
](https://www.amazon.fr/gp/product/B00Q6OJ8AC/)
* Capteur distance metreà ultrason [HC-SR04](https://www.amazon.fr/gp/product/B06XSJPVW9/)
*  Capteur d'ouverture de porte ou fenêtre  [Contact Magnétique
](https://www.amazon.fr/gp/product/B07HH658CQ/)  [ A venir ]

## Les scripts
Dans sa première version, 2 scripts sont utilisés :
Un script Python qui se lance en tache de fond et envoie les notifications à la centrale domoticz pour les capteur PIR et ultrason.
*TODO :* ajouter les capteurs d'ouverture de porte / fenêtres. 

Un script python lancé en crontab qui met à jour la centrale domotique régulièrement (fréquence de mise à jour en fonction de la conf crontab)  
pour les capteurs température humidité pression luminosité.


## Dépendances 
Utilisation des dépendances python  :
* RPi.GPIO
* smbus
* numpy
* HTTPBasicAuth

