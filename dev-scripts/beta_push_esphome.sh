echo "WARNING this is a dev script!"

sudo docker buildx create --name multibuilder_beta

sudo docker buildx use multibuilder_beta

sudo docker buildx build --platform linux/amd64 -t victordrijkoningen/auto-update-esphome:beta --push .