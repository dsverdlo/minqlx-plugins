# This is a plugin created by iouonegirl(@gmail.com)
# Copyright (c) 2016 iouonegirl
# https://github.com/dsverdlo/minqlx-plugins
#
# You are free to modify this plugin to your custom,
# except for the version command related code.
#
# It provides an option to receive a message when you become railable
#

import minqlx
import datetime
import time
import threading
import requests

VERSION = "v0.2"

PLAYER_KEY = "minqlx:players:{}"
RAIL_KEY = PLAYER_KEY + ":railable"
RAIL_MSG_KEY = PLAYER_KEY + ":railmsg"

DEFAULT_MESSAGE = "^7Railable! (edit via ^2!railmsg ^7or disable via ^2!railable^7)"

class railable(minqlx.Plugin):
    def __init__(self):
        super().__init__()

        self.shown = []
        self.running = False

        self.add_hook("round_start", self.handle_round_start)
        self.add_hook("round_end", self.handle_round_end)
        self.add_hook("death", self.handle_death)
        self.add_command("railable", self.cmd_toggle_pref)
        self.add_command("railmsg", self.cmd_set_rail_msg, usage="<message>")
        self.add_command("railinfo", self.cmd_info)
        self.add_command("v_railable", self.cmd_version)
        self.add_hook("player_connect", self.handle_player_connect)

    def cmd_version(self, player, msg, channel):
        self.check_version(channel=channel)

    @minqlx.thread
    def check_version(self, player=None, channel=None):
        url = "https://raw.githubusercontent.com/dsverdlo/minqlx-plugins/master/{}.py".format(self.__class__.__name__)
        res = requests.get(url)
        last_status = res.status_code
        if res.status_code != requests.codes.ok: return
        for line in res.iter_lines():
            if line.startswith(b'VERSION'):
                line = line.replace(b'VERSION = ', b'')
                line = line.replace(b'"', b'')
                # If called manually and outdated
                if channel and VERSION.encode() != line:
                    channel.reply("^7Currently using ^3iou^7one^4girl^7's ^6{}^7 plugin ^1outdated^7 version ^6{}^7.".format(self.__class__.__name__, VERSION))
                # If called manually and alright
                elif channel and VERSION.encode() == line:
                    channel.reply("^7Currently using ^3iou^7one^4girl^7's latest ^6{}^7 plugin version ^6{}^7.".format(self.__class__.__name__, VERSION))
                # If routine check and it's not alright.
                elif player and VERSION.encode() != line:
                    time.sleep(15)
                    try:
                        player.tell("^3Plugin update alert^7:^6 {}^7's latest version is ^6{}^7 and you're using ^6{}^7!".format(self.__class__.__name__, line.decode(), VERSION))
                    except Exception as e: minqlx.console_command("echo {}".format(e))
                return

    def cmd_info(self, player, msg, channel):
        channel.reply("^7Get a customizable ^2!railmsg ^7when you become ^2!railable^7.")

    def cmd_toggle_pref(self, player, msg, channel):
        self.set_notif_pref(player.steam_id)

        if self.get_notif_pref(player.steam_id):
            channel.reply("^7{} will now get a hint when ^2!railable^7.".format(player.name))
        else:
            channel.reply("^7{} will stop seeing ^2!railable ^7notifications.".format(player.name))


    def cmd_set_rail_msg(self, player, msg, channel):
        if len(msg) < 2:
            if not self.get_notif_pref(player.steam_id):
                channel.reply("^7{} does not have the ^2!railable ^7notifications activated.".format(player.name))
                return
            m = self.get_rail_msg(player.steam_id)
            channel.reply("^7{}^7's ^2!railmsg ^7is: {}.".format(player.name, m or DEFAULT_MESSAGE))
        else:
            self.set_rail_msg(player.steam_id, " ".join(msg[1:]))
            self.db[RAIL_KEY.format(player.steam_id)] = 1
            channel.reply("^7{}^7's ^2!railmsg ^7has been changed and ^2!railable ^7activated!".format(player.name))


    def handle_death(self, victim, killer, data):
        if victim.id in self.shown:
            self.shown.remove()

    def handle_round_start(self, n):
        self.running = True
        self.shown = []
        threading.Thread(target=self.looking).start()

    def handle_round_end(self, n):
        self.running = False

    def handle_player_connect(self, player):
        if self.db.has_permission(player, 5):
            self.check_version(player=player)

    def looking(self):
        while self.game.state == 'in_progress' and self.running:
            teams = self.teams()
            for p in teams['red'] + teams['blue']:
                pid = p.steam_id
                if self.get_notif_pref(pid) and self.railable(p) and not pid in self.shown:
                    railmsg = self.get_rail_msg(pid)
                    p.center_print(railmsg or DEFAULT_MESSAGE)
                    self.shown.append(pid)
            time.sleep(0.33)

    def railable(self, p):
        if p.is_alive:
            h = p.health
            a = p.armor
            return (h <= 26) or (h+a <= 80)
        return False

    def get_notif_pref(self, sid):
        try:
            return int(self.db[RAIL_KEY.format(sid)])
        except:
            return False

    def set_notif_pref(self, sid):
        self.db[RAIL_KEY.format(sid)] = 0 if self.get_notif_pref(sid) else 1

    def get_rail_msg(self, sid):
        try:
            return self.db[RAIL_MSG_KEY.format(sid)]
        except:
            return False

    def set_rail_msg(self, sid, msg):
        self.db[RAIL_MSG_KEY.format(sid)] = msg