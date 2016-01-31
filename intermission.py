# This is a plugin created by iouonegirl(@gmail.com)
# Copyright (c) 2016 iouonegirl
# https://github.com/dsverdlo/minqlx-plugins
#
# You are free to modify this plugin to your custom,
# except for the version command related code.
#
# Original idea from <roasticle>, but edited to support
# a list of sounds which will be played one by one after each match.
#
# Place the sounds files in a PK3 file and upload it to a workshop.
#
# If you have trouble hearing the music, I heard Mino's
# workshop.py plugin helps.


import minqlx

VERSION = "v0.9"

# These songs will be looped one by one
SONGS = [
    #"sound/songname/songtitle.ogg",
    #"sound/songname/songtitle.ogg",
    #"sound/songname/songtitle.ogg",
]

class intermission(minqlx.Plugin):
    def __init__(self):
        self.index = 0

        self.add_hook("game_end", self.handle_game_end)
        self.add_command("v_intermission", self.cmd_version)

    @minqlx.delay(0.3)
    def handle_game_end(self, *args, **kwargs):

        # If there are no songs defined, return
        if not SONGS: return

        # If last time the index was incremented too high, loop around
        if self.index == len(SONGS):
            self.index = 0

        # Try to play sound file
        try:
            self.play_sound(SONGS[self.index])
        except Exception as e:
            self.msg("^1Error: ^7{}".format(e))

        # Increase the counter so next round the next sound will be played
        self.index += 1

    def cmd_version(self, player, msg, channel):
        plugin = self.__class__.__name__
        channel.reply("^7Using ^3iou^7one^4girl^7's edit version ^6{}^7 of roasticle's ^6{}^7 plugin.".format(VERSION, plugin))
