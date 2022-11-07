# This is a plugin created by iouonegirl(@gmail.com)
# Copyright (c) 2016 iouonegirl
# https://github.com/dsverdlo/minqlx-plugins
#
# You are free to modify this plugin to your custom,
# except for the version command related code.
#
# Thanks to Bus Station, Minkyn, Melodeiro, BarelyMiSSeD,
# TNT and Shin0 for their input on this plugin.
#
# Its purpose is to balance the games on a server out.
# Some features of this plugin include:
# - setting up an ELO* limit (minimum and maximum values)
# - kicking players outside this limit
# - - prevent players from getting kicked with !nokick
# - allowing players outside the limit to only spec
# - blocking players outside the limit from connecting
# - - block players, but normal kick those who are close_enough
# - Uneven teams action: spec, slay, ignore
# - Display ready-up interval reminders during a long warmup
# - Optional autoshuffle before a match (disables shuffle callvotes)
# - Freezes then specs players while teams are uneven in CTF and TDM
#
#
# Uses:
# - set qlx_elo_limit_min "0"
# - set qlx_elo_limit_max "1600"
# - set qlx_elo_games_needed "10"
#
# - set qlx_mybalance_perm_allowed "2"
#       ^ (players with this perm-level will always be allowed)
#
# - set qlx_mybalance_autoshuffle "0"
#       ^ (set "1" if you want an automatic shuffle before every match)
#
# - set qlx_mybalance_exclude "0"
#       ^ (set "1" if you want to kick players without enough info/games)
#
# - set qlx_elo_kick "1"
#       ^ (set "1" to kick spectators after they joined)
#
# - set qlx_elo_block_connecters "0"
#       ^ (set "1" to block players from connecting)
#
# - set qlx_elo_close_enough "20"
#       ^ (if blocking is on, and a player's glicko differs less than N from
#          the limit, let them join for a normal kick (giving a chance to !nokick))
#         (set this to 0 to disable this feature)
#
# - set qlx_mybalance_warmup_seconds "300"
#       ^ (how many seconds of warmup before readyup messages come. Set to -1 to disable)
#
# - set qlx_mybalance_warmup_interval "60"
#       ^ (interval in seconds for readyup messages)
#
# - set qlx_mybalance_uneven_time "10"
#       ^ (for CTF and TDM, specify how many seconds to wait before balancing uneven teams)
#
# - set qlx_mybalance_elo_bump_regs "[]"
#       ^ (Add a little bump to the boundary for regulars.
#           This list must be in ordered lists of [games_needed, elo_bump] from small to big
#           E.g. "[ [25,100],  [50,200],  [75,400],  [100,800] ]"
#           --> if a player has played 60 games on our server -> he reaches [50,200] and the upper elo limit adds 200)
#
import minqlx
import requests
import itertools
import threading
import random
import time
import os
import re

from minqlx.database import Redis

VERSION = "v0.56.5"


# This code makes sure the required superclass is loaded automatically
try:
    from .iouonegirl import iouonegirlPlugin
except:
    try:
        abs_file_path = os.path.join(os.path.dirname(__file__), "iouonegirl.py")
        res = requests.get("https://raw.githubusercontent.com/dsverdlo/minqlx-plugins/master/iouonegirl.py")
        if res.status_code != requests.codes.ok: raise
        with open(abs_file_path,"a+") as f: f.write(res.text)
        from .iouonegirl import iouonegirlPlugin
    except Exception as e :
        minqlx.CHAT_CHANNEL.reply("^1iouonegirl abstract plugin download failed^7: {}".format(e))
        raise

BOUNDARIES = []

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


