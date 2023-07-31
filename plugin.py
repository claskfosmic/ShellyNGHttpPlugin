# ShellyNGHTTPPlugin
#
# NG Author: Claskfosmic
# Original Author: Mario Peters
#
"""
<plugin key="ShellyNGHTTPPlugin" name="Shelly NG HTTP Plugin" author="Claskfosmic" version="0.0.1" wikilink="https://github.com/claskfosmic/ShellyNGHttpPlugin/wiki" externallink="https://github.com/claskfosmic/ShellyNGHttpPlugin">
    <description>
        <h2>Shelly NG HTTP Plugin</h2><br/>
        Plugin for controlling Shelly devices via HTTP, using their local IP-adres and credentials. <b>This plug-in doesn't connect to the cloud/to the internet.</b>
        This plugin support Shelly Devices from the first generation and the second generation of Shelly devices, called Shelly-NG.
        <h3>Configuration</h3>
        <ul style="list-style-type:square">
            <li>IP Address is the IP Address of the Shelly device. Default value is 127.0.0.1</li>
            <li>The username to login onto the Shelly device.</li>
            <li>The password to login onto the local Shelly device.</li>
            <li>Type is the type of Shelly device you want to add.<br/>
            <b>Supported Shelly Gen 1 Devices:</b><br/>
            Shelly 1, Shelly PM, Shelly 2.5 (relay and roller), Shelly Dimmer, Shelly RGBW2 (color and white), Shelly Bulb, Shelly Door/Window 2 and Shelly Plug-S<br/>
            <br/><b>Supported Shelly Gen 2 Devices:</b><br/>
            Shelly Plus 1 PM
            </li>
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
               <option label="Shelly IX3" value="SHIX3-1"/>
               <option label="Shelly PM" value="SHSW-PM"/>
               <option label="Shelly 1L" value="SHSW-L"/>
               <option label="Shelly 2.5" value="SHSW-25"/>
               <option label="Shelly Motion" value="SHMOS-01"/>
               <option label="Shelly TRV" value="SHTRV-01"/>
               <option label="Shelly Plug" value="SHPLG-S"/>
               <option label="Shelly Bulb" value="SHBLB-1"/>
               <option label="Shelly RGBW2" value="SHRGBW2"/>
               <option label="Shelly Dimmer" value="SHDM-1"/>
               <option label="Shelly H&T" value="SHHT-1"/>
               <option label="Shelly Smoke" value="SHSM-01"/>
               <option label="Shelly Flood" value="SHWT-1"/>
               <option label="Shelly Door/Window 2" value="SHDW-2"/>
               <option label="Shelly Gas" value="SHGS-1"/>
               <option label="Shelly 3EM" value="SHEM-3"/>
               <option label="Shelly EM" value="SHEM"/>

               <option label="Shelly Plus 1PM" value="SHP1PM"/>
            </options> 
        </param>
       <param field="Mode2" label="Heartbeat In Seconds" width="50px" required="true" default="30"/>
    </params>
</plugin>
"""
import Domoticz
import requests
import json

