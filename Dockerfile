FROM python:latest
RUN mkdir -p /app
RUN cd /root && wget https://nodejs.org/dist/v12.18.3/node-v12.18.3-linux-x64.tar.xz
RUN cd /root && tar xf node-v12.18.3-linux-x64.tar.xz
ENV PATH "$PATH:/root/node-v12.18.3-linux-x64/bin"
COPY . /app
RUN cd /app/confessions-client && npm install -f
RUN cd /app/confessions-rest && pip install -r requirements.txt
CMD cd /app/confessions-rest && python manage.py runserver 0.0.0.0:$PORT
