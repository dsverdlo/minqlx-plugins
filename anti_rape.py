# This is a plugin created by iouonegirl(@gmail.com)
# Copyright (c) 2016 iouonegirl
# https://github.com/dsverdlo/minqlx-plugins
#
# You are free to modify this plugin to your custom,
# except for the version command related code.
#
# Its purpose is to detect rapers and give them fair handicaps.
# The detection rules have been intensely discussed and finetuned,
# and can be found on station.boards.net (home forum of the bus station).

# Disclaimer: any use of the word 'rape' is not meant to be offensive or
# offend anyone in any way. This was simply the most fitting term for an
# overpowered player, winning the game and defeating a lot of people with
# ease. Actual rape in the real world is a terrible crime and nothing to
# be taken lightly or laughed with.

import minqlx
import time
import datetime
import threading
import requests
from math import floor

VERSION = "v0.47"


# From which percentage we classify a rape.
# Anything over the upper rape gap will mark a player as a raper
# Rapers will receive to get a handicap if they are not in a losing team,
# or is their gap is below the lower rape gap.
# For more information about these gaps please visit station.boards.net
RAPE_MIDER_GAP = 20 # default 20
RAPE_UPPER_GAP = 20 # default 20

# We want the first rounds to have a higher treshhold to mark a player
# Adjust this dictionary to multiply the UPPER_GAP by an amount for a given round
# E.g. in (early) round 3 we can multiply UPPER_GAP * 4
# Note: this dict starts from round 2 because that's what we define later as the ROUNDS_NEEDED
RAPE_UPPER_GAP_ADJUSTMENTS = {2:8, 3:4, 4:3, 5:2} # remove items in {brackets} to disable service

# The lowest possible handicap that will be forced
HC_LOWEST = 50

# This allows us to multiply the original handicap according to round differences
# E.g. if the round difference is 3 --> multiply the handicap (%)  with 0.8 to make it stronger
USE_HANDICAP_ADJUSTMENTS = True
HANDICAP_ADJUSTMENTS = {0:1, 1:1, 2:0.9, 3:0.8}
DEFAULT_HANDICAP_ADJUSTMENT = 0.7

# The amount of rounds and people needed before we start calculating.
ROUNDS_NEEDED = 2 # default 2
PEOPLE_NEEDED = 4 # default 4


# Do not modify any of these variables
TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
COMPLETED_KEY = "minqlx:players:{}:games_completed"
PLAYER_KEY = "minqlx:players:{}"
_name_key = "minqlx:players:{}:colored_name"
HC_TAG = "new"
SHC_TAG = "new:"

