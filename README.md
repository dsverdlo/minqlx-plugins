# minqlx-plugins

This repo will contain several plugins which I have developed for [Mino's minqlx](https://github.com/MinoMino/minqlx "MinoMino/minqlx").

Most ideas have been created, worked out and evaluated on <station.boards.net>, the official forum of the 'Bus Station' servers.

If you wish to use my plugins, I'd really appreciate a small message, either via email, steam or on the forum. 
This way the people who have worked so hard on them get some praise and we know which servers are using them.

Creating an account on <http://station.boards.net> is advised if you want to follow updates on the plugins.
Just as minqlx, these plugins are still in development and prone to small updates.

You are free to change any variables and output messages in the file itself, but remember that the plugins are not 100% foolproof and unexpected behavior can occur. 
If you notice such strange behavior on your server, please contact me about it. 
This also goes for any advice or crazy ideas for new plugins you might have.
I can usually be found on IRC (http://webchat.quakenet.org/?channels=minqlbot).

# Plugin list:
| Name | Short Description | Raw |
| ---- | :---------------: | :-- |
[`afk`](https://github.com/dsverdlo/minqlx-plugins#afk)|Detect AFK people and place them in spectator (after a warning).|[`raw`](https://raw.githubusercontent.com/dsverdlo/minqlx-plugins/master/afk.py)
[`anti-rape`](https://github.com/dsverdlo/minqlx-plugins#anti-rape)|In round-based game modes; apply calculated handicaps to people playing above the server average|[`raw`](https://raw.githubusercontent.com/dsverdlo/minqlx-plugins/master/anti-rape.py)
[`autospec`](https://github.com/dsverdlo/minqlx-plugins#autospec)|If CA or FT teams are uneven, make the last person spec.|[`raw`](https://raw.githubusercontent.com/dsverdlo/minqlx-plugins/master/autospec.py)
[`centerprint`](https://github.com/dsverdlo/minqlx-plugins#centerprint)|Provides easy way to broadcast messages on peoples screens, and provides a "last enemy standing" toggle.|[`raw`](https://raw.githubusercontent.com/dsverdlo/minqlx-plugins/master/centerprint.py)
[`disable_votes`](https://github.com/dsverdlo/minqlx-plugins#disable_votes)|Disable the ability to make certain callvotes during a game.|[`raw`](https://raw.githubusercontent.com/dsverdlo/minqlx-plugins/master/disable_votes.py)
[`gauntonly`](https://github.com/dsverdlo/minqlx-plugins#gauntonly)|When 1 last standing person faces a lot of enemies, start gauntonly mode.|[`raw`](https://raw.githubusercontent.com/dsverdlo/minqlx-plugins/master/gauntonly.py)
[`intermission`](https://github.com/dsverdlo/minqlx-plugins#intermission)|Play 1 song out of a list after every match end.|[`raw`](https://raw.githubusercontent.com/dsverdlo/minqlx-plugins/master/intermission.py)
[`mybalance`](https://github.com/dsverdlo/minqlx-plugins#mybalance)|Elo-limits, warmup reminders, team balancing for CA,TDM,CTF,FT.|[`raw`](https://raw.githubusercontent.com/dsverdlo/minqlx-plugins/master/mybalance.py)
[`myban`](https://github.com/dsverdlo/minqlx-plugins#myban)|Use the !ban command with a player's name instead of ID.|[`raw`](https://raw.githubusercontent.com/dsverdlo/minqlx-plugins/master/myban.py)
[`myessentials`](https://github.com/dsverdlo/minqlx-plugins#myessentials)|Use names with the essential commands, like !red iou, !mute iou, !kick iou, ...|[`raw`](https://raw.githubusercontent.com/dsverdlo/minqlx-plugins/master/myessentials.py)
[`player_info`](https://github.com/dsverdlo/minqlx-plugins#player_info)|Display some player information. Maybe upon player connect if you want.|[`raw`](https://raw.githubusercontent.com/dsverdlo/minqlx-plugins/master/player_info.py)
[`railable`](https://github.com/dsverdlo/minqlx-plugins#railable)|Toggle to get a 'railable' message when your health drops too low.|[`raw`](https://raw.githubusercontent.com/dsverdlo/minqlx-plugins/master/railable.py)
[`translate`](https://github.com/dsverdlo/minqlx-plugins#translate)|Look up normal and urban definitions. Translate via google translate (broken atm).|[`raw`](https://raw.githubusercontent.com/dsverdlo/minqlx-plugins/master/translate.py)



# **afk**
- Detects players who are not moving and will slap them until they die and then puts them to spectator.
- CVARS
  -  qlx_afk_warning_seconds "10"
  -  qlx_afk_detection_seconds "20"
  -  qlx_afk_put_to_spec "1"

# **anti-rape**
- This plugin tries to detect overpowered players (for CA servers that like to maintain a certain range of skill), based on their score/second values. This plugin only works for round-based game modes. If players' score/second values are above a certain threshold (in regards to the server score/second average), an appropriate handicap will be assigned to them. This has proven to be an effective method of preventing one-sided games, ending in 0-10. The complete process of thoughts can be found in the 'handicap-thread' on the Bus Station forum. 
- CVARS
  - At the moment the values are all hard coded in the plugin itself
- COMMANDS
  - !hc [<name>] - Get your own or somebody elses handicap % (this can sometimes be unreadable by profile pictures)
  - !handicaps - View all the currently given handicaps and their %'s
  - !gaps [silent] - View all the players who are playing above the server average and how % they are above it. (add 'silent' if you don't want anyone to see it)
- NOTES
  - **Disclaimer:** The term 'rape' in this context is only used to describe an overpowered online player making the game unfair for others below his skill level. It is not meant in any way to offend or refer to the horrible crime that is also known under this name.

# **autospec**
- Displays a message during round countdown if teams are uneven, and forces the person (of the largest team) with the lowest score to spectate.
- CVARS
  - qlx_autospec_minplayers "2" (The minimum amount of players needed on the server to work)

# **centerprint**
- Provides a way to broadcast a message on everyone's screen, or just to individual people. Handy for important server announcements. Also shows a 'One enemy left' message on the screen if people want it. 
- CVARS
  - qlx_cp_message "One enemy left. Start the hunt"
- COMMANDS:
  - !showlast - toggle on/off if you want to see '1 enemy left' message 
  - !print - print a message to a person's screen
  - !broadcast - print a message on everybody's screen
- NOTES
  - Only works for round-based game modes

# **disable_votes**
- This plugin will disable the ability to callvote certain things during a match
- CVARS
  - qlx_disabled_votes_midgame "map, teamsize"
  - qlx_disabled_votes_permission "1"

# **gauntonly**
- This plugin will activate a special mode when one player in a team-based gametype is left last standing against a large number of opponents. The minimum amount of opponnents needed can be specified via MAX and the special mode will turn itself off when a minimum is reached. With the default variables, a 1v5 will activate it, and if it becomes 1v2 the mode will turn off
- CVARS
  - set qlx_gaunt_min "2"
  - set qlx_gaunt_max "4"

# **intermission**
- A music plugin similar to roasticle's intermission. This plugin will loop over a specified collection of sounds/music, by playing one sound at the end of a match. Upload sounds/music in a PK3 file to the workshop for it to work.
- CVARS
- COMMANDS
- NOTES
  - Read the installation and usage in the plugin code itself

# **mybalance**
- This plugin is designed to be used TOGETHER with Mino's balance plugin, but adds some more features, like skill rating-limits for connecting players, using the elo commands by names, and applying an action to the last person on uneven teams (slay, spec or ignore).
Furthermore this plugin uses a text file in which exceptions can be placed for the elo restrictions, and adds a little bump to the elo restriction for regular players. Players falling outside the provided skill rating interval can be blocked on their connection screen, be kicked after a while on the server, or can be allowed to just spectate. Furthermore warmup reminders can be scheduled to repeat at certain intervals to remind players to ready up. In CTF and TDM matches (no rounds), a player will be frozen in place until the teams are even again. Otherwise he is sent back to spectator. 
- CVARS
  - qlx_elo_limit_min "0"
  - qlx_elo_limit_max "1600"
  - qlx_elo_games_needed "10"
  - qlx_mybalance_perm_allowed "2" (players with this perm-level will always be allowed)
  - qlx_mybalance_autoshuffle "0" (set "1" if you want an automatic shuffle before every match)
  - qlx_mybalance_exclude "0" (set "1" if you want to kick players who don't have enough info/games)
  - qlx_elo_kick "1" (set "1" to kick spectators after they joined)
  - qlx_elo_block_connecters "0" (set "1" to block players from connecting)
  - qlx_mybalance_warmup_seconds "300" (how many seconds of warmup before readyup messages come. Set to -1 to disable)
  - qlx_mybalance_warmup_interval "60" (interval in seconds for readyup messages)
  - qlx_mybalance_uneven_time "10" (for CTF and TDM, specify how many seconds to wait before balancing uneven teams)
- COMMANDS
  - !limit, !limits, !elolimit - view the skill rating limits, and the action which will be performed on outliers
  - !elomin [n] - without number; shows minimum allowed glicko. with number; temporary changes the minimum glicko
  - !elomax [n] - without number; shows maximum allowed glicko. with number; temporary changes the maximum glicko
  - !rankings [A|B] - without A or B; shows which rankings are being fetched (A (normal) or B (fun settings))
  - !reminders [ON|OFF] - can turn warmup reminder messages on or off
  - !elo, !getelo - can get your own skill rating or that of someone else
  - !belo - this is like elo, but will show both your A-ranking and your B-ranking
  - !elokicked - view list of kicked people
  - !remkicked <list-id> - after !elokicked, you can use the ID from that list to remove them from the kicklist)
  - !add_exception <id|name> - adds an exception to the exception list
  - !nokick [<name>], !dontkick [<name>] - prevent a person from being kicked. (if only one player is being kicked, you dont have to pass their name)
  - !reload_exceptions - This will reload all the exceptions from the exceptions file. You will be able to see the ID's and names in the console.
- NOTES
  - If you enable strict mode (qlx_mybalance_exclude "1") and qlstats goes down, players will not be able to join the server, since they won't have enough information to prove that they fall in the right skill rating limitation.

# **myban**
- This plugin enhances all the commands of the ban plugin. With this plugin you can also pass (part of) names of players to commands, instead of ID's only.
- CVARS
- COMMANDS
  - ... all the same as the ban plugin ...
- NOTES
  - You don't have to remove the ban plugin, the loading of myban will unload it automatically

# **myessentials**
- This plugin enhances all the commands of the essentials plugin. With this plugin you can also give names, or part of names of players to call the commands, instead of ID's only.
- CVARS
- COMMANDS
  - ... all the same as the essentials plugin ...
- NOTES
  - You don't have to remove the essentials plugin, the loading of myessentials will unload it automatically
  
# **player_info**
- Displays some more info about a player if the info command is used, and also provides a method to check a player's scoreboard information (in big CA matches people sometimes fall off / just below the scoreboard)
- CVARS
  - qlx_pinfo_display_auto "0" (set this to 1 if you want to see automatic info upon player connect)
- COMMANDS
  - !info [<player>] - display some information, like games played, quit frequency, glicko
  - !scoreboard - display scoreboard information when players fall 'below' it
  - !allelo [<player>] - for one person, display the known skill ratings of each game-mode

# **railable**
- This plugin can give you a message (centerprinted) when your health drops to a level where you can be killed with 1 rail. Developed for Clan Arena.
- CVARS
- COMMANDS
  - !railable (this command toggles the service on and off)
  - !railmsg <sentence> (with this command you can choose the msg to be printed)
- NOTES
  - This plugin will do several checks each second, so if you notice too much CPU usage, it is advised to unload the plugin
  - This plugin is not considered cheating, since you could also get your HUD to display this information

# **translate**
- Provides methods to translate any words or sentences into another language, using the Google Translate API. Also able to look up normal english definitions and Urban Dictionaries definitions. There is also an automatic translation feature, which will automatically translate messages into your native or chosen language. **Important** Requires installation of the 'textblob' python library. Instructions are in the plugin comments
- CVARS
- COMMANDS
  - !translate <tag> <sentence>
  - !translate en Deze zin is vertaald geweest. -> Translation: This sentence has been translated.
  - !define match -> Definition: a contest in which people or teams compete against each other in a particular sport.
  - !urban bye -> UrbanDef: a nicer way to say "your f-ing ugly. get out of my face"
- NOTES
  - Currently the translation API is down!

