FROM python:slim

# install firefox for headless use firefox:
RUN apt-get update
RUN apt-get install -y firefox-esr
RUN rm -rf /var/lib/apt/lists/*

# add files
WORKDIR /app
COPY ./requirements.txt .

# install python requirements
RUN pip install --no-cache-dir -r requirements.txt

# add remaining files later (later for caching purposes) 
COPY ./main.py .
COPY ./helpers.py .
COPY ./LICENSE .
COPY ./VERSION .

# rootless running
RUN mkdir -p /tmp/home /tmp/.mozilla 
RUN chmod -R 777 /tmp
ENV HOME=/tmp/home
ENV SE_CACHE_PATH=/config/cache


RUN useradd -m appuser
USER appuser

# start python script
CMD ["python3", "-u", "main.py"]
