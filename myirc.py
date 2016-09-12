# minqlx - A Quake Live server administrator bot.
# Copyright (C) 2015 Mino <mino@minomino.org>

# This file is part of minqlx.

# minqlx is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# minqlx is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with minqlx. If not, see <http://www.gnu.org/licenses/>.

# Edited by iouonegirl to show different colors, broadcast more channels
# like red_team, blue_team, free_team, spec_team chat (thanks b1ngo)
# also updates the topic of an irc channel with LIVE updates

import minqlx
import threading
import asyncio
import threading
import urllib
import requests
import os
import random
import time
import re
import fcntl

VERSION = "v0.2.3"

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


# Colors using the mIRC color standard palette (which several other clients also comply with).
#          ^0 Black  ^1 RED    ^2 GREEN  ^3 YLW    ^4 BLUE   ^5 CYAN   ^6 PURPLE ^7WHITE
COLORS = ("\x0301", "\x0304", "\x0303", "\x0308", "\x0302", "\x0311", "\x0306", "\x0300")
EXTRA = {'connect': "\u001d\x0314", 'disconnect': "\u001d\x0314", 'map': "\x0310", 'vote':"\x0306"}
BOLDCHAT = "\x02" # set to "" to disable
FONTRESET = "\x0f"

class myirc(iouonegirlPlugin):
    def __init__(self):
        super().__init__(self.__class__.__name__, VERSION)
        self.add_hook("chat", self.handle_chat, priority=minqlx.PRI_LOWEST)
        self.add_hook("unload", self.handle_unload)
        self.add_hook("player_connect", self.handle_player_connect, priority=minqlx.PRI_LOWEST)
        self.add_hook("player_disconnect", self.handle_player_disconnect, priority=minqlx.PRI_LOWEST)
        self.add_hook("vote_started", self.handle_vote_started)
        self.add_hook("vote_ended", self.handle_vote_ended)
        self.add_hook("map", self.handle_map)
        self.add_command(("admin", "report"), self.cmd_admin, client_cmd_perm=0)

        # Update topic on these hooks
        for hook in ["round_end", "game_start", "game_end", "map", "game_countdown"]:
            self.add_hook(hook, self.update_topic, priority=minqlx.PRI_LOW)

        self.set_cvar_once("qlx_ircServer", "irc.quakenet.org")
        self.set_cvar_once("qlx_ircRelayChannel", "")
        self.set_cvar_once("qlx_ircRelayChannelPw", "")
        self.set_cvar_once("qlx_ircRelayIrcChat", "1")
        self.set_cvar_once("qlx_ircIdleChannels", "")
        self.set_cvar_once("qlx_ircReportChannel", "")
        self.set_cvar_once("qlx_ircReportChannelPw", "")
        self.set_cvar_once("qlx_ircNickname", "minqlx-{}".format(random.randint(1000, 9999)))
        self.set_cvar_once("qlx_ircPassword", "")
        self.set_cvar_once("qlx_ircColors", "0")
        self.set_cvar_once("qlx_ircQuakenetUser", "")
        self.set_cvar_once("qlx_ircQuakenetPass", "")
        self.set_cvar_once("qlx_ircQuakenetHidden", "0")

        self.server = self.get_cvar("qlx_ircServer")
        self.relay = self.get_cvar("qlx_ircRelayChannel")
        self.relay_pw = self.get_cvar("qlx_ircRelayChannelPw")
        self.idle = self.get_cvar("qlx_ircIdleChannels", list)
        self.report = self.get_cvar("qlx_ircReportChannel")
        self.report_pw = self.get_cvar("qlx_ircReportChannelPw")
        self.nickname = self.get_cvar("qlx_ircNickname")
        self.password = self.get_cvar("qlx_ircPassword")
        self.qnet = (self.get_cvar("qlx_ircQuakenetUser"),
            self.get_cvar("qlx_ircQuakenetPass"),
            self.get_cvar("qlx_ircQuakenetHidden", bool))
        self.is_relaying = self.get_cvar("qlx_ircRelayIrcChat", bool)

        self.authed = set()
        self.auth_attempts = {}

        if not self.server:
            self.logger.warning("IRC plugin loaded, but no IRC server specified.")
        elif not self.relay and not self.idle and not self.password:
            self.logger.warning("IRC plugin loaded, but no channels or password set. Not connecting.")
        else:
            self.irc = SimpleAsyncIrc(self.server, self.nickname, self.handle_msg, self.handle_perform, self.handle_raw)
            self.irc.start()
            self.logger.info("Connecting to {}...".format(self.server))

        self.topic = "" + u"\x0304[\u2022 Live] \x0301" + " {}"
        self.update_topic()

    def handle_chat(self, player, msg, channel):
        handled_channels = {"chat": [COLORS[2], ""],
                    "red_team_chat": [COLORS[1], ""],
                    "blue_team_chat": [COLORS[4], ""],
                    "spectator_chat": ["\x0310", "(spec)"]} # teal
        team_color = {"red": COLORS[1], "blue": COLORS[4], "spec": "\x0301", "free":COLORS[2]}

        if self.irc and self.relay and channel.name in handled_channels:
            color, label = handled_channels[channel.name]
            text = "<{tc}{p}{tc}{l}> {c}{b}{m}{b}{c}".format(tc=team_color.get(player.team, "\x0301"), c=color,p=player.name, l=label, m=msg, b=BOLDCHAT)
            self.irc.msg(self.relay, self.translate_colors(text))


    def handle_unload(self, plugin):
        if plugin == self.__class__.__name__ and self.irc and self.irc.is_alive():
            self.irc.quit("Plugin unloaded!")
            self.irc.stop()

    def handle_player_connect(self, player):
        if self.irc and self.relay:
            self.irc.msg(self.relay, EXTRA.get('connect', '') + self.translate_colors("{} connected.".format(player.name)))
            if self.game.state == "warmup":
                self.update_topic()

    def handle_player_disconnect(self, player, reason):
        if reason and reason[-1] not in ("?", "!", "."):
            reason = reason + "."

        if self.irc and self.relay:
            self.irc.msg(self.relay, EXTRA.get('disconnect', '') + self.translate_colors("{} {}".format(player.name, reason)))

            if self.game.state == "warmup":
                self.update_topic()


    def handle_vote_started(self, caller, vote, args):
        if self.irc and self.relay:
            caller = caller.name if caller else "The server"
            self.irc.msg(self.relay, EXTRA.get('vote', '') + self.translate_colors("{} called a vote: {} {}".format(caller, vote, args)))

    def handle_vote_ended(self, votes, vote, args, passed):
        if self.irc and self.relay:
            if passed:
                self.irc.msg(self.relay, EXTRA.get('vote', '') + self.translate_colors("Vote passed ({} - {}).".format(*votes)))
            else:
                self.irc.msg(self.relay, EXTRA.get('vote', '') + self.translate_colors("Vote failed."))

    def handle_map(self, map, factory):
        if self.irc and self.relay:
            self.irc.msg(self.relay, EXTRA.get('map', '') + self.translate_colors("Changing map to {}...".format(map)))

    def handle_msg(self, irc, user, channel, msg):
        if not msg:
            return

        cmd = msg[0].lower()
        if channel.lower() == self.relay.lower():
            if cmd in (".players", ".status", ".info", ".map", ".server"):
                self.server_report(self.relay)
            elif cmd in (".topic"):
                self.update_topic()
            elif self.is_relaying:
                minqlx.CHAT_CHANNEL.reply("[IRC] ^6{}^7:^2 {}".format(user[0], " ".join(msg)))
        elif channel == user[0]: # Is PM?
            if len(msg) > 1 and msg[0].lower() == ".auth" and self.password:
                if user in self.authed:
                    irc.msg(channel, "You are already authenticated.")
                elif msg[1] == self.password:
                    self.authed.add(user)
                    irc.msg(channel, "You have been successfully authenticated. You can now use .qlx to execute commands.")
                else:
                    # Allow up to 3 attempts for the user's IP to authenticate.
                    if user[2] not in self.auth_attempts:
                        self.auth_attempts[user[2]] = 3
                    self.auth_attempts[user[2]] -= 1
                    if self.auth_attempts[user[2]] > 0:
                        irc.msg(channel, "Wrong password. You have {} attempts left.".format(self.auth_attempts[user[2]]))
            elif len(msg) > 1 and user in self.authed and msg[0].lower() == ".qlx":
                @minqlx.next_frame
                def f():
                    try:
                        minqlx.COMMANDS.handle_input(IrcDummyPlayer(self.irc, user[0]), " ".join(msg[1:]), IrcChannel(self.irc, user[0]))
                    except Exception as e:
                        irc.msg(channel, "{}: {}".format(e.__class__.__name__, e))
                        minqlx.log_exception()
                f()

    def handle_perform(self, irc):
        self.logger.info("Connected to IRC!".format(self.server))

        quser, qpass, qhidden = self.qnet
        if quser and qpass and "NETWORK" in self.irc.server_options and self.irc.server_options["NETWORK"] == "QuakeNet":
            self.logger.info("Authenticating on Quakenet as \"{}\"...".format(quser))
            self.irc.msg("Q@CServe.quakenet.org", "AUTH {} {}".format(quser, qpass))
            if qhidden:
                self.irc.mode(self.irc.nickname, "+x")

        for channel in self.idle:
            irc.join(channel)
        if self.relay:
            irc.join(self.relay, self.relay_pw)
        if self.report:
            irc.join(self.report, self.report_pw)

    def handle_raw(self, irc, msg):
        split_msg = msg.split()
        if len(split_msg) > 2 and split_msg[1] == "NICK":
            user = re_user.match(split_msg[0][1:])
            if user and user.groups() in self.authed:
                # Update nick if an authed user changed it.
                self.authed.remove(user.groups())
                self.authed.add((split_msg[2][1:], user.groups()[1], user.groups()[2]))
        elif len(split_msg) > 1 and split_msg[1] == "433":
            irc.nick(irc.nickname + "_")

    @classmethod
    def translate_colors(cls, text):
        if not cls.get_cvar("qlx_ircColors", bool):
            return cls.clean_text(text)

        for i, color in enumerate(COLORS):
            text = text.replace("^{}".format(i), color)

        return text

    @minqlx.next_frame
    def server_report(self, channel, topic=None):
        teams = self.teams()
        players = teams["free"] + teams["red"] + teams["blue"] + teams["spectator"]
        game = self.game
        # Make a list of players.
        plist = []
        for t in teams:
            if not teams[t]:
                continue
            elif t == "free":
                plist.append("Free: " + ", ".join([p.clean_name for p in teams["free"]]))
            elif t == "red":
                plist.append(BOLDCHAT + "\x0304Red"+FONTRESET+"\x03: " + ", ".join([p.clean_name for p in teams["red"]]))
            elif t == "blue":
                plist.append(BOLDCHAT + "\x0302Blue"+FONTRESET+"\x03: " + ", ".join([p.clean_name for p in teams["blue"]]))
            elif t == "spectator":
                plist.append("\x02Spec\x02: " + ", ".join([p.clean_name for p in teams["spectator"]]))


        # Info about the game state.
        if game.state == "in_progress":
            if game.type_short == "race" or game.type_short == "ffa":
                ginfo = "The game is in progress"
            else:
                ginfo = "The score is \x02\x0304{}\x03 - \x0302{}\x03\x02".format(game.red_score, game.blue_score)
        elif game.state == "countdown":
            ginfo = "The game is about to start"
        else:
            ginfo = "The game is in warmup"

        ginfo_format = "{} on \x02{}\x02 ({}) with \x02{}/{}\x02 players:" .format(ginfo, self.clean_text(game.map_title),
            game.type_short.upper(), len(players), self.get_cvar("sv_maxClients"))

        if topic:
            self.irc.topic(self.relay, self.topic.format(ginfo_format))
            return

        self.irc.msg(channel, ginfo_format)
        self.irc.msg(channel, "{}".format(" ".join(plist)))

    def update_topic(self, one="", two="", three="", four="", five=""):
        self.server_report(self.relay, True)


    def cmd_admin(self, player, msg, channel):
        if self.irc and self.report:
            text = " ".join(msg[1:])
            self.irc.msg(self.report, self.translate_colors('{} ({}); {}"{}"'.format(player.name, player.steam_id, BOLDCHAT, text)))
            player.tell("Thank you for your report.")
        return minqlx.RET_STOP_ALL

