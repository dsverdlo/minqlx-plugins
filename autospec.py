# This is a plugin created by iouonegirl(@gmail.com)
# Copyright (c) 2016 iouonegirl
# https://github.com/dsverdlo/minqlx-plugins
#
# You are free to modify this plugin to your custom,
# except for the version command related code.
#
# It's purpose if to force the last player to spectate
#
# Uses:
# qlx_autospec_minplayers "2"

import minqlx
import time

VERSION = "v0.12"

class autospec(minqlx.Plugin):
    def __init__(self):
        super().__init__()

        self.jointimes = {}

        self.set_cvar_once("qlx_autospec_minplayers", "2")

        self.add_hook("round_start", self.handle_round_start)
        self.add_command("v_autospec", self.cmd_version)
        self.add_hook("round_countdown", self.handle_round_count)
        self.add_hook("player_connect", self.handle_player_connect)
        self.add_hook("player_disconnect", self.handle_player_disconnect)

    def handle_player_connect(self, player):
        self.jointimes[player.steam_id] = time.time()

    def handle_player_disconnect(self, player, reason):
        if player.steam_id in self.jointimes:
            del self.jointimes[player.steam_id]

    def find_time(self, player):
        if not (player.steam_id in self.jointimes):
            self.jointimes[player.steam_id] = time.time()
        return self.jointimes[player.steam_id]

    def handle_round_count(self, round_number):
        teams = self.teams()
        player_count = len(teams["red"] + teams["blue"])
        if (player_count % 2) == 0:
            return

        if player_count < int(self.get_cvar("qlx_autospec_minplayers")):
            return

        lowest_player = self.help_get_last(teams)
        self.msg("Uneven teams detected! {} will be forced to spec!".format(lowest_player.name))

    def handle_round_start(self, round_number):
        def is_even(n):
            return n % 2 == 0

        # Grab the teams
        teams = self.teams()
        player_count = len(teams["red"] + teams["blue"])

        # If teams are even, just return
        if is_even(player_count):
            return minqlx.RET_STOP_EVENT

        # If it is the last player, don't do this and let the game finish normally
        if player_count == 1:
            return

        # If there are less people than wanted, ignore
        if player_count < int(self.get_cvar("qlx_autospec_minplayers")):
            return

        # Get last person
        lowest_player = self.help_get_last(teams)

        # Perform action if it hasnt been prevented for reasons
        lowest_player.put("spectator")
        minqlx.CHAT_CHANNEL.reply("^6{} ^7was moved to spec to even teams!".format(lowest_player.name))


    def cmd_version(self, player, msg, channel):
        plugin = self.__class__.__name__
        channel.reply("^7Currently using ^3iou^7one^4girl^7's ^6{}^7 plugin version ^6{}^7.".format(plugin, VERSION))

    def help_get_last(self, teams):
        # See which team is bigger than the other
        if len(teams["red"]) < len(teams["blue"]):
            bigger_team = teams["blue"].copy()
        else:
            bigger_team = teams["red"].copy()

        if (self.game.red_score + self.game.blue_score) >= 1:

            minqlx.console_command("echo Picking someone to spec based on score")
            # Get the last person in that team
            lowest_players = [bigger_team[0]]
            for p in bigger_team:
                if p.stats.score < lowest_players[0].stats.score:
                    lowest_players = [p]
                elif p.stats.score == lowest_players[0].stats.score:
                    lowest_players.append(p)

            # Sort on joining times highest(newest) to lowest(oldest)
            lowest_players.sort(key= lambda el: self.find_time(el), reverse=True )
            lowest_player = lowest_players[0]

        else:

            minqlx.console_command("echo Picking someone to spec based on join times.")
            bigger_team.sort(key = lambda el: self.find_time(el), reverse=True)
            lowest_player = bigger_team[0]

        return lowest_player
