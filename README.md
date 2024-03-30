# Shelly NG HTTP - Domoticz Python Plugin
Welcome to the ShellyNGHttpPlugin wiki!

## Description
Python plugin for Domoticz to control Shelly Gen 1 and Gen2 (Shelly Plus, Shelly Pro) devices over HTTP, using their local IP-address. This plugin is based on the originalShellyMQTT - Domoticz Python Plugin of Alexander Mario Peters (https://github.com/mario-peters/ShellyCloudPlugin/), which isn't updated for Gen2 devices.

This plugin support Shelly Devices from the first generation (*like the Shelly 2.5 and Shelly Plug, see https://shelly-api-docs.shelly.cloud/gen1/#shelly-family-overview()*) **AND** the second generation (*like the Shelly Plus 2 PM, see https://shelly-api-docs.shelly.cloud/gen2/#, called Shelly NG (Next Gen) - this is still a work in progress*...)

This plugin is NOT a cloud plugin, but uses the local IP-address of a Shelly device to periodically fetch the latest update. For faster response, see my [Shelly NG MQTT - Domoticz Python Plugin](https://github.com/claskfosmic/ShellyNGMqttPlugin) instead. However, when MQTT is enabled, the Cloud connection will be disabled.

This plugin will work perfectly for devices which can be controlled via the physical switch as well as via Domoticz. In both cases, the light will turned on/off immediately. The only downside of the HTTP Plugin is that is can take some time for Domoticz to be updated when using the physical switch. When the "Heartbeat In Seconds" in set to 60 seconds and the user switches a light using the physical switch, it can take up to 60 seconds before the icon in Domoticz changes to match the state of the light.

## Prerequisites

Tested and works with Domoticz v2024.1

If you do not have a working Python >=3.5 installation, please install it first! (https://www.domoticz.com/wiki/Using_Python_plugins ). If '*Shelly NG Http Plugin*' does not appear in HW list after installation, read again the above article!

## Installation

1. Clone repository into your domoticz plugins folder
```
cd domoticz/plugins
git clone https://github.com/claskfosmic/ShellyNGHttpPlugin.git
```
2. Restart domoticz
3. Go to "Hardware" page and add new item with type "Shelly NG Http Plugin"
4. Set the IP-address of the Shelly device and the "Heartbeat in seconds" (*the interval in which the data from the Shelly device will be fetched and refreshed in Domoticz*).
5. Remember to allow new devices discovery in Domoticz settings

Once plugin is running, it will connect to the Shelly device on local IP-address and it will try to create appropriate device.

## Plugin manual update

Warning: if you use this method, Domoticz may duplicate devices after it!

1. Stop domoticz
2. Go to plugin folder and pull new version
```
cd domoticz/plugins/ShellyNGHttpPlugin
git pull
```
3. Start domoticz

## Configuration on your Shelly devices (*use the WebInterface or the Shelly Smart Control App*)

No configuration is required for the Shelly devices in order to work with this plugin.

## Supported devices

Based on the original plugin from Mario Peters, tested and working with:

- Gen 1
  - Shelly 1
  - Shelly PM
  - Shelly 1L
  - Shelly 2.5 (relay and roller)
  - Shelly Motion
  - Shelly TRV
  - Shelly PlugS
  - Shelly Bulb
  - Shelly RGBW2 (only Color and White)
  - Shelly Dimmer 1/2
  - Shelly H&T
  - Shelly Smoke
  - Shelly Flood sensor
  - Shelly Door/Window 2
  - Shelly Gas sensor
  - Shelly EM
  - Shelly 3EM

Based on my own tests, everything works for:
 - Gen 1:
   - Shelly 1PM (relay)*
   - Shelly Plug (relay)*
   - Shelly Plug S (relay)*
   - Shelly 2.5 (relay, roller not yet tested)*
   - Shelly Dimmer 2
   - Shelly Color Bulb
   - Shelly Motion
 - Gen 2:
   - Shelly Plus 1 PM
   - Shelly Plus 2 PM
   - Shelly Plus i4