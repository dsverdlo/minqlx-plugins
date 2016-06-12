# This is a plugin created by iouonegirl(@gmail.com)
# Copyright (c) 2016 iouonegirl
# https://github.com/dsverdlo/minqlx-plugins
#
# You are free to modify this plugin to your custom,
# except for the version command related code.
#
# It tracksprovides commands to translate words and sentences,
# look up definitions, and much more
#
# To use the translation functions, please make a free account
# on yandex.net and get an API key, which you'll set as a cvar.
#
# Uses
# set qlx_translate_api_key "apikey1337thisisnotanactualapikey69"
#       ^ get your key at: https://tech.yandex.com/keys/get/?service=trnsl

import minqlx
import os
import time
import re
import random
import threading
import requests

VERSION = "v0.13"



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

# customizable vars
C = "^4"
DEFAULT_LANG = "en"
SERVER_DEFAULT = "en"
AUTO_TRANS_COMMANDS = False

PLAYER_KEY = "minqlx:players:{}"
LANG_KEY = PLAYER_KEY + ":language"
AUTO_KEY = PLAYER_KEY + ":autotranslate"

LANGS = {
'Albanian': 'sq',
 'Armenian': 'hy',
 'Azerbaijani': 'az',
 'Belarusian': 'be',
 'Bulgarian': 'bg',
 'Catalan': 'ca',
 'Croatian': 'hr',
 'Czech': 'cs',
 'Danish': 'da',
 'Dutch': 'nl',
 'English': 'en',
 'Estonian': 'et',
 'Finnish': 'fi',
 'French': 'fr',
 'German': 'de',
 'Greek': 'el',
 'Hungarian': 'hu',
 'Italian': 'it',
 'Latvian': 'lv',
 'Lithuanian': 'lt',
 'Macedonian': 'mk',
 'Norwegian': 'no',
 'Polish': 'pl',
 'Portuguese': 'pt',
 'Romanian': 'ro',
 'Russian': 'ru',
 'Serbian': 'sr',
 'Slovak': 'sk',
 'Slovenian': 'sl',
 'Spanish': 'es',
 'Swedish': 'sv',
 'Turkish': 'tr',
 'Ukrainian': 'uk'}

yandex = [
    "az-ru","be-bg","be-cs","be-de","be-en","be-es","be-fr","be-it","be-pl",
    "be-ro","be-ru","be-sr","be-tr","bg-be","bg-ru","bg-uk","ca-en","ca-ru",
    "cs-be","cs-en","cs-ru","cs-uk","da-en","da-ru","de-be","de-en","de-es",
    "de-fr","de-it","de-ru","de-tr","de-uk","el-en","el-ru","en-be","en-ca",
    "en-cs","en-da","en-de","en-el","en-es","en-et","en-fi","en-fr","en-hu",
    "en-it","en-lt","en-lv","en-mk","en-nl","en-no","en-pt","en-ru","en-sk",
    "en-sl","en-sq","en-sv","en-tr","en-uk","es-be","es-de","es-en","es-ru",
    "es-uk","et-en","et-ru","fi-en","fi-ru","fr-be","fr-de","fr-en","fr-ru",
    "fr-uk","hr-ru","hu-en","hu-ru","hy-ru","it-be","it-de","it-en","it-ru",
    "it-uk","lt-en","lt-ru","lv-en","lv-ru","mk-en","mk-ru","nl-en","nl-ru",
    "no-en","no-ru","pl-be","pl-ru","pl-uk","pt-en","pt-ru","ro-be","ro-ru",
    "ro-uk","ru-az","ru-be","ru-bg","ru-ca","ru-cs","ru-da","ru-de","ru-el",
    "ru-en","ru-es","ru-et","ru-fi","ru-fr","ru-hr","ru-hu","ru-hy","ru-it",
    "ru-lt","ru-lv","ru-mk","ru-nl","ru-no","ru-pl","ru-pt","ru-ro","ru-sk",
    "ru-sl","ru-sq","ru-sr","ru-sv","ru-tr","ru-uk","sk-en","sk-ru","sl-en",
    "sl-ru","sq-en","sq-ru","sr-be","sr-ru","sr-uk","sv-en","sv-ru","tr-be",
    "tr-de","tr-en","tr-ru","tr-uk","uk-bg","uk-cs","uk-de","uk-en","uk-es",
    "uk-fr","uk-it","uk-pl","uk-ro","uk-ru","uk-sr","uk-tr"]