class BasePlugin:
 
    #mode = None
    mode = "color"
    SHELLY_1 = "SHSW-1"
    SHELLY_IX3 = "SHIX3-1"
    SHELLY_1PM = "SHSW-PM"
    SHELLY_1L="SHSW-L"
    SHELLY_25 = "SHSW-25"
    SHELLY_MOTION = "SHMOS-01"
    SHELLY_TRV="SHTRV-01"
    SHELLY_PLUG = "SHPLG-S"
    SHELLY_BULB = "SHBLB-1"    
    SHELLY_RGBW2 = "SHRGBW2"
    SHELLY_DIMMER = "SHDM-1"
    SHELLY_HT = "SHHT-1"
    SHELLY_SMOKE = "SHSM-01"
    SHELLY_FLOOD = "SHWT-1"
    SHELLY_DW = "SHDW-2"
    SHELLY_GAS="SHGS-1"
    SHELLY_EM="SHEM"
    SHELLY_3EM="SHEM-3"

    SHELLY_PLUS_1_PM="SHP1PM"

    SHELLY_GEN_1_DEVICES = [
        SHELLY_1,
        SHELLY_IX3,
        SHELLY_1PM,
        SHELLY_1L,
        SHELLY_25,
        SHELLY_MOTION,
        SHELLY_TRV,
        SHELLY_PLUG,
        SHELLY_BULB,
        SHELLY_RGBW2,
        SHELLY_DIMMER,
        SHELLY_HT,
        SHELLY_SMOKE,
        SHELLY_FLOOD,
        SHELLY_DW,
        SHELLY_GAS,
        SHELLY_EM,
        SHELLY_3EM
    ]

    SHELLY_GEN_2_DEVICES = [
        SHELLY_PLUS_1_PM
    ]

    SHELLY_GEN_1="GEN1"
    SHELLY_GEN_2="GEN2"

    HeartbeatInSeconds = 30

    def __init__(self):
        return
    
    def getGen(self):
        if Parameters["Mode1"] in self.SHELLY_GEN_2_DEVICES:
            return self.SHELLY_GEN_2
        elif Parameters["Mode1"] in self.SHELLY_GEN_1_DEVICES:
            return self.SHELLY_GEN_1

    def onStart(self):
        Domoticz.Log("onStart called")
        self.HeartbeatInSeconds = int(Parameters["Mode2"])
        if self.HeartbeatInSeconds < 0:
            Domoticz.Error("HeartbeatInSeconds size out of boundary error (HeartbeatInSeconds>0). Default value 30 is being used")

        Domoticz.Heartbeat(self.HeartbeatInSeconds)
        try:
            headers = {'content-type':'application/json'}

            if self.getGen() == self.SHELLY_GEN_1:
                response_shelly = requests.get("http://"+Parameters["Address"]+"/settings", headers=headers, auth=(Parameters["Username"], Parameters["Password"]), timeout=(10,10))
                json_items = json.loads(response_shelly.text)
                response_shelly.close()
                if len(Devices) == 0:
                    if Parameters["Mode1"] == self.SHELLY_1:
                        createSHSW1(json_items)
                    elif Parameters["Mode1"] == self.SHELLY_IX3:
                        createSHIX3(json_items)
                    elif Parameters["Mode1"] == self.SHELLY_1L or Parameters["Mode1"] == self.SHELLY_1PM:
                        createSHSWL(json_items)
                    elif Parameters["Mode1"] == self.SHELLY_25:
                        createSHSW25(self,json_items)
                    elif Parameters["Mode1"] == self.SHELLY_MOTION:
                        createMOTION(json_items)
                    elif Parameters["Mode1"] == self.SHELLY_TRV:
                        createTRV(json_items)
                    elif Parameters["Mode1"] == self.SHELLY_PLUG:
                        createSHPLG(json_items)
                    elif Parameters["Mode1"] == self.SHELLY_RGBW2 or Parameters["Mode1"] == self.SHELLY_BULB:
                        createSHRGBW2(self,json_items)
                    elif Parameters["Mode1"] == self.SHELLY_DIMMER:
                        createSHDM1(json_items)
                    elif Parameters["Mode1"] == self.SHELLY_HT:
                        createHT()
                    elif Parameters["Mode1"] == self.SHELLY_SMOKE:
                        createSMOKE()
                    elif Parameters["Mode1"] == self.SHELLY_FLOOD:
                        createFlood()
                    elif Parameters["Mode1"] == self.SHELLY_DW:
                        createSHDW2()
                    elif Parameters["Mode1"] == self.SHELLY_GAS:
                        createGAS()
                    elif Parameters["Mode1"] == self.SHELLY_EM:
                        createEM(json_items, "EM")
                    elif Parameters["Mode1"] == self.SHELLY_3EM:
                        createEM(json_items, "3EM")
                    else:
                        Domoticz.Log("Type: "+Parameters["Mode1"])
                else:
                    if Parameters["Mode1"] == self.SHELLY_25:
                        for key, value in json_items.items():
                            if key == "mode":
                                self.mode = value

            elif self.getGen() == self.SHELLY_GEN_2:

                device_config = {
                    'switches': [],
                    'inputs': []
                }

                # Read 1 switches
                switches=1

                # Read 0 inputs
                inputs=0
                
                for i in range(0,switches):
                    response_switch_config = requests.get('http://'+Parameters['Address']+'/rpc/Switch.GetConfig?id='+str(i), headers=headers, auth=(Parameters['Username'], Parameters['Password']), timeout=(10,10))
                    switch_config = json.loads(response_switch_config.text)
                    device_config['switches'].append(switch_config)
                    response_switch_config.close()

                    if switch_config['in_mode'] == 'detached':
                        response_input_config = requests.get('http://'+Parameters['Address']+'/rpc/Input.GetConfig?id='+str(i), headers=headers, auth=(Parameters['Username'], Parameters['Password']), timeout=(10,10))
                        input_config = json.loads(response_input_config.text)
                        device_config['inputs'].append(input_config)
                        response_input_config.close()

                for i in range(0,inputs):
                    response_input_config = requests.get('http://'+Parameters['Address']+'/rpc/Input.GetConfig?id='+str(i), headers=headers, auth=(Parameters['Username'], Parameters['Password']), timeout=(10,10))
                    input_config = json.loads(response_input_config.text)
                    device_config['inputs'].append(input_config)
                    response_input_config.close()

                if len(Devices) == 0:
                    if Parameters['Mode1'] == self.SHELLY_PLUS_1_PM:
                        createSHP1PM(device_config)
                    else:
                        Domoticz.Log('Type: '+Parameters['Mode1'])

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
        url = "http://"+Parameters["Address"]
        headers = {'content-type':'application/json'}
        
        if self.getGen() == self.SHELLY_GEN_1:
            if Parameters["Mode1"] != "SHDW-2" and Parameters["Mode1"] != self.SHELLY_TRV and Parameters["Mode1"] != self.SHELLY_GAS and Parameters["Mode1"] != self.SHELLY_EM and Parameters["Mode1"] != self.SHELLY_1L and Parameters["Mode1"] != self.SHELLY_MOTION:
                if Parameters["Mode1"] == "SHSW-1" or Parameters["Mode1"] == "SHPLG-S" or Parameters["Mode1"] == self.SHELLY_1PM:
                    url = url + "/relay/" + str(Unit-1)
                if Parameters["Mode1"] == "SHSW-25":
                    if self.mode == "relay":
                        url = url + "/relay/" + str(Unit-2)
                    elif self.mode == "roller":
                        url = url + "/roller/" + str(Unit-2)
                        if str(Command) == "Open":
                            url = url + "?go=open"
                        elif str(Command) == "Close":
                            url = url + "?go=close"
                        elif str(Command) == "Stop":
                            url = url + "?go=stop"
                if Parameters["Mode1"] == "SHDM-1":
                    url = url + "/light/" + str(Unit-1)
                if Parameters["Mode1"] == "SHRGBW2" or Parameters["Mode1"] == "SHBLB-1":
                    if self.mode == "color":
                        url = url +"/color/" + str(Unit-1)
                    if self.mode == "white":
                        url = url +"/white/" + str(Unit-1)
                if str(Command) == "On":
                    url = url + "?turn=on"
                elif str(Command) == "Off":
                    url = url + "?turn=off"
                elif str(Command) == "Set Level":
                    if self.mode == "color" and Parameters["Mode1"] != "SHDM-1":
                        url = url + "?turn=on&gain=" + str(Level)
                    elif self.mode == "white" or Parameters["Mode1"] == "SHDM-1":
                        url = url + "?turn=on&brightness=" + str(Level)
                    elif self.mode == "roller":
                        url = url + "?go=to_pos&roller_pos="+str(Level)
                elif str(Command) == "Set Color":
                    Domoticz.Debug(str(Devices[Unit].Color))
                    Domoticz.Debug(str(Hue))
                    color_info=json.loads(Hue)
                    r=color_info["r"]
                    g=color_info["g"]
                    b=color_info["b"]
                    m=color_info["m"]
                    cw=color_info["cw"]
                    ww=color_info["ww"]
                    Domoticz.Debug(str(color_info))
                    url = url + "?turn=on"
                    if self.mode == "color":
                        url = url +"&red="+str(r)+"&green="+str(g)+"&blue="+str(b)+"&white="+str(cw)+"&gain="+str(Level)
                    if self.mode == "white":
                        url = url +"&white="+str(cw)+"&brightness="+str(Level)
                else:
                    Domoticz.Log("Unknown command: "+str(Command))
            elif Parameters["Mode1"] == self.SHELLY_TRV:
                if str(Command) == "Set Level":
                    if Unit == 1:
                        if Level > 0:
                            url = url + "?schedule=true&schedule_profile="+str(Level/10)[0]
                    elif Unit == 3:
                        url = url + "/settings/thermostats/0?target_t="+str(Level)
                elif str(Command) == "On":
                    if Unit == 3:
                        url = url + "/settings/thermostats/0?schedule=true"
                    elif Unit == 4:
                        url = url + "/settings?child_lock=true"
                elif str(Command) == "Off":
                    if Unit == 3:
                        url = url + "/settings/thermostats/0?schedule=false"
                    elif Unit == 4:
                        url = url + "/settings?child_lock=false"
                else:
                    Domoticz.Log("Unknown command: "+str(Command))
            elif Parameters["Mode1"] == self.SHELLY_GAS:
                if str(Command) == "On":
                    if Unit == 3:
                        url = url + "/self_test"
                    elif Unit == 4:
                        url = url + "/unmute"
                if str(Command) == "Off":
                    if Unit == 4:
                        url = url + "/mute"
            elif Parameters["Mode1"] == self.SHELLY_EM or Parameters["Mode1"] == self.SHELLY_3EM:
                if str(Command) == "On":
                    if Unit == 1:
                        url = url + "/relay/0?turn=on"
                    elif Unit == 40:
                        url = url + "/settings?led_status_disable=true"
                elif str(Command) == "Off":
                    if Unit == 1:
                        url = url + "/relay/0?turn=off"
                    elif Unit == 40:
                        url = url + "/settings?led_status_disable=false"
            elif Parameters["Mode1"] == self.SHELLY_1L:
                if str(Command) == "On":
                    if Unit == 1:
                        url = url + "/relay/0?turn=on"
                    elif Unit == 40:
                        url = url + "/settings?led_status_disable=true"
                elif str(Command) == "Off":
                    if Unit == 1:
                        url = url + "/relay/0?turn=off"
                    elif Unit == 40:
                        url = url + "/settings?led_status_disable=false"
            elif Parameters["Mode1"] == self.SHELLY_MOTION:
                if str(Command) == "On":
                    if Unit == 3:
                        url = url + "/settings?motion_enable=true"
                elif str(Command) == "Off":
                    if Unit == 3:
                        url = url + "/settings?motion_enabled=false"            
            Domoticz.Log("url: "+url)
            try:
                response = requests.get(url,headers=headers, auth=(Parameters["Username"], Parameters["Password"]), timeout=(10,10))
                Domoticz.Debug(response.text)
                response.close()
            except requests.exceptions.Timeout as e:
                Domoticz.Error(str(e))

        elif self.getGen() == self.SHELLY_GEN_2:
            
            if str(Command) == "On":
                url = url + "/relay/" + str(Unit-100) + "?turn=on"
            elif str(Command) == "Off":
                url = url + "/relay/" + str(Unit-100) + "?turn=off"
            Domoticz.Log("url: "+url)
            
            try:
                response = requests.get(url,headers=headers, auth=(Parameters["Username"], Parameters["Password"]), timeout=(10,10))
                Domoticz.Debug(response.text)
                response.close()
            except requests.exceptions.Timeout as e:
                Domoticz.Error(str(e))

        if str(Command) == "On":
            Devices[Unit].Update(nValue=1,sValue="On")
        elif str(Command) == "Off":
            Devices[Unit].Update(nValue=0,sValue="Off")
        elif str(Command) == "Set Level":
            if self.mode == "roller":
                Devices[Unit].Update(nValue=2,sValue=str(Level))
            else:
                Devices[Unit].Update(nValue=1,sValue=str(Level))
        elif str(Command) == "Set Color":
            if self.mode == "color":
                #Devices[Unit].Update(nValue=1,sValue=str(Level), Color=str(Hue))
                Devices[Unit].Update(nValue=1,sValue=str(Level), Color=json.dumps(Hue))
            else:
                Devices[Unit].Update(nValue=1,sValue=str(Level))
        else:
            Domoticz.Log("Update "+Devices[Unit].Name+": Unknown command: "+str(Command))

    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        Domoticz.Log("Notification: " + Name + "," + Subject + "," + Text + "," + Status + "," + str(Priority) + "," + Sound + "," + ImageFile)

    def onDisconnect(self, Connection):
        Domoticz.Log("onDisconnect called")

    def onHeartbeat(self):
        Domoticz.Log("onHeartbeat called")
        headers = {'content-type':'application/json'}

        if self.getGen() == self.SHELLY_GEN_1:
            if Parameters["Mode1"] != "SHDW-2":
                try:
                    request_shelly_status = requests.get("http://"+Parameters["Address"]+"/status",headers=headers, auth=(Parameters["Username"], Parameters["Password"]), timeout=(10,10))
                    Domoticz.Debug(request_shelly_status.text)
                    json_request = json.loads(request_shelly_status.text)
                    #Domoticz.Log(str(json_request))
                    if Parameters["Mode1"] == self.SHELLY_1 or Parameters["Mode1"] == self.SHELLY_PLUG or Parameters["Mode1"] == self.SHELLY_1PM or Parameters["Mode1"] == self.SHELLY_1L:
                        updateSHSW1(json_request, self)
                    elif Parameters["Mode1"] == self.SHELLY_25:
                        updateSHSW25(json_request, self)
                    elif Parameters["Mode1"] == self.SHELLY_MOTION:
                        updateMOTION(json_request)
                    elif Parameters["Mode1"] == self.SHELLY_TRV:
                        updateTRV(self, json_request)
                    elif Parameters["Mode1"] == self.SHELLY_DIMMER:
                        updateSHDM1(json_request, self)
                    elif Parameters["Mode1"] == self.SHELLY_RGBW2 or Parameters["Mode1"] == self.SHELLY_BULB:
                        updateSHRGBW2(json_request, self)
                    elif Parameters["Mode1"] == self.SHELLY_SMOKE:
                        updateSMOKE(json_request)
                    elif Parameters["Mode1"] == self.SHELLY_HT:
                        updateHT(json_request)
                    elif Parameters["Mode1"] == self.SHELLY_FLOOD:
                        updateFlood(json_request)
                    #elif Parameters["Mode1"] == self.SHELLY_DW:
                    elif Parameters["Mode1"] == self.SHELLY_GAS:
                        updateGAS(self, json_request)
                    elif Parameters["Mode1"] == self.SHELLY_EM or Parameters["Mode1"] == self.SHELLY_3EM:
                        updateEM(json_request, self)
                    elif Parameters["Mode1"] == self.SHELLY_IX3:
                        updateSHIX3(json_request)
                    request_shelly_status.close()
                except requests.exceptions.Timeout as e:
                    Domoticz.Error(str(e))

        elif self.getGen() == self.SHELLY_GEN_2:

            device_status = {
                'switches': [],
                'inputs': []
            }

            # Read 1 switches
            switches=1

            # Read 0 inputs
            inputs=0
            
            try:
                for i in range(0,switches):
                    response_switch_status = requests.get('http://'+Parameters['Address']+'/rpc/Switch.GetStatus?id='+str(i), headers=headers, auth=(Parameters['Username'], Parameters['Password']), timeout=(10,10))
                    switch_status = json.loads(response_switch_status.text)
                    device_status['switches'].append(switch_status)
                    response_switch_status.close()

                for i in range(0,inputs):
                    response_input_status = requests.get('http://'+Parameters['Address']+'/rpc/Input.GetStatus?id='+str(i), headers=headers, auth=(Parameters['Username'], Parameters['Password']), timeout=(10,10))
                    input_status = json.loads(response_input_status.text)
                    device_status['inputs'].append(input_status)
                    response_input_status.close()

                if Parameters['Mode1'] == self.SHELLY_PLUS_1_PM:
                    updateSHP1PM(device_status)
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

