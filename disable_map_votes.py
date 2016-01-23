# This is a plugin created by iouonegirl(@gmail.com)
# Copyright (c) 2016 iouonegirl
# https://github.com/dsverdlo/minqlx-plugins
#
# This plugin disables mapvotes mid-game

import minqlx

VERSION = "v0.1"


class disable_map_votes(minqlx.Plugin):

    def __init__(self):
        self.add_hook("vote_called", self.handle_vote)

    def cmd_version(self, player, msg, channel):
        plugin = self.__class__.__name__
        channel.reply("^7Currently using ^3iou^7one^4girl^7's ^6{}^7 plugin version ^6{}^7.".format(plugin, VERSION))

    def handle_vote(self, player, vote, args):
        if vote == "map" and self.game.state == "in_progress":
            player.tell("^6You cannot callvote map during a game. Try /callvote map_restart.")
            self.force_vote(False)