TAGS = {v: k for k, v in LANGS.items()}


class translate(iouonegirlPlugin):
    def __init__(self):
        super().__init__(self.__class__.__name__, VERSION)

        self.set_cvar_once("qlx_translate_api_key", "")

        self.add_command("urban", self.cmd_urban, usage="<word>|<phrase>")
        #self.add_command(("leet", "1337", "l33t"), self.cmd_leet, usage="<word>|<phrase>")
        self.add_command("languages", self.cmd_languages)
        self.add_command("translations", self.cmd_translations)
        self.add_command(("translate-last", "trans-last", "translast", "translatelast"), self.cmd_translate_last, usage="<to> <player>")
        self.add_hook("player_disconnect", self.handle_player_disconnect)
        self.buffer = {}

        self.add_hook("chat", self.handle_chat)
        self.add_command(("translate", "trans"), self.cmd_translate, usage="<to> <sentence>")
        self.add_command(("stranslate", "strans"), self.cmd_silent_translate, usage="<to> <sentence>")
        #self.add_command(("define", "def", "definition"), self.cmd_define, usage="<word>")
##        self.add_command(("lang", "language"), self.cmd_language, usage="[<tag>|<language>]")
##        self.add_command(("autotrans", "autotranslate"), self.cmd_auto_translate)
        self.add_command(("translatecmds", "transcmds", "transcommands", "translatecommands"), self.cmd_commands)
        self.add_command(("transexamples", "translateexamples"), self.cmd_examples)
        if not self.get_cvar("qlx_translate_api_key"):
            self.msg("No Yandex API key set. Get one for free: https://tech.yandex.com/keys/get/?service=trnsl")

    def handle_chat(self, player, msg, channel):
        if channel != "chat": return

        #line = " ".join(msg)
        if msg[0] == "!": return

        if not player.steam_id in self.buffer:
            self.buffer[player.steam_id] = []

        self.buffer[player.steam_id].append(msg)

        if len(self.buffer[player.steam_id]) > 3:
            self.buffer[player.steam_id].pop(0)


