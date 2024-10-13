echo "WARNING this is a dev script!"

sudo docker rm -f auto-update-esphome

sudo docker run -d \
  --name="auto-update-esphome" \
  -v /tmp/esphomedev:/tmp/screenshots \
  --env-file .env \
  victordrijkoningen/auto-update-esphome