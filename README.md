# auto-update-esphome
auto update esphome devices

# How to use this container:
Just spin up the dockercontainer with the correct env variables as noted beneath:


# Environment:

| env variable name | value | remarks |
|-----|-----|-----|
| ESPHOME_TARGET | IP:PORT |  |
| MODE | 'selenium' or 'socket' | socket work is not yet completed |
| USERNAME | your esphome instance username | leave empty if instance has no auth |
| PASSWORD | your esphome instance password | leave empty if instance has no auth |
| RUN_DAYS | ex: '1,5,10' |  (comma separated list of days in the month that it should run the update cycle, leave empty for all days) |
| RUN_MONTHS | ex: '1,5,10' |  (comma separated list of months in the year that it should run the update cycle, leave empty for all months) |
| RUN_TIME |  |  |

-e ESPHOME_TARGET="IP:PORT"

-e MODE="selenium" or "socket" (socket work is not yet completed!)

-e USERNAME="your esphome instance username" (leave empty if no authentication)

-e PASSWORD="your esphome instance password" (leave empty if no authentication)

-e RUN_DAYS="1,10,20" (comma separated list of days in the month that it should run the update cycle, leave empty for all days)

-e RUN_MONTHS="1,10,12" (comma separated list of months in the year that it should run the update cycle, leave empty for all months)

-e RUN_TIME="01:00" (time to run the update cycle at, format: hour:minutes)

-e SCREENSHOT_LOG="TRUE" (OPTIONAL this enables the screenshot logging capability for debugging)

-e UPDATE_ON_STARTUP="TRUE" (OPTIONAL, when true, runs update cycle on startup of docker container)