class anti_rape(minqlx.Plugin):
    def __init__(self):
        super().__init__()

        # Some dictionaries (self explanatory) keys: steam_id, values: value
        self.handicaps = {}
        self.help_remove_handicaps()

        # Store a counter of the amount of rounds played per player
        self.rounds_played = {}

        # A frozen snapshot of the damages until the round ends
        # Format example: { '77935123':['red', 200], '78139445':['blue',50] }
        self.scores_snapshot = {}

        # Real scores for handicapped people steam_id:realscore
        self.realscores = {}
        self.realdamage = {}

        # List of players that have just joined. Start of round will empty this.
        # Ignore the players at the end of the round that are in here
        self.just_joined = []

        # Track when we are in round countdown (to compensate self-kills)
        self.round_countdown = True

        self.add_command("hc", self.cmd_get_hc, usage="[<id>|<name>] [silent]")
        self.add_command("sethc", self.cmd_set_hc, 2, usage="[<id>|<name>] [<1-100>]")
        self.add_command(("remhcs", "clearhcs", "delhcs"), self.cmd_rem_handicaps, 2)
        self.add_command(("viewhcs", "listhcs", "handicaps"), self.cmd_list_handicaps, usage="[silent]")
        self.add_command(("hc_info", "hcinfo"), self.cmd_info)
        self.add_command(("hc_gaps", "gaps"), self.cmd_get_gaps, usage="[silent]")
        self.add_command(("rapers", "getrapers"), self.cmd_get_rapers, 2, usage="[silent]")
        self.add_command(("raper", "setraper", "mark"), self.cmd_set_raper, 2, usage="<id>|<name>")
        self.add_command("unmark", self.cmd_unsert_raper, 2, usage="<id>|<name>")
        self.add_command(("hc_cmds", "hccmds"), self.cmd_hc_commands)
        self.add_command(("v_anti_rape", "version_anti_rape"), self.cmd_version)
        self.add_hook("game_countdown",self.handle_game_countdown)
        self.add_hook("player_connect", self.handle_player_connect)
        self.add_hook("player_loaded", self.handle_player_loaded)
        self.add_hook("team_switch", self.handle_team_switch)
        self.add_hook("round_start", self.handle_round_start)
        self.add_hook("round_end", self.handle_round_end)
        self.add_hook("userinfo", self.handle_user_info)
        self.add_hook("death", self.handle_death)


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

    def handle_game_countdown(self):
        # Remove all the handicaps
        self.help_remove_handicaps()

        # Clear all marks
        self.handicaps = {}

        # Clear the snapshots
        self.scores_snapshot = {}

        # Self explanatory
        self.realscores = {}
        self.realdamage = {}

        # Self explanatory
        self.round_countdown = True

        # Set the round count at 0 for each playing player
        teams = self.teams()
        for _p in teams['red'] + teams['blue']:
            self.rounds_played[_p.steam_id] = 0

    def handle_team_switch(self, player, old, new):
        # Not in-game, nothing to be done
        if not self.game or (self.game.state != "in_progress"): return

        # If a player joins/switches during the match, set his counter to 0
        if new in ['red', 'blue']:
            self.rounds_played[player.steam_id] = 0
            self.scores_snapshot[player.steam_id] = [new, 0]
            self.realscores[player.steam_id] = 0
            self.realdamage[player.steam_id] = 0
            if not player.steam_id in self.just_joined:
                self.just_joined.append(player.steam_id)

        # If a player specs during the match, remove his counters
        if new in ['spec', 'free']:
            if player.steam_id in self.rounds_played:
                del self.rounds_played[player.steam_id]
            if player.steam_id in self.scores_snapshot:
                del self.scores_snapshot[player.steam_id]
            if player.steam_id in self.realscores:
                del self.realscores[player.steam_id]
            if player.steam_id in self.realdamage:
                del self.realdamage[player.steam_id]


    # On disconnect, remove from our dictionaries
    def handle_player_disconnect(self, player, reason):
        if player.steam_id in self.rounds_played:
            del self.rounds_played[player.steam_id]
        if player.steam_id in self.handicaps:
            del self.handicaps[player.steam_id]
        if player.steam_id in self.realscores:
            del self.realscores[player.steam_id]
            if player.steam_id in self.realdamage:
                del self.realdamage[player.steam_id]

    def handle_player_connect(self, player):
        if self.db.has_permission(player, 5):
            self.check_version(player=player)

    # just a little longer delay than the myban plugin
    @minqlx.delay(5)
    def handle_player_loaded(self, player):

        try:
            player.update()
        except minqlx.NonexistentPlayerError:
            return

        if self.game and self.game.state == "in_progress":
            # Remove a potential previous handicap
            if ('handicap' in player.cvars) and (int(player.cvars['handicap']) < 100):
                self.set_silent_handicap(player, 100)
                del self.handicaps[player.steam_id]

    # We intercept every user info change, in order to block client handicap change requests
    def handle_user_info(self, player, d):
        if not 'handicap' in d: return d

        # If the player's handicap has been set by the server:
        if player.steam_id in self.handicaps:
            set_hc = self.handicaps[player.steam_id]

            # Is this a result of server forcing a handicap?
            if set_hc.startswith(HC_TAG):
                self.handicaps[player.steam_id] = set_hc.strip(SHC_TAG)
                if not (SHC_TAG in set_hc):
                    minqlx.CHAT_CHANNEL.reply("^6{}^7's handicap has been set to: ^3{}^7％".format(player.name, self.handicaps[player.steam_id]))
                return d

        # At this stage, the request was not started by the server, but by a player.
        # Restore his previous handicap and tell him this is not allowed on the server
        prev_hc = int(player.cvars['handicap'])
        new_hc = int( d['handicap'] )
        player.tell("^3Handicap request denied. This server will automatically set appropriate handicap levels.")
        d['handicap'] = prev_hc
        return d



    def handle_death(self, victim, killer, data):
        if not (self.game.state != 'in-progress' or self.round_countdown or killer):
            self.realscores[victim.steam_id] = self.realscores.get(victim.steam_id, 0) - 1

    def handle_round_start(self, round_number):
        self.just_joined = []
        self.round_countdown = False

    # On round end check if we need to check for rapist warnings
    @minqlx.delay(1)
    def handle_round_end(self, data):
        def calc_time_delta(time1, time2):
            return abs(time1 - time2)

        def say(message):
            minqlx.CHAT_CHANNEL.reply("^7"+message)

        def is_rapist(gap, steam_id):
            # If he was already marked
            if steam_id in self.handicaps: return True
            # Or if he satisfies the conditions
            if steam_id in self.rounds_played:
                # get rounds played of player
                n = self.rounds_played[steam_id]
                # get an adjustment maybe
                adjusted_gap = RAPE_UPPER_GAP * RAPE_UPPER_GAP_ADJUSTMENTS.get(n, 1)
                # if the player played the amount of rounds needed and is higher than threshold, mark him
                if n >= ROUNDS_NEEDED and gap >= adjusted_gap:
                    return True

            # Else not
            return False

        def mark_rapist(player):
            # add him into handicap table with default HC to mark him
            if not (player.steam_id in self.handicaps):
                self.handicaps[player.steam_id] = 100

        def unmark_rapist(player):
            if player.steam_id in self.handicaps:
                self.set_silent_handicap(player, 100)
                del self.handicaps[player.steam_id]

        def reset(player):
            if player.steam_id in self.handicaps:
                self.set_silent_handicap(player, 100)

        def update_realscores(teams):
            minqlx.console_command("echo Updating realscores (red: {} - blue: {})".format(self.game.red_score, self.game.blue_score))

            # Calculate if we are in a special case (in case of plugin reload)
            first_round = self.game.red_score + self.game.blue_score == 1
            special_case =  not (self.scores_snapshot or first_round)

            for _p in teams['red'] + teams['blue']:
                # Gather the data
                sid = _p.steam_id
                score = _p.stats.score
                frags = _p.stats.kills
                curr_dmg = _p.stats.damage_dealt
                hc = int(_p.cvars.get('handicap', 100))
                prev_dmg = self.scores_snapshot.get(sid, [None, curr_dmg if special_case else 0])[1]
                diff = curr_dmg - prev_dmg
                actual_diff = diff / hc

                # Calculate / update the 'real' scores
                self.realdamage[sid] = self.realdamage.get(sid, 0) + actual_diff
                self.realscores[sid] = int(self.realdamage[sid] + frags)

                # while we're here, update snapshots for next round
                self.scores_snapshot[sid] = [_p.team, curr_dmg]

                dbg = "echo DBG: {}({}％) pdmg: {} cdmg: {} diff: {} tot.kills: {} scr: {} rscr: {}"
                minqlx.console_command(dbg.format(_p.name, hc, prev_dmg, curr_dmg, diff, frags, score, self.realscores[sid]))

        # If this was the last round, nothing to do
        if self.game.roundlimit in [self.game.blue_score, self.game.red_score]:
            return self.clear_all_handicaps()

        # We are now in round countdown until round starts
        self.round_countdown = True

        # Add players that werent in it before (maybe plugin reload during game)
        teams = self.teams()
        for _p in teams['red'] + teams['blue']:
            if _p.steam_id not in self.rounds_played:
                self.rounds_played[_p.steam_id] = 0

        # Increase all the round counters (except people that just joined during a round)
        for _id in self.rounds_played:
            if not _id in self.just_joined:
                self.rounds_played[_id] += 1

        # Update the realscores
        update_realscores(teams)

        # Check will contain a list of players in the winning team(s)
        check = teams['blue'].copy()
        if self.game.red_score == self.game.blue_score:
            check += teams['red']
        elif self.game.red_score > self.game.blue_score:
            check = teams['red']

        # For all playing players
        all_players = teams['red'] + teams['blue']
        for p in all_players:
            gap = self.help_calc_rape_gap(p)
            if gap == "invalid": return  # no server average available, return function

            # If we have a rapist, mark him for the game
            rapist = is_rapist(gap, p.steam_id)
            if rapist: mark_rapist(p)

            # If player is not in losing team
            if p.steam_id in map(lambda _p: _p.steam_id, check):
                # If he is a rapist and  has higher than MID gap, set a normal handicap
                if rapist and (gap >= RAPE_MIDER_GAP):
                    hc = self.help_get_hc_suggestion(gap)
                    if hc: self.set_silent_handicap(p, hc)
                    if hc: self.delay(["","^6{}^7 score index: ^1{}^7％ above average - Handicap set to: ^3{}^7％".format(p.name, gap, hc)], 0.3)
                    continue

            # If player is in losing team or was not a rapist with a high gap
            reset(p)


    # Little debug command, to check the rape scores during a game. Rape scores <= 0% are not shown.
    # don't forget to add 'silent' behind it to get silent calculations
    def cmd_get_gaps(self, player, msg, channel):
        if self.game.state != "in_progress":
            player.tell("^1Error^7: No game in progress!")
            return minqlx.RET_STOP_ALL

        teams = self.teams()

        reds = {}
        for p in teams['red']:
            reds[p.name] = self.help_calc_rape_gap(p)
        blues = {}
        for p in teams['blue']:
            blues[p.name] = self.help_calc_rape_gap(p)

        if ("invalid" in reds.values()) or ("invalid" in blues.values()):
            if len(msg) < 2:
                channel.reply("^7Not enough data to calculate server average score/min...")
                return
            player.tell("^6Psst: ^7not enough data to calculate server average score/min...")
            return minqlx.RET_STOP_ALL

        rreds = []
        for name in sorted(reds, key=lambda i: reds[i], reverse=True): # sort small -> big
            gap = reds[name]
            if gap <= 0: continue
            rreds.append("{}:^3{}％^7".format(name, gap)) # append at the end

        bblues = []
        for name in sorted(blues, key=lambda i: blues[i], reverse=True):
            gap = blues[name]
            if gap <= 0: continue
            bblues.append("{}:^3{}％^7".format(name, gap))

        messages = ["^7Bus Station current score/min values compared to server average:",
            "^1Red^7: {}".format("^1,^7".join(rreds)),
            "^4Blue^7: {}".format("^4,^7".join(bblues))]

        if len(msg) < 2:
            self.delay(messages, 0.3)
        else:
            self.delaytell(messages, player, 0.3)
            return minqlx.RET_STOP_ALL



    def cmd_get_hc(self, player, msg, channel):
        """Check a person's handicap percentage. If no one was specified,
           display the handicap of the command calling player

           Ex: !hc - Returns callers' own HC
           Ex: !hc 2 - Returns the HC of player with ingame id 2
           Ex: !hc 2 silent - Returns a pm of the HC of player with ingame id 2
           Ex: !hc iou - Returns the HC of person with iou in their name.
           Ex: !hc iou silent - Returns a PM of the HC of person with iou in their name.
          """

        if len(msg) == 1:
            target_player = player
            silent = False
        elif len(msg) == 2:
            target_player = self.find_by_name_or_id(player, msg[1])
            silent = False
        elif len(msg) == 3 and msg[2] == "silent":
            target_player = self.find_by_name_or_id(player, msg[1])
            silent = True
        else:
            return minqlx.RET_USAGE

        if target_player:
            name = target_player.name
            try:
                target_player.update()
                hc = target_player.cvars["handicap"]
                if int(hc) < 100:
                    m = "^7Player ^6{} ^7is currently playing with handicap ^3{}^7％".format(target_player.name, hc)
                    if silent:
                        player.tell("^6Psst: "+m)
                        return minqlx.RET_STOP_ALL
                    else:
                        channel.reply(m)
                else:
                    m = "^7Player ^6{} ^7has no active handicap.".format(target_player.name)
                    if silent:
                        player.tell("^6Psst: "+m)
                        return minqlx.RET_STOP_ALL
                    else:
                        channel.reply(m)
            except Exception as e:
                minqlx.console_command("echo Error: {}".format(e))
                m = "^7Something unexpected happened while getting ^6{}^7's handicap.".format(name)
                if silent:
                    player.tell("^6Psst: "+m)
                else:
                    channel.reply(m)


    def cmd_get_rapers(self, player, msg, channel):
        def id_to_name(steam_id):
            # Try in the names database
            if self.db[_name_key.format(steam_id)]:
                return self.db[_name_key.format(steam_id)]
            # Try every player
            for p in self.players():
                if p.steam_id == steam_id:
                    return p.name
            # Give up
            return steam_id

        if (not self.game) or (self.game.state != "in_progress"):
            message = "^7No game in progress..."
        else:
            message = "^7Rapers: {}".format(",".join(['%s(^3%s％^7)' % (id_to_name(key), value) for (key, value) in self.handicaps.items()]))

        if len(msg) == 2 and msg[1] == "silent":
            player.tell("^6Psst: " + message)
            return minqlx.RET_STOP_ALL

        channel.reply(message)

    def cmd_hc_commands(self, player, msg, channel):
        cmds = ["!hc", "^1!sethc", "!hc_info", "!hc_info_mid", "!gaps", "^1!rapers", "^1!raper", "!unmark" ]
        channel.reply("^7Available anti_rape commands: ^2{}^7.".format("^7, ^2".join(cmds)))

    def cmd_info(self, player, msg, channel):
        channel.reply("^7Players with more than ^3{}^7％ score/min than server average will be handicapped.".format(RAPE_UPPER_GAP))
        return minqlx.RET_STOP_ALL


    def cmd_list_handicaps(self, player, msg, channel):
        handicapable_players = []
        message = "^7There are no active handicaps on the server."

        for p in self.players():
            if int(p.cvars.get('handicap', '100')) < 100:
                handicapable_players.append(p)

        if handicapable_players:
            message = "^7" + ",".join(list(map(lambda _p: "{}-^3{}％^7".format(_p.name, _p.cvars['handicap']), handicapable_players)))

        if len(msg) < 2:
            return channel.reply(message)
        elif len(msg) < 3 and msg[1] == 'silent':
            player.tell("^6Psst: ^7" + message)
            return minqlx.RET_STOP_ALL

        return minqlx.RET_USAGE

    def cmd_rem_handicaps(self, player, msg, channel):
        self.help_remove_handicaps()
        channel.reply("^7Done! There are no current handicaps on the server.")


    def cmd_set_hc(self, player, msg, channel):
        if len(msg) == 3:
            target = msg[1]
            target_player = self.find_by_name_or_id(player, target)
            if not target_player:
                return minqlx.RET_STOP_ALL
            try:
                hc = int(msg[2])
            except:
                return minqlx.RET_USAGE
        elif len(msg) == 2:
            target_player = player
            try:
                hc = int(msg[1])
                if not ( 1 <= hc <= 100 ):
                    raise ValueError
            except:
                return minqlx.RET_USAGE
        else:
            return minqlx.RET_USAGE

        self.set_handicap(target_player, hc)
        # Delete so the plugin doesnt think it's a raper
        del self.handicaps[target_player.steam_id]



    def cmd_set_raper(self, player, msg, channel):
        if len(msg) < 2:
            return minqlx.RET_USAGE

        target_player = self.find_by_name_or_id(player, msg[1])
        if not target_player:
            return minqlx.RET_STOP_ALL

        if target_player.steam_id in self.handicaps:
            player.tell("^6Player {} is already marked as a rapist :-)".format(target_player.name))
            return minqlx.RET_STOP_ALL

        self.set_silent_handicap(target_player, 100)
        player.tell("^6Player {} has succesfully been marked as a raper!".format(target_player.name))
        return minqlx.RET_STOP_ALL

    def cmd_unsert_raper(self, player, msg, channel):
        if len(msg) < 2:
            return minqlx.RET_USAGE

        target_player = self.find_by_name_or_id(player, msg[1])
        if not target_player:
            return minqlx.RET_STOP_ALL

        if target_player.steam_id in self.handicaps:
            self.set_silent_handicap(target_player, 100)
            del self.handicaps[target_player.steam_id]
            player.tell("^6Player {} has been unmarked as a rapist :-)".format(target_player.name))
            return minqlx.RET_STOP_ALL

        player.tell("^6Player {} was not even a raper!".format(target_player.name))
        return minqlx.RET_STOP_ALL








    # ====================================================================
    #                               HELPERS
    # ====================================================================
    def delay(self, messages, interval = 1):
        channel = lambda m: minqlx.CHAT_CHANNEL.reply("^7{}".format(m))
        threading.Thread(target=self.thread_list, args=(messages, channel, interval)).start()

    def delaytell(self, messages, player, interval = 1):
        channel = lambda m: player.tell("^6{}".format(m))
        threading.Thread(target=self.thread_list, args=(messages, channel, interval)).start()

    def thread_list(self, items, channel, interval):
        for m in items:
            if m: channel(m) # allow "" to be used as a skip
            time.sleep(interval)

    def find_players(self, query):
        players = []
        for p in self.find_player(query):
            if p not in players:
                players.append(p)
        return players

    def clear_all_handicaps(self):
        for _p in self.players():
            self.set_silent_handicap(_p, 100)
            del self.handicaps[_p.steam_id]

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


    def set_handicap(self, player, hc):
        self.handicaps[player.steam_id] = HC_TAG+str(hc)
        player.handicap = hc

    def set_silent_handicap(self, player, hc):
        self.handicaps[player.steam_id] = SHC_TAG+str(hc)
        player.handicap = hc

    def help_get_avg_score(self):
        teams = self.teams()
        # Get scores/second of all players
        avg_scores = []
        for p in teams['red'] + teams['blue']:
            if self.rounds_played.get(p.steam_id, 0):
                score = self.realscores.get(p.steam_id, p.stats.score)
                avg_scores.append(score / p.stats.time)

        # Now calculate the averages
        if len(avg_scores): return sum(avg_scores) / len(avg_scores)
        return -1

    # Calculate handicap suggestion (as discussed on station.boards.net):
    def help_get_hc_suggestion(self, rape_score):
        hc = int( 108 - rape_score / 2.1 )

        diff = abs ( self.game.red_score - self.game.blue_score )

        if USE_HANDICAP_ADJUSTMENTS:
           hc *= HANDICAP_ADJUSTMENTS.get(diff, DEFAULT_HANDICAP_ADJUSTMENT)

        hc = min(int(hc), 100)
        hc = max(hc, HC_LOWEST)
        return hc


    # Calculate rape percentage
    def help_calc_rape_gap(self, player):
        score = self.realscores.get(player.steam_id, player.stats.score)
        time = player.stats.time
        sps = score / time

        avg_score = self.help_get_avg_score()
        if avg_score > 0: return int ( sps * 100 / avg_score - 100 )
        return "invalid"

    def help_remove_handicaps(self):
        # Reset al handicaps and suggestions
        for _p in self.players():
            self.set_silent_handicap(_p, 100)
            del self.handicaps[_p.steam_id]