# ====================================================================
#                     DUMMY PLAYER & IRC CHANNEL
# ====================================================================

class IrcChannel(minqlx.AbstractChannel):
    name = "irc"
    def __init__(self, irc, recipient):
        self.irc = irc
        self.recipient = recipient

    def __repr__(self):
        return "{} {}".format(str(self), self.recipient)

    def reply(self, msg):
        for line in msg.split("\n"):
            self.irc.msg(self.recipient, line)

class IrcDummyPlayer(minqlx.AbstractDummyPlayer):
    def __init__(self, irc, user):
        self.irc = irc
        self.user = user
        super().__init__(name="IRC-{}".format(irc.nickname))

    @property
    def steam_id(self):
        return minqlx.owner()

    @property
    def channel(self):
        return IrcChannel(self.irc, self.user)

    def tell(self, msg):
        for line in msg.split("\n"):
            self.irc.msg(self.user, line)

# ====================================================================
#                       SIMPLE INTERPROCESS LOCK
# ====================================================================

class FLock:
    """Simple(st) filelock to provide interprocess syncronisation featuring fcntl."""   
    def __init__(self, filename):
        self.filename = filename
        self.handle   = open(filename, 'w')

    def acquire(self):
        """Acquire the lock."""
        fcntl.flock(self.handle, fcntl.LOCK_EX)
        
    def release(self):
        """Release the lock."""
        fcntl.flock(self.handle, fcntl.LOCK_UN)
        
    def __del__(self):
        self.handle.close()

