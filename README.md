# Daily Discord Bot BDO
![Generic badge](https://img.shields.io/badge/version-2.0.0-green.svg) ![Generic badge](https://img.shields.io/github/license/Gliger13/bdo_daily_bot) ![Generic badge](https://img.shields.io/badge/python-3.8-blue.svg) [![Discord](https://img.shields.io/discord/669448016591060992)](https://discord.gg/95BgCbt)

Discord Bot for help in collection daily raid in the game **Black Desert Online[RU]**(BDO).

Discord Bot making for BDO community that help collect daily raid, usually sea raids. You can specify the raid collection time, the end time. The bot will send through each interval an image of the raid structure table. Users can enter the raid with one click and they won’t need to worry about anything.

**Technologies**: Python 3.8, discord, Pillow, MongoDB.

**Command localisation**: so far only Russian.

## Features

Arguments with * are required

 -------------------------------

**Create raid**
 - ```!!капитан *[captain_name] *[bdo_server] *[time_leaving] [reservation_open] [reservation_count]``` - Users with role 'Капитан' can create raid.
     - *_captain name_ - this is the game surname of the person who will carry the raid.
    -  *_bdo server_ - a raid will be organized on this server.
    - *_time leaving_ - the raid will be leaving at this time.
    - _reservation open_ - at this time users will be able to get into the raid.
    - _reservation count_ - places you can not take.

Maximum number of members in the raid = 20 - _reserrvation count_. 
When a members successfully enters the raid, the number of remaining seats in the collection message is updated.
Between the _reservation open_ and _time leaving_ the bot will at some interval send images of the raid composition table similar to this.

![alt text](https://github.com/Gliger13/bdo_daily_bot/blob/update_2.0.0/readme_images/raid_example.png?raw=true)

**Start collecting**
 - ```!!сбор *[captain_name] [time_leaving]``` - send a message of collection immediately.

**Remove raid**
- ```!!удали_рейд *[captain_name] [time_leaving]```

**Get into the raid**
There are two options for getting into a raid.
1. ```!!бронь *[name] [captain_name] [time_leaving]``` - old way.
2. Just click on the reaction under the collection message, but the user must be registered.

**Exit raid**
Also there are two options to leave a raid.
1. ```!!удали_бронь *[name] [captain_name] [time_leaving]```
2. Just unclick on the reaction under the collection message, but the user must be registered.

**Registration**
To get into the raid using the reaction member need to register. Must entered once in his life.
- ```!!рег *[name]``` - The bot remembers the player in the database. _name_ - game surname.
- ```!!перерег *[name]``` - Also user can re-register.

**Table**
 - ```!!покажи *[captain_name] [time_leaving]``` - The bot send the image of the raid structure table.
 - ```!!покажи_состав *[captain_name] [time_leaving]``` - Also the bot can send raid structure table in text format.
 - ```!!покажи_рейды``` - Show main information about all raids.

**Save/Load**
The bot does auto-save the raid when it changes.
- ```!!сохрани_рейд *[captain_name] [time_leaving]``` - Also the bot can save raid by command.
- ```!!сохрани_рейды``` - Save all raids.
- ```!!загрузи_рейд *[captain_name] *[time_leaving]``` - Load raid.

## Additional features

- ```!!удалять_тут``` - Bot specify a channel where can remove messages.
- ```!!очисти_чат``` - Remove last 100 messages in the channel.

-----
# Community

If you want to ask a question or look at the work of the bot, then you can visit discord server

<a href="https://discord.gg/95BgCbt"><img src="https://discordapp.com/api/guilds/669448016591060992/widget.png?style=banner2"></a>

# Author

Made by Andrei Zaneuski (@Gliger13), Belarus, Minsk.

# License

**MIT**
