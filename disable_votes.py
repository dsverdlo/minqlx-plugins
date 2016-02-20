# This is a plugin created by iouonegirl(@gmail.com)
# Copyright (c) 2016 iouonegirl
# https://github.com/dsverdlo/minqlx-plugins
#
# You are free to modify this plugin to your custom,
# except for the version command related code.
#
# This plugin disables certain votes during a game
#
# Uses
# - qlx_disabled_votes_midgame "map, teamsize"
# - qlx_disabled_votes_permission "1"

import minqlx
import time
import os
import requests

VERSION = "v0.10"


class disable_votes(minqlx.Plugin):

    def __init__(self):
        self.set_cvar_once("qlx_disabled_votes_midgame", "map, teamsize")
        self.set_cvar_once("qlx_disabled_votes_permission", "1")

        self.add_hook("vote_called", self.handle_vote)
        self.add_hook("player_connect", self.handle_player_connect)
        self.add_command("v_disable_votes", self.cmd_version)


    def handle_vote(self, player, vote, args):

        if self.game.state != "in_progress": return

        for v in self.get_cvar("qlx_disabled_votes_midgame", set):
            if v == vote and not self.db.has_permission(player, self.get_cvar("qlx_disabled_votes_permission")):
                self.msg('^1You are not allowed to callvote {} during a match!'.format(v))
                return minqlx.RET_STOP_ALL


    def handle_player_connect(self, player):
        if self.db.has_permission(player, 5):
            self.check_version(player=player)

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

