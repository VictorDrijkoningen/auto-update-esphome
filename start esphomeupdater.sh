echo "WANRING this is a dev script!"

sudo docker rm -f auto-update-esphome

sudo docker run -d \
  --name="auto-update-esphome" \
  -e ESPHOME_TARGET="IP:PORT" \
  -e MODE="selenium" \
  -v /dev/shm:/dev/shm \
  victordrijkoningen/auto-update-esphome

