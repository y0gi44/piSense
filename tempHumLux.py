#!/usr/bin/env python
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time
from time import gmtime, strftime
import bme280
import piSenseConfig as cfg

#capteur luxmetre
import smbus

import requests
from requests.auth import HTTPBasicAuth

dz_host = cfg.domoticzHost['host']
dz_port = cfg.domoticzHost['port']
dz_user = cfg.domoticzHost['user']
dz_pass = cfg.domoticzHost['pass']

idx_lux   = cfg.dzDevices['lux']
idx_temp  = cfg.dzDevices['temp']
idx_hum   = cfg.dzDevices['hum']
idx_bar   = cfg.dzDevices['bar']

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
               'svalue' : str(value)
               }
    r = requests.get(url, auth=HTTPBasicAuth(dz_user, dz_pass), params=payload)
    #print 'output : '+r.text

def updateHumSensor(idx, value):
    url = 'http://'+dz_host+':'+dz_port+'/json.htm'
    payload = {'type': 'command',
               'param': 'udevice',
               'idx': str(idx),
               'nvalue': str(value),
               'svalue' : '0'
               }
    r = requests.get(url, auth=HTTPBasicAuth(dz_user, dz_pass), params=payload)
    #print 'output : '+r.text

    
def log(message):
  print (strftime("%a, %d %b %Y %H:%M:%S ", time.localtime())+ message)

    
def getLuxSensor():
  global last_lux
  # TSL2561 address, 0x39(57) Select control register, 0x00(00) with command register, 0x80(128)	0x03(03)	Power ON mode
  bus.write_byte_data(0x39, 0x00 | 0x80, 0x03)
  # TSL2561 address, 0x39(57) Select timing register, 0x01(01) with command register, 0x80(128) 	0x02(02)	Nominal integration time = 402ms
  bus.write_byte_data(0x39, 0x01 | 0x80, 0x02)
  
  time.sleep(0.5)
  
  # Read data back from 0x0C(12) with command register, 0x80(128), 2 bytes ch0 LSB, ch0 MSB
  data = bus.read_i2c_block_data(0x39, 0x0C | 0x80, 2)
   
  # Read data back from 0x0E(14) with command register, 0x80(128), 2 bytes ch1 LSB, ch1 MSB
  data1 = bus.read_i2c_block_data(0x39, 0x0E | 0x80, 2)
  
  # Convert the data
  ch0 = data[1] * 256 + data[0]
  ch1 = data1[1] * 256 + data1[0]
  
  # Output data to screen
  log( "TCL2561 - IR + Visible ({} lux), IR({} lux) Visible({} lux)".format(ch0, ch1,(ch0 - ch1))) 
  updateSensor(idx_lux, ch0)
    

def getTempHumSensor():
  global last_temp, last_hum, last_press 
  
  temperature,pression,humidite = bme280.readBME280All()
  log('BME280 - Temp = {0:0.2f} °C'.format(temperature))
  log('BME280 - Hum  = {0:0.2f} %'.format(humidite))
  log('BME280 - Pressure = {0:0.2f} Pa'.format(pression))
  
  updateSensor(idx_temp, temperature)
  updateHumSensor(idx_hum, humidite)
  updateSensor(idx_bar, str(pression)+";0" )

# Configuration GPIO
GPIO.setmode(GPIO. BCM)

#r�cup du bus i2C
bus = smbus.SMBus(1)


log(" - starting detection")
getTempHumSensor()
getLuxSensor()