def createFlood():
    Domoticz.Device(Name="Flood", Unit=1, Type=243, Subtype=22, Used=1).Create()

def createHT():
    Domoticz.Device(Name="Temperature", Unit=1, Type=80, Used=1).Create()
    Domoticz.Device(Name="Humidity", Unit=2, Type=81, Used=1).Create()
    Domoticz.Device(Name="Temperature + Humidity", Unit=3, Type=82, Used=1).Create()

def createGAS():
    Domoticz.Device(Name="Alarm", Unit=1, Type=243, Subtype=22, Used=1).Create()
    Options={"ValueUnits": "ppm"}
    Domoticz.Device(Name="Concentration", Unit=2, Type=243, Subtype=33, Switchtype=3, Used=1, Options=Options).Create()
    Domoticz.Device(Name="Self-test", Unit=3, Type=244, Subtype=73, Switchtype=9, Used=1).Create()
    Domoticz.Device(Name="(Un)mute alarm", Unit=4, Type=244, Subtype=73, Switchtype=0, Used=1).Create()

def createMOTION(json_items):
    Domoticz.Device(Name="Motion", Unit=1, Type=244, Subtype=62, Switchtype=8, Used=1).Create()
    Domoticz.Device(Name="Illumination", Unit=2, Type=246, Used=1).Create()
    Domoticz.Device(Name="Motion enabled", Unit=3, Type=244, Subtype=62, Switchtype=0, Used=1).Create()
    Devices[3].Update(nValue=1, sValue="True")

