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

# Plugin list:

- **autospec**
Displays a message during round countdown if teams are uneven, and forces the person (of the largest team) with the lowest score to spectate.

- **anti-rape**
This plugin tries to detect overpowered players (for CA servers that like to maintain a certain range of skill), based on their score/second values.
If their score/second values are above a certain threshold (in regards to the server score/second average), an appropriate handicap will be assigned to them.
The complete process of thoughts can be found in the 'handicap-thread' on the Bus Station forum. **Disclaimer:** The term 'rape' in this context is only used to describe an overpowered online player making the game unfair for others below his skill level. It is not meant in any way to offend or refer to the horrible crime that is also known under this name.

- **mybalance**
This plugin is designed to be used with Mino's balance plugin, but adds some more features, like elo-limits for connecting players, using the elo commands by name, and applying an action to the last person on uneven teams (slay, spec or ignore).
Furthermore this plugin creates a text file in which exceptions can be placed for the elo restrictions, and adds a little bump to the elo restriction for regular players.
**IMPORTANT: to use the mybalance plugin, please comment out, or delete the following lines from the original balance.py:***
```python
      self.add_command(("setrating", "setelo"), self.cmd_setrating, 3, usage="<id> <rating>")
      self.add_command(("getrating", "getelo", "elo"), self.cmd_getrating, usage="<id> [gametype]")
      self.add_command(("remrating", "remelo"), self.cmd_remrating, 3, usage="<id>")
```