class mybalance(iouonegirlPlugin):
    def __init__(self):
        super().__init__(self.__class__.__name__, VERSION)

        # set cvars once. EDIT THESE IN SERVER.CFG!
        self.set_cvar_once("qlx_elo_limit_min", "0")
        self.set_cvar_once("qlx_elo_limit_max", "1600")
        self.set_cvar_once("qlx_elo_games_needed", "10")
        self.set_cvar_once("qlx_balanceApi", "elo")
        self.set_cvar_once("qlx_elo_kick", "1")
        self.set_cvar_once("qlx_elo_block_connecters", "0")
        self.set_cvar_once("qlx_mybalance_warmup_seconds", "300")
        self.set_cvar_once("qlx_mybalance_warmup_interval", "60")
        self.set_cvar_once("qlx_mybalance_autoshuffle", "0")
        self.set_cvar_once("qlx_mybalance_perm_allowed", "2")
        self.set_cvar_once("qlx_mybalance_exclude", "0")
        self.set_cvar_once("qlx_mybalance_uneven_time", "10")
        self.set_cvar_once("qlx_mybalance_elo_bump_regs", "[]")
        self.set_cvar_once("qlx_elo_close_enough", "20")

        # get cvars
        self.ELO_MIN = int(self.get_cvar("qlx_elo_limit_min"))
        self.ELO_MAX = int(self.get_cvar("qlx_elo_limit_max"))
        self.GAMES_NEEDED = int(self.get_cvar("qlx_elo_games_needed"))
        try:
            global BOUNDARIES
            BOUNDARIES = eval(self.get_cvar("qlx_mybalance_elo_bump_regs"))
            assert type(BOUNDARIES) is list
            for _e, _b in BOUNDARIES:
                assert type(_e) is int
                assert type(_b) is int
        except:
            BOUNDARIES = []

        self.prevent = False
        self.last_action = DEFAULT_LAST_ACTION
        self.jointimes = {}

        self.game_active = self.game.state == "in_progress"

        # Vars for CTF / TDM
        self.ctfplayer = False
        self.checking_balance = False

        # steam_id : [name, elo]
        self.kicked = {}

        # collection of [steam_id, name, thread]
        self.kickthreads = []

        # Collection of threads looking up elo of players {steam_id: thread }
        self.connectthreads = {}

        # Keep broadcasting warmup reminders?
        self.warmup_reminders = True

        self.ratings_lock = threading.RLock()
        # Keys: steam_id - Items: {"ffa": {"elo": 123, "games": 321, "local": False}, ...}
        self.ratings = {}

        self.exceptions = []
        self.cmd_help_load_exceptions(None, None, None)

        self.add_command("prevent", self.cmd_prevent_last, 2)
        self.add_command("last", self.cmd_last_action, 2, usage="[SLAY|SPEC|IGNORE]")
        self.add_command(("load_exceptions", "reload_exceptions", "list_exceptions", "listexceptions", "exceptions"), self.cmd_help_load_exceptions, 3)
        self.add_command(("add_exception", "elo_exception"), self.cmd_add_exception, 3, usage="<name>|<steam_id> <name>")
        self.add_command(("del_exception", "rem_exception"), self.cmd_del_exception, 3, usage="<name>|<id>|<steam_id>")
        self.add_command("elokicked", self.cmd_elo_kicked)
        self.add_command("remkicked", self.cmd_rem_kicked, 2, usage="<id>")
        self.add_command(("nokick", "dontkick"), self.cmd_nokick, 2, usage="[<name>]")
        self.add_command(("limit", "limits", "elolimit"), self.cmd_elo_limit)
        self.add_command(("elomin", "minelo"), self.cmd_min_elo, 3, usage="[ELO]")
        self.add_command(("elomax", "maxelo"), self.cmd_max_elo, 3, usage="[ELO]")
        self.add_command(("rankings", "elotype"), self.cmd_elo_type, usage="[A|B]")
        self.add_command("reminders", self.cmd_warmup_reminders, 2, usage="[ON|OFF]")
        self.add_hook("team_switch", self.handle_team_switch)
        self.add_hook("round_end", self.handle_round_end)
        self.add_hook("round_countdown", self.handle_round_count)
        self.add_hook("round_start", self.handle_round_start)
        self.add_hook("game_start", self.handle_game_start)
        self.add_hook("game_end", self.handle_game_end)
        self.add_hook("map", self.handle_map)
        self.add_hook("player_connect", self.handle_player_connect, priority=minqlx.PRI_HIGH)
        self.add_hook("player_disconnect", self.handle_player_disconnect)
        self.add_hook("game_countdown", self.handle_game_countdown)
        self.add_hook("new_game", self.handle_new_game)
        self.add_hook("vote_called", self.handle_vote_called)

        self.add_command(("setrating", "setelo"), self.cmd_setrating, 3, priority=minqlx.PRI_HIGH, usage="<id>|<name> <rating>")
        self.add_command(("getrating", "getelo", "elo"), self.cmd_getrating, priority=minqlx.PRI_HIGH, usage="<id>|<name> [gametype]")
        self.add_command(("remrating", "remelo"), self.cmd_remrating, 3, priority=minqlx.PRI_HIGH, usage="<id>|<name>")
        self.add_command("belo", self.cmd_getratings, usage="<id>|<name> [gametype]")

        #self.unload_overlapping_commands()
        self.handle_new_game() # start counting reminders if we are in warmup

        if self.game_active and self.game.type_short in ['ctf', 'tdm']:
            self.balance_before_start(self.game.type_short, True)


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
            channel.reply("^7The minimum skill rating required for this server is: ^6{}^7.".format(self.ELO_MIN))
        elif len(msg) < 3:
            try:
                new_elo = int(msg[1])
                assert new_elo >= 0
            except:
                return minqlx.RET_USAGE
            self.ELO_MIN = new_elo
            channel.reply("^7The server minimum skill rating has been temporarily set to: ^6{}^7.".format(new_elo))
        else:
            return minqlx.RET_USAGE

    def cmd_max_elo(self, player, msg, channel):
        if len(msg) < 2:
            channel.reply("^7The maximum skill rating set for this server is: ^6{}^7.".format(self.ELO_MAX))
        elif len(msg) < 3:
            try:
                new_elo = int(msg[1])
                assert new_elo >= 0
            except:
                return minqlx.RET_USAGE
            self.ELO_MAX = new_elo
            channel.reply("^7The server maximum skill ratings has been temporarily set to: ^6{}^7.".format(new_elo))
        else:
            return minqlx.RET_USAGE

    def cmd_elo_limit(self, player, msg, channel):
        if int(self.get_cvar('qlx_elo_block_connecters')):
            close_enough = self.get_cvar("qlx_elo_close_enough", int)
            if close_enough:
                close_enough = " (and normal kick when ^6{}^7 from limit)".format(close_enough)
            else:
                close_enough = ""

            self.msg("^7Players will be blocked on connection outside limits: [^6{}^7-^6{}^7]{}.".format(self.ELO_MIN, self.ELO_MAX, close_enough))
        elif int(self.get_cvar('qlx_elo_kick')):
            self.msg("^7The server will kick players who fall outside [^6{}^7-^6{}^7].".format(self.ELO_MIN, self.ELO_MAX))
        else:
            self.msg("^7Players who don't have a skill rating between ^6{} ^7and ^6{} ^7are only allowed to spec.".format(self.ELO_MIN, self.ELO_MAX))



    # View a list of kicked players with their ID and elo
    @minqlx.thread
    def cmd_elo_kicked(self, player, msg, channel):
        @minqlx.next_frame
        def reply(m):
            if player: player.tell(m)
            else: channel.reply(m)

        n = 0
        if not self.kicked:
            reply("No players kicked since plugin (re)start.")
        for sid in self.kicked:
            name, elo = self.kicked[sid]
            m = "^7{}: ^6{}^7 - ^6{}^7 - ^6{}".format(n, sid, elo, name)
            reply(m)
            n += 1
            time.sleep(0.2)
        return minqlx.RET_STOP_ALL

    def cmd_rem_kicked(self, player, msg, channel):
        if len(msg) < 2:
            return minqlx.RET_USAGE

        try:
            n = int(msg[1])
            assert 0 <= n < len(self.kicked)
        except:
            return minqlx.RET_USAGE

        counter = 0
        for sid in self.kicked.copy():
            if counter == n:
                name, elo = self.kicked[sid]
                del self.kicked[sid]
                break
            counter += 1

        channel.reply("^7Successfully removed ^6{}^7 (glicko {}) from the list.".format(name, elo))

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
                else:
                    kt[2].stop()
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
            match_id = re.search('[0-9]{17}',  msg[1])
            if match_id and match_id.group() == msg[1]:
                add_sid = int(msg[1])
                add_nam = msg[2]

            # if name given
            else:
                target = self.find_by_name_or_id(player, msg[1])
                if not target:
                    return minqlx.RET_STOP_ALL
                add_sid = target.steam_id
                add_nam = msg[2] if len(msg) == 3 else target.name

            abs_file_path = os.path.join(self.get_cvar("fs_homepath"), EXCEPTIONS_FILE)
            with open (abs_file_path, "r") as file:
                for line in file:
                    if line.startswith("#"): continue
                    split = line.split()
                    sid = split.pop(0)
                    name = " ".join(split)
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
        names = {}
        for p in self.players():
            names[p.steam_id] = p.name
        try:
            abs_file_path = os.path.join(self.get_cvar("fs_homepath"), EXCEPTIONS_FILE)
            with open (abs_file_path, "r") as file:
                excps = []
                n = 0
                if player: player.tell("^6Psst: ^7Glicko exceptions:\n")
                for line in file:
                    if line.startswith("#"): continue # comment lines
                    split = line.split()
                    sid = split.pop(0)
                    name = " ".join(split)
                    try:
                        excps.append(int(sid))
                        if player:
                            _name = names[int(sid)] if int(sid) in names else name.strip('\n\r\t')
                            player.tell("^6Psst: ^7{} ({})".format(sid, _name))

                        n += 1
                    except:
                        continue

                self.exceptions = excps
                if player:
                    player.tell("^6Open your console to see {} exceptions.".format(n))

        except IOError as e:
            try:
                abs_file_path = os.path.join(self.get_cvar("fs_homepath"), EXCEPTIONS_FILE)
                with open(abs_file_path,"a+") as f:
                    f.write("# This is a commented line because it starts with a '#'\n")
                    f.write("# Every exception on a newline, format: STEAMID NAME\n")
                    f.write("# The NAME is for a mental reference and may contain spaces\n")
                    f.write("{} (owner)\n".format(self.get_cvar('qlx_owner')))
                minqlx.CHAT_CHANNEL.reply("^6mybalance plugin^7: No exception list found, so I made one myself.")
            except:
                minqlx.CHAT_CHANNEL.reply("^1Error: ^7reading and creating exception list: {}".format(e))

        except Exception as e:
            minqlx.CHAT_CHANNEL.reply("^1Error: ^7reading exception list: {}".format(e))


    def cmd_del_exception(self, player, msg, channel):
        if len(msg) != 2:
            return minqlx.RET_USAGE
        try:
           # if steam_id given
            assert len(msg[1]) == 17
            add_sid = int(msg[1])
        except:
            # if name given
            target = self.find_by_name_or_id(player, msg[1])
            if not target:
                return minqlx.RET_STOP_ALL
            add_sid = target.steam_id

        try:
            f = open(os.path.join(self.get_cvar("fs_homepath"), EXCEPTIONS_FILE),"r+")
            d = f.readlines()
            f.seek(0)
            for i in d:
                if not i.startswith(str(add_sid)):
                    f.write(i)
                else:
                    player.tell("^6Player found and removed!")
                    if add_sid in self.exceptions:
                        self.exceptions.remove(add_sid)
                    msg = None
            f.truncate()
            f.close()
            if msg: player.tell("^6{} was not found in the exception list...".format(msg[1]))
        except:
            player.tell("^1Error^7: cannot open exception list.")
        return minqlx.RET_STOP_ALL


    def handle_vote_called(self, caller, vote, args):
        # If it is not shuffle, whatever
        if vote.lower() != "shuffle": return

        # Shuffle won't be called in ffa or duel
        if self.game.type_short in ["ffa", "duel"]: return

        # If it is shuffle and we have autoshuffle enabled...
        if self.get_cvar("qlx_mybalance_autoshuffle", int):
            self.msg("^7Callvote shuffle ^1DENIED ^7since the server will ^3autoshuffle ^7on match start.")
            return minqlx.RET_STOP_ALL



    def cmd_warmup_reminders(self, player, msg, channel):
        if len(msg) < 2 and self.warmup_reminders:
            s = self.get_cvar('qlx_mybalance_warmup_seconds')
            i = self.get_cvar('qlx_mybalance_warmup_interval')
            channel.reply("^7Warmup reminders will be displayed after {}s at {}s intervals.".format(s,i))
        elif len(msg) < 2:
            channel.reply("^7Warmup reminders have currently been turned ^6off^7.")
        elif len(msg) < 3 and msg[1].lower() in ['on', 'off']:
            if not self.warmup_reminders and (msg[1].lower() == 'on'):
                self.warmup_reminders = True
                self.check_warmup(time.time(), self.game.map)
            self.warmup_reminders = msg[1].lower() == 'on'
            channel.reply("^7Warmup reminders have been turned ^6{}^7.".format(msg[1].lower()))
        else:
            return minqlx.RET_USAGE


    # Goes off when new maps are loaded, games are aborted, games ended but stay on same map and matchstart
    @minqlx.delay(3)
    def handle_new_game(self):
        if self.game.state in ["in_progress", "countdown"]: return
        self.game_active = False
        self.checking_balance = False
        self.check_warmup(time.time(), self.game.map)

    @minqlx.thread
    def check_warmup(self, warmup, mapname):
        while self.is_game_in_warmup() and self.game_with_map_loaded(mapname) and self.warmup_reminders and \
            self.is_plugin_still_loaded() and self.is_warmup_seconds_enabled() and \
            self.is_there_more_than_one_player_joined():
            diff = time.time() - warmup # difference in seconds
            if diff >= int(self.get_cvar('qlx_mybalance_warmup_seconds')):
                pgs = minqlx.Plugin._loaded_plugins
                if 'maps' in pgs and pgs['maps'].plugin_active:
                    m = "^7Type ^2!s^7 to skip this map, or ^3ready up^7! "
                    if self.get_cvar("qlx_mybalance_autoshuffle", int):
                        m += "\nTeams will auto shuffle+balance!"
                    self.msg(m.replace('\n', ''))
                    self.center_print(m)
                else:
                    m = "^7Time to ^3ready^7 up! "
                    if self.get_cvar("qlx_mybalance_autoshuffle", int):
                        m += "\nTeams will be auto shuffled and balanced!"
                    self.msg(m.replace('\n', ''))
                    self.center_print(m)
                time.sleep(int(self.get_cvar('qlx_mybalance_warmup_interval')))
                continue
            time.sleep(1)

    def is_game_in_warmup(self) -> bool:
        if not self.game:
            return False
        
        return self.game.state == "warmup"
    
    def game_with_map_loaded(self, mapname) -> bool:
        if not self.game:
            return False
            
        return self.game.map == mapname
    
    def is_plugin_still_loaded(self) -> bool:
        return self.__class__.__name__ in minqlx.Plugin._loaded_plugins
        
    def is_warmup_seconds_enabled(self) -> bool:
        return self.get_cvar('qlx_mybalance_warmup_seconds', int) > -1
        
    def is_there_more_than_one_player_joined(self) -> bool:
        teams = self.teams()
        return len(teams["red"] + teams["blue"]) > 1
        
    @minqlx.delay(5)
    def handle_game_countdown(self):

        if self.game.type_short in ["ffa", "race"]: return

        # Make sure teams have even amount of players
        self.balance_before_start(0, True)

        # If autoshuffle is off, return
        if not int(self.get_cvar("qlx_mybalance_autoshuffle")): return

        # Do the autoshuffle
        self.center_print("*autoshuffle*")
        self.msg("^7Autoshuffle...")
        self.shuffle()

        if 'balance' in minqlx.Plugin._loaded_plugins:
            self.msg("^7Balancing on skill ratings...")
            b = minqlx.Plugin._loaded_plugins['balance']
            teams = self.teams()
            players = dict([(p.steam_id, self.game.type_short) for p in teams["red"] + teams["blue"]])
            b.add_request(players, b.callback_balance, minqlx.CHAT_CHANNEL)
        else:
            self.msg("^7Couldn't balance on skill, make sure ^6balance^7 is loaded.")




    def handle_player_connect(self, player):

        # If they joined very very very recently (like a short block from other plugins)
        if player.steam_id in self.jointimes:
            if (time.time() - self.jointimes[player.steam_id]) < 5: # dunno why 5s but should be enough
                return

        # Record their join times regardless
        self.jointimes[player.steam_id] = time.time()

        # If you are not an exception (or have high enough perm lvl);
        # you must be checked for elo limit
        if not (player.steam_id in self.exceptions or self.db.has_permission(player, self.get_cvar("qlx_mybalance_perm_allowed", int))):

            # If we don't want to block, just look up his skill rating for a kick
            if not int(self.get_cvar("qlx_elo_block_connecters")):
                self.fetch(player, self.game.type_short, self.callback)
                return

            # If want to block, check for a lookup thread. Else create one
            if not player.steam_id in self.connectthreads:
                ct = ConnectThread(self, player)
                self.connectthreads[player.steam_id] = ct
                ct.start()
                self.remove_thread(player.steam_id) # remove it after a while

            # Check if thread is ready or not
            ct = self.connectthreads[player.steam_id]
            if ct.isAlive():
                return "Fetching your skill rating..."
            try:
                res = ct._result
                if not res: return "Fetching your skill rating..."
                if res.status_code != requests.codes.ok: raise
                js = res.json()
                gt = self.game.type_short
                if "players" not in js: raise
                for p in js["players"]:
                    if int(p["steamid"]) == player.steam_id:
                        # Evaluate if their skill rating is not allowed on server
                        _elo, _games = [p[gt]['elo'], p[gt]['games']] if gt in p else [0,0]
                        eval_elo = self.evaluate_elo_games(player, _elo, _games )

                        # If it's too high, but it is close enough to the limit, start kickthread
                        if eval_elo and eval_elo[0] == "high" and (eval_elo[1] - self.ELO_MAX) <= self.get_cvar("qlx_elo_close_enough",int):
                            self.msg("^7Connecting player ({}^7)'s glicko ^6{}^7 is too high, but maybe close enough for a ^2!nokick ^7?".format(player.name, eval_elo[1]))
                            self.kicked[player.steam_id] = [player.name, eval_elo[1]]
                            self.help_start_kickthread(player, eval_elo[1], eval_elo[0])

                        # If it's too low, but close enough to the limit, start kickthread
                        elif eval_elo and eval_elo[0] == "low" and (self.ELO_MIN - eval_elo[1]) <= self.get_cvar("qlx_elo_close_enough",int):
                            self.kicked[player.steam_id] = [player.name, eval_elo[1]]
                            self.msg("^7Connecting player ({}^7)'s glicko ^6{}^7 is too low, but maybe close enough for a ^2!nokick ^7?".format(player.name, eval_elo[1]))
                            self.help_start_kickthread(player, eval_elo[1], eval_elo[0])

                        # If it's still not allowed, block connection
                        elif eval_elo:
                            return "^1Sorry, but your skill rating {} is too {}!".format(eval_elo[1], eval_elo[0])

                        # If the player was found, he will have been blocked or fetched
                        return

                # If the player we want was not returned, and we are strict, block him
                if self.get_cvar("qlx_mybalance_exclude",int):
                    return "This server requires a minimum of {} {} games".format(self.GAMES_NEEDED, self.game.type_short.upper())



            except Exception as e:
                minqlx.console_command("echo MybalanceError: {}".format(e))






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

        if self.game_active and player.team != "spectator" and self.game.type_short in ["ctf", "tdm"]:
            self.balance_before_start(self.game.type_short, True)


    def handle_team_switch(self, player, old, new):
        if new in ['red', 'blue', 'free']:
            if player.steam_id in self.kicked:
                player.put("spectator")
                if self.get_cvar("qlx_elo_kick") == "1":
                    kickmsg = "so you'll be kicked shortly..."
                else:
                    kickmsg = "but you are free to keep watching."
                player.tell("^6You do not meet the skill rating requirements to play on this server, {}".format(kickmsg))
                player.center_print("^6You do not meet the skill rating requirements to play on this server, {}".format(kickmsg))
                return

        # If the game mode has no rounds, and a player joins, set a timer
        if self.game_active and self.game.type_short in ["ctf", "tdm"]:
            teams = self.teams()
            # If someone joins, check if teams are even
            if new in ['red', 'blue']:
                if len(teams['red']) != len(teams['blue']):
                    self.msg("^7If teams will remain uneven for ^6{}^7 seconds, {} will be put to spec.".format(self.get_cvar("qlx_mybalance_uneven_time", int), player.name))
                    self.ctfplayer = player
                    self.evaluate_team_balance(player)
                else:
                    # If teams are even now, it's all good.
                    self.ctfplayer = None
            else:
                # If someone goes to spec, check later if they are still uneven
                self.ctfplayer = None # stop watching anyone
                if len(teams['red']) != len(teams['blue']):
                    self.msg("^7Uneven teams detected! If teams are still uneven in {} seconds, I will spec someone.".format(self.get_cvar("qlx_mybalance_uneven_time")))
                    if not self.checking_balance:
                        self.checking_balance = True
                        self.evaluate_team_balance()




    @minqlx.thread
    def evaluate_team_balance(self, player=None):
        @minqlx.next_frame
        def setpos(_p, _x, _y, _z):
            _p.position(x=_x, y=_y, z=_z)
            _p.velocity(reset=True)
        @minqlx.next_frame
        def cprint(_p, _m):
            if _p: _p.center_print(_m)

        if not self.game_active: return

        pos = None
        if player: pos = list(player.position())

        cvar = float(self.get_cvar("qlx_mybalance_uneven_time", int))
        while (cvar > 0):
            if not self.game_active: return
            # If there was a player to watch given, see if he is still extra
            if player:
                if self.ctfplayer:
                    if(self.ctfplayer.steam_id != player.steam_id):
                        return # different guy? return without doing anything
                else:
                    return # If there is a player but he is not tagged; return

                setpos(player, pos[0], pos[1], pos[2])
                if cvar.is_integer():
                    cprint(player, "^7Teams are uneven. ^6{}^7s until spec!".format(int(cvar)))

            time.sleep(0.1)
            cvar -= 0.1

        # Time's up; time to check the teams
        self.checking_balance = False
        self.balance_before_start(self.game.type_short, True)




    @minqlx.thread
    def balance_before_start(self, roundnumber, direct=False):
        @minqlx.next_frame # Game logic should never be done in a thread directly
        def game_logic(func): func()
        @minqlx.next_frame
        def slay_player(p): p.health = 0 # assignment wasnt allowed in lambda

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
        if not direct: time.sleep(max(countdown / 1000 - 0.8, 0))

        # Grab the teams
        teams = self.teams()
        player_count = len(teams["red"] + teams["blue"])

        # If it is the last player, don't do this and let the game finish normally
        # OR if there is no match going on
        if player_count == 1 or not self.game_active:
            return

        # Double check to not do anything you don't have to
        if self.game.type_short == "ca":
            if self.game.roundlimit in [self.game.blue_score, self.game.red_score]:
                return

        if self.game.type_short == "tdm":
            if self.game.fraglimit in [self.game.blue_score, self.game.red_score]:
                return

        if self.game.type_short == "ctf":
            if self.game.capturelimit in [self.game.blue_score, self.game.red_score]:
                return

        # If the last person is prevented or ignored to spec, we need to exclude him to balance the rest.
        excluded_teams = False

        # While there is a difference in teams of more than 1
        while abs(red_min_blue(excluded_teams)) >= 1:

            last = self.algo_get_last(excluded_teams)
            diff = red_min_blue(excluded_teams)

            if not last:
                #self.msg("^1Mybalance couldn't retrieve the last player. Please consult error logs.")
                minqlx.console_command("echo Error: Trying to balance before round {} start. Red({}) - Blue({}) players".format(roundnumber, len(teams['red']), len(teams['blue'])))
                return
            if self.is_even(diff): # one team has an even amount of people more than the other
                to, fr = ['blue','red'] if diff > 0 else ['red', 'blue']
                game_logic(lambda: last.put(to))
                self.msg("^6Uneven teams action^7: Moved {} from {} to {}".format(last.name, fr, to))

            else: # there is an odd number of players, then one will have to spec

                if self.prevent or self.last_action == "ignore":
                    excluded_teams = exclude_player(last)
                    self.msg("^6Uneven teams^7: {} will not be moved to spec".format(last.name))
                elif self.last_action == "slay":
                    if 'anti_rape' in minqlx.Plugin._loaded_plugins:
                        game_logic(lambda: last.put("spectator"))
                        self.msg("^6Uneven teams action^7: {} was moved to spec to even teams!".format(last.name))
                        minqlx.console_command("echo Not slayed because anti_rape plugin is loaded.")
                    else:
                        slay_player(last)
                        self.msg("{} ^7has been ^1slain ^7to even the teams!")
                else:
                    self.msg("^6Uneven teams action^7: {} was moved to spec to even teams!".format(last.name))
                    game_logic(lambda: last.put("spectator"))
            time.sleep(0.2)





    def cmd_last_action(self, player, msg, channel):
        if len(msg) < 2:
            if self.last_action == 'slay' and 'anti_rape' in minqlx.Plugin._loaded_plugins:
                return channel.reply("^7The current action is ^6slay^7, but will ^6spec^7 since ^6anti_rape^7 is active.")
            return channel.reply("^7The current action when teams are uneven is: ^6{}^7.".format(self.last_action))

        if msg[1] not in ["slay", "spec", "ignore"]:
            return minqlx.RET_USAGE

        self.last_action = msg[1]

        if self.last_action == 'slay' and 'anti_rape' in minqlx.Plugin._loaded_plugins:
            return channel.reply("^7Action has been set to ^6slay^7, but will ^6spec^7 because ^6anti_rape^7 is loaded.")
        channel.reply("^7Action has been succesfully changed to: ^6{}^7.".format(msg[1]))


    # At the end of a round, prevent is reset back to false.
    # This gives us 10 seconds to prevent slaying before the
    # next round starts
    def handle_round_end(self, data):
        self.prevent = False

    def handle_round_count(self, round_number):
        def red_min_blue():
            t = self.teams()
            return len(t['red']) - len(t['blue'])

        # Grab the teams
        teams = self.teams()
        player_count = len(teams["red"] + teams["blue"])

        # If it is the last player, don't do this and let the game finish normally
        if player_count == 1:
            return

        # If there is a difference in teams of more than 1
        diff = red_min_blue()
        to, fr = ['blue', 'red'] if diff > 0 else ['red','blue']
        n = int(abs(diff) / 2)
        if abs(diff) >= 1:
            last = self.algo_get_last()
            if not last:
                self.msg("^7No last person could be predicted in round countdown from teams:\nRed:{}\nBlue:{}".format(teams['red'], teams['blue']))

            elif self.is_even(diff):
                n = last.name if n == 1 else "{} players".format(n)
                self.msg("^6Uneven teams detected!^7 At round start i'll move {} to {}".format(n, to))
            else:
                m = 'lowest player' if n == 1 else '{} lowest players'.format(n)
                m = " and move the {} to {}".format(m, to) if n else ''
                self.msg("^6Uneven teams detected!^7 Server will auto spec {}{}.".format(last.name, m))

        self.balance_before_start(round_number)

    # Normally the teams have already been balanced so players are switched in time,
    # but check it again to make sure the round starts even
    def handle_round_start(self, round_number):
        self.balance_before_start(round_number, True)
    # If there is no round delay, then round_count hasnt been called.
