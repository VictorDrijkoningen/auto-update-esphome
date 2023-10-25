echo "WARNING this is a dev script!"

sudo docker build ./ --tag=victordrijkoningen/auto-update-esphome:latest

sudo docker push victordrijkoningen/auto-update-esphome:latest