# ====================================================================
#                        SIMPLE ASYNC IRC
# ====================================================================

re_msg = re.compile(r"^:([^ ]+) PRIVMSG ([^ ]+) :(.*)$")
re_user = re.compile(r"^(.+)!(.+)@(.+)$")

IDENTFILE = os.path.join(os.environ["HOME"], ".oidentd.conf")
IDENTFMT  = 'global {{ reply "{}" }}'
LOCKFILE  = "/tmp/ident.lock"

class SimpleAsyncIrc(threading.Thread):
    def __init__(self, address, nickname, msg_handler, perform_handler, raw_handler=None, stop_event=threading.Event(), ident=None):
        split_addr = address.split(":")
        self.host = split_addr[0]
        self.port = int(split_addr[1]) if len(split_addr) > 1 else 6667
        self.nickname = nickname
        self.msg_handler = msg_handler
        self.perform_handler = perform_handler
        self.raw_handler = raw_handler
        self.stop_event = stop_event
        self.reader = None
        self.writer = None
        self.server_options = {}
        super().__init__()

        self._lock = threading.Lock()
        self._old_nickname = self.nickname
        
        # support for ident server oidentd 
        self.ident        = ident if ident else nickname
        self.ifile_buf    = None
        self.flock        = FLock(LOCKFILE)

    def run(self):
        loop = asyncio.new_event_loop()
        logger = minqlx.get_logger("irc")
        asyncio.set_event_loop(loop)
        while not self.stop_event.is_set():
            try:
                loop.run_until_complete(self.connect())
            except Exception:
                minqlx.log_exception()

            # Disconnected. Try reconnecting in 30 seconds.
            logger.info("Disconnected from IRC. Reconnecting in 30 seconds...")
            time.sleep(30)
        loop.close()

    def stop(self):
        self.stop_event.set()

    def write(self, msg):
        if self.writer:
            with self._lock:
                self.writer.write(msg.encode(errors="ignore"))

    @asyncio.coroutine
    def connect(self):
        # Tell oidentd our 'self.ident' before connecting
        self.writeIdentFile()
        
        self.reader, self.writer = yield from asyncio.open_connection(self.host, self.port)
        self.write("NICK {0}\r\nUSER {0} 0 * :{0}\r\n".format(self.nickname))

        while not self.stop_event.is_set():
            line = yield from self.reader.readline()
            if not line:
                break
            line = line.decode("utf-8", errors="ignore").rstrip()
            if line:
                yield from self.parse_data(line)

        self.write("QUIT Quit by user.\r\n")
        self.writer.close()

    @asyncio.coroutine
    def parse_data(self, msg):
        split_msg = msg.split()
        if len(split_msg) > 1 and split_msg[0] == "PING":
            self.pong(split_msg[1].lstrip(":"))
        elif len(split_msg) > 3 and split_msg[1] == "PRIVMSG":
            r = re_msg.match(msg)
            user = re_user.match(r.group(1)).groups()
            channel = user[0] if self.nickname == r.group(2) else r.group(2)
            self.msg_handler(self, user, channel, r.group(3).split())
        elif len(split_msg) > 2 and split_msg[1] == "NICK":
            user = re_user.match(split_msg[0][1:])
            if user and user.group(1) == self.nickname:
                self.nickname = split_msg[2][1:]
        elif split_msg[1] == "005":
            for option in split_msg[3:-1]:
                opt_pair = option.split("=", 1)
                if len(opt_pair) == 1:
                    self.server_options[opt_pair[0]] = ""
                else:
                    self.server_options[opt_pair[0]] = opt_pair[1]
            # We're connected, restore the ident file
            self.restoreIdentFile()
        elif len(split_msg) > 1 and split_msg[1] == "433":
            self.nickname = self._old_nickname
        # Stuff to do after we get the MOTD.
        elif re.match(r":[^ ]+ (376|422) .+", msg):
            self.perform_handler(self)

        # If we have a raw handler, let it do its stuff now.
        if self.raw_handler:
            self.raw_handler(self, msg)

    def msg(self, recipient, msg):
        self.write("PRIVMSG {} :{}\r\n".format(recipient, msg))

    def nick(self, nick):
        with self._lock:
            self._old_nickname = self.nickname
            self.nickname = nick
        self.write("NICK {}\r\n".format(nick))

    def join(self, channels, pw=""):
        self.write("JOIN {} {}\r\n".format(channels, pw))

    def part(self, channels):
        self.write("PART {}\r\n".format(channels))

    def mode(self, what, mode):
        self.write("MODE {} {}\r\n".format(what, mode))

    def kick(self, channel, nick, reason):
        self.write("KICK {} {}:{}\r\n".format(channel, nick, reason))

    def quit(self, reason):
        self.write("QUIT :{}\r\n".format(reason))

    def pong(self, n):
        self.write("PONG :{}\r\n".format(n))

    def topic(self, channel, newtopic):
        self.write("TOPIC {} : {}\r\n".format(channel, newtopic))
    
    def writeIdentFile(self):
        """Write self.ident to oidentd's user cfg file but
        keep any entries for restoring them later."""

        if not os.path.isfile(IDENTFILE):
            return
        
        # In the process of connecting, acquire the lock 
        self.flock.acquire()
        try:
            with open(IDENTFILE, 'r') as ifile:
                self.ifile_buf = ifile.readlines()
            with open(IDENTFILE, 'w') as ifile:
                ifile.write(IDENTFMT.format(self.ident))
        except Exception:
            minqlx.log_exception()
          
    def restoreIdentFile(self):
        """Restore the identfile."""
        if not os.path.isfile(IDENTFILE):
            return
        
        try:
            with open(IDENTFILE, 'w') as ifile:
                for l in self.ifile_buf:
                    ifile.write(l)
        except Exception:
            minqlx.log_exception()
        # We're done, release the lock so other 
        # minqlx-plugins can do the same
        self.flock.release()
