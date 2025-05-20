# auto-update-esphome
Auto update esphome devices.

# How to use this container:
Just spin up the docker container with the correct env variables as noted beneath:


# Environment:

| env variable name | value | optional | remarks |
|-----|-----|-----|-----|
| ESPHOME_TARGET | IP:PORT | ✘ |  |
| MODE | 'selenium' or 'socket' | ✘ | socket work is not yet completed |
| USERNAME | your esphome instance username | ✔ | leave empty if instance has no auth |
| PASSWORD | your esphome instance password | ✔ | leave empty if instance has no auth |
| RUN_DAYS | ex: '1,5,10' | ✔ |  comma separated list of days in the month that it should run the update cycle, leave empty for all days |
| RUN_MONTHS | ex: '1,5,10' | ✔ |  comma separated list of months in the year that it should run the update cycle, leave empty for all months |
| RUN_TIME | ex: '01:00' | ✘ | time to run the update cycle at, format: hour:minutes |
| UPDATE_ON_STARTUP | TRUE | ✔ | when TRUE, runs the update cycle on startup of the docker container |
| SCREENSHOT_LOG | TRUE | ✔ | this enables the screenshot logging for debugging |

# Sample docker run

```
docker run -d \
  --name="auto-update-esphome" \
  -v /path-to-some-storage:/config \
  -e ESPHOME_TARGET=IP:6052 \
  -e MODE=selenium \
  -e RUN_DAYS=1 \
  -e RUN_TIME=02:00 \
  -e USERNAME=insertusernamehere \
  -e PASSWORD=insertpasswordhere \
  victordrijkoningen/auto-update-esphome
```

# How does this container work?
This docker container has a headless firefox instance, which renders the 'ESPHOME_TARGET' link, and assumes this is a esphome instance. Depending on the username and password environment variables it will then plug those credentials into the login form and logs in. After this the program will press the update button if it detects an esphome device with status 'update available'.
