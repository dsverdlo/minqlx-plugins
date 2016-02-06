# This is a plugin created by iouonegirl(@gmail.com)
# Copyright (c) 2016 iouonegirl
# https://github.com/dsverdlo/minqlx-plugins
#
# You are free to modify this plugin to your custom,
# except for the version command related code.
#
# Thanks to Minkyn for his input on this plugin.
#
# Its purpose is to balance the teams out. For now we don't
# have ways to compare players, so that might be added later
# for now it can move players by name, and perform an action
# to the lowest score. (or person last to join)
#
# Update: the original balance plugin now balances people on elo.
# this plugin does improve upon it by vetoing NO to shuffles on
# uneven teams, and kicking people if they fall below server elo
# requirements
#
# Uses:
# - qlx_elo_limit_min "0"
# - qlx_elo_limit_max "1600"
# - qlx_elo_games_needed "10"
# - qlx_elo_kick "1"
# - qlx_elo_block_connecters "0"


import minqlx
import requests
import itertools
import threading
import random
import time
import os

from minqlx.database import Redis

VERSION = "v0.45"

# Add a little bump to the boundary for regulars.
# This list must be in ordered lists of [games_needed, elo_bump] from small to big
# E.g. [ [25,100],  [50,200],  [75,400],  [100,800] ]
# --> if a player has played 60 games on our server -> he reaches [50,200] and the upper elo limit adds 200
# To disable service: set BOUNDARIES = []
BOUNDARIES = [ [50,100], [75,200], [100,400] ]

# If this is True, a message will be printed on the screen of the person who should spec when teams are uneven
CP = True
CP_MESS = "\n\n\nTeams are uneven. You will be forced to spec."

# Default action to be performed when teams are uneven:
# Options: spec, slay, ignore
DEFAULT_LAST_ACTION = "spec"

# Database Keys
TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
PLAYER_KEY = "minqlx:players:{}"
LAST_KEY = "minqlx:last"
COMPLETED_KEY = PLAYER_KEY + ":games_completed"
LEFT_KEY = PLAYER_KEY + ":games_left"

# Yep
EXCEPTIONS_FILE = "exceptions.txt"

# Elo retrieval vars
EXT_SUPPORTED_GAMETYPES = ("ca", "ctf", "dom", "ft", "tdm", "duel", "ffa")
RATING_KEY = "minqlx:players:{0}:ratings:{1}" # 0 == steam_id, 1 == short gametype.
MAX_ATTEMPTS = 3
CACHE_EXPIRE = 60*30 # 30 minutes TTL.
DEFAULT_RATING = 1500
SUPPORTED_GAMETYPES = ("ca", "ctf", "dom", "ft", "tdm")