def createSMOKE():
    Domoticz.Device(Name="Smoke", Unit=1, Type=244, Subtype=62, Switchtype=5, Used=1).Create()
    Domoticz.Device(Name="Temperature", Unit=2, Used=1, Type=80, Subtype=5).Create()

def createTRV(json_items):
    json_items = {"thermostats": [{"schedule_profile_names": ["Livingroom","Livingroom 1","Bedroom","Bedroom 1","Holiday"]}]}
    for key, value in json_items.items():
        if key == "thermostats":
            for thermostat in value:
                schedule_profile_names = "---|"
                for key_thermostats, value_thermostats in thermostat.items():
                    if key_thermostats == "schedule_profile_names":
                        for item in value_thermostats:
                            schedule_profile_names += str(item) + "|"
                if schedule_profile_names != "":
                    levelactions = ""
                    count = 0
                    schedule_profile_names = schedule_profile_names[:-1]
                    for count in range(0,schedule_profile_names.count("|")):
                        levelactions += "|"
                    Options = {"LevelActions": levelactions, "LevelNames": schedule_profile_names, "LevelOffHidden": "false", "SelectorStyle": "1"}
                    Domoticz.Device(Name="Schedule Profile Names", Unit=1, Used=1, TypeName="Selector Switch", Options=Options).Create() 
    Domoticz.Device(Name="Temperature", Unit=2, Used=1, Type=80, Subtype=5).Create()
    Domoticz.Device(Name="Setpoint", Unit=3, Type=242, Subtype=1, Used=1).Create()
    Domoticz.Device(Name="Child lock", Unit=4, Type=244, Subtype=73, Switchtype=0, Used=1).Create()