##        if self.game.type_short == "ft":
##            if not int(self.get_cvar('g_freezeRoundDelay')):
##                self.balance_before_start(round_number, True)
##        else:
##            if not int(self.get_cvar('g_roundWarmupDelay')):
##                self.balance_before_start(round_number, True)


    def handle_game_start(self, data):
        self.game_active = True

        # There are no rounds?? Check it yourself then, pronto!
        if self.game.type_short in ["ctf", "tdm"]:
            self.balance_before_start(self.game.type_short, True)

    def handle_game_end(self, data):
        self.game_active = False

    def handle_map(self, mapname, factory):
        self.game_active = False

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

        # If you allow someone, check to remove them from the kick list
        if (self.ELO_MIN <= rating <= self.ELO_MAX) and sid in self.kicked:
            del self.kicked[sid]
        return minqlx.RET_STOP

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

        return minqlx.RET_STOP


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
        return minqlx.RET_STOP

    def cmd_getratings(self, player, msg, channel):
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

        self.fetch_both(target_player or sid, gt, channel)

    # ====================================================================
    #                               HELPERS
    # ====================================================================

    def find_players(self, query):
        players = []
        for p in self.find_player(query):
            if p not in players:
                players.append(p)
        return players

    @minqlx.thread
    def delayact(self, messages, interval = 1):
        @minqlx.next_frame
        def logic(func): func()

        for m in messages:
            if m: logic(m) # allow "" or None to be used as a skip
            time.sleep(interval)

    def find_time(self, player):
        if not (player.steam_id in self.jointimes):
            self.jointimes[player.steam_id] = time.time()
        return self.jointimes[player.steam_id]

    def algo_get_last(self, excluded_teams = False):
        # Find the player to be acted upon. If there are more than 1 rounds
        # played, we will take the lowest score. Otherwise the last to join

        # If teams are even, just return
        teams = excluded_teams or self.teams()

        # See which team is bigger than the other
        if len(teams["blue"]) > len(teams["red"]):
            bigger_team = teams["blue"].copy()
        elif len(teams["red"]) > len(teams["blue"]):
            bigger_team = teams["red"].copy()
        else:
            minqlx.console_command("echo Cannot pick last player since there are none.")
            return

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
            url = "http://qlstats.net/{elo}/{}".format(sid, elo=self.get_cvar('qlx_balanceApi'))
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
                        minqlx.console_command("echo No {} rating for {}".format(gt, _sid))
                        return callback(player, gt, 0, 0)

                    _gt = p[gt]
                    return callback(player, gt, _gt["elo"], _gt["games"])

            # If our players has not been found yet, then he is not known in the system
            return callback(player, gt, 0, 0)


        self.msg("^1echo Problem fetching {} glicko: {}".format(gt, last_status))
        return

    @minqlx.thread
    def fetch_both(self, player, gt, channel):
        @minqlx.next_frame
        def msg(m): channel.reply(m)

        try:
            sid = player.steam_id
        except:
            sid = player

        rating = [None,None]
        brating = [None, None]

        try:
            url = "http://qlstats.net/elo/{}".format(sid)
            res = requests.get(url)
            if res.status_code != requests.codes.ok: raise

            js = res.json()
            if "players" not in js: raise

            for p in js["players"]:
                _sid = int(p["steamid"])
                if _sid == sid: # got our player
                    if gt in p: rating = [p[gt]["elo"], p[gt]["games"]]
                    break

            url = "http://qlstats.net/elo_b/{}".format(sid)
            res = requests.get(url)
            if res.status_code != requests.codes.ok: raise

            js = res.json()
            if "players" not in js: raise

            for p in js["players"]:
                _sid = int(p["steamid"])
                if _sid == sid: # got our player
                    if gt in p: brating = [p[gt]["elo"], p[gt]["games"]]
                    break

            elomsg = "{} ^7qlstats.net {} ".format(player.name, gt.upper())
            if rating != [None, None]:
                elomsg += "| rating: ^6{} ({} games)^7 ".format(rating[0], rating[1])
            if brating != [None, None]:
                elomsg += "| B-rating: ^6{} ({} games)^7 ".format(brating[0], brating[1])
            key = RATING_KEY.format(sid, gt)
            if key in self.db:
                elomsg += "| local: ^6{} ".format(int(self.db[key]))
            channel.reply(elomsg)

        except Exception as e:
            channel.reply("^1Problem fetching {} glicko: {}".format(gt, e))
            raise e
            return

    def callback_elo(self, player, gt, elo = 0, games=0):
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
            elos.append("^7local {} glicko: ^6{}".format(gt.upper(), dbelo))
        #if elo and games:
        b = " ^3B^7" if self.get_cvar('qlx_balanceApi') == "elo_b" else ""
        elos.append("^7qlstats.net {}{} glicko: ^6{} ({} games)".format(gt.upper(), b, elo, games))

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
                time.sleep(1)
                if self.plugin.get_cvar("qlx_elo_kick") == "1":
                    kickmsg = "so you'll be ^6kicked ^7shortly..."
                else:
                    kickmsg = "but you are free to keep watching."
                self.plugin.msg("^7Sorry, {} your glicko ({}) is too {}, {}".format(self.player.name, self.elo, self.highlow, kickmsg))
            def try_mute(self):
                @minqlx.next_frame
                def execute():
                    try:
                        self.player.mute()
                    except:
                        pass
                time.sleep(4)
                #self.player = self.plugin.player(self.player.id)
                if not self.player: self.stop()
                if self.go and self.plugin.get_cvar("qlx_elo_kick") == "1": execute()
            def try_kick(self):
                @minqlx.next_frame
                def execute():
                    try:
                        self.player.kick("^1GOT KICKED!^7 Glicko ({}) was too {} for this server.".format(self.elo, self.highlow))
                    except:
                        pass
                if self.plugin.get_cvar("qlx_elo_kick") == "0": return
                time.sleep(16)
                #self.player = self.plugin.player(self.player.id)
                if not self.player: self.stop()
                if self.go: execute()
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


    def callback(self, player, gt, elo, games):
        eval_elo = self.evaluate_elo_games(player, elo, games)
        if eval_elo:
            if len(self.kicked) >= 15: # if 15 or more entries, delete an old one
                for sid in self.kicked:
                    del self.kicked[sid]
                    break
            self.kicked[player.steam_id] = [player.name, eval_elo[1]]
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

        if self.get_cvar("qlx_mybalance_exclude", int) and games < self.GAMES_NEEDED:
            #self.msg("{}'s ratings are too uninformative for this server. ({}/{} games played)".format(player.name, games, self.GAMES_NEEDED))
            return ['uninformative', elo]

        if not elo and not games: return # allow person to join

        if elo < self.ELO_MIN:
            if games < self.GAMES_NEEDED:
                self.msg("{}'s ({}) is below the server limit ({}), but insufficient tracked games ({}/{}).".format(player.name, elo, self.ELO_MIN, games, self.GAMES_NEEDED))
                return
            return ['low', elo]
        if max_elo < elo:
            if games < self.GAMES_NEEDED:
                self.msg("{}'s ({}) is above the server limit ({}), but insufficient tracked games ({}/{}).".format(player.name, elo, self.ELO_MAX, games, self.GAMES_NEEDED))
                return
            return ['high', elo]


    @minqlx.delay(600) # 10 minutes
    def remove_thread(self, sid):
        if sid in self.connectthreads:
            del self.connectthreads[sid]

class ConnectThread(threading.Thread):
    def __init__(self, plugin, player):
        super(ConnectThread, self).__init__()
        self._plugin = plugin
        self._player = player
        self._result = None
    def run(self):
        url = "http://qlstats.net/{elo}/{}".format(self._player.steam_id, elo=self._plugin.get_cvar('qlx_balanceApi'))
        self._result = requests.get(url)
