# ShellyCloudPlugin
#
# Author: Mario Peters
#
"""
<plugin key="ShellyCloudPlugin" name="Shelly Cloud Plugin" author="mariopeters" version="1.0.0" wikilink="https://github.com/mario-peters/ShellyCloudPlugin/wiki" externallink="https://github.com/mario-peters/ShellyCloudPlugin">
    <description>
        <h2>Shelly Cloud Plugin</h2><br/>
        Plugin for controlling Shelly devices.
        <h3>Configuration</h3>
        <ul style="list-style-type:square">
            <li>IP Address is the IP Address of the Shelly device. Default value is 127.0.0.1</li>
            <li>Username</li>
            <li>Password</li>
            <li>Type is the type of Shelly device you want to add. Shelly 1 and Shelly 2.5 (only relay) are currently supported</li>
        </ul>
        <br/><br/>
    </description>
    <params>
        <param field="Address" label="IP Address" width="200px" required="true" default="127.0.0.1"/>
        <param field="Username" label="Username" width="200px" required="true"/>
        <param field="Password" label="Password" width="200px" required="true" password="true"/>
        <param field="Mode1" label="Type" width="200px" required="true">
            <options>
               <option label="Shelly 1" value="SHSW-1"/>
               <option label="Shelly 2.5" value="SHSW-25"/>
            </options> 
        </param>
    </params>
</plugin>
"""
import Domoticz
import requests
import json

class BasePlugin:
 
    modeRelay = True

    def __init__(self):
        return

    def onStart(self):
        Domoticz.Log("onStart called")
        Domoticz.Heartbeat(30)
        if len(Devices) == 0:
            headers = {'content-type':'application/json'}
            try:
                response_shelly = requests.get("http://"+Parameters["Address"]+"/settings",headers=headers, auth=(Parameters["Username"], Parameters["Password"]), timeout=(10,10))
                json_items = json.loads(response_shelly.text)
                response_shelly.close()
                if Parameters["Mode1"] == "SHSW-1":
                    createSHSW1(json_items)
                elif Parameters["Mode1"] == "SHSW-25":
                    createSHSW25(json_items)
                else:
                    Domoticz.Log("Type: "+Parameters["Mode1"])
            except requests.exceptions.Timeout as e:
                Domoticz.Error(str(e))

    def onStop(self):
        Domoticz.Log("onStop called")
        
    def onConnect(self, Connection, Status, Description):
        Domoticz.Log("onConnect called")

    def onMessage(self, Connection, Data):
        Domoticz.Log("onMessage called")

    def onCommand(self, Unit, Command, Level, Hue):
        Domoticz.Log("onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level))
        headers = {'content-type':'application/json'}
        url = "http://"+Parameters["Address"]+"/relay/"
        if Parameters["Mode1"] == "SHSW-1":
            url = url + str(Unit-1)
        if Parameters["Mode1"] == "SHSW-25":
            url = url + str(Unit-2)
        url = url + "?turn="
        if str(Command) == "On":
            url = url + "on"
        else:
            url = url + "off"
        Domoticz.Debug(url)
        try:
            response = requests.get(url,headers=headers, auth=(Parameters["Username"], Parameters["Password"]), timeout=(10,10))
            Domoticz.Debug(response.text)
            response.close()
        except requests.exceptions.Timeout as e:
            Domoticz.Error(str(e))
        if str(Command) == "On":
            Devices[Unit].Update(nValue=1,sValue="On")
        else:
            Devices[Unit].Update(nValue=0,sValue="Off")

    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        Domoticz.Log("Notification: " + Name + "," + Subject + "," + Text + "," + Status + "," + str(Priority) + "," + Sound + "," + ImageFile)

    def onDisconnect(self, Connection):
        Domoticz.Log("onDisconnect called")

    def onHeartbeat(self):
        Domoticz.Log("onHeartbeat called")
        headers = {'content-type':'application/json'}
        try:
            request_shelly_status = requests.get("http://"+Parameters["Address"]+"/status",headers=headers, auth=(Parameters["Username"], Parameters["Password"]), timeout=(10,10))
            Domoticz.Debug(request_shelly_status.text)
            json_request = json.loads(request_shelly_status.text)
            if Parameters["Mode1"] == "SHSW-1":
                updateSHSW1(json_request)
            if Parameters["Mode1"] == "SHSW-25":
                updateSHSW25(json_request)
            request_shelly_status.close()
        except requests.exceptions.Timeout as e:
            Domoticz.Error(str(e))

global _plugin
_plugin = BasePlugin()

def onStart():
    global _plugin
    _plugin.onStart()

def onStop():
    global _plugin
    _plugin.onStop()

def onConnect(Connection, Status, Description):
    global _plugin
    _plugin.onConnect(Connection, Status, Description)

def onMessage(Connection, Data):
    global _plugin
    _plugin.onMessage(Connection, Data)

def onCommand(Unit, Command, Level, Hue):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Hue)

def onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile):
    global _plugin
    _plugin.onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile)

def onDisconnect(Connection):
    global _plugin
    _plugin.onDisconnect(Connection)

def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

    # Generic helper functions
def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug( "'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Device ID:       '" + str(Devices[x].ID) + "'")
        Domoticz.Debug("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Debug("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
    return

def createSHSW1(json_items):
    relays = None
    for key, value in json_items.items():
        if key == "relays":
            relays = value
    count = 0
    for relay in relays:
        name = createRelay(relay, count)
        for key, value in relay.items():
            if key == "power":
                createPower(name, value, count)
        count = count + 1

def createSHSW25(json_items):
    relays = None
    rollers = None
    mode = None
    meters = None
    for key, value in json_items.items():
        if key == "relays":
            relays = value
        if key == "rollers":
            rollers = value
        if key == "mode":
            mode = value
        if key == "meters":
            meters = value
    Domoticz.Device("Temperature", Unit=1, Used=1, TypeName="Temperature").Create()
    if mode == "relay":
       count = 1
       for relay in relays:
           name = createRelay(relay, count)
           meter = meters[1-count]
           createMeter(name, meter, count)
           count = count + 1

def createRelay(relay, count):
    name = ""
    ison = False
    for key, value in relay.items():
        if key == "name":
            name = value
        if key == "ison":
            ison = value
    if name == "" or name is None:
        name = "Relay"+str(count)
    Domoticz.Device(Name=name, Unit=1+count, Used=1, Type=244, Subtype=73).Create()
    if ison == True:
        Devices[1+count].Update(nValue=1, sValue="On")
    return name

def createMeter(name, meter, count):
    power = 0.0
    for key, value in meter.items():
        if key == "power":
            power = value
            createPower(name, power, count)
    for key, value in meter.items():
        if key == "total":
            createTotal(name, power, value, count)

def createPower(name, power, count):
    Domoticz.Device(Name=name+"_power", Unit=11+count, Used=1, Type=248, Subtype=1).Create()
    Devices[11+count].Update(nValue=0, sValue=str(power))

def createTotal(name, power, value, count):
    Domoticz.Device(Name=name+"_kWh", Unit=21+count, Used=1, Type=243, Subtype=29).Create()
    total = int(value)
    total = total/60
    total = int(total)
    Devices[21+count].Update(nValue=0,sValue=str(power)+";"+str(total))

def updateSHSW1(json_request):
    relays = None
    meters = None
    for key, value in json_request.items():
        if key == "relays":
            relays = value
        if key == "meters":
            meters = value
    count = 0
    for relay in relays:
        updateRelay(relay, count)
        updateMeter(meters[count], count)
        count = count + 1

def updateSHSW25(json_request):
    relays = None
    meters = None
    for key, value in json_request.items():
        if key == "relays":
            relays = value
        if key == "meters":
            meters = value
        if key == "temperature":
            Devices[1].Update(nValue=Devices[1].nValue, sValue=str(value))
    count = 1
    for relay in relays:
        updateRelay(relay, count)
        updateMeter(meters[count-1], count)
        count = count + 1

def updateRelay(relay, count):
    for key, value in relay.items():
        if key == "ison":
            if value:
                if Devices[1+count].nValue != 1:
                    Devices[1+count].Update(nValue=1, sValue="On")
            else:
                Devices[1+count].Update(nValue=0, sValue="Off")

def updateMeter(meter, count):
    power = ""
    for key, value in meter.items():
        if key == "power":
            power = str(value)
            Devices[11+count].Update(nValue=0,sValue=power)
    for key, value in meter.items():
        if key == "total":
            total=int(value)
            total=total/60
            total=int(total)
            Devices[21+count].Update(nValue=0,sValue=power+";"+str(total))
