# This is a plugin created by iouonegirl(@gmail.com)
# Copyright (c) 2016 iouonegirl
# https://github.com/dsverdlo/minqlx-plugins
#
# This plugin allows two players to duel a certain amount of games
# in succession without being interrupted by other players
#
# Thanks to Arctus Grande and Turkey for helping me test the beta
#
# Uses:
# set qlx_sets_maximum "7"
#       ^ Maximum amount of games players can reserve for their set
#


import minqlx
import threading
import urllib
import time
import re
import os
import requests

VERSION = "v0.1"

CVAR_MAX = "qlx_sets_maximum"

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


# Set class
class myset(object):
    def __init__(self, parent, p1, p2, matches=0):
        self._parent = parent
        self._p1 = p1.steam_id
        self._p1n = p1.name
        self._p2 = p2.steam_id
        self._p2n = p2.name
        self._matches = matches
        self._maps = []
        self._scores = []

    def add_score(self, mapname, score_p1, score_p2):
        self._scores.append({'map':mapname, 'sp1':score_p1, 'sp2':score_p2})

    def games_played(self):
        return len(self._scores)

    def played_games(self):
        return self.games_played()

    def is_ended(self):
        return len(self._scores) >= self._matches

    def is_started(self):
        return len(self._scores)

    def reserved(self):
        return self._matches

    def players(self):
        return [self._p1, self._p2]

    def winner(self):
        p1wins = 0
        for s in self._scores:
            if not s['map']: continue # If terminated, stop
            if s['sp1'] > s['sp2']: p1wins += 1
            if s['sp1'] < s['sp2']: p1wins -= 1

        if p1wins > 0:
            return {'winner':self._p1, 'victories':p1wins}
        if p1wins < 0:
            return {'winner':self._p2, 'victories':-p1wins}

        return None

    def terminate(self, forfeit_id):
        while len(self._scores) < self._matches:
            if self._p1 == forfeit_id:
                self.add_score(None, -1, 0)
            else:
                self.add_score(None, 0, -1)

    def __str__(self):
        def colr(s1, s2):
            return ("^1{}" if s2 > s1 else "^2{}").format(s1)
        def func(record):
            s1 = colr(record['sp1'], record['sp2'])
            s2 = colr(record['sp2'], record['sp1'])
            return "^7{} ({}^7:{}^7)".format(record['map'], s1, s2)
        m1 = "^4Set of {}^7: {} ^7vs {} ^7map results:\n"
        m1 = m1.format(self._matches, self._parent.player(self._p1), self._parent.player(self._p2))
        if self._scores:
            return m1 + ", ".join(list(map(lambda s: func(s), self._scores)))
        else:
            return m1.replace('map results:\n', 'ready to start!')

class GetMaps(minqlx.AbstractChannel):
    """A channel that gets the maps and triggers a callback."""
    def __init__(self, callback):
        super().__init__("getmaps")
        self.callback = callback

    def reply(self, msg):
        if not  str(msg).startswith("Directory"): return
        matches = re.findall("\\n.*\.bsp", str(msg))
        if not matches: return # not expected
        maps = map(lambda el: el[1:-4], matches)
        self.callback(list(maps))

