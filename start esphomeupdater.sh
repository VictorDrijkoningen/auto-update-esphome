sudo docker build ./ --tag=esphomeupdate

sudo docker rm -f ESPHOME_UPDATER

sudo docker run -d \
  --name="ESPHOME_UPDATER" \
  -e ESPHOME_TARGET="192.168.2.115:6052" \
  -e SELENIUM_TARGET="172.17.0.3:4444" esphomeupdate

