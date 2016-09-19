# This is a plugin created by iouonegirl(@gmail.com)
# Copyright (c) 2016 iouonegirl
# https://github.com/dsverdlo/minqlx-plugins
#
# You are free to modify this plugin to your custom,
# except for the version command related code.
#
# This plugin protects spectators from being targeted
# by kick callvotes.
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


class specprotect(iouonegirlPlugin):
    def __init__(self):
        super().__init__(self.__class__.__name__, VERSION)

        # CVARS

        # HOOKS
        self.add_hook("vote_called", self.handle_vote_called)

        # COMMANDS

        # Instance variables

    def handle_vote_called(self, caller, vote, args):
        # If it is not vote, whatever
        if not vote.lower() in ["kick", "clientkick"]: return
        if not args: return

        try:
            target = self.player(int(args))
        except ValueError:
            target = self.player(args)

        if target and target.team == "spectator":
            caller.tell("^3Server^7: spectators cannot be kicked on this server.")
            return minqlx.RET_STOP_ALL



