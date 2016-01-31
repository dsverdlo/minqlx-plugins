# This is a plugin created by iouonegirl(@gmail.com)
# Copyright (c) 2016 iouonegirl
# https://github.com/dsverdlo/minqlx-plugins
#
# You are free to modify this plugin to your custom,
# except for the version command related code.
#
# This plugin disables certain votes during a game

import minqlx

VERSION = "v0.6"

DISABLE_VOTES = {
    'map': '^1You are not allowed to callvote maps during a match!',
    'teamsize': '^1You are not allowed to change the teamsize during a match!'
    }

class disable_votes(minqlx.Plugin):

    def __init__(self):
        self.add_hook("vote_called", self.handle_vote)
        self.add_command("v_disable_votes", self.cmd_version)

    def cmd_version(self, player, msg, channel):
        plugin = self.__class__.__name__
        channel.reply("^7Currently using ^3iou^7one^4girl^7's ^6{}^7 plugin version ^6{}^7.".format(plugin, VERSION))

    def handle_vote(self, player, vote, args):

        if self.game.state != "in_progress": return

        for v in DISABLE_VOTES:
            if v == vote:
                self.msg(DISABLE_VOTES[v])
                return minqlx.RET_STOP_ALL


