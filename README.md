# auto-update-esphome
auto update esphome devices 

# How to:
1. Spin up the dockercontainer with the correct env variables

TIME IS IN UTC!
-e ESPHOME_TARGET="IP:PORT"
-e MODE="selenium" or "socket"
-e PASSWORD="your esphome instance password" #TODO
-e USERNAME="your esphome instance username" #TODO