##        def callback(player, query, results):
##            def callback_autotrans(_p, _q, _r):
##                _j = _r.json()
##                _lang = _j['lang']
##                _text = _j['text'][0]
##                _p.tell("^6AutoTrans^7({}){}: {}".format(_lang, C, _text))
##
##            # Okay we received a lang tag for the chat message. check if anyone needs a translation
##            json = results.json()
##            l = json['lang']
##            if l != SERVER_DEFAULT: # If the tag is not the server default language...
##                for p in self.players():
##                    # If the message comes from this player, go to next
##                    if p.id == player.id: continue
##                    # If this player doesnt want auto trans, go to next
##                    if not self.help_get_auto_pref(p): continue
##                    # If this is the say_team from another team, go to next
##                    if channel == minqlx.RED_TEAM_CHAT_CHANNEL and p.team != 'red': continue
##                    if channel == minqlx.BLUE_TEAM_CHAT_CHANNEL and p.team != 'blue': continue
##                    # if this is the default language of the player, go to next
##                    pref_tag = self.help_get_lang_tag(p)
##                    if pref_tag == l: continue
##                    # Go fetch the translation
##                    url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
##                    params = {'key':'trnsl.1.1.20160215T152939Z.eb62d98148b07bcd.911d314592dc12c39c3be65184da90198998225c',
##                        'text':query, 'lang':pref_tag}
##                    hdr = None
##                    self.help_fetch(p, query, url, hdr, params, callback_autotrans)
##
##        if not player: return
##        if not msg: return
##
##        # If you don't want the server to translate commands to people
##        if not AUTO_TRANS_COMMANDS:
##            # check if a command was spoken
##            if msg[0].startswith("!"): return
##
##        if not self.get_cvar("qlx_translate_api_key"):
##            self.msg("^7No yandex.net API key found. Cannot translate without one...")
##            return
##
##        url = 'https://translate.yandex.net/api/v1.5/tr.json/detect'
##        params = {'key':self.get_cvar("qlx_translate_api_key"),
##                'text':msg}
##        hdr = None
##
##        # Fetch the language of the msg
##        self.help_fetch(player, msg, url, hdr, params, callback)



    def cmd_examples(self, player, msg, channel):
        player.tell("^6Translation example commands:\n")
        player.tell("^2!translate ru What is love?    ^3(tr to russian)")
        player.tell("^2!stranslate fr No one will see this   ^3(silent translation)")
        player.tell("^2!translate nl-en Boom    ^3(force origin language)")
        player.tell("^2!translate-last en cooller   ^3(tr last 3 cooller msgs to english)")


    def cmd_commands(self, player, msg, channel):
        channel.reply("^7TranslationCommands: ^2!languages^7, ^2!translations^7, ^2!urban^7, ^2!translate^7, ^2!stranslate^7, ^2!translate-last")

    def cmd_silent_translate(self, player, msg, channel):
        #player.tell("^6TranslateRequest: ^2{}".format(msg[1:]))
        self.cmd_translate(player, msg, channel, True)
        return minqlx.RET_STOP_ALL

    def cmd_translate(self, player, msg, channel, silent=False):
        def callback(_player, _query, _results):
            _res = _results.json()
            translated = _res['text'][0]
            output = "^7({}): {}{}".format(_res['lang'], C, translated)
            if silent:
                player.tell("^6Psst: " + output)
                return minqlx.RET_STOP_ALL
            if self.help_be_quiet(player):
                minqlx.SPECTATOR_CHAT_CHANNEL.reply(output)
            else:
                channel.reply(output)


        if len(msg) < 3:
            return minqlx.RET_USAGE

        if "-" in msg[1].lower():
            if msg[1].lower() in yandex:
                to = msg[1]
            else:
                player.tell("^6Translation ({}) not supported... Try ^2!translations ^6for a list.".format(msg[1]))
                return minqlx.RET_STOP_ALL
        elif msg[1].lower() in TAGS:
            to = msg[1]
        elif msg[1].title() in LANGS:
            to = LANGS[msg[1].title()]
        else:
            matches = []
            for lang in LANGS:
                if msg[1] in lang.lower():
                    matches.append([lang, LANGS[lang]])
            if not matches:
                player.tell("^6No languages matched {}... Try ^2!languages ^6for a list.".format(msg[1]))
                return minqlx.RET_STOP_ALL
            elif len(matches) == 1:
                lang, tag = matches[0]
                to = tag
            else:
                _map = map(lambda pair: "{}-{}".format(pair[0], pair[1]), matches)
                player.tell("^6Multiple matches found: ^7" + ", ".join(list(_map)))
                return minqlx.RET_STOP_ALL


        message = " ".join(msg[2:])
        if not self.get_cvar("qlx_translate_api_key"):
            player.tell("^7No yandex.net API key installed. Please contact server admin.")
            return minqlx.RET_STOP_ALL

        url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
        params = {'key':self.get_cvar("qlx_translate_api_key"),
                'text':message,
                'lang':to}
        hdr = None

        self.help_fetch(player, message, url, hdr, params, callback)

    def cmd_translate_last(self, player, msg, channel, silent=False):
        @minqlx.next_frame
        def callback(_player, _query, _results):
            _res = _results.json()
            translated = _res['text'][0]
            output = "^7({}): {}{}".format(_res['lang'], C, translated)
            player.tell(output)
            return minqlx.RET_STOP_ALL

        @minqlx.thread
        def fetch_intervals(lst):
            for message in lst:
                url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
                params = {'key':self.get_cvar("qlx_translate_api_key"),
                    'text':message,
                    'lang':to}
                hdr = None
                self.help_fetch(player, message, url, hdr, params, callback)
                time.sleep(0.8)

        if len(msg) < 3:
            return minqlx.RET_USAGE

        if "-" in msg[1].lower():
            if msg[1].lower() in yandex:
                to = msg[1]
            else:
                player.tell("^6Translation ({}) not supported... Try ^2!translations ^6for a list.".format(msg[1]))
                return minqlx.RET_STOP_ALL
        elif msg[1].lower() in TAGS:
            to = msg[1]
        elif msg[1].title() in LANGS:
            to = LANGS[msg[1].title()]
        else:
            matches = []
            for lang in LANGS:
                if msg[1] in lang.lower():
                    matches.append([lang, LANGS[lang]])
            if not matches:
                player.tell("^6No languages matched {}... Try ^2!languages ^6for a list.".format(msg[1]))
                return minqlx.RET_STOP_ALL
            elif len(matches) == 1:
                lang, tag = matches[0]
                to = tag
            else:
                _map = map(lambda pair: "{}-{}".format(pair[0], pair[1]), matches)
                player.tell("^6Multiple matches found: ^7" + ", ".join(list(_map)))
                return minqlx.RET_STOP_ALL


        target_player = self.find_by_name_or_id(player, msg[2])
        if not target_player:
            return minqlx.RET_STOP_ALL
        # move up
        if not target_player.steam_id in self.buffer or not self.buffer[target_player.steam_id]:
            player.tell("Translate error: No chat buffered from {}.".format(target_player.name))

        if not self.get_cvar("qlx_translate_api_key"):
            player.tell("^7No yandex.net API key installed. Cannot translate without one...")
            return minqlx.RET_STOP_ALL

        fetch_intervals(self.buffer[target_player.steam_id])
        return minqlx.RET_STOP_ALL





