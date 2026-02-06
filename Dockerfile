FROM python:slim
WORKDIR /app
COPY ./main.py .
COPY ./helpers.py .
COPY ./requirements.txt .
COPY ./LICENSE .
COPY ./VERSION .


#install firefox for headless use firefox:
RUN apt-get update
RUN apt-get install -y firefox-esr
RUN rm -rf /var/lib/apt/lists/*

#install python requirements
RUN pip install --no-cache-dir -r requirements.txt


RUN useradd -m appuser
USER appuser

# Create writable dirs for ANY uid
RUN mkdir -p /tmp/home /tmp/.mozilla 
RUN chmod -R 777 /tmp
ENV HOME=/tmp/home

#change cache dir for running rootless
ENV SE_CACHE_PATH=/config/cache

#start python script
CMD ["python3", "-u", "main.py"]
