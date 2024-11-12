echo "WARNING this is a dev script!"

sudo docker buildx create --name multibuilder_with_tagname

sudo docker buildx use multibuilder_with_tagname

sudo docker buildx build --platform linux/amd64,linux/arm64,linux/arm/v7 -t "victordrijkoningen/auto-update-esphome:$(cat ./VERSION)" --push .
