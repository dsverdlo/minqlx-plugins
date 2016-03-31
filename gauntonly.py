# This is a plugin written by iouonegirl(@gmail.com) and Gelenkbusfahrer
# Copyright (c) 2016 iouonegirl, Gelenkbusfahrer
# https://github.com/dsverdlo/minqlx-plugins
#
# You are free to modify this plugin to your custom,
# except for the version command related code.
#
# The idea for this plugin comes from Gelenkbusfahrer
# and has been discussed on station.boards.net.
# Home forum of the Bus Station server.
#
# This plugin detects when a last standing player is
# facing more than [MAX] opponents and will disable all
# weapons until there are only [MIN] players left standing.
#
# Round based game modes only
#
# Uses
# - set qlx_gaunt_max "4"
# - set qlx_gaunt_min "2"

import minqlx
import datetime
import time
import os
import re
import requests
import random

VERSION = "v0.2"

class gauntonly(minqlx.Plugin):
    def __init__(self):
        super().__init__()

        self.set_cvar_once("qlx_gaunt_min", "2")
        self.set_cvar_once("qlx_gaunt_max", "4")

        self.add_hook("death", self.handle_death)
        self.add_hook("team_switch", self.handle_switch)
        self.add_hook("round_end", self.handle_round_end)

        self.add_command("v_gauntonly", self.cmd_version)
        self.add_command("update", self.cmd_autoupdate, 5, usage="<plugin>|all")

        self.min_opp = self.get_cvar("qlx_gaunt_min", int)
        self.max_opp = self.get_cvar("qlx_gaunt_max", int)

        self.gauntmode = False
        self.weapons_taken = None

    def handle_switch(self, player, _old, _new):
        # Somebody noob quits? Check if we need to switch modes
        self.detect()

    def handle_death(self, victim, killer, data):
        # Some noob dies? Check if we need to switch modes
        self.detect()

    def handle_round_end(self, data):
        # Round finally ended? Turn the mode off
        self.gauntmode = False


    def detect(self):
        # Not in a match? Do nothing
        if self.game.state != 'in_progress': return

        # Grab some info and put that stuff into variables for readability yo
        teams = self.teams()
        alive_r = list(filter(lambda p: p.is_alive, teams['red']))
        alive_b = list(filter(lambda p: p.is_alive, teams['blue']))

        # If we do not have a last standing, do nothing
        if not 1 in [len(alive_r), len(alive_b)]: return

        # If one team is completely dead, do nothing
        if not (alive_r and alive_b): return

        # Ok things are getting more complicated, listen closely!

        # If the gauntmode was active, and both teams have less than [MIN] players: TURN IT OFF
        if len(alive_r) <= self.min_opp and len(alive_b) <= self.min_opp and self.gauntmode:

            # Deactivate gaunt mode: take everyone's gauntlets, display warning and then restore weapons
            self.gauntmode = False
            for p in self.players(): # Take their gauntlet away and switch to empty
                p.weapons(g=False, mg=False, sg=False, gl=False, rl=False, lg=False, rg=False, pg=False, bfg=False, gh=False, ng=False, pl=False, cg=False, hmg=False, hands=False)
                p.weapon(15)
            # Countdown will display messages and then restore the weapons
            r = "^3Restoring weapons in "
            self.countdown([r+"5", r+"4", r+"3", r+"2", r+"1", "^2FIGHT!"])
            return

        # If we were not in gaunt mode yet, check if we have enough opponents.
        # Remember at least one team has 1 player; add the teams and subtract one
        if (not self.gauntmode) and self.game.state == "in_progress" and len(alive_b + alive_r[1:]) > self.max_opp:
            self.gauntmode = True
            self.weapons_taken = self.weapons_taken or alive_r[0].weapons()
            for p in self.players():
                p.weapons(g=False, mg=False, sg=False, gl=False, rl=False, lg=False, rg=False, pg=False, bfg=False, gh=False, ng=False, pl=False, cg=False, hmg=False, hands=False)
                p.weapon(15)
            self.blink(["Prepare your pummel!", ""] * 9 + ["^2{}vs{} - Go pummeling!".format(len(alive_r), len(alive_b))])
            self.msg("^7Pummel showdown! Weapons will be restored when ^3{}^7 players are left standing.".format(self.min_opp+1))
            return

        # If we didn't have to turn the gauntmode ON, and not OFF,
        # it will be the case someone died or changed teams
        if self.gauntmode:
            self.msg("^7Pummel showdown! Gaunt ^3{}^7 more enemies to restore weapons".format(len(alive_b+alive_r)-1-self.min_opp))

            # Let's make some noise
            d = random.randint(1, 3)
            self.play_sound("sound/vo/humiliation{}".format(d))

            if len(alive_r) > len(alive_b):
                self.blink2((["{} Reds left!".format(len(alive_r))] + [""]) * 6)
            else:
                self.blink2((["{} Blues left!".format(len(alive_b))] + [""]) * 6)


    @minqlx.thread
    def blink(self, messages, interval = .12):
        @minqlx.next_frame
        def logic(_m): self.center_print("^3{}".format(_m))
        @minqlx.next_frame
        def setgaunt(_p):
            _p.weapons(g=True, mg=False, sg=False, gl=False, rl=False, lg=False, rg=False, pg=False, bfg=False, gh=False, ng=False, pl=False, cg=False, hmg=False, hands=True)
            _p.weapon(1)
        # First centerprint all the messages
        for m in messages:
            logic(m)
            time.sleep(interval)
        # Then change the weapons to gauntlet
        for p in self.players():
            setgaunt(p)
        self.play_sound("sound/vo_evil/go")

    @minqlx.thread
    def blink2(self, messages, interval = .12):
        @minqlx.next_frame
        def logic(_m): self.center_print("^3{}".format(_m))
        for m in messages:
            logic(m)
            time.sleep(interval)

    @minqlx.thread
    def countdown(self, messages, interval = 1):
        @minqlx.next_frame
        def logic(_m): self.center_print("^3{}".format(_m))
        @minqlx.next_frame
        def setweap(_p): minqlx.set_weapons(_p.id, self.weapons_taken or _p.weapons())
        # First centerprint to warn players
        for m in messages:
            time.sleep(interval)
            logic(m)
        # Then restore their weapons
        for p in self.players():
            setweap(p)
        self.play_sound("sound/vo_evil/fight")







    def cmd_version(self, player, msg, channel):
        self.check_version(channel=channel)

    @minqlx.thread
    def check_version(self, player=None, channel=None):
        url = "https://raw.githubusercontent.com/dsverdlo/minqlx-plugins/master/{}.py".format(self.__class__.__name__)
        res = requests.get(url)
        last_status = res.status_code
        if res.status_code != requests.codes.ok:
            m = "^7Currently using ^3iou^7one^4girl^7's & Bus' ^6{}^7 plugin version ^6{}^7.".format(self.__class__.__name__, VERSION)
            if channel: channel.reply(m)
            else: self.msg(m)
            return
        for line in res.iter_lines():
            if line.startswith(b'VERSION'):
                line = line.replace(b'VERSION = ', b'')
                line = line.replace(b'"', b'')
                # If called manually and outdated
                if channel and VERSION.encode() != line:
                    channel.reply("^7Currently using ^3iou^7one^4girl^7's & Bus' ^6{}^7 plugin ^1outdated^7 version ^6{}^7.".format(self.__class__.__name__, VERSION))
                # If called manually and alright
                elif channel and VERSION.encode() == line:
                    channel.reply("^7Currently using ^3iou^7one^4girl^7's & Bus' latest ^6{}^7 plugin version ^6{}^7.".format(self.__class__.__name__, VERSION))
                # If routine check and it's not alright.
                elif player and VERSION.encode() != line:
                    time.sleep(15)
                    try:
                        player.tell("^3Plugin update alert^7:^6 {}^7's latest version is ^6{}^7 and you're using ^6{}^7!".format(self.__class__.__name__, line.decode(), VERSION))
                    except Exception as e: minqlx.console_command("echo {}".format(e))
                return


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
            channel.reply("^2updated ^3iou^7one^4girl^7's & Bus' ^6{} ^7plugin to the latest version!".format(self.__class__.__name__))
            #self.cmd_version(player, msg, channel)
            return True
        except Exception as e :
            channel.reply("^1Update failed for {}^7: {}".format(self.__class__.__name__, e))
            return False