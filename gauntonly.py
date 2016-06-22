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
# Round based modes only

# Uses
# - set qlx_gaunt_max "4"
# - set qlx_gaunt_min "2"     Invulnerability

import minqlx
import datetime
import time
import os
import re
import requests
import random

VERSION = "v0.3"

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

class gauntonly(iouonegirlPlugin):
    def __init__(self):
        super().__init__(self.__class__.__name__, VERSION)

        self.set_cvar_once("qlx_gaunt_min", "2")
        self.set_cvar_once("qlx_gaunt_max", "4")

        self.add_hook("death", self.handle_death)
        self.add_hook("team_switch", self.handle_switch)
        self.add_hook("round_end", self.handle_round_end)

        self.min_opp = self.get_cvar("qlx_gaunt_min", int)
        self.max_opp = self.get_cvar("qlx_gaunt_max", int)

        self.gauntmode = False
        self.weapons_taken = None
        self.checkonce = True
        self.blinking = False

    def handle_switch(self, player, _old, _new):
        # Somebody noob quits? Check if we need to switch modes
        if self.checkonce: self.detect()

    def handle_death(self, victim, killer, data):
        # Some noob dies? Check if we need to switch modes
        if self.checkonce: self.detect()

    def handle_round_end(self, data):
        # Round finally ended? Turn the mode off
        self.gauntmode = False
        self.checkonce = True


    def detect(self):
        # Not in a match? Do nothing
        if not self.game: return
        if self.game.roundlimit in [self.game.blue_score, self.game.red_score]: return

        # Grab some info and put that stuff into variables for readability yo
        teams = self.teams()
        alive_r = list(filter(lambda p: p.is_alive, teams['red']))
        alive_b = list(filter(lambda p: p.is_alive, teams['blue']))

        #if self.gauntmode:
        #    if not (alive_r and alive_b):
        #        self.stop_sound()

        # If we do not have a last standing, do nothing
        if not 1 in [len(alive_r), len(alive_b)]: return

        # If one team is completely dead, do nothing
        if not (alive_r and alive_b):
            return

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
            if self.checkonce:

                # Compare healths+armors and decide if last standing had a chance winning. If there's a good chance, this doesn't gonna be a pummel round.
                if len(alive_r) > len(alive_b):
                    calc_opp = alive_r
                    ha_last = alive_b[0].health + alive_b[0].armor
                else:
                    calc_opp = alive_b
                    ha_last = alive_r[0].health + alive_r[0].armor
                ha_opp_total = 0
                for p in calc_opp:
                    ha_opp_total += p.health + p.armor
                ha_required = 1000*(ha_last/300)/1.43+300

                p_amount = len(alive_b + alive_r[1:])
                if p_amount == 5: chance = 10
                elif p_amount == 6: chance = 20
                elif p_amount == 7: chance = 40
                else: chance = 100
                if random.randint(1,100) > chance or ha_opp_total < ha_required:
                    self.checkonce = False
                    return

            self.gauntmode = True
            self.weapons_taken = self.weapons_taken or alive_r[0].weapons()
            for p in self.players():
                p.weapons(g=False, mg=False, sg=False, gl=False, rl=False, lg=False, rg=False, pg=False, bfg=False, gh=False, ng=False, pl=False, cg=False, hmg=False, hands=False)
                p.weapon(15)
            self.blink(["Prepare your pummel!", ""] * 9 + ["^2{}vs{} - Go pummeling!".format(len(alive_r), len(alive_b))])
            self.blinking = True
            self.msg("^7Pummel showdown! Weapons will be restored when ^3{}^7 players are left standing.".format(self.min_opp+1))
            return

        # If we didn't have to turn the gauntmode ON, and not OFF,
        # it will be the case someone died or changed teams
        if self.gauntmode and not self.blinking:
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
            _p.powerups(haste=30)
        # First centerprint all the messages
        for m in messages:
            logic(m)
            time.sleep(interval)
        # Then change the weapons to gauntlet
        for p in self.players():
            setgaunt(p)
        self.play_sound("sound/vo_evil/go")
        self.blinking = False

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