##    def cmd_language(self, player, msg, channel):
##        # if no arguments given, just check the language
##        if len(msg) < 2:
##            if self.help_get_auto_pref(player):
##                tag = self.help_get_lang_tag(player)
##                lang = TAGS.get(tag, DEFAULT_LANG)
##                channel.reply("^7Your default language is: ^6{}^7({}). Use ^2!lang^7 to change it.".format(lang, tag))
##                return
##            else:
##                channel.reply("^7AutoTranslation is turned off. Activate with !autotrans or !language X")
##                return
##        # otherwise try to set a new language
##        else:
##            lang = TAGS.get(msg[1].lower()) # try correct tag
##            if lang:
##                self.help_set_lang_tag(player, msg[1].lower())
##                channel.reply("^7AutoTranslate language changed to: ^6{}^7({}).".format(lang, msg[1]))
##                self.help_change_auto_pref(player, 1)
##                return
##            else: # try every language for a match
##                maybe = []
##                for lang in LANGS:
##                    if msg[1].title() in lang:
##                        maybe.append([lang, LANGS[lang]])
##                if not maybe:
##                    player.tell("^6No languages matched {}... Try ^2!languages ^6for a list.".format(msg[1]))
##                    return minqlx.RET_STOP_ALL
##                elif len(maybe) == 1:
##                    lang, tag = maybe[0]
##                    self.help_set_lang_tag(player, tag)
##                    channel.reply("^7AutoTranslate language changed to: ^6{}^7({}).".format(lang, tag))
##                    self.help_change_auto_pref(player, 1)
##                    return
##                else:
##                    _map = map(lambda pair: "{}->{}".format(pair[0], pair[1]), maybe)
##                    player.tell("^6Multiple matches found: ^7" + ", ".join(list(_map)))
##                    return minqlx.RET_STOP_ALL



    def cmd_languages(self, player, msg, channel):
        _printable = []
        keys = list(LANGS.keys())
        keys.sort()
        for i,lang in enumerate(keys):
            newline = "" if i % 4 else "\n"
            _printable.append("{}^5{}^7: ^4{}".format(newline, lang, LANGS[lang]))
        #_printable.sort()
        player.tell("^6Supported languages: ^7" + "^7, ".join(_printable))

        msg = "^7{} can open their console to see all the supported languages.".format(player.name)
        if self.help_be_quiet(player):
            minqlx.SPECTATOR_CHAT_CHANNEL.reply(msg)
        else:
            channel.reply(msg)


