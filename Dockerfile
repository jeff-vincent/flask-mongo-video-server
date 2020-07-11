FROM jdvincent/ubuntu-python3.8
COPY requirements.txt /tmp/
RUN apt-get update \
&& apt-get install python3-pip -y
RUN pip3 install -r /tmp/requirements.txt
RUN rm -rf /temp
COPY . /app
CMD python3.8 /app/app/flask_mongo_video.py
