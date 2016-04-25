# This is a plugin created by iouonegirl(@gmail.com)
# Copyright (c) 2016 iouonegirl
# https://github.com/dsverdlo/minqlx-plugins
#
# You are free to modify this plugin to your custom,
# except for the version command related code.
#
# This plugin changes the GLOBAL VOICE to TEAM VOICE
# during a team-based match
#
# Uses:

import minqlx
import threading
import time
import os
import requests

VERSION = "v0.1"


# This code makes sure the required superclass is loaded automatically
try:
    from .iouonegirl import iouonegirlPlugin
except:
    try:
        abs_file_path = os.path.join(os.path.dirname(__file__), "iouonegirl.py")
        res = requests.get("https://raw.githubusercontent.com/dsverdlo/minqlx-plugins/master/iouonegirl.py")
        if res.status_code != requests.codes.ok: raise
        with open(abs_file_path,"a+") as f: f.write(res.text)
        from .iouonegirl import iouonegirlPlugin
    except Exception as e :
        minqlx.CHAT_CHANNEL.reply("^1iouonegirl abstract plugin download failed^7: {}".format(e))
        raise


class auto_voice_switch(iouonegirlPlugin):
    def __init__(self):
        super().__init__(self.__class__.__name__, VERSION)

        self.add_hook("game_countdown", self.handle_game_start)
        self.add_hook("game_end", self.handle_game_end)
        self.add_hook("map", self.handle_map)
        self.add_hook("new_game", self.handle_new_game)

        self.add_command("setvoicemode", self.cmd_set_mode, 2, usage="GLOBAL|TEAM")
        self.add_command(("voicemode", "voicechat"), self.cmd_voice)

        if self.game and self.game.state == "in_progress" and not self.game.type_short in ["ffa", "duel"]:
            self.set_team()
        else:
            self.set_global()


    def handle_game_start(self):
        self.set_team()

    def handle_game_end(self, data):
        self.set_global()


    def handle_map(self, mapname, factory):
        self.set_global()

    def handle_new_game(self):
        if self.game.state != "countdown":
            self.set_global()


    def cmd_set_mode(self, player, msg, channel):
        if len(msg) < 2:
            return minqlx.RET_USAGE

        if msg[1].lower() not in ["global", "team"]:
            return minqlx.RET_USAGE

        if msg[1].lower() == "global":
            return self.set_global()
        self.set_team()


    def cmd_voice(self, player, msg, channel):
        if self.game and self.game.type_short not in ["ca", "tdm", "ctf", "ft", "dom"]:
            channel.reply("Voicechat cannot be switched for non team-based gametypes.")
            return

        if self.get_cvar("g_alltalk", int):
            player.tell("^6Psst^7: Voicechat is currently ^6GLOBAL^7.")
        else:
            player.tell("^6Psst:^7: Voicechat is currently ^6TEAM ONLY^7.")
        return minqlx.RET_STOP_ALL

    def set_global(self):
        if self.game and self.game.type_short not in ["ca", "tdm", "ctf", "ft", "dom"]: return
        if self.get_cvar("g_alltalk", int): return
        minqlx.console_command("set g_alltalk 1")
        self.msg("^7Voicechat switched to ^6GLOBAL^7.")
        self.center_print("^7Voicechat now ^6GLOBAL^7.")

    def set_team(self):
        if self.game and self.game.type_short not in ["ca", "tdm", "ctf", "ft", "dom"]: return
        if not self.get_cvar("g_alltalk", int): return
        minqlx.console_command("set g_alltalk 0")
        self.msg("^7Voicechat switched to ^6TEAM ONLY^7.")
        self.center_print("^7Voicechat now ^6TEAM ONLY^7.")

