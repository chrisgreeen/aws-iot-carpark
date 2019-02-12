#!/usr/bin/python
#--------------------------------------------------------------------------------
#    ___      _____   ___    _____    ___            ___          _
#   /_\ \    / / __| |_ _|__|_   _|  / __|__ _ _ _  | _ \__ _ _ _| |__
#  / _ \ \/\/ /\__ \  | |/ _ \| |   | (__/ _` | '_| |  _/ _` | '_| / /
# /_/ \_\_/\_/ |___/ |___\___/|_|    \___\__,_|_|   |_| \__,_|_| |_\_\
#
# Copyright (c) Chris Green 2019
#
# Name   : getUpdates.py
# version: 0.1 beta
#
# About  : Subscribes to the AWS IoT MQTT topic for car park sensor device state changes.
#          sends an MQTT message containing a JSON record like the following
#
#
#         {
#           "state": {
#             "reported": {
#               "isOccupied": true
#             }
#           },
#           "metadata": {
#             "reported": {
#               "isOccupied": {
#                 "timestamp": 1549883560
#               }
#             }
#           },
#           "version": 57,
#           "timestamp": 1549883560
#         }
#
# Author : ChrisGreen2007@gmail.com
# Date   : 2019-02-12
#
# https://chrisgreen2004.wordpress.com/2019/02/11/aws-iot-car-park-demo/
# pw: carpark
#
#--------------------------------------------------------------------------------

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import json
from sense_hat import SenseHat

clientId = "carpark001"
client = AWSIoTMQTTClient(clientId)
shadowTopic = "$aws/things/carpark001/shadow/update/accepted"
sense = SenseHat()

#--------------------------------------------------------------------------------
def initAWSIoTclient():
  host = "a36ltrhdr9gz28-ats.iot.us-west-2.amazonaws.com"
  certPath = "/home/cgreen/aws/certs/"

  # Init AWSIoTMQTTClient
  print("Initializing client ...")
  client.configureEndpoint(host, 8883)
  client.configureCredentials("{}aws-root-cert.pem".format(certPath), "{}2979960641-private.pem.key".format(certPath), "{}2979960641-certificate.pem.crt".format(certPath))

  # AWSIoTMQTTClient connection configuration
  print("Connecting client ...")
  client.configureAutoReconnectBackoffTime(1, 32, 20)
  client.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
  client.configureDrainingFrequency(2)  # Draining: 2 Hz
  client.configureConnectDisconnectTimeout(10)  # 10 sec
  client.configureMQTTOperationTimeout(5)  # 5 sec
  client.connect()

#--------------------------------------------------------------------------------
def main():
  client.subscribe(shadowTopic, 1, updatesCallback)

def updatesCallback(client, userdata, message):
  print("Hello from callback()")
  print("client = " + str(client))
  print("userdata = " + str(userdata))
  j = json.loads(str(message.payload))
  isOccupied = j['state']['reported']['isOccupied']
  print("isOccupied = " + str(isOccupied))
  if isOccupied:
    sense.show_letter('4')
  else:
    sense.show_letter('5')

#--------------------------------------------------------------------------------
if __name__=="__main__":
  initAWSIoTclient()
  main()

  sense.show_letter('5')
  print("Waiting for updates ...")
  while True:
    time.sleep(0.5)
