sudo docker build ./ --tag=victordrijkoningen/auto-update-esphome

sudo docker rm -f auto-update-esphome

sudo docker run -d \
  --name="auto-update-esphome" \
  -e ESPHOME_TARGET="192.168.2.115:6052" \
  -e SELENIUM_TARGET="172.17.0.3:4444" victordrijkoningen/auto-update-esphome