def createEM(json_items, aname):
    #EM
    #json_items = {"relays": [{"name": "TEST", "ison": False}], "emeters": [{"appliance_type": "General"},{"appliance_type": "General"}], "led_status_disable": False}
    #3EM
    #json_items = {"relays": [{"name": "TEST", "ison": False}], "emeters": [{"appliance_type": "General"},{"appliance_type": "General"},{"appliance_type": "General"}], "led_status_disable": False}
    relays = None
    meters = None
    for key, value in json_items.items():
        if key == "relays":
            relays = value
        elif key == "emeters":
            meters = value
    count = 0
    for relay in relays:
        name = createRelay(relay, count)
        count = count + 1
    count = 1
    for meter in meters:
        name = aname+str(count)
        Domoticz.Device(Name=name+"_power", Unit=11+count-1, Used=1, Type=248, Subtype=1).Create()
        Domoticz.Device(Name=name+"_Total_kWh", Unit=21+count-1, Used=1, Type=243, Subtype=29).Create()
        Domoticz.Device(Name=name+"_Total returned_kWh", Unit=31+count-1, Used=1, Type=243, Subtype=29).Create()
        count = count + 1 
    Domoticz.Device(Name="Led Disable", Unit=40, Type=244, Subtype=73, Switchtype=0, Used=1).Create()

def createSHSWL(json_items):
    relays = None
    for key, value in json_items.items():
        if key == "relays":
            relays = value
    count = 0
    for relay in relays:
        name = createRelay(relay, count)
        meter={"power":0,"total":0}
        createMeter(name, meter, count)
        count = count + 1
    #Domoticz.Device(Name="Led Disable", Unit=40, Type=244, Subtype=73, Switchtype=0, Used=1).Create()

def createSHIX3(json_items):
    Domoticz.Log("createSHIX3")
    inputs = None
    for key, value in json_items.items():
        if key == "inputs":
            inputs = value
    count = 0
    for inputix3 in inputs:
        name = createInput(inputix3, count)
        count = count + 1

def createSHSW1(json_items):
    relays = None
    for key, value in json_items.items():
        if key == "relays":
            relays = value
    count = 0
    for relay in relays:
        name = createRelay(relay, count)
        meter={"power":0,"total":0}
        createMeter(name, meter, count)
        count = count + 1

def createSHSW25(self,json_items):
    relays = None
    rollers = None
    #mode = None
    num_meters = None
    hostname = ""
    for key, value in json_items.items():
        if key == "relays":
            relays = value
        if key == "rollers":
            rollers = value
        if key == "mode":
            self.mode = value
        #if key == "meters":
            #meters = value
        #if key == "num_meters":
            #num_meters = value
        if key == "device":
            for q, v in value.items():
                if q == "hostname":
                    hostname = v
    Domoticz.Device("Temperature", Unit=1, Used=1, TypeName="Temperature").Create()
    #self.mode="roller"
    if self.mode == "relay":
       count = 1
       for relay in relays:
           name = createRelay(relay, count)
           #meter = meters[1-count]
           meter = {"power":0,"total":0}
           createMeter(name, meter, count)
           count = count + 1
    elif self.mode == "roller":
        count = 1
        for roller in rollers:
            createRoller(hostname, count)
            count = count + 1

def createSHPLG(json_items):
    relays = None
    for key, value in json_items.items():
        if key == "relays":
            relays = value
    count = 0;
    for relay in relays:
        name = createRelay(relay, count)
        meter = {"power":0,"total":0}
        createMeter(name, meter, count)
        count = count + 1

def createSHDM1(json_items):
    lights = []
    meters = None
    brightness = None
    for key, value in json_items.items():
        if key == "lights":
            lights = value
        if key == "meters":
            meters = value
        if key == "brightness":
            brightness = value
    count = 0
    for light in lights:
        name = createLight(light, count)
        meter = {"power":0,"total":0}
        createMeter(name, meter, count)
        count = count + 1

