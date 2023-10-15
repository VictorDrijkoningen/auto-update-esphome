FROM python:slim
WORKDIR /app
COPY ./* .


RUN apt update 
RUN apt-get install -y wget xvfb unzip gnupg

# Set up the Chrome PPA
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list

RUN apt install -y google-chrome-stable 
RUN rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
CMD ["python3", "-u", "main.py"]