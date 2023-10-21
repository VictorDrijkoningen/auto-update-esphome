echo "WANRING this is a dev script!"

sudo docker rm -f auto-update-esphome

sudo docker run -d \
  --name="auto-update-esphome" \
  -e ESPHOME_TARGET="IP:PORT" \
  -e MODE="selenium" \
  -e USERNAME="user" \
  -e PASSWORD="pass" \
  -e SCREENSHOT_LOG="TRUE" \
  victordrijkoningen/auto-update-esphome