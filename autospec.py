# minqlx - A Quake Live server administrator bot.
# Copyright (C) 2015 Mino <mino@minomino.org>

# This is a plugin created by iouonegirl(@gmail.com)

import minqlx

VERSION = "v0.2"

class autospec(minqlx.Plugin):
    def __init__(self):
        super().__init__()
        self.add_hook("round_start", self.handle_round_start)
        self.add_command("v_autospec", self.cmd_version)
        self.add_hook("round_countdown", self.handle_round_count)

    def handle_round_count(self, round_number):
        self.msg("Uneven teams detected!")
        
    def handle_round_start(self, round_number):
        def is_even(n):
            return n % 2 == 0

        def get_last(teams):
            # See which team is bigger than the other
            if len(teams["red"]) < len(teams["blue"]):
                bigger_team = teams["blue"]
            else:
                bigger_team = teams["red"]

            # Get the last person in that team
            lowest_player = bigger_team[0]
            for p in bigger_team:
                if p.stats.score < lowest_player.stats.score:
                    lowest_players = p
            # Return player with lowest score
            return lowest_player

        # Grab the teams
        teams = self.teams()

        # If teams are even, just return
        if is_even(len(teams["red"] + teams["blue"])):
            return minqlx.RET_STOP_EVENT

        # Get last person
        lowest_player = get_last(teams)

        # Perform action if it hasnt been prevented for reasons
        lowest_player.put("spectator")
        minqlx.CHAT_CHANNEL.reply("^6{} ^7was moved to spec to even teams!".format(lowest_player.name))


    def cmd_version(self, player, msg, channel):
        plugin = self.__class__.__name__
        channel.reply("^7Currently using ^3iou^7one^4girl^7's ^6{}^7 plugin version ^6{}^7.".format(plugin, VERSION))