def createSHRGBW2(self,json_items):
    lights = []
    for key, value in json_items.items():
        if key == "lights":
            lights = value
        if key == "mode":
            self.mode = value
    ison = False
    for light in lights:
        if key == "ison":
            ison = value
    self.mode="color"
    if self.mode == "color":
        Domoticz.Device(Name="RGBW", Unit=1, Used=1, Type=241, Subtype=1).Create()
        Domoticz.Device(Name="RGBW_power", Unit=11, Used=1, Type=248, Subtype=1).Create()
        Devices[11].Update(nValue=0, sValue="0")
        createTotal("RGBW", 0, 0, 0)
    elif self.mode == "white":
        Domoticz.Device(Name="White", Unit=1, Used=1, Type=241, Subtype=3).Create()
        Domoticz.Device(Name="White_power", Unit=11, Used=1, Type=248, Subtype=1).Create()
        Devices[11].Update(nValue=0, sValue="0")
        createTotal("White", 0, 0, 0)
    else:
        Domoticz.Log("Unknown mode: "+str(self.mode)) 
    if ison == True:
        Devices[1].Update(nValue=1, sValue="On")

def createSHDW2():
    Domoticz.Device(Name="SHDW2", Unit=1, Used=1, Type=244, Subtype=73, Switchtype=11).Create()

def createLight(light, count):
    name = ""
    ison = False
    for key, value in light.items():
        if key == "name":
            name = value
        if key == "ison":
            ison = value
    if name == "" or name is None:
        name = "Light"+str(count)
    Domoticz.Device(Name=name, Unit=1+count, Used=1, Type=244, Subtype=73, Switchtype=7).Create()
    if ison == True:
        Devices[1+count].Update(nValue=1, sValue="On")
    return name


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

def createInput(inputix3, count):
    Domoticz.Log("createInput")
    name = ""
    for key, value in inputix3.items():
        if key == "name":
            name = value
    if name == "" or name is None:
        name = "Input"+str(count)
    Domoticz.Device(Name=name, Unit=1+count, Used=1, Type=244, Subtype=62, Switchtype=2).Create()
    return name

def createRoller(hostname, count):
    Domoticz.Device(Name=hostname+"_Roller"+str(count), Unit=1+count, Used=1, Type=244, Subtype=73, Switchtype=13).Create()

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

def updateFlood(json_request):
    json_request0 = {"flood": False,"bat": {"value": 71}}
    json_request1 = {"flood": True,"bat": {"value": 71}}
    #json_request = json_request1
    for key, value in json_request.items():
        if key == "bat":
            for key_bat, value_bat in value.items():
                if key_bat == "value":
                    Devices[1].Update(nValue=Devices[1].nValue, sValue=Devices[1].sValue, BatteryLevel=value_bat)
        elif key == "flood":
            if value == True:
                Devices[1].Update(nValue=4, sValue="Flood")
            else:
                Devices[1].Update(nValue=1, sValue="None")

def updateHT(json_request):
    #json_request = {"tmp": {"value": 22}, "hum": {"value": 57}, "bat": {"value": 71}}
    tmp = ""
    hum = ""
    for key, value in json_request.items():
        if key == "bat":
            for key_bat, value_bat in value.items():
                if key_bat == "value":
                    Devices[1].Update(nValue=Devices[1].nValue, sValue=Devices[1].sValue, BatteryLevel=value_bat)
                    Devices[2].Update(nValue=Devices[2].nValue, sValue=Devices[2].sValue, BatteryLevel=value_bat)
                    Devices[3].Update(nValue=Devices[3].nValue, sValue=Devices[3].sValue, BatteryLevel=value_bat)
        elif key == "tmp":
            for key_tmp, value_tmp in value.items():
                if key_tmp == "value":
                    tmp = str(value_tmp)
                    Devices[1].Update(nValue=Devices[1].nValue, sValue=tmp)
        elif key == "hum":
            for key_hum, value_hum in value.items():
                if key_hum == "value":
                    hum = str(value_hum)
                    Devices[2].Update(nValue=value_hum, sValue=Devices[2].sValue)
    if tmp != "" and hum != "":
        Devices[3].Update(nValue=Devices[3].nValue, sValue=tmp+";"+hum)

def updateGAS(self, json_request):
    json_request0 = {"gas_sensor": {"alarm_state": "none"}, "concentration": {"ppm": 100}}
    json_request1 = {"gas_sensor": {"alarm_state": "mild"}, "concentration": {"ppm": 200}}
    json_request2 = {"gas_sensor": {"alarm_state": "heavy"}, "concentration": {"ppm": 300}}
    json_request3 = {"gas_sensor": {"alarm_state": "test"}, "concentration": {"ppm": 400}}
    json_request4 = {"gas_sensor": {"alarm_state": "unknown"}, "concentration": {"ppm": 500}}
    #json_request = json_request2
    #Domoticz.Log(str(json_request))
    for key, value in json_request.items():
        if key == "gas_sensor":
            for key_gs, value_gs in value.items():
                if key_gs == "alarm_state":
                    if value_gs == "none":
                        Devices[1].Update(nValue=1,sValue="None")
                    elif value_gs == "mild":
                        Devices[1].Update(nValue=3,sValue="Mild")
                    elif value_gs == "heavy":
                        Devices[1].Update(nValue=4,sValue="Heavy")
                        Devices[4].Update(nValue=1,sValue="Unmute")
                    elif value_gs == "test":
                        Devices[1].Update(nValue=0,sValue="TEST")
                    else:
                        Devices[1].Update(nValue=0,sValue="Unknown alarm state")
        elif key == "concentration":
            for key_concentration, value_concentration in value.items():
                if key_concentration == "ppm":
                    Devices[2].Update(nValue=value_concentration, sValue=str(value_concentration))

