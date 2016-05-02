# This is a plugin created by iouonegirl(@gmail.com)
# Copyright (c) 2016 iouonegirl
# https://github.com/dsverdlo/minqlx-plugins
#
# Thanks to Minkyn for his idea for an abstract plugin.
#
# DO NOT MANUALLY LOAD THIS ABSTRACT "PLUGIN"
# OR CHANGE ANY CODE IN IT. TRUST ME.
#


import minqlx
import threading
import time
import os
import requests
import re

VERSION = "v0.29.1 IMPORTANT"

class iouonegirlPlugin(minqlx.Plugin):
    def __init__(self, name, vers):
        self._name = name
        self._vers = vers
        self._loc = "https://raw.githubusercontent.com/dsverdlo/minqlx-plugins/master/"

        # Add custom v_PLUGINNAME command
        self.add_command("v_"+name, self.iouonegirlplugin_cmd_version)

        # these will be added with every subclass, so use RET_STOP in them
        self.add_command(("v_iouonegirlplugin", "v_iouonegirlPlugin", "v_iouonegirl"), self.iouonegirlplugin_cmd_myversion)
        self.add_command("update", self.iouonegirlplugin_cmd_autoupdate, 5, usage="<plugin>|all")
        self.add_command("iouplugins", self.iouonegirlplugin_cmd_list)

        self.add_hook("player_connect", self.iouonegirlplugin_handle_player_connect)


    def iouonegirlplugin_cmd_version(self, player, msg, channel):
        self.iouonegirlplugin_check_version(player, channel)

    # command for checking superclass plugin. One handler is enough
    def iouonegirlplugin_cmd_myversion(self, player, msg, channel):
        self.iouonegirlplugin_check_myversion(player=player, channel=channel)
        return minqlx.RET_STOP

    @minqlx.thread
    def iouonegirlplugin_check_version(self, player=None, channel=None):
        url = "{}{}.py".format(self._loc, self.__class__.__name__)
        res = requests.get(url)
        last_status = res.status_code
        if res.status_code != requests.codes.ok:
            m = "^7Currently using ^3iou^7one^4girl^7's ^6{}^7 plugin version ^6{}^7."
            if channel: channel.reply(m.format(self.__class__.__name__, self._vers))
            elif player: player.tell(m.format(self.__class__.__name__, self._vers))
            return
        for line in res.iter_lines():
            if line.startswith(b'VERSION'):
                line = line.replace(b'VERSION = ', b'')
                line = line.replace(b'"', b'')
                # If called manually and outdated
                if channel and self._vers.encode() != line:
                    channel.reply("^7Currently using ^3iou^7one^4girl^7's ^6{}^7 plugin ^1outdated^7 version ^6{}^7.".format(self.__class__.__name__, self._vers))
                # If called manually and alright
                elif channel and self._vers.encode() == line:
                    channel.reply("^7Currently using ^3iou^7one^4girl^7's latest ^6{}^7 plugin version ^6{}^7.".format(self.__class__.__name__, self._vers))
                # If routine check and it's not alright.
                elif player and self._vers.encode() != line:
                    time.sleep(15)
                    try:
                        player.tell("^3Plugin update alert^7:^6 {}^7's latest version is ^6{}^7 and you're using ^6{}^7!".format(self.__class__.__name__, line.decode(), self._vers))
                    except Exception as e: minqlx.console_command("echo Error: {}".format(e))
                return

    # Check abstract plugin version
    @minqlx.thread
    def iouonegirlplugin_check_myversion(self, player=None, channel=None):
        url = "https://raw.githubusercontent.com/dsverdlo/minqlx-plugins/master/iouonegirl.py"
        res = requests.get(url)
        last_status = res.status_code
        if res.status_code != requests.codes.ok:
            m = "^7Currently using ^3iou^7one^4girl^7's ^6iouonegirl^7 superplugin version ^6{}^7."
            if channel: channel.reply(m.format(VERSION))
            elif player: player.tell(m.format(VERSION))
            return
        for line in res.iter_lines():
            if line.startswith(b'VERSION'):
                line = line.replace(b'VERSION = ', b'')
                line = line.replace(b'"', b'')
                # If called manually and outdated
                if channel and VERSION.encode() != line:
                    channel.reply("^7Currently using ^3iou^7one^4girl^7's ^6iouonegirl^7 superplugin ^1OUTDATED^7 version ^6{}^7!".format(VERSION))
                # If called manually and alright
                elif channel and VERSION.encode() == line:
                    channel.reply("^7Currently using ^3iou^7one^4girl^7's latest ^6iouonegirl^7 superplugin version ^6{}^7.".format(VERSION))
                # If routine check and it's not alright.
                elif player and VERSION.encode() != line:
                    time.sleep(15)
                    try:
                        player.tell("^3Plugin update alert^7:^6 iouonegirl^7's latest version is ^6{}^7 and you're using ^6{}^7! ---> ^2!update iouonegirl".format(line.decode(), VERSION))
                    except Exception as e: minqlx.console_command("echo IouoneError: {}".format(e))
                return

    def iouonegirlplugin_cmd_autoupdate(self, player, msg, channel):
        if len(msg) < 2:
            return minqlx.RET_USAGE

        if msg[1].startswith("iouonegirl"):
            self.iouonegirlplugin_updateAbstract(player, msg, channel)
            return minqlx.RET_STOP

        if msg[1] in [self.__class__.__name__, 'all']:
            self.iouonegirlplugin_update(player, msg, channel)

    def iouonegirlplugin_cmd_list(self, player, msg, channel):
        m = "^7Currently using following iouonegirl plugins: ^6{}^7."
        iou_plugins = []
        plugin_dict =  minqlx.Plugin._loaded_plugins
        for plugin_name in plugin_dict:
            plugin = plugin_dict[plugin_name]
            if iouonegirlPlugin in plugin.__class__.__bases__:
                iou_plugins.append(plugin_name)
        iou_plugins.sort()
        channel.reply("{}^7: ^2{}".format(player.name, " ".join(msg)))
        if iou_plugins:
            channel.reply(m.format("^7, ^6".join(iou_plugins)))
        else:
            channel.reply("^7No iouonegirl plugins installed... Get some from ^6https://github.com/dsverdlo/minqlx-plugins")
        return minqlx.RET_STOP # once is enough, thanks


    def iouonegirlplugin_handle_player_connect(self, player):
        if self.db.has_permission(player, 5):
            self.iouonegirlplugin_check_version(player=player)


    @minqlx.thread
    def iouonegirlplugin_update(self, player, msg, channel):
        try:
            url = "{}{}.py".format(self._loc, self.__class__.__name__)
            res = requests.get(url)
            if res.status_code != requests.codes.ok: return
            script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
            abs_file_path = os.path.join(script_dir, "{}.py".format(self.__class__.__name__))
            with open(abs_file_path,"w") as f: f.write(res.text)
            minqlx.reload_plugin(self.__class__.__name__)
            channel.reply("^2Updated ^3iou^7one^4girl^7's ^6{} ^7plugin to the latest version!".format(self.__class__.__name__))
            return True
        except Exception as e :
            channel.reply("^1Update failed for {}^7: {}".format(self.__class__.__name__, e))
            return False

    @minqlx.thread
    def iouonegirlplugin_updateAbstract(self, player, msg, channel):
        url = "https://raw.githubusercontent.com/dsverdlo/minqlx-plugins/master/iouonegirl.py"
        res = requests.get(url)
        if res.status_code != requests.codes.ok: return
        abs_file_path = os.path.join(os.path.dirname(__file__), "iouonegirl.py")
        with open(abs_file_path,"w") as f: f.write(res.text)
        channel.reply("^2Reloaded ^7abstract plugin, but requires a pyrestart for the changes to take effect.")



    def find_by_name_or_id(self, player, target):
        # Find players returns a list of name-matching players
        def find_players(query):
            players = []
            for p in self.find_player(query):
                if p not in players:
                    players.append(p)
            return players

        # Tell a player which players matched
        def list_alternatives(players, indent=2):
            player.tell("A total of ^6{}^7 players matched for {}:".format(len(players),target))
            out = ""
            for p in players:
                out += " " * indent
                out += "{}^6:^7 {}\n".format(p.id, p.name)
            player.tell(out[:-1])

        # Get the list of matching players on name
        target_players = find_players(target)

        # If id:X is given and it amounts to a player, give it precedence.
        # This is to avoid deadlocks
        match = re.search("(id[=:][0-9]{1,2})", target)
        if match and match.group() == target:
            try:
                match_id = re.search("([0-9]{1,2})", target)
                player = self.player(int(match_id.group()))
                if player.steam_id:
                    return player
            except:
                pass

        # even if we get only 1 person, we need to check if the input was meant as an ID
        # if we also get an ID we should return with ambiguity

        try:
            i = int(target)
            target_player = self.player(i)
            if not (0 <= i < 64) or not target_player:
                raise ValueError
            # Add the found ID if the player was not already found
            if not target_player in target_players:
                target_players.append(target_player)
        except ValueError:
            pass

        # If there were absolutely no matches
        if not target_players:
            player.tell("Sorry, but no players matched your tokens: {}.".format(target))
            return None

        # If there were more than 1 matches
        if len(target_players) > 1:
            list_alternatives(target_players)
            return None

        # By now there can only be one person left
        return target_players.pop()

    def delaytell(self, messages, player, interval = 1):
        def tell(mess):
            return lambda: player.tell("^6{}".format(mess)) if mess else None
        interval_functions(map(tell, messages), interval)

    def delaymsg(self, messages, interval = 1):
        def msg(m):
            return lambda: minqlx.CHAT_CHANNEL.reply("^7{}".format(m)) if m else None
        self.interval_functions(map(msg, messages), interval)

    # Executes functions in a seperate thread with a certain interval
    @minqlx.thread
    def interval_functions(self, items, interval):
        @minqlx.next_frame
        def do(func): func()

        for m in items:
            if m: do(m) # allow "" to be used as a skip
            time.sleep(interval)

    def is_even(self, number):
        return number % 2 == 0

    def is_odd(self, number):
        return not self.is_even(number)