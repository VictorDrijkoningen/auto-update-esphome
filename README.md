# auto-update-esphome
auto update esphome devices 

# How to:
Just spin up the dockercontainer with the correct env variables as noted beneath:


# Environment:
-e ESPHOME_TARGET="IP:PORT"

-e MODE="selenium" or "socket"

-e PASSWORD="your esphome instance password" (leave empty if no authentication)

-e USERNAME="your esphome instance username" (leave empty if no authentication)