def updateSMOKE(json_request):
    #json_request = {"smoke": False, "tmp": {"value": 22}, "bat": {"value": 71}}
    #json_request = {"smoke": True, "tmp": {"value": 12}, "bat": {"value": 61}}
    for key, value in json_request.items():
        if key == "smoke":
            if value == True:
                Devices[1].Update(nValue=1, sValue=Devices[1].sValue)
            else:
                Devices[1].Update(nValue=0, sValue=Devices[1].sValue)
        elif key == "tmp":
            for key_tmp, value_tmp in value.items():
                if key_tmp == "value":
                    Devices[2].Update(nValue=1, sValue=str(value_tmp))
        elif key == "bat":
            for key_bat, value_bat in value.items():
                if key_bat == "value":
                    Devices[1].Update(nValue=Devices[1].nValue, sValue=Devices[1].sValue, BatteryLevel=value_bat)
                    Devices[2].Update(nValue=Devices[2].nValue, sValue=Devices[2].sValue, BatteryLevel=value_bat)

def updateMOTION(json_request):
    json_request1 = {"lux": {"value": 1111}, "sensor": {"motion": False, "active": True}, "bat": {"value": 11}}
    json_request2 = {"lux": {"value": 2222}, "sensor": {"motion": True, "active": True}, "bat": {"value": 21}}
    json_request3 = {"lux": {"value": 3333}, "sensor": {"motion": False, "active": False}, "bat": {"value": 31}}
    json_request4 = {"lux": {"value": 4444}, "sensor": {"motion": False, "active": True}, "bat": {"value": 41}}
    #json_request = json_request2
    for key, value in json_request.items():
        if key == "lux":
            for key_lux, value_lux in value.items():
                if key_lux == "value":
                    Devices[2].Update(nValue=Devices[2].nValue, sValue=str(value_lux))
        elif key == "sensor":
            for key_sensor, value_sensor in value.items():
                if key_sensor == "motion":
                    if value_sensor == True:
                        Devices[1].Update(nValue=1, sValue=Devices[1].sValue)
                    else:
                        Devices[1].Update(nValue=0, sValue=Devices[1].sValue)
                if key_sensor == "active":
                    if value_sensor == True:
                        Devices[3].Update(nValue=1, sValue=Devices[3].sValue)
                    else:
                        Devices[3].Update(nValue=0, sValue=Devices[3].sValue)
        elif key == "bat":
            for key_bat, value_bat in value.items():
                if key_bat == "value":
                    Devices[1].Update(nValue=Devices[1].nValue, sValue=Devices[1].sValue, BatteryLevel=value_bat)
                    Devices[2].Update(nValue=Devices[2].nValue, sValue=Devices[2].sValue, BatteryLevel=value_bat)
                    Devices[3].Update(nValue=Devices[3].nValue, sValue=Devices[3].sValue, BatteryLevel=value_bat)

def updateTRV(self, json_request):
    #json_request = {"thermostats": [{"schedule_profile": 2, "schedule": True, "tmp": {"value": 17.4, "units": "C", "is_valid": True}}], "bat": {"value": 78, "voltage": 3.127}}
    #json_request = {"thermostats": [{"schedule_profile": 2, "schedule": False, "tmp": {"value": 17.4, "units": "C", "is_valid": True}}], "bat": {"value": 78, "voltage": 3.127}}
    #json_request = {"thermostats": [{"schedule_profile": 0, "schedule": False, "tmp": {"value": 21.6, "units": "C", "is_valid": True}}], "bat": {"value": 100, "voltage": 4.136}}
    #Domoticz.Log(str(json_request))
    for key, value in json_request.items():
        if key == "thermostats":
            for thermostat in value:
                for key_thermostats, value_thermostats in thermostat.items():
                    if key_thermostats == "schedule_profile":
                        Devices[1].Update(nValue=value_thermostats, sValue=str(value_thermostats))
                    elif key_thermostats == "schedule":
                        if value_thermostats == True:
                            Devices[1].Update(nValue=1, sValue=Devices[1].sValue)
                        else:
                            Devices[1].Update(nValue=0, sValue=Devices[1].sValue)
                    elif key_thermostats == "tmp":
                        for key_tmp, value_tmp in value_thermostats.items():
                            if key_tmp == "value":
                                Devices[2].Update(nValue=1, sValue=str(value_tmp))
        elif key == "child_lock":
            if value_bat == True:
                Devices[4].Update(nValue=1, sValue=Devices[4].sValue)
            else:
                Devices[4].Update(nValue=0, sValue=Devices[4].sValue)
        elif key == "bat":
            for key_bat, value_bat in value.items():
                if key_bat == "value":
                    Devices[1].Update(nValue=Devices[1].nValue, sValue=Devices[1].sValue, BatteryLevel=value_bat)
                    Devices[2].Update(nValue=Devices[2].nValue, sValue=Devices[2].sValue, BatteryLevel=value_bat)
                    Devices[3].Update(nValue=Devices[3].nValue, sValue=Devices[3].sValue, BatteryLevel=value_bat)
                    Devices[4].Update(nValue=Devices[4].nValue, sValue=Devices[4].sValue, BatteryLevel=value_bat)

def updateEM(json_request, self):
    #EM
    json_request1 = {"relays": [{"ison": False}], "emeters": [{"power": 120.4, "total": 1213.1, "total_returned": 1221.3}, {"power": 10.3, "total": 1111.3, "total_returned": 1222.3}]}
    #json_request = json_request1
    #3EM
    json_request2 = {"relays": [{"ison": False}], "emeters": [{"power": 120, "total": 121, "total_returned": 122}, {"power": 10, "total": 11, "total_returned": 12},{"power": 300, "total": 311, "total_returned": 312}]}
    #json_request = json_request2
    relays = None
    meters = None
    for key, value in json_request.items():
        if key == "relays":
            relays = value
        if key == "emeters":
            meters = value
    count = 0
    for relay in relays:
        updateRelay(relay, count)
    count = 0
    for meter in meters:
        updateMeter(meters[count], count, self)
        count = count + 1
        
