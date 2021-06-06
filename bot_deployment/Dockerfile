# set base image (host OS)
FROM python:3.8

# set the working directory in the container
WORKDIR /bot

RUN apt-get update ##[edited]
RUN apt-get install ffmpeg libsm6 libxext6 -y

# download source code and install dependencies

RUN git clone -branch update git@github.com:Gliger13/bdo_daily_bot.git . && \
    pip install --no-cache-dir -r requirements.txt

# run bot
CMD [ "python", "./bot.py" ]
