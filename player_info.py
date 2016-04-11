# This is a plugin created by iouonegirl(@gmail.com)
# Copyright (c) 2016 iouonegirl + Minkyn
# https://github.com/dsverdlo/minqlx-plugins
#
# You are free to modify this plugin to your custom,
# except for the version command related code.
#
# Its purpose is to display some information about the players.
# When players fall off the scoreboard, they are now also able
# to view their information
#
# Uses:
# - qlx_pinfo_display_auto "0"
# - qlx_pinfo_show_deactivated "1"
#       ^ (If this is 1 then a warning will be shown of players who are deactivated on qlstats)

import minqlx
import requests
import itertools
import threading
import random
import time
import os

VERSION = "v0.27"

PLAYER_KEY = "minqlx:players:{}"
COMPLETED_KEY = PLAYER_KEY + ":games_completed"
LEFT_KEY = PLAYER_KEY + ":games_left"

# Elo retrieval vars
EXT_SUPPORTED_GAMETYPES = ("ca", "ctf", "dom", "ft", "tdm", "duel", "ffa")
RATING_KEY = "minqlx:players:{0}:ratings:{1}" # 0 == steam_id, 1 == short gametype.
MAX_ATTEMPTS = 3
CACHE_EXPIRE = 60*30 # 30 minutes TTL.
DEFAULT_RATING = 1500
SUPPORTED_GAMETYPES = ("ca", "ctf", "dom", "ft", "tdm")


