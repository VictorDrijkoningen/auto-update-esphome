echo "WANRING this is a dev script!"

sudo docker rm -f auto-update-esphome

sudo docker run -d \
  --name="auto-update-esphome" \
  -e ESPHOME_TARGET="IP:PORT" \
  -e MODE="selenium" \
  -e USERNAME="user" \
  -e PASSWORD="pass" \
  -e RUN_DAYS="5,15,25" \
  victordrijkoningen/auto-update-esphome