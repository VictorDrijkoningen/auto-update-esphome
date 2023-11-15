# auto-update-esphome
Auto update esphome devices.

# How to use this container:
Just spin up the docker container with the correct env variables as noted beneath:


# Environment:

| env variable name | value | remarks |
|-----|-----|-----|
| ESPHOME_TARGET | IP:PORT |  |
| MODE | 'selenium' or 'socket' | socket work is not yet completed |
| USERNAME | your esphome instance username | leave empty if instance has no auth |
| PASSWORD | your esphome instance password | leave empty if instance has no auth |
| RUN_DAYS | ex: '1,5,10' |  comma separated list of days in the month that it should run the update cycle, leave empty for all days |
| RUN_MONTHS | ex: '1,5,10' |  comma separated list of months in the year that it should run the update cycle, leave empty for all months |
| RUN_TIME | ex: '01:00' | time to run the update cycle at, format: hour:minutes |
| UPDATE_ON_STARTUP | TRUE | OPTIONAL, when TRUE, runs the update cycle on startup of the docker container |
| SCREENSHOT_LOG | 'TRUE' | OPTIONAL, this enables the screenshot logging for debugging |
