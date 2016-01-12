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

class intermission(minqlx.Plugin):

    def __init__(self):
        self.add_hook("game_end", self.handle_game_end)
        self.add_hook("round_end", self.handle_round_end)

    def handle_game_end(self, *args, **kwargs):
        self.play_sound(self.get_cvar("qlx_intermissionSound"))

    def handle_round_end(self, roundnumber):
        rounds_songs = {
            1: "sound/songname/songtitle",
            2: "sound/songname/songtitle",
            3: "sound/songname/songtitle",
            4: "sound/songname/songtitle",
            5: "sound/songname/songtitle",
            6: "sound/songname/songtitle"
            # add / remove whichever round numbers you want
        }

        # If this was the last round, let the handle_game_end hook play something
        if self.game.roundlimit in [self.game.blue_score, self.game.red_score]:
            return

        try:
            if roundnumber in rounds_songs:
                self.play_sound(rounds_songs[roundnumber])
        except Exception as e:
            self.msg("^1Error: ^7{}".format(e))

