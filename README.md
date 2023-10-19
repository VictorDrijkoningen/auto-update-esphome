# auto-update-esphome
auto update esphome devices 

# How to:
Just spin up the dockercontainer with the correct env variables as noted beneath:


# Environment:
-e ESPHOME_TARGET="IP:PORT"

-e MODE="selenium" or "socket"

-e PASSWORD="your esphome instance password" (leave empty if no authentication)

-e USERNAME="your esphome instance username" (leave empty if no authentication)



# dev:
For testing there is a directory where screenshots are stored so the built in firefox can be screencapped to see what is going on. This is in /tmp/screenshots. Use -v somedir:/tmp/screenshots to see these built in screenshots. _This is strictly a temporary dev feature._