def updateSHSW1(json_request, self):
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
        updateMeter(meters[count], count, self)
        count = count + 1

def updateSHIX3(json_request):
    Domoticz.Log("updateSHIX3")
    inputs = None
    for key, value in json_request.items():
        if key == "inputs":
            inputs = value

    count = 0
    for inputix3 in inputs:
        updateInput(inputix3, count)
        count = count + 1

def updateSHSW25(json_request, self):
    relays = None
    meters = None
    for key, value in json_request.items():
        if key == "relays":
            relays = value
        if key == "meters":
            meters = value
        if key == "temperature":
            Devices[1].Update(nValue=Devices[1].nValue, sValue=str(value))
    if self.mode == "relay":
        count = 1
        for relay in relays:
            updateRelay(relay, count)
            updateMeter(meters[count-1], count, self)
            count = count + 1

def updateSHDM1(json_request, self):
    lights = []
    meters = None
    for key, value in json_request.items():
        if key == "lights":
            lights = value
        if key == "meters":
            meters = value
    count = 0
    #Devices[1].Update(nValue=1, sValue="50")
    for light in lights:
        updateLight(light, count)
        updateMeter(meters[count], count, self)
        count = count + 1

def updateSHRGBW2(json_request, self):
    lights = []
    meters = []
    for key, value in json_request.items():
        if key == "lights":
            lights = value
        if key == "meters":
            meters = value
    count = 0
    for light in lights:
        updateLight(light, count)
        updateMeter(meters[count], count, self)
        count = count + 1

def updateRGBLight(self,light,count):
    updateLight(light, count)
    m = 0
    r = 0
    g = 0
    b = 0
    ww = 0
    cw = 0
    for key, value in light.items():
        if key == "mode":
            if value == "color":
                m = 3
            if value == "white":
                m = 1
        if key == "red":
            r = value
        if key == "green":
            g = value
        if key == "blue":
           b = value
        if key == "white":
           ww = value
        if key == "brightness":
           ww = value * 255 / 100
        if key == "cw":
           cw = value
    color = json.dumps({
      'm': m, #mode 3: RGB
      'r': r,
      'g': g,
      'b': b,
      'ww': ww,
      'cw': cw
    })
    Devices[count].Update(nValue=1,sValue="1", Color=str(color)) 

def updateLight(light, count):
    for key, value in light.items():
        if key == "ison":
            if value:
                if Devices[1+count].nValue != 1:
                    Devices[1+count].Update(nValue=1, sValue=Devices[1+count].sValue)
            else:
                Devices[1+count].Update(nValue=0, sValue=Devices[1+count].sValue)
        if key == "brightness":
            Devices[1+count].Update(nValue=Devices[1+count].nValue, sValue=str(value))

def updateRelay(relay, count):
    for key, value in relay.items():
        if key == "ison":
            if value:
                if Devices[1+count].nValue != 1:
                    Devices[1+count].Update(nValue=1, sValue="On")
            else:
                Devices[1+count].Update(nValue=0, sValue="Off")

def updateInput(inputix3, count):
    Domoticz.Log("updateInput")
    for key, value in inputix3.items():
        if key == "input":
            if value:
                if Devices[1+count].nValue != 1:
                    Devices[1+count].Update(nValue=1, sValue="On")
            else:
                Devices[1+count].Update(nValue=0, sValue="Off")

def updateMeter(meter, count, self):
    power = ""
    for key, value in meter.items():
        if key == "power":
            power = str(value)
            Devices[11+count].Update(nValue=0,sValue=power)
    for key, value in meter.items():
        if key == "total":
            total=int(value)
            if Parameters["Mode1"] != self.SHELLY_EM and Parameters["Mode1"] != self.SHELLY_3EM:
                total = total/60
            total=int(total)
            Devices[21+count].Update(nValue=0,sValue=power+";"+str(total))
        if key == "total_returned":
            total = int(value)
            total = total/60
            total = int(total)
            Devices[31+count].Update(nValue=0,sValue=power+";"+str(total))

def createSHP1PM(device_config):

    Domoticz.Log("Got deviceConfig: " + str(device_config))

    for switch in device_config['switches']:
        name = ""
        if 'name' in switch and switch['name'] != '':
            name = switch['name']
        if name == "":
            name = "Switch"+switch["id"]
        Domoticz.Device(Name=name, Unit=100+int(switch["id"]), Used=1, Type=244, Subtype=73).Create()

        # meter = {"power":0,"total":0}
        # createMeter(name, meter, 100+int(switch["id"]))

    for input in device_config['inputs']:
        name = ""
        if 'name' in input and input['name'] != '':
            name = input['name']
        if name == "":
            name = "Input"+input["id"]
        Domoticz.Device(Name=name, Unit=200+int(input["id"]), Used=1, Type=244, Subtype=62, Switchtype=2).Create()

def updateSHP1PM(device_status):

    Domoticz.Log("Got deviceStatus: " + str(device_status))

    for switch in device_status['switches']:

        if "output" in switch and switch['output'] == True:
            if Devices[100+int(switch['id'])].nValue != 1:
                Devices[100+int(switch['id'])].Update(nValue=1, sValue="On")
        else:
            Devices[100+int(switch['id'])].Update(nValue=0, sValue="Off")

    for input in device_status['inputs']:

        if "state" in switch and switch['state'] == True:
            if Devices[200+int(switch['id'])].nValue != 1:
                Devices[200+int(switch['id'])].Update(nValue=1, sValue="On")
        else:
            Devices[200+int(switch['id'])].Update(nValue=0, sValue="Off")