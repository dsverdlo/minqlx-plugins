# minqlx - A Quake Live server administrator bot.
# Copyright (C) 2015 Mino <mino@minomino.org>
#
# This is a plugin created by roasticle
# https://github.com/roasticle/minqlx-plugins
#
# Has been edited by iouonegirl(@gmail.com) to support
# a sound playing at the end of every round.
# A PK3 file must exist and the songnames/paths too,
# or you'll get an error on your screen.

import minqlx

VERSION = "v0.3"

class intermission(minqlx.Plugin):

    def __init__(self):

        self.index = 0

        self.add_hook("game_end", self.handle_game_end)
        self.add_hook("round_end", self.handle_round_end)
        self.add_command("v_intermission", self.cmd_version)

    def handle_game_end(self, *args, **kwargs):
        self.play_sound(self.get_cvar("qlx_intermissionSound"))

    def handle_round_end(self, roundnumber):

        # These songs will be looped one by one
        rounds_songs = [
            "sound/songname/songtitle",
            "sound/songname/songtitle",
            "sound/songname/songtitle",
            "sound/songname/songtitle",
        ]

        # If this was the last round, let the handle_game_end hook play something
        if self.game.roundlimit in [self.game.blue_score, self.game.red_score]:
            return

        # If last time the index was incremented too high, loop around
        if self.index == len(rounds_songs):
            self.index = 0

        # Try to play the file
        try:
            self.play_sound(rounds_songs[self.index])
        except Exception as e:
            self.msg("^1Error: ^7{}".format(e))

        # Increase the counter so next round the next sound will be played
        self.index += 1

    def cmd_version(self, player, msg, channel):
        plugin = self.__class__.__name__
        channel.reply("^7Currently using ^3iou^7one^4girl^7's version ^6{}^7 of roasticle's edited ^6{}^7 plugin.".format(plugin, VERSION))