class player_info(minqlx.Plugin):
    def __init__(self):
        super().__init__()

        # set cvars once. EDIT THESE IN SERVER.CFG
        self.set_cvar_once("qlx_balanceApi", "elo")
        self.set_cvar_once("qlx_pinfo_display_auto", "0")
        self.set_cvar_once("qlx_pinfo_show_deactivated", "1")

        self.add_command("info", self.cmd_player_info,  usage="[<id>|<name>]")
        self.add_command("scoreboard", self.cmd_scoreboard, usage="[<id>|<name>]")
        self.add_command(("v_player_info", "version_player_info"), self.cmd_version)
        self.add_command("update", self.cmd_autoupdate, 5, usage="<plugin>|all")
        self.add_command(("allelo", "allelos", "aelo", "eloall"), self.cmd_all_elos, usage="[<id>|<name>]")

        self.add_hook("player_connect", self.handle_player_connect, priority=minqlx.PRI_LOWEST)


    def handle_player_connect(self, player):
        if self.get_cvar("qlx_pinfo_display_auto", int) or self.get_cvar("qlx_pinfo_show_deactivated", int):
            self.fetch(player, self.game.type_short, None)

        if self.db.has_permission(player, 5):
            self.check_version(player=player)

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


    def cmd_player_info(self, player, msg, channel):
        if len(msg) > 2:
            return minqlx.RET_USAGE

        if len(msg) < 2:
            target_player = player
        else:
            try:
                sid = int(msg[1])
                assert len(msg[1]) == 17
                target_player = sid
            except:
                target_player = self.find_by_name_or_id(player, msg[1])
                if not target_player: return minqlx.RET_STOP_EVENT

        # go fetch his elo
        self.fetch(target_player, self.game.type_short, channel)


    def cmd_all_elos(self, player, msg, channel):
        if len(msg) > 2:
            return minqlx.RET_USAGE

        if len(msg) < 2:
            target_player = player
        else:
            try:
                sid = int(msg[1])
                assert len(msg[1]) == 17
                target_player = sid
            except:
                target_player = self.find_by_name_or_id(player, msg[1])
                if not target_player: return minqlx.RET_STOP_EVENT

        # go fetch his elo
        self.fetch(target_player, None, channel)

    # Show info of people fallen off the scoreboard
    def cmd_scoreboard(self, player, msg, channel):
        def show(target):
            _n = target.name
            _s = target.stats.score
            _k = target.stats.kills
            _d = target.stats.deaths
            try:
                _p = target.stats.ping
            except:
                _p = "--" # in case of older minqlx version

            _tm = int(target.stats.time / 60000 )
            _ts = int((target.stats.time % 60000) / 1000)
            _dd = target.stats.damage_dealt
            _t = target.team
            _hc = int(target.cvars.get('handicap', 100))
            _c = '^7,'
            if _t == 'blue': _c = '^4,'
            if _t == 'red': _c = '^1,'
            if _hc < 100:
                _hc = '^7(^3{}％^7)'.format(_hc)
            else:
                _hc = ''


            message = "{}{} {k}score ^7{}{c} {k}k/d ^7{}/{}{c} {k}dmg ^7{}{c} {k}time ^7{}m{}s{c} {k}ping ^7{} "
            message = message.format(_n, _hc, _s, _k, _d, _dd, _tm, _ts, _p, c=_c, k=_c[0:-1])
            channel.reply("^7" + message)

        teams = self.teams()
        scoreboard_length = 8

        players = []
        if len(teams['red']) > scoreboard_length:
            sorted_red = sorted(teams["red"], key=lambda p: p.score, reverse=True)
            for p in sorted_red[scoreboard_length:]:
                players.append(p)
        if len(teams['blue']) > scoreboard_length:
            sorted_blue = sorted(teams['blue'], key=lambda p: p.score, reverse=True)
            for p in sorted_blue[scoreboard_length:]:
                players.append(p)

        if not players:
            channel.reply("^7No players falling off the scoreboard...")
            return

        for p in players:
            show(p)





    @minqlx.thread
    def fetch(self, player, gt, channel):
        try:
            sid = player.steam_id
        except:
            sid = player

        attempts = 0
        last_status = 0
        while attempts < MAX_ATTEMPTS:
            attempts += 1
            url = "http://qlstats.net:8080/{elo}/{}".format(sid, elo=self.get_cvar('qlx_balanceApi'))
            res = requests.get(url)
            last_status = res.status_code
            if res.status_code != requests.codes.ok:
                continue

            js = res.json()
            if "players" not in js:
                last_status = -1
                continue

            if not channel and self.get_cvar("qlx_pinfo_show_deactivated", int):
                if "deactivated" in js and js["deactivated"]:
                    self.msg("^3SERVER WARNING^7! {}^7's account has been ^1DEACTIVATED^7 on qlstats.".format(player.name))
                if not self.get_cvar("qlx_pinfo_display_auto", int):
                    return

            if not channel:
                channel = minqlx.CHAT_CHANNEL

            for p in js["players"]:
                _sid = int(p["steamid"])
                if _sid == sid: # got our player
                    # If they want all the elos
                    if not gt: return self.callback_all(player, p, channel)
                    # If the request gametype is found
                    if gt in p: return self.callback(player, p[gt]["elo"], p[gt]["games"], channel)
                    # If the gametype was not found
                    else: return self.callback(player, 0,0, channel)



        return self.callback(player, 0, 0, channel)


    def callback_all(self, player, modes, channel):
        info = []
        for mode in modes:
            if mode not in EXT_SUPPORTED_GAMETYPES: continue
            elo = modes[mode]['elo']
            games = modes[mode]["games"]
            info.append(" ^3{}^7: {} ({} games)".format(mode.upper(), elo, games))

        if not info:
            channel.reply("^6{}^7 has no tracked elos.".format(player.name))
        else:
            b = 'b' if self.get_cvar('qlx_balanceApi') == 'elo_b' else ''
            channel.reply("^6{}^7's {}ELO's: {}".format(player.name, b, ", ".join(info)))


    def callback(self, target_player, elo, games, channel):
        try:
            ident = target_player.steam_id
            name = target_player.name
        except:
            ident = target_player
            name = target_player

        try:
            completed = int(self.db[COMPLETED_KEY.format(ident)])
        except:
            completed = 0
        try:
            left = int(self.db[LEFT_KEY.format(ident)])
        except:
            left = 0


        if left + completed == 0:
            games_here_p = 1
        else:
            games_here_p = left + completed


        info = ["^6{} ^7games here".format(completed + left)]
        info[0] = info[0] + " ^7(^6{}^7 tracked {})".format(games, self.game.type_short)

        info.append("^7quit ^6{}^7％".format(round(left/(games_here_p)*100)))

        info.append("^3{} ^7{}ELO: ^6{}^7".format(self.game.type_short.upper(),'b' if self.get_cvar('qlx_balanceApi') == 'elo_b' else '', elo, games))

        return channel.reply("^6{}^7: ".format(name) + "^7, ".join(info) + "^7.")


    # ====================================================================
    #                               HELPERS
    # ====================================================================


    def find_by_name_or_id(self, player, target):
        # Find players returns a list of name-matching players
        def find_players(query):
            players = []
            for p in self.find_player(query):
                if p not in players:
                    players.append(p)
            return players

        # Tell a player which players matched
        def list_alternatives(players, indent=2):
            player.tell("A total of ^6{}^7 players matched for {}:".format(len(players),target))
            out = ""
            for p in players:
                out += " " * indent
                out += "{}^6:^7 {}\n".format(p.id, p.name)
            player.tell(out[:-1])

        # Get the list of matching players on name
        target_players = find_players(target)

        # even if we get only 1 person, we need to check if the input was meant as an ID
        # if we also get an ID we should return with ambiguity

        try:
            i = int(target)
            target_player = self.player(i)
            if not (0 <= i < 64) or not target_player:
                raise ValueError
            # Add the found ID if the player was not already found
            if not target_player in target_players:
                target_players.append(target_player)
        except ValueError:
            pass

        # If there were absolutely no matches
        if not target_players:
            player.tell("Sorry, but no players matched your tokens: {}.".format(target))
            return None

        # If there were more than 1 matches
        if len(target_players) > 1:
            list_alternatives(target_players)
            return None

        # By now there can only be one person left
        return target_players.pop()


    def cmd_autoupdate(self, player, msg, channel):
        if len(msg) < 2:
            return minqlx.RET_USAGE

        if msg[1] in [self.__class__.__name__, 'all']:
            self.update(player, msg, channel)

    @minqlx.thread
    def update(self, player, msg, channel):
        try:
            url = "https://raw.githubusercontent.com/dsverdlo/minqlx-plugins/master/{}.py".format(self.__class__.__name__)
            res = requests.get(url)
            last_status = res.status_code
            if res.status_code != requests.codes.ok: return
            script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
            abs_file_path = os.path.join(script_dir, "{}.py".format(self.__class__.__name__))
            with open(abs_file_path,"w") as f:
                f.write(res.text)
            minqlx.reload_plugin(self.__class__.__name__)
            channel.reply("^2updated ^3iou^7one^4girl^7's ^6{} ^7plugin to the latest version!".format(self.__class__.__name__))
            #self.cmd_version(player, msg, channel)
            return True
        except Exception as e :
            channel.reply("^1Update failed for {}^7: {}".format(self.__class__.__name__, e))
            return False

