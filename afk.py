# This is a plugin created by iouonegirl(@gmail.com)
# Copyright (c) 2016 iouonegirl
# https://github.com/dsverdlo/minqlx-plugins
#
# You are free to modify this plugin to your custom,
# except for the version command related code.
#
# Its purpose is to detect afk players and provide actions
# to be taken on them.
#
# Uses:
# - qlx_afk_warning_seconds "10"
# - qlx_afk_detection_seconds "20"
# - qlx_afk_put_to_spec "1"


import minqlx
import threading
import time
import requests

VERSION = "v0.5"

VAR_WARNING = "qlx_afk_warning_seconds"
VAR_DETECTION = "qlx_afk_detection_seconds"
VAR_PUT_SPEC = "qlx_afk_put_to_spec"

# Interval for the thread to update positions. Default = 0.33
interval = 0.33

class afk(minqlx.Plugin):

    def __init__(self):

        # Set required cvars once. DONT EDIT THEM HERE BUT IN SERVER.CFG
        self.set_cvar_once(VAR_WARNING, "10")
        self.set_cvar_once(VAR_DETECTION, "20")
        self.set_cvar_once(VAR_PUT_SPEC, "1")

        # Get required cvars
        self.warning = int(self.get_cvar(VAR_WARNING))
        self.detection = int(self.get_cvar(VAR_DETECTION))
        self.put_to_spec = int(self.get_cvar(VAR_PUT_SPEC))

        # steamid : [position, seconds]
        self.positions = {}

        # keep looking for AFK players
        self.running = False

        # punished players
        self.punished = []

        self.add_command("v_afk", self.cmd_version)
        self.add_hook("round_start", self.handle_round_start)
        self.add_hook("round_end", self.handle_round_end)
        self.add_hook("team_switch", self.handle_player_switch)
        self.add_hook("unload", self.handle_unload)
        self.add_hook("player_connect", self.handle_player_connect)

    def handle_player_connect(self, player):
        if self.db.has_permission(player, 5):
            self.check_version(player=player)


    def handle_unload(self, plugin):
        if plugin == self.__class__.__name__:
            self.running = False
            self.punished = []

    def handle_round_start(self, round_number):
        teams = self.teams()
        for p in teams['red'] + teams['blue']:
            self.positions[p.steam_id] = [self.help_get_pos(p), 0]

        self.punished = []

        # start checking thread
        self.running = True
        threading.Thread(target=self.help_create_thread).start()

    def handle_round_end(self, round_number):
        self.running = False
        self.punished = []

    def handle_player_switch(self, player, old, new):
        if new == 'spectator':
            if player.steam_id in self.positions:
                del self.positions[player.steam_id]
            if player in self.punished:
                self.punished.remove(player)

        if new in ['red', 'blue']:
            self.positions[player.steam_id] = [self.help_get_pos(player), 0]

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

    def help_create_thread(self):
        while self.running and self.game.state == 'in_progress':
            teams = self.teams()
            for p in teams['red'] + teams['blue']:
                pid = p.steam_id

                if pid not in self.positions:
                    self.positions[pid] = [self.help_get_pos(p), 0]

                prev_pos, secs = self.positions[pid]
                curr_pos = self.help_get_pos(p)

                # If position stayed the same, add the time difference and check for thresholds
                if prev_pos == curr_pos:
                    self.positions[pid] = [curr_pos, secs+interval]
                    if secs+interval >= self.warning and secs < self.warning:
                        self.help_warn(p)
                    elif secs+interval >= self.detection and secs < self.detection:
                        self.help_detected_print(p)
                else:
                    self.positions[pid] = [curr_pos, 0]
                    if p in self.punished:
                        # if the player started moving, remove him from punished players
                        self.punished.remove(p)

            time.sleep(interval)

    def help_warn(self, player):
        message = "You have been inactive for {} seconds...".format(self.warning)
        minqlx.send_server_command(player.id, "cp \"\n\n\n{}\"".format(message))

    def help_detected_print(self, player):
        self.msg("^1{} ^1has been inactive for {} seconds! Commencing punishment!".format(player.name, int(self.positions[player.steam_id][1])))
        self.punished.append(player)
        self.punish(player)


    @minqlx.thread
    def punish(self, player, pain=10, wait=0.5):
        while self.game.state == 'in_progress' and player in self.punished:
            if player.health >= pain:
                player.health -= pain
                if player.steam_id in self.positions:
                    s = int((self.positions[player.steam_id])[1])
                else:
                    s = self.detection
                message = "^1Inactive for {} seconds! \n\n^7Move or keep getting damage!".format(s)
                minqlx.send_server_command(player.id, "cp \"\n\n\n{}\"".format(message))
                time.sleep(wait)
            else:
                break
        self.punished.remove(player)
        if self.put_to_spec: player.put('spectator')
        return


    def help_get_pos(self, player):
        return player.position()