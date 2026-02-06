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


# rootless running
RUN mkdir -p /tmp/home /tmp/.mozilla 
RUN chmod -R 777 /tmp
ENV HOME=/tmp/home
ENV SE_CACHE_PATH=/config/cache


RUN useradd -m appuser
USER appuser

#start python script
CMD ["python3", "-u", "main.py"]
