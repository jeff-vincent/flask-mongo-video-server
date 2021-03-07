FROM python:3.9
RUN mkdir /temp
COPY requirements.txt /temp
RUN pip install -r /temp/requirements.txt
RUN rm -rf /temp
RUN mkdir /app
COPY ./app /app
