# This is a plugin created by iouonegirl(@gmail.com)
# Copyright (c) 2016 iouonegirl
# https://github.com/dsverdlo/minqlx-plugins
#
# You are free to modify this plugin to your custom,
# except for the version command related code.
#
# Thanks to Minkyn for his assistance.
#
# Its purpose if to force the last player to spectate
# Algorithm: http://i.imgur.com/8P60gRq.png
#
# Uses:
# qlx_autospec_minplayers "2"

import minqlx
import time
import requests

VERSION = "v0.16"

class autospec(minqlx.Plugin):
    def __init__(self):
        super().__init__()

        self.jointimes = {}

        self.set_cvar_once("qlx_autospec_minplayers", "2")

        self.add_command("v_autospec", self.cmd_version)
        self.add_hook("round_countdown", self.handle_round_count)
        self.add_hook("player_connect", self.handle_player_connect)
        self.add_hook("player_disconnect", self.handle_player_disconnect)

    def handle_player_connect(self, player):
        self.jointimes[player.steam_id] = time.time()

        if self.db.has_permission(player, 5):
            self.check_version(player=player)

    def handle_player_disconnect(self, player, reason):
        if player.steam_id in self.jointimes:
            del self.jointimes[player.steam_id]

    def find_time(self, player):
        if not (player.steam_id in self.jointimes):
            self.jointimes[player.steam_id] = time.time()
        return self.jointimes[player.steam_id]

    def handle_round_count(self, round_number):
        def is_even(n):
            return n % 2 == 0

        def red_min_blue():
            t = self.teams()
            return len(t['red']) - len(t['blue'])

        # Grab the teams
        teams = self.teams()
        player_count = len(teams["red"] + teams["blue"])

        if player_count < int(self.get_cvar("qlx_autospec_minplayers")):
            return

        # If there is a difference in teams of more than 1
        diff = red_min_blue()
        to, fr = ['blue', 'red'] if diff > 0 else ['red','blue']
        last = self.help_get_last()
        n = int(abs(diff) / 2)
        if abs(diff) >= 1:
            if is_even(diff):
                n = last.name if n == 1 else "{} players".format(n)
                self.msg("^6Uneven teams detected!^7 Server will move {} to {}".format(n, to))
            else:
                m = 'lowest player' if n == 1 else '{} lowest players'.format(n)
                m = " and move the {} to {}".format(m, to) if n else ''
                self.msg("^6Uneven teams detected!^7 Server will auto spec {}{}.".format(last.name, m))

        self.balance_before_start(round_number)



    @minqlx.thread
    def balance_before_start(self, roundnumber):
        def is_even(n):
            return n % 2 == 0

        def red_min_blue():
            t = self.teams()
            return len(t['red']) - len(t['blue'])

        # Wait until round almost starts
        countdown = int(self.get_cvar('g_roundWarmupDelay'))
        if self.game.type_short == "ft":
            countdown = int(self.get_cvar('g_freezeRoundDelay'))
        time.sleep(max(countdown / 1000 - 0.3, 0))

        # Grab the teams
        teams = self.teams()
        player_count = len(teams["red"] + teams["blue"])

        # If it is the last player, don't do this and let the game finish normally
        if player_count == 1:
            return

        # If there are less people than wanted, ignore
        if player_count < int(self.get_cvar("qlx_autospec_minplayers")):
            return

        # While there is a difference in teams of more than 1
        while abs(red_min_blue()) >= 1:
            last = self.help_get_last()
            diff = red_min_blue()

            if is_even(diff): # one team has an even amount of people more than the other

                to, fr = ['blue','red'] if diff > 0 else ['red', 'blue']
                last.put(to)
                self.msg("^6Uneven teams action^7: Moved {} from {} to {}".format(last.name, fr, to))

            else:

                last.put("spectator")
                self.msg("^6Uneven teams action^7: {} was moved to spec to even teams!".format(last.name))






    def cmd_version(self, player, msg, channel):
        self.check_version(channel=channel)

    @minqlx.thread
    def check_version(self, player=None, channel=None):
        url = "https://raw.githubusercontent.com/dsverdlo/minqlx-plugins/master/{}.py".format(self.__class__.__name__)
        res = requests.get(url)
        last_status = res.status_code
        if res.status_code != requests.codes.ok: return
        for line in res.iter_lines():
            if line.startswith(b'VERSION'):
                line = line.replace(b'VERSION = ', b'')
                line = line.replace(b'"', b'')
                # If called manually and outdated
                if channel and VERSION.encode() != line:
                    channel.reply("^7Currently using ^3iou^7one^4girl^7's ^6{}^7 plugin ^1outdated^7 version ^6{}^7.".format(self.__class__.__name__, VERSION))
                # If called manually and alright
                elif channel and VERSION.encode() == line:
                    channel.reply("^7Currently using ^3iou^7one^4girl^7's latest ^6{}^7 plugin version ^6{}^7.".format(self.__class__.__name__, VERSION))
                # If routine check and it's not alright.
                elif player and VERSION.encode() != line:
                    time.sleep(15)
                    try:
                        player.tell("^3Plugin update alert^7:^6 {}^7's latest version is ^6{}^7 and you're using ^6{}^7!".format(self.__class__.__name__, line.decode(), VERSION))
                    except Exception as e: minqlx.console_command("echo {}".format(e))
                return



    def help_get_last(self):

        teams = self.teams()

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

        minqlx.console_command("echo Picked {} from the {} team.".format(lowest_player.name, lowest_player.team))
        return lowest_player
