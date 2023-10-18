echo "WANRING this is a dev script!"

sudo docker build ./ --tag=victordrijkoningen/auto-update-esphome:latest

sudo docker rm -f auto-update-esphome

sudo docker run -d \
  --name="auto-update-esphome" \
  -e ESPHOME_TARGET="192.168.2.115:6052" \
  -e SELENIUM_TARGET="172.17.0.5:4444" \
  -e MODE="selenium" \
  -v /dev/shm:/dev/shm \
  victordrijkoningen/auto-update-esphome