class mybalance(minqlx.Plugin):
    def __init__(self):
        super().__init__()

        # set cvars once. EDIT THESE IN SERVER.CFG!
        self.set_cvar_once("qlx_elo_limit_min", "0")
        self.set_cvar_once("qlx_elo_limit_max", "1600")
        self.set_cvar_once("qlx_elo_games_needed", "10")
        self.set_cvar_once("qlx_balanceApi", "elo")
        self.set_cvar_once("qlx_elo_kick", "1")
        self.set_cvar_once("qlx_elo_block_connectors", "0")

        # get cvars
        self.ELO_MIN = int(self.get_cvar("qlx_elo_limit_min"))
        self.ELO_MAX = int(self.get_cvar("qlx_elo_limit_max"))
        self.GAMES_NEEDED = int(self.get_cvar("qlx_elo_games_needed"))

        self.prevent = False
        self.last_action = DEFAULT_LAST_ACTION
        self.jointimes = {}

        # steam_id : [name, elo]
        self.kicked = {}

        # collection of [steam_id, name, thread]
        self.kickthreads = []

        self.ratings_lock = threading.RLock()
        # Keys: steam_id - Items: {"ffa": {"elo": 123, "games": 321, "local": False}, ...}
        self.ratings = {}

        self.exceptions = []
        self.cmd_help_load_exceptions(None, None, None)

        self.add_command("prevent", self.cmd_prevent_last, 2)
        self.add_command("last", self.cmd_last_action, 2, usage="[SLAY|SPEC|IGNORE]")
        self.add_command(("load_exceptions", "reload_exceptions"), self.cmd_help_load_exceptions, 3)
        self.add_command("add_exception", self.cmd_add_exception, 3, usage="<name>|<steam_id> <name>")
        self.add_command("elokicked", self.cmd_elo_kicked)
        self.add_command("remkicked", self.cmd_rem_kicked, 2, usage="<id>")
        self.add_command(("nokick", "dontkick"), self.cmd_nokick, 2, usage="[<name>]")
        self.add_command(("v_mybalance", "version_mybalance"), self.cmd_version)
        self.add_command(("limit", "limits", "elolimit"), self.cmd_elo_limit)
        self.add_command(("elomin", "minelo"), self.cmd_min_elo, 3, usage="[ELO]")
        self.add_command(("elomax", "maxelo"), self.cmd_max_elo, 3, usage="[ELO]")
        self.add_command(("rankings", "elotype"), self.cmd_elo_type, usage="[A|B]")
        self.add_hook("team_switch", self.handle_team_switch)
        self.add_hook("round_end", self.handle_round_end)
        self.add_hook("round_countdown", self.handle_round_count)
        self.add_hook("player_connect", self.handle_player_connect)
        self.add_hook("player_disconnect", self.handle_player_disconnect)

        self.add_command(("setrating", "setelo"), self.cmd_setrating, 3, usage="<id>|<name> <rating>")
        self.add_command(("getrating", "getelo", "elo"), self.cmd_getrating, usage="<id>|<name> [gametype]")
        self.add_command(("remrating", "remelo"), self.cmd_remrating, 3, usage="<id>|<name>")

        self.unload_overlapping_commands()

    @minqlx.delay(1)
    def unload_overlapping_commands(self):
        try:
            balance = minqlx.Plugin._loaded_plugins['balance']
            remove_commands = set(['setrating', 'getrating', 'remrating'])
            for cmd in balance.commands.copy():
                if remove_commands.intersection(cmd.name):
                    balance.remove_command(cmd.name, cmd.handler)
        except Exception as e:
            pass

    def cmd_elo_type(self, player, msg, channel):
        if len(msg) < 2:
            if self.get_cvar('qlx_balanceApi') == 'elo':
                channel.reply("^7The server is retrieving A (normal) rankings.")
            elif self.get_cvar('qlx_balanceApi') == 'elo_b':
                channel.reply("^7The server is retrieving with B (fun server) rankings.")
            return
        elif len(msg) < 3:
            # If the player doesnt have the permission to change it
            if not self.db.has_permission(player, 3):
                player.tell("^6You don't have the required permission (3) to perform this action. ")
                return minqlx.RET_STOP_ALL
            # If there was not a correct ranking type given
            rankings = {'a':'elo', 'b': 'elo_b'}
            if not (msg[1].lower() in rankings):
                return minqlx.RET_USAGE
            self.set_cvar('qlx_balanceApi', rankings[msg[1].lower()])
            channel.reply("^7Switched to ^6{}^7 rankings.".format(msg[1].upper()))
            return



    def cmd_min_elo(self, player, msg, channel):
        if len(msg) < 2:
            channel.reply("^7The minimum elo required for this server is: ^6{}^7.".format(self.ELO_MIN))
        elif len(msg) < 3:
            try:
                new_elo = int(msg[1])
                assert new_elo >= 0
            except:
                return minqlx.RET_USAGE
            self.ELO_MIN = new_elo
            channel.reply("^7The server minimum elo has been temporarily set to: ^6{}^7.".format(new_elo))
        else:
            return minqlx.RET_USAGE

    def cmd_max_elo(self, player, msg, channel):
        if len(msg) < 2:
            channel.reply("^7The maximum elo set for this server is: ^6{}^7.".format(self.ELO_MAX))
        elif len(msg) < 3:
            try:
                new_elo = int(msg[1])
                assert new_elo >= 0
            except:
                return minqlx.RET_USAGE
            self.ELO_MAX = new_elo
            channel.reply("^7The server maximum elo has been temporarily set to: ^6{}^7.".format(new_elo))
        else:
            return minqlx.RET_USAGE

    def cmd_elo_limit(self, player, msg, channel):
        if int(self.get_cvar('qlx_elo_block_connecters')):
            self.msg("^7The server will block players upon connection who fall outside [^6{}^7-^6{}^7].".format(self.ELO_MIN, self.ELO_MAX))
        elif int(self.get_cvar('qlx_elo_kick')):
            self.msg("^7The server will kick players who fall outside [^6{}^7-^6{}^7].".format(self.ELO_MIN, self.ELO_MAX))
        else:
            self.msg("^7Players who don't have a skill rating between ^6{} ^7and ^6{} ^7are only allowed to spec.".format(self.ELO_MIN, self.ELO_MAX))



    # View a list of kicked players with their ID and elo
    def cmd_elo_kicked(self, player, msg, channel):
        n = 0
        if not self.kicked:
            channel.reply("No players kicked since plugin (re)start.")
        for sid in self.kicked:
            name, elo = self.kicked[sid]
            m = "^7{}: ^6{}^7 - ^6{}^7 - ^6{}".format(n, sid, elo, name)
            channel.reply(m)
            n += 1

    def cmd_rem_kicked(self, player, msg, channel):
        if len(msg) < 2:
            return minqlx.RET_USAGE

        try:
            n = int(msg[1])
            assert 0 <= n < len(self.kicked)
        except:
            return minqlx.RET_USAGE

        for sid in self.kicked.copy():
            if not n:
                name, elo = self.kicked[sid]
                del self.kicked[sid]
            else:
                n -= 1
        channel.reply("^7Successfully removed ^6{}^7 (elo {}) from the list.".format(name, elo))

    def cmd_nokick(self, player, msg, channel):
        def dontkick(kickthread):
            sid, nam, thr = kickthread
            thr.stop()
            if sid in self.kicked:
                del self.kicked[sid]

            new_kickthreats = []
            for kt in self.kickthreads:
                if kt[0] != sid:
                    new_kickthreats.append(kt)
            self.kickthreads = new_kickthreats

            try:
                self.find_player(nam)[0].unmute()
            except:
                pass
            channel.reply("^7An admin has prevented {} from being kicked.".format(nam))

        if not self.kickthreads:
                player.tell("^6Psst^7: There are no people being kicked right now.")
                return minqlx.RET_STOP_ALL

        # if there is only one
        if len(self.kickthreads) == 1:
            dontkick(self.kickthreads[0])
            return

        # If no arguments given
        if len(msg) < 2:
            _names = map(lambda _el: _el[1], self.kickthreads)
            player.tell("^6Psst^7: did you mean ^6{}^7?".format("^7 or ^6".join(_names)))
            return minqlx.RET_STOP_ALL

        # If a search term, name, was given
        else:

            match_threads = [] # Collect matching names
            new_threads = [] # Collect non-matching threads

            for kt in self.kickthreads:
                if msg[1] in kt[1]:
                    match_threads.append(kt)
                else:
                    new_threads.append(kt)

            # If none of the threads had a name like that
            if not match_threads:
                player.tell("^6Psst^7: no players matched '^6{}^7'?".format(msg[1]))
                return minqlx.RET_STOP_ALL

            # If there was one result:
            if len(match_threads) == 1:
                self.kickthreads = new_threads
                dontkick(match_threads.pop())
                return

            # If multiple results were found:
            else:
                _names = map(lambda el: el[1], match_threads)
                player.tell("^6Psst^7: did you mean ^6{}^7?".format("^7 or ^6".join(_names)))
                return minqlx.RET_STOP_ALL






    def cmd_add_exception(self, player, msg, channel):
        try:
            # more than 2 arguments = NO NO
            if len(msg) > 3:
                return minqlx.RET_USAGE

            # less than 2 arguments is NOT OKAY if it was with a steam id
            if len(msg) < 3 and len(msg[1]) == 17:
                return minqlx.RET_USAGE

            # if steam_id given
            if len(msg[1]) == 17:
                add_sid = int(msg[1])
                add_nam = msg[2]

            # if name given
            else:
                target = self.find_by_name_or_id(player, msg[1])
                if not target:
                    return minqlx.RET_STOP_ALL
                add_sid = target.steam_id
                add_nam = msg[2] if len(msg) == 3 else target.name


            script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
            abs_file_path = os.path.join(script_dir, EXCEPTIONS_FILE)
            with open (abs_file_path, "r") as file:
                for line in file:
                    sid, name = line.split(" ")
                    if int(sid) == add_sid:
                        player.tell("^6Psst: ^7This ID is already in the exception list under name ^6{}^7!".format(name))
                        return minqlx.RET_STOP_ALL

            with open (abs_file_path, "a") as file:
                file.write("{} {}\n".format(add_sid, add_nam))

            if not add_sid in self.exceptions:
                self.exceptions.append(add_sid)
            if add_sid in self.kicked:
                del self.kicked[add_sid]
            player.tell("^6Psst: ^2Succesfully ^7added ^6{} ^7to the exception list.".format(add_nam))
            return minqlx.RET_STOP_ALL

        except IOError as e:
            player.tell("^6Psst: IOError: ^7{}".format(e))

        except ValueError as e:
            return minqlx.RET_USAGE

        except Exception as e:
            player.tell("^6Psst: ^1Error: ^7{}".format(e))
        return minqlx.RET_STOP_ALL


    # Load a list of exceptions
    def cmd_help_load_exceptions(self, player, msg, channel):
        try:
            script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
            abs_file_path = os.path.join(script_dir, EXCEPTIONS_FILE)
            with open (abs_file_path, "r") as file:
                excps = []
                n = 0
                for line in file:
                    if line.startswith("#"): continue # comment lines
                    sid, name = line.split(" ")
                    try:
                        excps.append(int(sid))
                        if player:
                            player.tell("^6Psst: ^2Loaded: ^7{} ({})".format(sid, name.strip('\n\r\t')))

                        n += 1
                    except:
                        continue

                self.exceptions = excps
                if player:
                    minqlx.CHAT_CHANNEL.reply("^2Succesfully loaded {} exceptions".format(n))

        except IOError as e:
            try:
                script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
                abs_file_path = os.path.join(script_dir, EXCEPTIONS_FILE)
                with open(abs_file_path,"a+") as f:
                    f.write("# This is a commented line because it starts with a '#'\n")
                    f.write("# Every exception on a newline, format: STEAMID NAME\n")
                    f.write("76561198045154609 iouonegirl\n")
                minqlx.CHAT_CHANNEL.reply("^6mybalance plugin^7: No exception list found, so I made one myself.")
            except:
                minqlx.CHAT_CHANNEL.reply("^1Error: ^7reading and creating exception list: {}".format(e))

        except Exception as e:
            minqlx.CHAT_CHANNEL.reply("^1Error: ^7reading exception list: {}".format(e))



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


    def handle_player_connect(self, player):
        # If admin, check version number
        if self.db.has_permission(player, 5):
            self.check_version(player=player)

        # If you are not an exception, you must be checked for elo limit
        if not (player.steam_id in self.exceptions):

            if int(self.get_cvar("qlx_elo_block_connecters")):
                try:
                    url = "http://qlstats.net:8080/{elo}/{}".format(player.steam_id, elo=self.get_cvar('qlx_balanceApi'))
                    res = requests.get(url)
                    if res.status_code != requests.codes.ok: raise
                    js = res.json()
                    gt = self.game.type_short
                    if "players" not in js: raise
                    for p in js["players"]:
                        if int(p["steamid"]) == player.steam_id and gt in p:
                            eval_elo = self.evaluate_elo_games(player, p[gt]['elo'], p[gt]['games'])
                            if eval_elo:
                                return "^1Sorry, but your skill rating {} is too {}! Accepted ratings: {} - {}".format(eval_elo[1], eval_elo[0], self.ELO_MIN, self.ELO_MAX)
                except Exception as e:
                    minqlx.console_command("echo Error: {}".format(e))
                    pass
            else:
                self.fetch(player, self.game.type_short, self.callback)


        # Record their join times regardless
        self.jointimes[player.steam_id] = time.time()

    def handle_player_disconnect(self, player, reason):
        if player.steam_id in self.jointimes:
            del self.jointimes[player.steam_id]

        new_kickthreads = []
        for kt in self.kickthreads:
            if kt[0] != player.steam_id:
                new_kickthreads.append(kt)
            else:
                try:
                    thread = kt[2]
                    thread.stop()
                except:
                    pass
        self.kickthreads = new_kickthreads


    def handle_team_switch(self, player, old, new):
        if new in ['red', 'blue']:
            if player.steam_id in self.kicked:
                player.put("spectator")
                if self.get_cvar("qlx_elo_kick") == "1":
                    kickmsg = "so you'll be kicked shortly..."
                else:
                    kickmsg = "but you are free to keep watching."
                player.tell("^6You do not meet the ELO requirements to play on this server, {}".format(kickmsg))
                player.center_print("^6You do not meet the ELO requirements to play on this server, {}".format(kickmsg))



    @minqlx.thread
    def balance_before_start(self, roundnumber):
        def is_even(n):
            return n % 2 == 0

        # Calculate the difference between teams (optional excluded teams argument)
        def red_min_blue(t = False):
            if not t: t = self.teams()
            return len(t['red']) - len(t['blue'])

        # Return a copy of the teams without the given player
        def exclude_player(p):
            t = self.teams().copy()
            if p in t['red']: t['red'].remove(p)
            if p in t['blue']: t['blue'].remove(p)
            return t

        # Wait until round almost starts
        countdown = int(self.get_cvar('g_roundWarmupDelay'))
        if self.game.type_short == "ft":
            countdown = int(self.get_cvar('g_freezeRoundDelay'))
        time.sleep(max(countdown / 1000 - 0.5, 0))

        # Grab the teams
        teams = self.teams()
        player_count = len(teams["red"] + teams["blue"])

        # If it is the last player, don't do this and let the game finish normally
        if player_count == 1:
            return

        # If the last person is prevented or ignored to spec, we need to exclude him to balance the rest.
        excluded_teams = False

        # While there is a difference in teams of more than 1
        while abs(red_min_blue(excluded_teams)) >= 1:

            diff = red_min_blue(excluded_teams)
            last = self.algo_get_last(excluded_teams)

            if is_even(diff): # one team has an even amount of people more than the other

                to, fr = ['blue','red'] if diff > 0 else ['red', 'blue']
                last.put(to)
                self.msg("^6Uneven teams action^7: Moved {} from {} to {}".format(last.name, fr, to))

            else: # there is an odd number of uneven, then one will have to spec

                if self.prevent or self.last_action == "ignore":
                    excluded_teams = exclude_player(last)
                    self.msg("^6Uneven teams^7: {} will not be moved to spec".format(last.name))
                else:
                    last.put("spectator")
                    self.msg("^6Uneven teams action^7: {} was moved to spec to even teams!".format(last.name))





    def cmd_last_action(self, player, msg, channel):
        if len(msg) < 2:
            return channel.reply("^7The current action when teams are uneven is: ^6{}^7.".format(self.last_action))

        if msg[1] not in ["slay", "spec", "ignore"]:
            return minqlx.RET_USAGE

        self.last_action = msg[1]
        channel.reply("^7Action has been succesfully changed to: ^6{}^7.".format(msg[1]))

    # At the end of a round, prevent is reset back to false.
    # This gives us 10 seconds to prevent slaying before the
    # next round starts
    def handle_round_end(self, data):
        self.prevent = False

    def handle_round_count(self, round_number):
        def is_even(n):
            return n % 2 == 0

        def red_min_blue():
            t = self.teams()
            return len(t['red']) - len(t['blue'])

        # Grab the teams
        teams = self.teams()
        player_count = len(teams["red"] + teams["blue"])


        # If there is a difference in teams of more than 1
        diff = red_min_blue()
        to, fr = ['blue', 'red'] if diff > 0 else ['red','blue']
        last = self.algo_get_last()
        n = int(abs(diff) / 2)
        if abs(diff) >= 1:
            if is_even(diff):
                n = last.name if n == 1 else "{} players".format(n)
                self.msg("^6Uneven teams detected!^7 At round start i'll move {} to {}".format(n, to))
            else:
                m = 'lowest player' if n == 1 else '{} lowest players'.format(n)
                m = " and move the {} to {}".format(m, to) if n else ''
                self.msg("^6Uneven teams detected!^7 Server will auto spec {}{}.".format(last.name, m))

        self.balance_before_start(round_number)

    def cmd_prevent_last(self, player, msg, channel):
        """A command to prevent the last player on a team being kicked if
        teams are magically balanced """
        self.prevent = True
        channel.reply("^7You will prevent the last player to be acted on at the start of next round.")


    def cmd_setrating(self, player, msg, channel):
        if len(msg) < 3:
            return minqlx.RET_USAGE

        try:
            sid = int(msg[1])
            assert len(msg[1]) == 17
            name = sid
        except:
            target_player = self.find_by_name_or_id(player, msg[1])
            if not target_player: return minqlx.RET_STOP_ALL
            sid = target_player.steam_id
            name = target_player.name

        try:
            rating = int(msg[2])
        except ValueError:
            channel.reply("Invalid rating.")
            return minqlx.RET_STOP_ALL

        gt = self.game.type_short
        self.db[RATING_KEY.format(sid, gt)] = rating

        # If we have the player cached, set the rating.
        with self.ratings_lock:
            if sid in self.ratings and gt in self.ratings[sid]:
                self.ratings[sid][gt]["elo"] = rating
                self.ratings[sid][gt]["local"] = True
                self.ratings[sid][gt]["time"] = -1

        channel.reply("{}'s {} rating has been set to ^6{}^7.".format(name, gt.upper(), rating))

    def cmd_remrating(self, player, msg, channel):
        if len(msg) < 2:
            return minqlx.RET_USAGE

        try:
            sid = int(msg[1])
            assert len(msg[1]) == 17
            name = sid
        except:
            target_player = self.find_by_name_or_id(player, msg[1])
            if not target_player: return minqlx.RET_STOP_ALL
            sid = target_player.steam_id
            name = target_player.name

        gt = self.game.type_short
        del self.db[RATING_KEY.format(sid, gt)]

        # If we have the player cached, remove the game type.
        with self.ratings_lock:
            if sid in self.ratings and gt in self.ratings[sid]:
                del self.ratings[sid][gt]

        channel.reply("{}'s locally set {} rating has been deleted.".format(name, gt.upper()))

    def cmd_getrating(self, player, msg, channel):
        if len(msg) == 1:
            target_player = player
        else:
            try:
                sid = int(msg[1])
                assert len(msg[1]) == 17
                target_player = self.player(sid)
            except:
                target_player = self.find_by_name_or_id(player, msg[1])
                if not target_player: return minqlx.RET_STOP_ALL
                sid = target_player.steam_id
                name = target_player.name

        if len(msg) > 2:
            if msg[2].lower() in EXT_SUPPORTED_GAMETYPES:
                gt = msg[2].lower()
            else:
                player.tell("Invalid gametype. Supported gametypes: {}"
                    .format(", ".join(EXT_SUPPORTED_GAMETYPES)))
                return minqlx.RET_STOP_ALL
        else:
            gt = self.game.type_short
            if gt not in EXT_SUPPORTED_GAMETYPES:
                player.tell("This game mode is not supported by the mybalance plugin.")
                return minqlx.RET_STOP_ALL

        self.fetch(target_player or sid, gt, self.callback_elo)

    # ====================================================================
    #                               HELPERS
    # ====================================================================

    def find_players(self, query):
        players = []
        for p in self.find_player(query):
            if p not in players:
                players.append(p)
        return players

    def delayact(self, messages, interval = 1):
        threading.Thread(target=self.thread_list, args=(messages, interval)).start()

    def thread_list(self, items, interval):
        for m in items:
            if m: m() # allow "" or None to be used as a skip
            time.sleep(interval)

    def find_time(self, player):
        if not (player.steam_id in self.jointimes):
            self.jointimes[player.steam_id] = time.time()
        return self.jointimes[player.steam_id]

    def is_even(self, number):
        return number % 2 == 0

    def is_odd(self, number):
        return not self.is_even(number)

    def put_or_tell(self, player, msg, team):
        def list_alternatives(players, indent=2):
            out = ""
            for p in players:
                out += " " * indent
                out += "{}^6:^7 {}\n".format(p.id, p.name)
            player.tell(out[:-1])

        player_list = self.players()
        if not player_list:
            player.tell("There are no players connected at the moment.")

        else:
            players = self.find_players(msg[1])
            if players:
                if len(players) == 1:
                    players[0].put(team)
                else:
                    player.tell("A total of ^6{}^7 players matched:".format(len(players)))
                    list_alternatives(players)
            else:
                player.tell("Sorry, but no players matched your tokens.")

    def algo_get_last(self, excluded_teams = False):
        # Find the player to be acted upon. If there are more than 1 rounds
        # played, we will take the lowest score. Otherwise the last to join

        # If teams are even, just return
        teams = excluded_teams or self.teams()


        # See which team is bigger than the other
        if len(teams["red"]) < len(teams["blue"]):
            bigger_team = teams["blue"].copy()
        else:
            bigger_team = teams["red"].copy()

        if (self.game.red_score + self.game.blue_score) >= 1:

            minqlx.console_command("echo Picking someone to {} based on score".format(self.last_action))
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

            minqlx.console_command("echo Picking someone to {} based on join times.".format(self.last_action))
            bigger_team.sort(key = lambda el: self.find_time(el), reverse=True)
            lowest_player = bigger_team[0]

        minqlx.console_command("echo Picked {} from the {} team.".format(lowest_player.name, lowest_player.team))
        return lowest_player



    @minqlx.thread
    def fetch(self, player, gt, callback):
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

            for p in js["players"]:
                _sid = int(p["steamid"])
                if _sid == sid: # got our player
                    if gt not in p:
                        return minqlx.console_command("echo No {} rating for {}".format(gt, _sid))
                    _gt = p[gt]
                    return callback(player, _gt["elo"], _gt["games"])


        minqlx.console_command("echo Problem fetching elo: " + str(last_status))
        return

    def callback_elo(self, player, elo = 0, games=0):
        if type(player) in [str, int]:
            name = player
            sid = player
        else:
            name = player.name
            sid = player.steam_id

        m = "{} ".format(name)
        elos = []
        key = RATING_KEY.format(sid, self.game.type_short)
        if key in self.db:
            dbelo = int(self.db[key])
            elos.append("^7local {} elo: ^6{}".format(self.game.type_short.upper(), dbelo))
        #if elo and games:
        elos.append("^7qlstats.net {} elo: ^6{} ({} games)".format(self.game.type_short.upper(), elo, games))

        if elos: minqlx.CHAT_CHANNEL.reply("^6{}".format(m) + " ^7, ".join(elos) + "^7.")


    def help_start_kickthread(self, player, elo, highlow):
        class kickThread(threading.Thread):
            def __init__(self, plugin, player, elo):
                threading.Thread.__init__(self)
                self.plugin = plugin
                self.player = player
                self.elo = elo
                self.highlow = highlow
                self.go = True
            def try_mess(self):
                time.sleep(4)
                if self.plugin.get_cvar("qlx_elo_kick") == "1":
                    kickmsg = "so you'll be ^6kicked ^7shortly..."
                else:
                    kickmsg = "but you are free to keep watching."
                self.plugin.msg("^7Sorry, {} your elo ({}) doesn't meet the server requirements, {}".format(self.player.name, self.elo, kickmsg))
            def try_mute(self):
                time.sleep(4)
                self.player = self.plugin.find_player(self.player.name)[0]
                if not self.player: self.stop()
                if self.go and self.plugin.get_cvar("qlx_elo_kick") == "1": self.player.mute()
            def try_kick(self):
                if self.plugin.get_cvar("qlx_elo_kick") == "0": return
                time.sleep(14)
                self.player = self.plugin.find_player(self.player.name)[0]
                if not self.player: self.stop()
                if self.go: self.player.kick("^1GOT KICKED!^7 Elo ({}) was too {} for this server.".format(self.elo, self.highlow))
            def run(self):
                self.try_mute()
                self.try_mess()
                self.try_kick()
                self.stop()
            def stop(self):
                self.go = False
                new_kickthreads = []
                for kt in self.plugin.kickthreads:
                    if kt[0] != self.player.steam_id:
                        new_kickthreads.append(kt)
                self.plugin.kickthreads = new_kickthreads
                del self

        t = kickThread(self, player, elo)
        t.start()
        self.kickthreads.append([player.steam_id, player.clean_name.lower(), t])


    def callback(self, player, elo, games):
        eval_elo = self.evaluate_elo_games(player, elo, games)
        if eval_elo:
            self.kicked[player.steam_id] = [player.name or "unknown_name", eval_elo[1]]
            self.help_start_kickthread(player, eval_elo[1], eval_elo[0])


    def evaluate_elo_games(self, player, elo, games):

        key = RATING_KEY.format(player.steam_id, self.game.type_short)
        if (key in self.db):
            elo = int(self.db[key])

        try:
            completed = int(self.db[COMPLETED_KEY.format(player.steam_id)])
        except:
            completed = 0
        try:
            left = int(self.db[LEFT_KEY.format(player.steam_id)])
        except:
            left = 0

        max_elo = self.ELO_MAX
        for threshold, boundary in reversed(BOUNDARIES):
            if left + completed >= threshold:
                max_elo += boundary
                break

        if elo < self.ELO_MIN:
            if games < self.GAMES_NEEDED:
                self.msg("{}'s elo ({}) is below the server limit ({}), but they don't have enough tracked games yet ({}/{}).".format(player.name, elo, self.ELO_MIN, games, self.GAMES_NEEDED))
                return
            return ['low', elo]
        if max_elo < elo:
            if games < self.GAMES_NEEDED:
                self.msg("{}'s elo ({}) is above the server limit ({}), but they don't have enough tracked games yet ({}/{}).".format(player.name, elo, self.ELO_MAX, games, self.GAMES_NEEDED))
                return
            return ['high', elo]

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
            ident = int(target)
            target_player = None
            if ident >= 0 and ident < 64:
                target_player = self.player(ident)
                ident = target_player.steam_id

            # Add the found ID if the player was not already found
            if target_player and not (target_player in target_players):
                target_players.append(target_player)
        except:
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