##    def cmd_auto_translate(self, player, msg, channel):
##        # Get the preference
##        old_pref = self.help_get_auto_pref(player)
##        # Change it
##        self.help_change_auto_pref(player)
##
##        if old_pref:
##            channel.reply("^7{} will stop receiving automatic translations.".format(player.name))
##        else:
##            tag = self.help_get_lang_tag(player)
##            channel.reply("^7{} activated auto translations in their default language ({}).".format(player.name, tag))

    def cmd_translations(self, player, msg, channel):
        def add_colors(tr):
            return "{}{}^7-{}{}".format("^5", tr[0:2], "^4", tr[3:5])

        _printable = map(add_colors, yandex)
        player.tell("^6Supported translations: \n" + "^7, ".join(list(_printable)))
        m = "^7{} can open their console to see all the supported translations.".format(player.name)
        if self.help_be_quiet(player):
            minqlx.SPECTATOR_CHAT_CHANNEL.reply(m)
        else:
            channel.reply(m)


    def cmd_urban(self, player, msg, channel):
        if len(msg) < 2:
            return minqlx.RET_USAGE

        query = " ".join(msg[1:])
        url = 'https://mashape-community-urban-dictionary.p.mashape.com/define?term={}'.format(query)
        headers =  { "X-Mashape-Key": "CAwrPAMPB6msh3K3YsRflDE0hmswp14vd4tjsnwbD5rMUVQWvo" }

        self.help_fetch(player, query, url, headers, None, self.help_callback_urban)

    def cmd_leet(self, player, msg, channel):
        if len(msg)< 2:
            return minqlx.RET_USAGE
        query = "+".join(msg[1:])
        url = 'https://montanaflynn-l33t-sp34k.p.mashape.com/encode?text={}'.format(query)
        headers =  { "X-Mashape-Key": "CAwrPAMPB6msh3K3YsRflDE0hmswp14vd4tjsnwbD5rMUVQWvo" }
        self.help_fetch(player, query, url, headers, None, self.help_callback_leet)
        return minqlx.RET_STOP_ALL

    @minqlx.thread
    def help_fetch(self, player, query, url, headers, params, callback):
        @minqlx.next_frame
        def error(m): self.msg(m)
        res = requests.get(url, headers=headers, params=params)
        if res.status_code != requests.codes.ok:
            error("^1RequestError^7: code {}.".format(res.status_code))
        else:
            callback(player, query, res)

    def help_callback_urban(self, player, query, results):
        @minqlx.next_frame
        def msg(m):
            if self.help_be_quiet(player):
                minqlx.SPECTATOR_CHAT_CHANNEL.reply(m)
            else:
                self.msg(m)

        results = results.json()
        if results['result_type'] != "no_results":
            first_result = results['list'][0]
            definition = first_result['definition']
            example = first_result['example']

            msg("^5UrbanDef: ^7{}".format(definition))
            if example:
                msg("^5UrbanExample: ^7{}".format(example))
        else:
            msg("{}No urban dict results found for: ".format(C, query))

    def help_be_quiet(self, player):
        return player.team == "spectator" and self.game.type_short == "duel" and self.game.state == "in_progress"

    def help_callback_leet(self, player, query, results):
        self.msg("{}^7: ^2(!leet) {}".format(player.name, results))

##    def help_get_auto_pref(self, player):
##        key = AUTO_KEY.format(player.steam_id)
##        if not (key in self.db): self.db[key] = 0
##        return int(self.db[key])
##
##    def help_change_auto_pref(self, player, force=0):
##        key = AUTO_KEY.format(player.steam_id)
##        self.db[key] = force or 0 if self.help_get_auto_pref(player) else 1
##
##    def help_get_lang_tag(self, player):
##        # formulate key
##        key = LANG_KEY.format(player.steam_id)
##        # if no language defined yet, set the default
##        if not (key in self.db): self.help_set_lang_tag(player, DEFAULT_LANG)
##        # return tag
##        return self.db[key]
##
##    def help_set_lang_tag(self, player, tag):
##        # formulate key
##        key = LANG_KEY.format(player.steam_id)
##        # set it (after a quick test that it exists)
##        if TAGS.get(tag): self.db[key] = tag

    @minqlx.delay(0.3)
    def help_delay_msg(self, message):
        self.msg(message)

    def handle_player_disconnect(self, player, reason):
        if player.steam_id in self.buffer:
            del self.buffer[player.steam_id]
