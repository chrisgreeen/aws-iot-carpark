                                                                                      
 Copyright (c) Chris Green 2019

 Name   : #getCarPark001Status.py
 version: 0.1 beta

 About  : Loops reading a switch (the car park sensor) on a RaspberryPi and 
          sends an MQTT message containing a JSON record like the following
          {
            "timestamp": "1549844689.0",
            "meter": {
              "address": "76229 Eveline Pass, XYZ, AB",
              "number": 1,
              "location": [
                "75.5712",
                "130.5355"
              ]
            },
            "isOccupied": false
          }

 Author : ChrisGreen2007@gmail.com
 Date   : 20190212

 Github : https://github.com/chrisgreeen/awsiotcarpark




 Copyright (c) Chris Green 2019

 Name   : #getUpdates.py
 version: 0.1 beta

 About  : Subscribes to the AWS IoT MQTT topic for car park sensor device state changes.
          sends an MQTT message containing a JSON record like the following


         {
           "state": {
             "reported": {
               "isOccupied": true
             }
           },
           "metadata": {
             "reported": {
               "isOccupied": {
                 "timestamp": 1549883560
               }
             }
           },
           "version": 57,
           "timestamp": 1549883560
         }

 Author : ChrisGreen2007@gmail.com
 Date   : 20190212

 Github : https://github.com/chrisgreeen/awsiotcarpark


