echo "WARNING this is a dev script!"

sudo docker buildx create --name multibuilder

sudo docker buildx use multibuilder

sudo docker buildx build --platform linux/amd64,linux/arm64,linux/arm/v7 -t victordrijkoningen/auto-update-esphome:latest --push .