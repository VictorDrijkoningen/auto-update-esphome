# auto-update-esphome
auto update esphome devices 

# How to:
1. Spin up "docker run -d -p 4444:4444 selenium/standalone-chrome"
2. Spin up the dockercontainer with the correct env variables

TIME IS IN UTC!
-e ESPHOME_TARGET="IP:PORT"
-e SELENIUM_TARGET="IP:PORT"
