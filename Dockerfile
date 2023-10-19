FROM python:slim
WORKDIR /app
COPY ./* .


#install firefox for headless use firefox:
RUN apt-get update
RUN apt-get install -y firefox-esr wget
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-linux64.tar.gz -O /tmp/geckodriver.tar.gz
RUN tar -C /opt -xzf /tmp/geckodriver.tar.gz
RUN chmod 755 /opt/geckodriver
RUN ln -fs /opt/geckodriver /usr/bin/geckodriver 
RUN ln -fs /opt/geckodriver /usr/local/bin/geckodriver
RUN rm -rf /var/lib/apt/lists/*

#install python requirements
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

#start python script
CMD ["python3", "-u", "main.py"]