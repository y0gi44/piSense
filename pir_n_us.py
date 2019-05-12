#!/usr/bin/env python
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time
from time import gmtime, strftime
#capteur luxmetre
import numpy as np
import requests
from requests.auth import HTTPBasicAuth

import piSenseConfig as cfg


dz_host = cfg.domoticzHost['host']
dz_port = cfg.domoticzHost['port']
dz_user = cfg.domoticzHost['user']
dz_pass = cfg.domoticzHost['pass']

idx_pir   = cfg.dzDevices['pir']
idx_dist  = cfg.dzDevices['dist']

last_dist = 0
last_lux  = 0

# récupération de l'information data du capteur
def getDzDeviceInfo(idx):
    url = 'http://'+dz_host+':'+dz_port+'/json.htm?type=devices&rid='+str(idx)
    r = requests.get(url, auth=HTTPBasicAuth(dz_user, dz_pass))
    jsonOut = json.loads(r.text)
    #print 'Data field = '+jsonOut['result'][0]['Data']
    return jsonOut['result'][0]['Data']

def updateSensor(idx, value):
    url = 'http://'+dz_host+':'+dz_port+'/json.htm'
    payload = {'type': 'command',
               'param': 'udevice',
               'idx': str(idx),
               'nvalue': '0',
               'svalue' : value
               }
    r = requests.get(url, auth=HTTPBasicAuth(dz_user, dz_pass), params=payload)
    #print 'output : '+r.text

def updateSensorIfChangedDelta(idx, value, last_value, delta):
    new='{0:0.2f}'.format(value)
    old='{0:0.2f}'.format(last_value)
    #if (new != old):
    if (abs(last_value-value) > delta ):
      updateSensor(idx, value)
      log("DZ update idx {} lastvalue({})  newValue({}) ecart({}) consigne({})".format(idx, old, new, abs(last_value-value) , delta))


def updateSensorIfChanged(idx, value, last_value):
    new='{0:0.2f}'.format(value)
    old='{0:0.2f}'.format(last_value)
    if (new != old):
      updateSensor(idx, value)
      log("DZ update idx {} lastvalue({})  newValue({})".format(idx, old, new))

def updateSensorIfChangedSuf(idx, value, last_value, suffixe):
    new="%.2f" % value
    old="%.2f" % last_value
    if (new != old):
      updateSensor(idx, str(value)+suffixe)
      log("DZ update idx {} lastvalue({})  newValue({})".format(idx, last_value, value))


def updateMotionSensor(idx):
    url = 'http://'+dz_host+':'+dz_port+'/json.htm'
    payload = {'type': 'command',
               'param': 'switchlight',
               'idx': str(idx),
               'switchcmd': 'On'
               }
    r = requests.get(url, auth=HTTPBasicAuth(dz_user, dz_pass), params=payload)
    #print 'output : '+r.text




def log(message):
  print (strftime("%a, %d %b %Y %H:%M:%S ", time.localtime())+ message)

## callback pour la gestion du détecteur de mouvement
def callback_up(channel):
    log("PIR - mouvement detected  on channel {} ".format( channel))
    #notif domoticz
    updateMotionSensor(idx_pir)


def getDistanceSensor():
  mesures =[]
  global last_dist
  for x in range(4):    # On prend la mesure "repet" fois
    time.sleep(0.01)       # On la prend toute les 1 seconde
    GPIO.output(Trig, True)
    time.sleep(0.00001)
    GPIO.output(Trig, False)
    debutImpulsion = time.time()
    while GPIO.input(Echo)==0:  ## Emission de l'ultrason
      debutImpulsion = time.time()

    while GPIO.input(Echo)==1:   ## Retour de l'Echo
      finImpulsion = time.time()

    distance = round((finImpulsion - debutImpulsion) * 340 * 100 / 2, 1)  ## Vitesse du son = 340 m/s
    mesures.append(distance)


  log( "HC-S04 - Distance : {} cm" .format(np.mean(mesures)))
  updateSensorIfChangedDelta(idx_dist, np.mean(mesures), last_dist, 30)
  last_dist = np.mean(mesures)

# Configuration GPIO
GPIO.setmode(GPIO. BCM)
#partie PIR sensor
PIR = 4
GPIO.setup(PIR, GPIO.IN)
# partie télémètre ultrasons
Trig = 17          # Entree Trig du HC-SR04 branchee au GPIO 23
Echo = 27         # Sortie Echo du HC-SR04 branchee au GPIO 24
GPIO.setup(Trig,GPIO.OUT)
GPIO.setup(Echo,GPIO.IN)
GPIO.output(Trig, False)



log(" - starting detection")
try:
    GPIO.add_event_detect(PIR, GPIO.RISING, callback=callback_up)
    while 1:
        #récup des infos des capteurs toutes les minutes
        getDistanceSensor()
        time.sleep(0.5)

except KeyboardInterrupt:
    print(" Cleaning up the GPIO")
    GPIO.cleanup()
