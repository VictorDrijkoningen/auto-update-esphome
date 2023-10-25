# auto-update-esphome
auto update esphome devices 

# How to:
Just spin up the dockercontainer with the correct env variables as noted beneath:


# Environment:
-e ESPHOME_TARGET="IP:PORT"

-e MODE="selenium" or "socket" (socket work is not yet completed!)

-e USERNAME="your esphome instance username" (leave empty if no authentication)

-e PASSWORD="your esphome instance password" (leave empty if no authentication)

-e RUN_DAYS="1,10,20" (comma seperated list of days in the month that it should run the update cycle)

-e SCREENSHOT_LOG="TRUE" (this enables the screenshot logging capability for debugging)
