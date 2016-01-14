# minqlx - A Quake Live server administrator bot.
# Copyright (C) 2015 Mino <mino@minomino.org>

# This is a plugin created by iouonegirl(@gmail.com)
#
# It provides a method to print something in the center of a player's screen,
# and a toggle command to view when there is only one enemy left

import minqlx
import datetime
import time
import re

VERSION = "v0.3"
PLAYER_KEY = "minqlx:players:{}"
NOTIFY_LAST_KEY = PLAYER_KEY + ":notifylast"

class centerprint(minqlx.Plugin):
    def __init__(self):
        super().__init__()
        self.add_command(("print", "pprint", "cprint", "centerprint"), self.cmd_center_print, 3, usage="<name>|<id> <message>")
        self.add_command("broadcast", self.cmd_broadcast, 3)
        self.add_command("showlast", self.cmd_toggle_pref)
        self.add_command("v_centerprint", self.cmd_version)
        self.add_hook("death", self.handle_death)


    def cmd_version(self, player, msg, channel):
        plugin = self.__class__.__name__
        channel.reply("^7Currently using ^3iou^7one^4girl^7's ^6{}^7 plugin version ^6{}^7.".format(plugin, VERSION))

    def cmd_broadcast(self, player, msg, channel):
        for p in self.players():
            message = " ".join(msg[1:])
            minqlx.send_server_command(p.id, "cp \"\n\n\n{}\"".format(message))
        player.tell("^6Psst^7: Broadcast successful: '{}'".format(message))

    def cmd_center_print(self, player, msg, channel):
        if len(msg) < 3:
            return minqlx.RET_USAGE

        target = self.find_by_name_or_id(player, msg[1])
        if not target:
            return minqlx.RET_STOP_ALL

        message = " ".join(msg[2:])
        minqlx.send_server_command(target.id, "cp \"\n\n\n{}\"".format(message))
        player.tell("^6Psst^7: succesfully printed '{}' on {}'s screen.".format(message, target.name))
        return minqlx.RET_STOP_ALL

    def handle_death(self, victim, killer, data):
        _vic = self.find_player(victim.name)[0]
        _vic_team = _vic.team

        if data['MOD'] == 'SWITCHTEAM':
            _vic_team == "red" if data['VICTIM']['TEAM'] == 2 else "blue"

        if self.game and self.game.state == 'in_progress':
            teams = self.teams()

            if int(data['TEAM_ALIVE']) == 1: # viewpoint of victim
                for _p in teams["red" if _vic_team == "blue" else "blue"]:
                    if self.get_notif_pref(_p.steam_id):
                        minqlx.send_server_command(_p.id, "cp \"\n\n\nOne enemy left. Start the hunt!\"")



    def cmd_toggle_pref(self, player, msg, channel):
        if len(msg) > 2:
            return minqlx.RET_USAGE

        self.set_notif_pref(player.steam_id)

        if self.get_notif_pref(player.steam_id):
            channel.reply("^7{} will now see a message if there is only 1 enemy left.".format(player.name))
        else:
            channel.reply("^7{} will stop seeing '1 enemy left' messages.".format(player.name))


    # ====================================================================
    #                               HELPERS
    # ====================================================================

    def get_notif_pref(self, sid):
        try:
            return int(self.db[NOTIFY_LAST_KEY.format(sid)])
        except:
            return False

    def set_notif_pref(self, sid):
        self.db[NOTIFY_LAST_KEY.format(sid)] = 0 if self.get_notif_pref(sid) else 1



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