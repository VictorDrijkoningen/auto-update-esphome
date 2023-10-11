
sudo docker pull selenium/standalone-chrome:latest

#sudo docker run -d -p 4444:4444 -v /dev/shm:/dev/shm selenium/standalone-chrome

sudo docker rm -f Selenium

sudo docker run -d -p 4444:4444 \
  --name="Selenium" \
  selenium/standalone-chrome
