# set base image (host OS)
FROM python:3.8

# set the working directory in the container
WORKDIR /bdo_daily_bot/bot

ENV TZ=Europe/Minsk

# upate and install environment
RUN apt-get update \
    && apt-get install -y \
    && apt-get install ffmpeg libsm6 libxext6 -y \
    && rm -rf /var/lib/apt/lists/* \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone

# copy source code and requirements
COPY requirements.txt bot/ ./
# install python dependencies
RUN python -m pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# run bot
CMD [ "python", "bot.py" ]
