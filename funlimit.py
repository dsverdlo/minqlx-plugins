# This is a plugin created by iouonegirl(@gmail.com)
# Copyright (c) 2016 iouonegirl
# https://github.com/dsverdlo/minqlx-plugins
#
# You are free to modify this plugin to your custom,
# except for the version command related code.
#
# This plugin disables (fun) sounds during a match.
#
# Thanks to Cabbe and ph0en|X of TNT for their input
# in the making of this plugin
#
# Uses:
# set qlx_funlimit_messages "1"
#     ^ (Set to "1" to see messages, "0" to disable)

import minqlx
import threading
import time
import os
import requests

VERSION = "v0.1.2"

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


class funlimit(iouonegirlPlugin):
    def __init__(self):
        super().__init__(self.__class__.__name__, VERSION)

        # CVARS
        self.set_cvar_once("qlx_funlimit_messages", "1")

        # HOOKS
        self.add_hook("game_countdown", self.handle_game_start)
        self.add_hook("game_end", self.handle_game_end)
        self.add_hook("round_end", self.handle_round_end)
        self.add_hook("round_start", self.handle_round_start)
        self.add_hook("map", self.handle_map)
        self.add_hook("new_game", self.handle_new_game)
        self.add_hook("unload", self.handle_unload)

        # COMMANDS
        self.add_command("funsounds", self.cmd_funsounds)

        # Instance variables
        self.store_hook = None

        if self.game and self.game.state == "in_progress":
            self.disable_sounds()
        else:
            self.allow_sounds()

    def handle_round_end(self, data):
        self.allow_sounds()

    def handle_round_start(self, roundnumber):
        self.disable_sounds()

    def handle_game_start(self, data=None): # works on countdown now
        # Don't disable yet for round-based gametypes (rounds will do it)
        if self.game and self.game.type_short in ['ca', 'ft', 'ad']: return
        self.disable_sounds()

    def handle_game_end(self, data):
        # Don't enable after round-based gametypes
        if self.game and self.game.type_short in ['ca', 'ft', 'ad']: return
        self.allow_sounds()

    def handle_map(self, mapname, factory):
        self.allow_sounds()

    def handle_new_game(self):
        if self.game.state != "countdown":
            self.allow_sounds()

    def handle_unload(self, plugin):
        if plugin == self.__class__.__name__:
            self.allow_sounds()

    def cmd_funsounds(self, player, msg, channel):
        enabled = "^1not loaded"
        if 'fun' in self.plugins:
            enabled = "^1disabled"
            fun = self.plugins['fun']
            for hook in fun.hooks:
                if hook[0] == "chat":
                    enabled = "^2enabled"

        channel.reply("Fun sounds are currently {}.".format(enabled))


    def disable_sounds(self):
        if not 'fun' in self.plugins: return
        fun = self.plugins['fun']
        for hook in fun.hooks:
            if hook[0] == "chat":
                if not self.store_hook:
                    self.store_hook = hook
                fun.remove_hook(hook[0], hook[1], hook[2])
                self.delay_msg("^7Fun sounds temporarily ^1disabled^7.")
                return

    def allow_sounds(self):
        if not self.store_hook: return
        if not 'fun' in self.plugins: return
        fun = self.plugins['fun']
        for hook in fun.hooks:
            if hook[0] == "chat": return
        fun.add_hook(self.store_hook[0], self.store_hook[1], self.store_hook[2])
        self.delay_msg("^7Fun sounds ^2enabled^7.")

    @minqlx.delay(0.5)
    def delay_msg(self, m):
        if self.get_cvar("qlx_funlimit_messages", int):
            self.msg(m)

