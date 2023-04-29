# Daily Discord Bot BDO
![Generic badge](https://img.shields.io/badge/version-3.1.3-green.svg) 
![Generic badge](https://img.shields.io/github/license/Gliger13/bdo_daily_bot) 
![Generic badge](https://img.shields.io/badge/python-3.10-blue.svg) 
[![Discord](https://img.shields.io/discord/726859545082855483)](https://discord.gg/VaEsRTc)

## Purpose

Discord Bot to organize and collect daily sea raids in the game **Black Desert Online[RU]**(BDO).

Discord Bot for Black Desert Online RU community to collect daily sea raids. We
can specify the raid collection and leaving time. The bot will send an image 
with the raid members every interval. Users can join the raid with one click
and don't have to worry about anything. 

## Content

- [Purpose](#purpose)
- [Features](#features)
- [Additional features](#additional-features)
- [Localisation](#localisation)
- [Author](#author)
- [License](#license)

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

![alt text](https://github.com/Gliger13/bdo_daily_bot/blob/master/.images/raid_example.png?raw=true)

- ```!!кэп``` - allows the user to create a raid from the past 3 raid by clicking on emoji.

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
 - ```!!покажи_рейды [all_guild='']``` - Show main information about all raids. Can show of all guilds.

**Save/Load**
The bot does auto-save the raid when it changes.
 - ```!!сохрани_рейд *[captain_name] [time_leaving]``` - Also the bot can save raid by command.
 - ```!!сохрани_рейды``` - Save all raids.
 - ```!!загрузи_рейд *[captain_name] *[time_leaving]``` - Load raid.

**Statistics**
 - ```!!стат [name]``` - Show statistics that the bot knows about user. 
 - ```!!сервер_стат``` - Show statistics that the bot knows about user.

## Additional features

**Custom help**
 - ```!!help```
 
**Admin**
 - ```!!удалять_тут``` - Bot specify a channel where can remove messages.
 - ```!!не_удалять``` - Bot deny users use remove messages command in this channel.
 - ```!!очисти_чат [n=100]``` - Remove last n messages in the channel.
 - ```!!логи``` - Send logs list as message.

-----

## Localisation

Only russian. Others will be added later I hope.

## Community

If you want to ask a question or look at the work of the bot, then you can visit discord server

<a href="https://discord.gg/VaEsRTc">
    <img src="https://discordapp.com/api/guilds/726859545082855483/widget.png?style=banner2">
</a>

## Author

Made by Andrei Zaneuski (@Gliger13), Belarus, Minsk.

## License

[**GNUv3**](LICENSE)