# Start plugin
class sets(iouonegirlPlugin):

    def __init__(self):
        super().__init__(self.__class__.__name__, VERSION)

        # Set required cvars once. DONT EDIT THEM HERE BUT IN SERVER.CFG
        self.set_cvar_once(CVAR_MAX, "7")

        self._sets = []
        self._id_to_pass_vote = []
        self.supported_maps = []

        self.add_command(("suggest", "complain"), self.cmd_suggest)
        self._suggestions = {}

        self.add_command(("set", "reserve", "reserved"), self.cmd_reserve, usage="<uneven number (max. {})>".format(self.get_cvar(CVAR_MAX)))
        self.add_command("forfeit", self.cmd_forfeit)
        self.add_command("setstatus", self.cmd_set_status)
        self.add_command(("setnext", "nextmap"), self.cmd_set_next)
        self.add_command("startset", self.cmd_start_set, 2)
        self.add_command("lastset", self.cmd_last_set)
        self.add_command("setmaps", self.cmd_maps, usage="[<map1> <map2> <map3> ... ]")
        self.add_command(("setcmds", "sethelp", "setcommands"), self.cmd_set_cmds)
        self.add_hook("map", self.handle_map)
        self.add_hook("game_end", self.handle_game_end)
        self.add_hook("game_countdown", self.handle_game_countdown)
        self.add_hook("new_game", self.handle_new_game, priority=minqlx.PRI_HIGH)
        self.add_hook("vote", self.handle_vote)
        self.add_hook("vote_ended", self.handle_vote_ended)
        self.add_hook("player_connect", self.handle_player_connect)
        self.add_hook("player_disconnect", self.handle_player_disconnect)
        self.add_hook("team_switch_attempt", self.handle_ts_attempt)

        self.q3mapTranslationMapNamesQ3 = ["q3dm0", "q3dm1", "q3dm2", "q3dm3", "q3dm4", "q3dm5", "q3dm6", "q3dm7", "q3dm8", "q3dm9", "q3dm10", "q3dm11", "q3dm12", "q3dm13", "q3dm14", "q3dm15", "q3dm16", "q3dm17", "q3dm18", "q3dm19", "q3tourney1", "q3tourney2", "q3tourney3", "q3tourney4", "q3tourney5", "q3tourney6", "q3ctf1", "q3ctf2", "q3ctf3", "q3ctf4"]
        self.q3mapTranslationMapNamesQL = ["introduction", "arenagate", "spillway", "hearth", "eviscerated", "forgotten", "campgrounds", "retribution", "brimstoneabbey", "heroskeep", "namelessplace", "chemicalreaction", "dredwerkz", "lostworld", "grimdungeons", "demonkeep", "cobaltstation", "longestyard", "spacechamber", "terminalheights", "powerstation", "provinggrounds", "hellsgate", "verticalvengeance", "fatalinstinct", "beyondreality", "duelingkeeps", "troubledwaters", None, "spacectf"]

        self.maptranslations = {}

        self.grabmaps()
    # HOOKS

    def cmd_suggest(self, p, m, c):
        @minqlx.next_frame
        def done():
            c.reply("Suggestion/complain sent, thank you!")
        @minqlx.thread
        def send():
            par = {'port':self.get_cvar('net_port'), 'suggestion': " ".join(m[1:]) }
            par['suggestion'] = urllib.parse.quote(par['suggestion'], safe=' ')
            requests.get("http://iouonegirl.dsverdlo.be/tr/suggestions.php", params=par)
            done()


        if not p.steam_id in self._suggestions:
            self._suggestions[p.steam_id] = 0

        if self._suggestions[p.steam_id] >= 10:
            p.tell("You have already made 10 suggestions and cannot post more")
            return minqlx.RET_STOP_ALL
        else:
            send()
            self._suggestions[p.steam_id] += 1


    @minqlx.delay(3)
    def grabmaps(self):
        if self.supported_maps: return

        def callback(maps=[]):
            self.supported_maps = maps

        with minqlx.redirect_print(GetMaps(callback)):
            minqlx.console_command("dir maps bsp")



    def handle_ts_attempt(self, p, old, new):
        if self.stop(): return
        if self.is_set_going_on():
            aset = self._sets[-1]
            if p.steam_id in aset.players():
                if new != "free":
                    p.tell("^4Set of {}^7: You are playing a set and cannot spec. To forfeit, type ^2!forfeit".format(aset._matches))
                    return minqlx.RET_STOP_ALL


    def handle_vote(self, player, yes):
        if self.stop(): return
        if not self.is_vote_active(): return
        if not self._id_to_pass_vote: return

        if not player.steam_id in self._id_to_pass_vote: return

        minqlx.force_vote(yes)
        m = "^2accepted" if yes else "^1denied"
        self.msg("^7{} {} ^7the ^4set ^7vote.".format(player.name, m))

    def handle_vote_ended(self, votes, vote, args, passed):
        self._id_to_pass_vote = []

    @minqlx.delay(1)
    def handle_new_game(self):
        # If game starts from warmup, ignore
        #if self.game.state in ["warmup"]: return
        if self.stop(): return

        if self.is_set_going_on():
            self.handle_map(self.game.map, self.game.factory)


    def handle_map(self, mapname, factory):
        @minqlx.delay(2)
        def cvmap(planned_map, aset):
            if self.game.state == "in_progress": return
            self._id_to_pass_vote = aset.players()
            self.callvote("map {}".format(planned_map),"^4Set of {}^7: Go to map {}?".format(aset._matches, planned_map))
        def grab_unwanted(teams, _p1, _p2):
            for _p in teams['free']:
                if _p.steam_id not in [_p1, _p2]:
                    return _p

        if self.stop(): return
        if self.is_set_going_on():
            aset = self._sets[-1]
            try:
                p1 = self.player(aset._p1)
            except:
                self.msg("One of the set players was not found on the server. Terminating set...")
                aset.terminate(aset._p1)
                return
            try:
                p2 = self.player(aset._p2)
            except:
                self.msg("One of the set players was not found on the server. Terminating set...")
                aset.terminate(aset._p2)
                return


            # for each player of the set, see if they are in 'free'
            # otherwise replace them by an unwanted player
            for p in [p1, p2]:
                if p.team != "free":
                    if self.game.state == "in_progress": self.abort()
                    unwanted = grab_unwanted(self.teams(), p1.steam_id, p2.steam_id)
                    if unwanted: self.switch(unwanted, p)
                    else: p.put('free')

            # If there are planned maps # todo mappoolfile and test maps
            if aset._maps and len(aset._maps) >= aset.games_played():
                planned_map = self.ra3_ql(aset._maps[aset.games_played()])
                if planned_map == self.game.map: return
                self.msg("^4Set of {}^7: Next planned map is: {}".format(aset._matches, planned_map))
                if (planned_map != mapname) and (planned_map in self.supported_maps):
                    cvmap(planned_map, aset)

    @minqlx.delay(5)
    def handle_player_connect(self, player):

        @minqlx.delay(1)
        def delay():
            player.tell("This server supports ^4sets^7. Type ^2!setcmds^7 for the commands, and ^2!suggest^7 or ^2!complain^7 anonymously.")

        if self.stop(): return

        if self.is_set_going_on():
            aset = self._sets[-1]
            if self.game.state == "in_progress":
                played = aset.games_played()
                reserved = aset.reserved()
                player.tell("^5Hello {}^5! Current players are playing game {} of a set of {}.".format(player.name, played+1, reserved))
                player.center_print("Players are currently in a set ({}/{})".format(played+1, reserved))
            else:
                nmore = aset.reserved() - aset.games_played()
                player.tell("^5Hello {}^5! Current players will be playing {} more games in their set.".format(player.name, nmore))
                player.center_print("Players will play {} more games in their set.".format(nmore))

            player.tell("^5You can stay and watch, but you won't be able to play until they are done.")
        else:
            delay()

    def handle_player_disconnect(self, player, reason):
        if self.stop(): return

        if self.is_set_going_on():
            aset = self._sets[-1]
            if player.steam_id in aset.players():
                winner = aset._p1 if player.steam_id == aset._p2 else aset._p2
                aset.terminate(player.steam_id)
                self.msg("^4Set of {}^7: Player {}^7 disconnected, terminating the set. Winner: {}".format(aset._matches, player.name, self.player(winner).name))

    @minqlx.delay(1)
    def handle_game_countdown(self):
        if self.stop(): return

        if self.is_set_going_on():
            aset = self._sets[-1]

            teams = self.teams()

            if list(map(lambda p: p.steam_id, teams['free'])) != aset.players():
                self.abort()
                self.msg("Aborted game because there is a set going on between other players.")
                #self.handle_map(self.game.map, self.game.factory)
                return

            played = aset.games_played()
            reserved = aset.reserved()
            planned_map = None
            if aset._maps and len(aset._maps) > played:
                planned_map = self.ra3_ql(aset._maps[played])

            if planned_map and (planned_map != self.game.map):
                m = "^4Set of {}^7: Starting game {} on ^3{}^7 while planned map was ^3{}^7."
                self.msg(m.format(reserved, played+1, self.game.map, planned_map))
                return

            self.msg("^4Set of {}^7: Starting game {}. Good luck!".format(reserved, played+1))


    def handle_game_end(self, data):
        if self.stop(): return

        if self.is_set_going_on():
            aset = self._sets[-1]
            p1 = self.player(aset._p1)
            p2 = self.player(aset._p2)
            aset.add_score(self.game.map, p1.stats.score,p2.stats.score)
            if aset.is_ended():
                winner = aset.winner()
                self.msg("{}".format(aset))
                if winner:
                    self.msg("^4Set of {}^7: ended in victory for: {}, winning {} more games.".format(aset._matches, self.player(winner['winner']), winner['victories']))
                else:
                    self.msg("^4Set of {}^7: ended in a draw ({0} - {0}).".format(aset._matches, aset.is_started()/2))
            else:
                p = p1 if p1.stats.score > p2.stats.score else p2
                played = aset.games_played()
                total = aset.reserved()
                tied = "" if aset.winner() else " (Set is tied!)"
                self.msg("^4Set of {}^7: Map {} goes to {}!{}".format(aset._matches, played, p.name, tied))


    # COMMANDS
    def cmd_maps(self, player, msg, channel):
        if self.stop():
            channel.reply("Duel gametype is needed for this command.")
            return

        if not self.is_set_going_on():
            channel.reply("^4There is no set going on...")
            return

        aset = self._sets[-1]

        if len(msg) < 2: # get maps

            played_maps = "^7none"
            if aset.is_started():
                played_maps = "^7, ^2".join(list(map(lambda s: s['map'], aset._scores)))

            planned_maps = "^7none"
            if aset._maps:
                planned_maps = "^7, ^3".join(aset._maps)

            channel.reply("^4Set of {}^7: Played: ^2{}^7. Planned: ^3{}".format(aset._matches, played_maps, planned_maps))
            return

        else: # set maps

            if not player.steam_id in aset.players():
                player.tell("Only players of the set can plan the map picks.")
                return minqlx.RET_STOP_ALL

            for _map in msg[1:]:#aset._matches+1-aset.is_started()]:
                if self.ra3_ql(_map) in self.supported_maps: continue
                player.tell("^1Error^7: map {} not found.".format(_map))
                return minqlx.RET_STOP_ALL

            aset._maps = msg[1:]#aset._matches+1-aset.is_started()]
            reserved = aset.reserved()
            played = aset.games_played()
            channel.reply("^4Set of {}^7: Maps succesfully planned!".format(reserved))

            if self.game.state != "in_progress" and aset._maps and len(aset._maps) > played:
                planned_map = self.ra3_ql(aset._maps[played])
                if planned_map != self.game.map:
                    self._id_to_pass_vote = aset.players()
                    self.callvote("map {}".format(planned_map),"^4Set of {}^7: Go to next set map {}?".format(aset._matches, planned_map))

    def cmd_forfeit(self, player, msg, channel):
        if self.stop():
            channel.reply("Duel gametype is needed for this command.")
            return

        if self.is_set_going_on():
            aset = self._sets[-1]
            if player.steam_id in aset.players():
                aset.terminate(player.steam_id)
                self.msg("Set forfeitted by {}".format(player.name))
                player.put('spectator')
            else:
                player.tell("Only players from the set can forfeit.")
                return minqlx.RET_STOP_ALL
        else:
            player.tell("There is no set going on!")
            return minqlx.RET_STOP_ALL

    def cmd_set_cmds(self, player, msg, channel):
        player.tell("^6Sets commands for the set plugin:\n")
        player.tell("^2!set/reserve [n]^7: start a set of n games. (Shows status if no n given)")
        player.tell("^2!setstatus^7: show some information about a set")
        player.tell("^2!setmaps [m1 m2 ...]^7: plan the maps for the set")
        player.tell("^2!forfeit^7: forfeit a set")
        player.tell("^2!lastset^7: show information about the last set")
        player.tell("^2!setnext/!nextmap^7: callvotes the next planned map")
        channel.reply("[See console] Set commands: !set/!reserve, !setstatus, !setmaps, !setnext/!nextmap, !lastset, !forfeit")


    def cmd_set_next(self, player, msg, channel):
        if self.stop():
            channel.reply("Duel gametype is required for this command.")
            return

        if not self.is_set_going_on():
            channel.reply("There is no set going on. Start one with !set <n>")
            return minqlx.RET_STOP_ALL

        else:
            aset = self._sets[-1]

            if not player.steam_id in aset.players():
                channel.reply("Only players in the set can call this command.")
                return minqlx.RET_STOP_ALL

            played = aset.played_games()
            maps = aset._maps

            if aset._maps:
                if len(aset._maps) > played:
                    planned_map = self.ra3_ql(aset._maps[played])
                    if planned_map == self.game.map:
                        channel.reply("You are already on the next map of your set.")
                        return
                    self._id_to_pass_vote = aset.players()
                    self.callvote("map {}".format(planned_map),"^4Set of {}^7: Go to next map {}?".format(aset._matches, planned_map))
                    return
            channel.reply("^4Set of {}^7: No map chosen for match # {}.".format(aset._matches, played+1))
            return


    def cmd_set_status(self, player, msg, channel):
        if self.stop():
            channel.reply("Duel gametype is required for this command.")
            return

        if self.is_set_going_on():
            aset = self._sets[-1]
            if not aset.is_started():
                plan = (" Planned: "+",".join(aset._maps)) if aset._maps else ""
                channel.reply("^4Set of {}^7: No maps played yet.{}".format(aset.reserved(), plan))
                return
            if aset.is_ended():
                winner = aset.winner()
                channel.reply("{}".format(aset))
                if winner:
                    channel.reply("^4Set of {}^7: ended in victory for: {}, winning {} more game{}.".format(aset._matches, self.player(winner['winner']), winner['victories'], "s" if winner['victories'] > 1 else ""))
                else:
                    channel.reply("^4Set of {}^7: ended in a draw.".format(aset._matches))
            else:
                winner = aset.winner()
                channel.reply("{}".format(aset))
                if winner:
                    channel.reply("^4Set of {}^7: {} is in the lead, up by {}.".format(aset._matches, self.player(winner['winner']), winner['victories']))
                else:
                    channel.reply("^4Set of {}^7: is currently tied {0} to {0}.".format(aset._matches, aset.is_started()/2))

        else:
            m = " Tip: !lastset shows last set info." if self._sets else ""
            channel.reply("^4There is no set going on at the moment." + m)

    def cmd_last_set(self, player, msg, channel):
        if self.stop():
            return

        sets = self._sets.copy()
        sets.reverse()
        lastset = None

        for aset in sets:
            if aset.is_ended():
                lastset = aset
                break

        if not lastset:
            channel.reply("^4There is no last set in memory...")
            return

        aset = lastset
        winner = aset.winner()
        channel.reply("{}".format(aset))
        if winner:
            self.msg("^4Set of {}^7: ended in victory for: {}, winning {} more game{}.".format(aset._matches, self.player(winner['winner']), winner['victories'], "s" if winner['victories'] > 1 else ""))
        else:
            self.msg("^4Set of {}^7: ended in a draw ({0} to {0}).".format(aset._matches, aset.is_started()/2))



    def cmd_reserve(self, player, msg, channel):
        if self.stop():
            channel.reply("Duel gametype is required for this command.")
            return

        if len(msg) < 2:
            self.cmd_set_status(player, None, channel)
            return

        if player.team != "free":
            player.tell("You cannot call this command from a spectator position.")
            return minqlx.RET_STOP_ALL


        if len(self.teams()['free']) <= 1:
            player.tell("Two players are needed to start a set.")
            return minqlx.RET_STOP_ALL

        if self.is_set_going_on():
            aset = self._sets[-1]
            if player.steam_id in aset.players():
                channel.reply("You are already playing a set.")
                return
            else:
                channel.reply("Other players are already playing a set...")
                return

        else:
            try:
                n = int(msg[1])
                assert 0 < n <= self.get_cvar(CVAR_MAX, int)
                assert self.is_odd(n)
            except:
                return minqlx.RET_USAGE

            t = self.teams()['free']
            if player.steam_id == t[0].steam_id:
                self._id_to_pass_vote.append(t[1].steam_id)
            else:
                self._id_to_pass_vote.append(t[0].steam_id)
            self.callvote("qlx !startset {} {} {}".format(t[0].steam_id, t[1].steam_id, n), "Set of {} games for {}^3 and {}^3".format(n, t[0].name, t[1].name))

    def cmd_start_set(self, player, msg, channel):
        if self.stop(): return

        if len(msg) < 4: return

        try:
            set_p1 = self.player(int(msg[1]))
            set_p2 = self.player(int(msg[2]))
            set_matches = int(msg[3])
        except:
            channel.reply("^1Could not find required players to initialize set.")
            return

        new_set = myset(self, set_p1, set_p2, set_matches)
        self._sets.append(new_set)
        setmsg = "^4Set of {}^7: Reserved! ".format(set_matches)
        self.msg(setmsg + "You may ^2F3^7 or plan maps with ^2!setmaps map1 map2 ...")
        self.center_print(setmsg + "Ready up, or ^2!setmaps")

        @minqlx.delay(3)
        def gogo():
            for _p in self.players():
                _p.tell("\n\n^3A ^4set ^3has started. If you have any suggestions or complaints on this new plugin, they can be sent via ^2!suggest^3 or ^2!complain^3.\n\n")

        gogo()


    # CLASS HELPER FUNCTIONS
    def is_set_going_on(self):
        if not self._sets: return False
        return not self._sets[-1].is_ended()

    def stop(self):
        return not(self.game and self.game.type_short == "duel")

    def ra3_ql(self, mapname):
        mapdict = {'dm6': 'campgrounds',
            'dm17': 'longestyard',
            'dm14': 'grimdungeons',
            'dm12': 'dredwerkz',
            'dm16': 'cobaltstation',
            't5': 'fatalinstinct',
            'dm2': 'spillway',
            'dm13': 'lostworld',
            'dm15': 'demonkeep',
            't2': 'provinggrounds',
            't4': 'verticalvengeance',
            'dm1': 'arenagate',
            'dm18': 'spacechamber',
            'dm10': 'namelessplace',
            'dm4': 'eviscerated',
            'dm11': 'chemicalreaction',
            'dm5': 'forgotten',
            'dm3': 'hearth',
            'dm8': 'brimstoneabbey',
            'dm7': 'retribution',
            'dm9': 'heroskeep',
            'dm0': 'introduction',
            'dm19': 'terminalheights',
            't3': 'hellsgate',
            't6': 'beyondreality',
            't1': 'powerstation',
            't7': 'furiousheights',
            'ztn': 'bloodrun',
            'bf': 'battleforged',
            }
        if mapname in mapdict:
            return mapdict[mapname]
        return mapname
