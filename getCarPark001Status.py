#!/usr/bin/python
#--------------------------------------------------------------------------------
#    ___      _____   ___    _____    ___            ___          _   
#   /_\ \    / / __| |_ _|__|_   _|  / __|__ _ _ _  | _ \__ _ _ _| |__
#  / _ \ \/\/ /\__ \  | |/ _ \| |   | (__/ _` | '_| |  _/ _` | '_| / /
# /_/ \_\_/\_/ |___/ |___\___/|_|    \___\__,_|_|   |_| \__,_|_| |_\_\
#                                                                                      
# Copyright (c) Chris Green 2019
#
# Name   : getCarPark001Status.py
# version: 0.1 beta
#
# About  : Loops reading a switch (the car park sensor) on a RaspberryPi and 
#          sends an MQTT message containing a JSON record like the following
#          {
#            "timestamp": "1549844689.0",
#            "meter": {
#              "address": "76229 Eveline Pass, XYZ, AB",
#              "number": 1,
#              "location": [
#                "-75.5712",
#                "-130.5355"
#              ]
#            },
#            "isOccupied": false
#          }
#
# Author : ChrisGreen2007@gmail.com
# Date   : 2019-02-12
#
# https://chrisgreen2004.wordpress.com/2019/02/11/aws-iot-car-park-demo/
# pw: carpark
#
#--------------------------------------------------------------------------------
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import sys
import json
import time

clientId = "carpark001"
myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
topic = "carpark"
shadowTopic = "$aws/things/carpark001/shadow/update"

#--------------------------------------------------------------------------------
def initAWSIoTclient():
  host = "a36ltrhdr9gz28-ats.iot.us-west-2.amazonaws.com"
  certPath = "/home/pi/aws/certs/"

  # Init AWSIoTMQTTClient
  print("Initializing client ...")
  myAWSIoTMQTTClient.configureEndpoint(host, 8883)
  myAWSIoTMQTTClient.configureCredentials("{}aws-root-cert.pem".format(certPath), "{}2979960641-private.pem.key".format(certPath), "{}2979960641-certificate.pem.crt".format(certPath))

  # AWSIoTMQTTClient connection configuration
  print("Connecting client ...")
  myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
  myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
  myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
  myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
  myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
  myAWSIoTMQTTClient.connect()

#--------------------------------------------------------------------------------
def pubAWSIoTmessage(isOccupied):
  location = ["-75.5712", "-130.5355"]
  meter = {}
  meter['number'] = 1
  meter['location'] = location
  meter['address'] = "76229 Eveline Pass, XYZ, AB"
  message = {}
  message['timestamp'] =  str(time.mktime(time.localtime()))
  message['isOccupied'] = isOccupied
  message['meter'] = meter
  messageJson = json.dumps(message)
  myAWSIoTMQTTClient.publish(topic, messageJson, 1)
  print('Published topic %s: %s' % (topic, messageJson))

def updateShadow(isOccupied):
  message = {}
  state = {}
  reported = {}
  reported['isOccupied'] = isOccupied
  state['reported'] = reported
  message['state'] = state
  messageJson = json.dumps(message)
  myAWSIoTMQTTClient.publish(shadowTopic, messageJson, 1)
  print('Published shadow update %s: %s' % (shadowTopic, messageJson))

#--------------------------------------------------------------------------------
def initGPIO():
  GPIO.setwarnings(False) # Ignore warning for now
  GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
  # Set pin 10 to be an input pin and set initial value to be pulled low (off)
  GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
  GPIO.setup(12,GPIO.OUT)

#--------------------------------------------------------------------------------
def main():
  while True:
    isOccupied = False
    # Check the car space
    if GPIO.input(10) == GPIO.HIGH:
        isOccupied = True
        #print(str(ts) + ":  Car space 1 is occupied")
        GPIO.output(12,GPIO.HIGH)
    else:
        isOccupied = False
        #print(str(ts) + ":  Car space 1 is available")
        GPIO.output(12,GPIO.LOW)
    pubAWSIoTmessage(isOccupied)
    updateShadow(isOccupied)
    # Wait for the specified time
    time.sleep(float(sys.argv[1]))

#--------------------------------------------------------------------------------
if __name__=="__main__":
  if len(sys.argv) < 2:
    print "Use: python " + sys.argv[0] + " <sleep time>"
    exit()
  initGPIO()
  initAWSIoTclient()
  main()
