# minqlbot - A Quake Live server administrator bot.
# Copyright (C) 2015 Mino <mino@minomino.org>

# This file is part of minqlbot.

# minqlbot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# minqlbot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with minqlbot. If not, see <http://www.gnu.org/licenses/>.

import minqlx
import random

class stationfun(minqlx.Plugin):
	def __init__(self):
		self.add_command("cookie", self.cmd_cookies)
		self.add_command("drugs", self.cmd_drugs)
		self.add_command("weed", self.cmd_weed)
		self.add_command("meth", self.cmd_meth)
		self.add_command("beer", self.cmd_beer)
		self.add_command("sex", self.cmd_sex)
		self.add_command("anal", self.cmd_anal)
		self.add_command("piss", self.cmd_piss)
		self.add_command("oralsex", self.cmd_oralsex)
		self.add_command("fellatio", self.cmd_fellatio)
		self.add_command("surprisebuttsex", self.cmd_surprisebuttsex)
		self.add_command("vodka", self.cmd_vodka)
		self.add_command("whiskey", self.cmd_whiskey)
		self.add_command("muffins", self.cmd_muffins)
		self.add_command("blowjob", self.cmd_blowjob)
		self.add_command("hookers", self.cmd_hookers)
		self.add_command("peen", self.cmd_peen)
		self.add_command("ecstasy", self.cmd_ecstasy)
		self.add_command("exstasy", self.cmd_exstasy)
		self.add_command("mdma", self.cmd_mdma)
		self.add_command("molly", self.cmd_molly)
		self.add_command("coke", self.cmd_coke)
		self.add_command("cocaine", self.cmd_cocaine)
		self.add_command("heroin", self.cmd_heroin)
		self.add_command("cock", self.cmd_cock)
		self.add_command("dick", self.cmd_dick)
		self.add_command("cunt", self.cmd_cunt) 
		self.add_command("tnuc", self.cmd_tnuc) 
		self.add_command("wanker", self.cmd_wanker)
		self.add_command("porn", self.cmd_porn)
		self.add_command("bastard", self.cmd_bastard)
		self.add_command("suck", self.cmd_suck)
		self.add_command("skill", self.cmd_skill)
		self.add_command("noob", self.cmd_noob)
		self.add_command("nab", self.cmd_nab)
		self.add_command("nub", self.cmd_nub)
		self.add_command("nubz", self.cmd_nubz)
		self.add_command("fucking", self.cmd_fucking)
		self.add_command("fuck", self.cmd_fuck)
		self.add_command("hodor", self.cmd_hodor)
		self.add_command("fun", self.cmd_fun)
		self.add_command("ass", self.cmd_ass)
		self.add_command("arse", self.cmd_arse)
		self.add_command("vag", self.cmd_vag)
		self.add_command("vagina", self.cmd_vagina)
		self.add_command("penis", self.cmd_penis)
		self.add_command("balls", self.cmd_balls)
		self.add_command("gay", self.cmd_gay)
		self.add_command("lesbian", self.cmd_lesbian)
		self.add_command("homo", self.cmd_homo)
		self.add_command("homosex", self.cmd_homosex)
		self.add_command("cake", self.cmd_cake)
		self.add_command("caek", self.cmd_caek)
		self.add_command("rape", self.cmd_rape)
		self.add_command("raep", self.cmd_raep)
		self.add_command("fag", self.cmd_fag)
		self.add_command("faggot", self.cmd_faggot)
		self.add_command("rail", self.cmd_rail)
		self.add_command("shaft", self.cmd_shaft)
		self.add_command("smoke", self.cmd_smoke)
		self.add_command("urine", self.cmd_urine)
		self.add_command("mermaid", self.cmd_mermaid)
		self.add_command("wank", self.cmd_wank)
		self.add_command("jerkoff", self.cmd_jerkoff)
		self.add_command("cum", self.cmd_cum)
		self.add_command("discharge", self.cmd_discharge)
		self.add_command("mysperm", self.cmd_mysperm)
		self.add_command("whore", self.cmd_whore)
		self.add_command("lost", self.cmd_lost)
		self.add_command("bukkake", self.cmd_bukkake)
		self.add_command("goldenshower", self.cmd_goldenshower)
		self.add_command("bugger", self.cmd_bugger)
		self.add_command("grape", self.cmd_grape)
		self.add_command("turd", self.cmd_turd)
		self.add_command("fark", self.cmd_fark)
		self.add_command("headshot", self.cmd_headshot)
		self.add_command("rekt", self.cmd_rekt)
		self.add_command("trap", self.cmd_trap)
		self.add_command("tarp", self.cmd_tarp)
		self.add_command("joke", self.cmd_joke)
		self.add_command("aim", self.cmd_aim)
		self.add_command("wut", self.cmd_wut)
		self.add_command("wot", self.cmd_wot)
		self.add_command("milk", self.cmd_milk)
		self.add_command("brazilianfartporn", self.cmd_brazilianfartporn)
		self.add_command("ballsack", self.cmd_ballsack)
		self.add_command("scrotum", self.cmd_scrotum)
		self.add_command("diarrhea", self.cmd_diarrhea)
		self.add_command("diarrhoea", self.cmd_diarrhoea)
		self.add_command("diahrrea", self.cmd_diahrrea)
		self.add_command("tard", self.cmd_tard)
		self.add_command("retard", self.cmd_retard)
		self.add_command("mongoloid", self.cmd_mongoloid)
		self.add_command("tosser", self.cmd_tosser)
		self.add_command("tits", self.cmd_tits)
		self.add_command("boob", self.cmd_boob)
		self.add_command("boobs", self.cmd_boobs)
		self.add_command("breasts", self.cmd_breasts)
		self.add_command("knockers", self.cmd_knockers)
		self.add_command("minge", self.cmd_minge)
		self.add_command("cooch", self.cmd_cooch)
		self.add_command("pussy", self.cmd_pussy)
		self.add_command("clam", self.cmd_clam)
		self.add_command("waffles", self.cmd_waffles)
		self.add_command("pie", self.cmd_pie)
		self.add_command("dessert", self.cmd_dessert)
		self.add_command("kuk", self.cmd_kuk)
		self.add_command("helvete", self.cmd_helvete)
		self.add_command("perkele", self.cmd_perkele)
		self.add_command("bussie", self.cmd_bussie)
		self.add_command("fucker", self.cmd_fucker)
		self.add_command("jugs", self.cmd_jugs)
		self.add_command("monkey", self.cmd_monkey)
		self.add_command("joint", self.cmd_joint)
		self.add_command("spliff", self.cmd_spliff)
		self.add_command("smegma", self.cmd_smegma)
		self.add_command("jesus", self.cmd_jesus)
		self.add_command("christ", self.cmd_christ)
		self.add_command("transgenderstriptease", self.cmd_transgenderstriptease)
		self.add_command("sativa", self.cmd_sativa)
		self.add_command("bitch", self.cmd_bitch)
		self.add_command("bitches", self.cmd_bitches)
		self.add_command("love", self.cmd_love)
		self.add_command("fap", self.cmd_fap)
		self.add_command("flange", self.cmd_flange)
		self.add_command("fart", self.cmd_fart)
		self.add_command("puke", self.cmd_puke)
		self.add_command("barf", self.cmd_barf)
		self.add_command("burp", self.cmd_burp)
		self.add_command("buff", self.cmd_buff)
		self.add_command("gangbang", self.cmd_gangbang)
		self.add_command("spank", self.cmd_spank)
		self.add_command("gg", self.cmd_gg)
		self.add_command("naked", self.cmd_naked)
		self.add_command("nude", self.cmd_nude)
		self.add_command("dicksize", self.cmd_dicksize)
		self.add_command("peepee", self.cmd_peepee)
		self.add_command("lust", self.cmd_lust)
		self.add_command("juice", self.cmd_juice)
		self.add_command("cheese", self.cmd_cheese)
		self.add_command("fitte", self.cmd_fitte)
		self.add_command("fail", self.cmd_fail)
		self.add_command("surprisepoopydick", self.cmd_surprisepoopydick)
		self.add_command("surprisepoopypenis", self.cmd_surprisepoopypenis)
		self.add_command("stark", self.cmd_stark)
		self.add_command("targaryen", self.cmd_targaryen)
		self.add_command("tyrell", self.cmd_tyrell)
		self.add_command("lannister", self.cmd_lannister)
		self.add_command("greyjoy", self.cmd_greyjoy)
		self.add_command("arryn", self.cmd_arryn)
		self.add_command("baratheon", self.cmd_baratheon)
		self.add_command("martell", self.cmd_martell)
		self.add_command("tully", self.cmd_tully)
		self.add_command("tarly", self.cmd_tarly)
		self.add_command("bolton", self.cmd_bolton)
		self.add_command("tourettes", self.cmd_tourettes)
		self.add_command("vaseline", self.cmd_vaseline)
		self.add_command("rimming", self.cmd_rimming)
		self.add_command("rimjob", self.cmd_rimjob)
		self.add_command("sphincter", self.cmd_sphincter)
		self.add_command("goatse", self.cmd_goatse)
		self.add_command("coprophilia", self.cmd_coprophilia)
		self.add_command("scat", self.cmd_scat)
		self.add_command("feels", self.cmd_feels)
		self.add_command("moin", self.cmd_moin)
		self.add_command("win", self.cmd_win)
		self.add_command("lmao", self.cmd_lmao)
		self.add_command("lol", self.cmd_lol)
		self.add_command("lag", self.cmd_lag)
		self.add_command("lube", self.cmd_lube)
		self.add_command("rage", self.cmd_rage)
		self.add_command("minkyn", self.cmd_minkyn)
		self.add_command("iosys", self.cmd_iosys)
		self.add_command("hurzhurz", self.cmd_hurzhurz)
		self.add_command("railgunnar", self.cmd_railgunnar)
		self.add_command("d1jon", self.cmd_d1jon)
		self.add_command("crash7", self.cmd_crash7)
		self.add_command("crash", self.cmd_crash)
		self.add_command("pestenoire", self.cmd_pestenoire)
		self.add_command("psych", self.cmd_psych)
		self.add_command("kikindas", self.cmd_kikindas)
		self.add_command("milkydischarge", self.cmd_milkydischarge)
		self.add_command("papryk", self.cmd_papryk)
		self.add_command("fiszek", self.cmd_fiszek)
		self.add_command("forthewin", self.cmd_forthewin)
		self.add_command("eveshka", self.cmd_eveshka)
		self.add_command("groberunfug", self.cmd_groberunfug)
		self.add_command("obiarshi", self.cmd_obiarshi)
		self.add_command("ogopogo", self.cmd_ogopogo)
		self.add_command("roleplayer", self.cmd_roleplayer)
		self.add_command("woolph", self.cmd_woolph)
		self.add_command("p0lymer", self.cmd_p0lymer)
		self.add_command("scorpse", self.cmd_scorpse)
		self.add_command("whahaha", self.cmd_whahaha)
		self.add_command("milky", self.cmd_milky)
		self.add_command("feck", self.cmd_feck)
		self.add_command("queef", self.cmd_queef)
		self.add_command("bullshit", self.cmd_bullshit)
		self.add_command("iouonegirl", self.cmd_iouonegirl)
		self.add_command("chillin1", self.cmd_chillin1)
		self.add_command("crumbsucker", self.cmd_crumbsucker)
		self.add_command("robo", self.cmd_robo)
		self.add_command("enema", self.cmd_enema)
		self.add_command("fragstealer", self.cmd_fragstealer)
		self.add_command("condom", self.cmd_condom)
		self.add_command("bareback", self.cmd_bareback)
		self.add_command("pedestrian", self.cmd_pedestrian)
		self.add_command("equality4all", self.cmd_equality4all)
		self.add_command("crexx", self.cmd_crexx)
		self.add_command("crexx_chaos", self.cmd_crexx_chaos)
		self.add_command("staycool", self.cmd_staycool)
		self.add_command("nemesis", self.cmd_nemesis)
		self.add_command("stupid", self.cmd_stupid) 
		self.add_command("asshole", self.cmd_asshole)  
		self.add_command("virgin", self.cmd_virgin)  
		self.add_command("fuckface", self.cmd_fuckface)  
		self.add_command("curry", self.cmd_curry)  
		self.add_command("bg", self.cmd_bg)  
		self.add_command("fu", self.cmd_fu)  
		self.add_command("herpes", self.cmd_herpes)  
		self.add_command("dildo", self.cmd_dildo)  
		self.add_command("tea", self.cmd_tea)  
		self.add_command("doublepenetration", self.cmd_doublepenetration)  
		self.add_command("flirt", self.cmd_flirt)  
		self.add_command("jaxzii", self.cmd_jaxzii)  
		self.add_command("ratamahatta", self.cmd_ratamahatta)  
		self.add_command("stalls", self.cmd_stalls)  
		self.add_command("qwasyx", self.cmd_qwasyx)  
		self.add_command("beanz", self.cmd_beanz)  
		self.add_command("featuredib", self.cmd_featuredib)  
		self.add_command("oshcovoq", self.cmd_oshcovoq)  
		self.add_command("tape", self.cmd_tape)  
		self.add_command("daime", self.cmd_daime)  
		self.add_command("tjtjtjtj", self.cmd_tjtjtjtj)  
		self.add_command("danielhjorvar", self.cmd_danielhjorvar)  
		self.add_command("barbarossa", self.cmd_barbarossa)  
		self.add_command("hansgruber", self.cmd_hansgruber)  
		self.add_command("spermi", self.cmd_spermi)  
		self.add_command("revilian", self.cmd_revilian)  
		self.add_command("omek", self.cmd_omek)    
		self.add_command("ranzige", self.cmd_ranzige)    
		self.add_command("boobsize", self.cmd_boobsize)    
		self.add_command("crap", self.cmd_crap)    
		self.add_command("gebakkengarnaal", self.cmd_gebakkengarnaal)    
		self.add_command("goenigoegoe", self.cmd_goenigoegoe)    
		self.add_command("gelenkbusfahrer", self.cmd_gelenkbusfahrer)    
		self.add_command("bus", self.cmd_bus)    
		self.add_command("station", self.cmd_station)    
		self.add_command("whitefeather", self.cmd_whitefeather)    
		self.add_command("timescar", self.cmd_timescar)    
		self.add_command("darkmo", self.cmd_darkmo)    
		self.add_command("masturbate", self.cmd_masturbate)    
		self.add_command("killerboy", self.cmd_killerboy)    
		self.add_command("jimmyvulgar", self.cmd_jimmyvulgar)    
		self.add_command("angelripper", self.cmd_angelripper)    
		self.add_command("satanclaws", self.cmd_satanclaws)    
		self.add_command("bane", self.cmd_bane)    
		
	def cmd_cookies(self, player, msg, channel):
                n = random.randint(0, 1)
                if n == 0:
                        channel.reply("^5There better be some THC up in this shit, {}^5!".format(player))
                elif n == 1:
                        channel.reply("^5I don't trust any cookie that's been in your hands, {}^5!".format(player))

	def cmd_drugs(self, player, msg, channel):
		channel.reply("^5Drugs are bad, mm'kay?".format(player))

	def cmd_weed(self, player, msg, channel):
                n = random.randint(0, 1)
                if n == 0:
                        channel.reply("^5Das some good shit right dere, mane.".format(player))
                elif n == 1:
                        channel.reply("^5No, it's not normal weed. It's some fucked-up skunk, class A, I-can't-think-let-alone-move shit.".format(player))

	def cmd_crack(self, player, msg, channel):
		channel.reply("^5Whitney Houston, we have a problem...".format(player))

	def cmd_meth(self, player, msg, channel):
		channel.reply("^5Put me on your magical boat, man, and sail me down your chocolatey river of meth!".format(player))

	def cmd_beer(self, player, msg, channel):
		channel.reply("^5Don't mind if I do. Prost!".format(player))

	def cmd_sex(self, player, msg, channel):
                a = random.randint(0, 1)
                if a == 0:
                        channel.reply("^5What? Right here and now?".format(player))
                elif a == 1:
                        channel.reply("^5Sounds good, {}^5, make sure you use protection. Red Armour should suffice.".format(player))

	def cmd_anal(self, player, msg, channel):
                a = random.randint(0, 3)
                if a == 0:
                        channel.reply("^5If {}^5 brings the lube, I'll bring the beads!".format(player))
                elif a == 1:
                        channel.reply("^5Ever try anal? It's fucking shit.".format(player))
                elif a == 2:
                        channel.reply("^5Anal: It's not for pussies.".format(player))
                elif a == 3:
                        channel.reply("^5My dyslexic girlfriend really wants to do Alan.".format(player))

	def cmd_piss(self, player, msg, channel):
		channel.reply("^5Nah... just went, so I'm good.".format(player))

	def cmd_oralsex(self, player, msg, channel):
		channel.reply("^5Ooh yeah... Ahhh... Ow! Ow! No teeth!".format(player))

	def cmd_fellatio(self, player, msg, channel):
		channel.reply("^5Alas, poor {}^5. I knew him, Fellatio...".format(player))

	def cmd_surprisebuttsex(self, player, msg, channel):
		channel.reply("^5Bloody hell! Where'd that come from?".format(player))

	def cmd_vodka(self, player, msg, channel):
		channel.reply("^5You're trying to get me drunk as a Russian, aren't you, {}^5?".format(player))

	def cmd_whiskey(self, player, msg, channel):
		channel.reply("^5I like my whisky old and my women young.".format(player))

	def cmd_muffins(self, player, msg, channel):
		channel.reply("^5You ain't seen nothin' 'til you're down on a muffin...".format(player))

	def cmd_blowjob(self, player, msg, channel):
		channel.reply("^5Suck it and see ;)".format(player))

	def cmd_hookers(self, player, msg, channel):
		channel.reply("^5Now we just need Charlie Sheen and an eightball of coke...".format(player))

	def cmd_peen(self, player, msg, channel):
		channel.reply("^5ALL GLORY TO THE HYPNOPEEN".format(player))

	def cmd_ecstasy(self, player, msg, channel):
		channel.reply("^5I love you man...".format(player))

	def cmd_exstasy(self, player, msg, channel):
		channel.reply("^5Someone needs to learn how to spell ecstasy...".format(player))

	def cmd_mdma(self, player, msg, channel):
		channel.reply("^5Oh, {}^5, you're so generous.".format(player))

	def cmd_molly(self, player, msg, channel):
		channel.reply("^5I've already got a dealer thanks, {}^5.".format(player))

	def cmd_coke(self, player, msg, channel):
		channel.reply("^5No thanks {}^5, I prefer Pepsi (R)".format(player))

	def cmd_cocaine(self, player, msg, channel):
		channel.reply("^5What is this, the 80s?".format(player))

	def cmd_heroin(self, player, msg, channel):
		channel.reply("^5Who need reasons when you've got heroin?".format(player))

	def cmd_cock(self, player, msg, channel):
                f = random.randint(0, 1)
                if f == 0:
                        channel.reply("^5Oh look, {}^5 is trying to get it up.".format(player))
                elif f == 1:
                        channel.reply("^5Think you're the cock o' the walk eh, {}^5?".format(player))

	def cmd_dick(self, player, msg, channel):
                c = random.randint(0, 1)
                if c == 0:
                        channel.reply("^5Don't want no short dick man, {}^5.".format(player))
                elif c == 1:
                        channel.reply("^5No-one needs a dick when we've got {}^5 around.".format(player))

	def cmd_cunt(self, player, msg, channel):
                d = random.randint(0, 3)
                if d == 0:
                        channel.reply("^5TNUC TNUC TNUC".format(player))
                elif d == 1:
                        channel.reply("^5It's tnuc! FFS".format(player))
                elif d == 2:
                        channel.reply("^5Tnuc! Got it?".format(player))
                elif d == 3:
                        channel.reply("^5tnuc".format(player)) 

	def cmd_tnuc(self, player, msg, channel):
                d = random.randint(0, 3)
                if d == 0:
                        channel.reply("^5CUNT CUNT CUNT".format(player))
                elif d == 1:
                        channel.reply("^5It's cunt! FFS".format(player))
                elif d == 2:
                        channel.reply("^5Cunt! Got it?".format(player))
                elif d == 3:
                        channel.reply("^5cunt".format(player))

	def cmd_wanker(self, player, msg, channel):
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("^51,000 years from now there will be no guys and no girls, just wankers.".format(player))
                elif d == 1:
                        channel.reply("^5Always had you pegged for a wanker, {}^5.".format(player))
                        
	def cmd_porn(self, player, msg, channel):
		channel.reply("^5Backdoor Sluts 9! Hang on. Is that your mum I see fisting that donkey, {}^5?".format(player))

	def cmd_bastard(self, player, msg, channel):
		channel.reply("^5Yer a right proper bastard, {}^5, but we love you anyway.".format(player))

	def cmd_suck(self, player, msg, channel):
                e = random.randint(0, 1)
                if e == 0:
                        channel.reply("^5Oh look, {}^5 is trying to get it up.".format(player))
                elif e == 1:
                        channel.reply("^5It's ok to admit you suck, {}^5.".format(player))

	def cmd_skill(self, player, msg, channel):
		channel.reply("^5{}^5's skill is non-existent. {}^5 is ranked #69 in worst ever players.".format(player))

	def cmd_noob(self, player, msg, channel):
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("^5No-one could possibly be as noobly as you, {}^5.".format(player))
                elif d == 1:
                        channel.reply("^5We're all noobs here on the Station.".format(player))

	def cmd_nab(self, player, msg, channel):
		channel.reply("^5Let's nab us some nabs!".format(player))

	def cmd_nub(self, player, msg, channel):
		channel.reply("^5{}^5 is a nubile young thang...".format(player))

	def cmd_nubz(self, player, msg, channel):
		channel.reply("^5We all had to begin somewhere, {}^5. Pity you never left the starting line.".format(player))

	def cmd_fucking(self, player, msg, channel):
                d = random.randint(0, 3)
                if d == 0:
                        channel.reply("^5It's a town in Austria.".format(player))
                elif d == 1:
                        channel.reply("^5You need your mouth washed out with soap, {}^5".format(player))
                elif d == 2:
                        channel.reply("^5What's with all the cussin'?".format(player))
                elif d == 3:
                        channel.reply("^5You're demonstrating your lack of vocabulary, {}^5.".format(player))

	def cmd_fuck(self, player, msg, channel):
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("^5Oh all right, let's just get it over with, then.".format(player))
                elif d == 1:
                        channel.reply("^5Hey! You use language like that again, son, you'll wish you hadn't!".format(player))

	def cmd_hodor(self, player, msg, channel):
		channel.reply("^5Hodor. Hodor. HODOR!!!!!!!".format(player))

	def cmd_fun(self, player, msg, channel):
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("^5Fun? WTF is that? This is srs business.".format(player))
                elif d == 1:
                        channel.reply("^5You mongrels better be having fun there, or there'll be hell to pay.".format(player))

	def cmd_ass(self, player, msg, channel):
		channel.reply("^5You've got it all ass-backwards, {}^5.".format(player))

	def cmd_arse(self, player, msg, channel):
		channel.reply("^5I had a bit of a tickle in my... ARSE!".format(player))

	def cmd_vag(self, player, msg, channel):
		channel.reply("^5The stench of rotting fish wafts disagreeably throughout the server...".format(player))

	def cmd_vagina(self, player, msg, channel):
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("^5Theres nothing finer than having a vagina!".format(player))
                elif d == 1:
                        channel.reply("^5You see boys, a woman is sensitive in her vagina and it feels good to have a man's penis inside of it.".format(player))

	def cmd_penis(self, player, msg, channel):
                d = random.randint(0, 2)
                if d == 0:
                        channel.reply("^5It's true: the pen IS mightier!".format(player))
                elif d == 1:
                        channel.reply("^5If only you knew the joy of possessing a penis, {}^5.".format(player))
                elif d == 2:
                        channel.reply("^5Boys have a penis; Girls have a HODOR!".format(player))

	def cmd_balls(self, player, msg, channel):
                d = random.randint(0, 2)
                if d == 0:
                        channel.reply("^5You have balls. I like balls.".format(player))
                elif d == 1:
                        channel.reply("^5Low and to the left, {}^5.".format(player))
                elif d == 2:
                        channel.reply("^5There are two types of balls. There are big brave balls, and there are little mincey faggot balls.".format(player))

	def cmd_gay(self, player, msg, channel):
                d = random.randint(0, 4)
                if d == 0:
                        channel.reply("^5...and the closet door swings laboriously open for {}^5.".format(player))
                elif d == 1:
                        channel.reply("^5The Station is full of gaiety tonight, it seems.".format(player))
                elif d == 2:
                        channel.reply("^5No milk today, the company was gay.".format(player))
                elif d == 3:
                        channel.reply("^5Gayer than all the men getting in a big pile and having sex with each other.".format(player))
                elif d == 4:
                        channel.reply("^5I was gonna make a gay joke, butt fuck it.".format(player))

	def cmd_lesbian(self, player, msg, channel):
                d = random.randint(0, 2)
                if d == 0:
                        channel.reply("^5{}^5 enjoys munching on a particularly fine rug.".format(player))
                elif d == 1:
                        channel.reply("^5Greets to all our sapphic sisters!".format(player))
                elif d == 2:
                        channel.reply("^5What do you call a lesbian dinosaur? Lickalotapus".format(player))

	def cmd_homo(self, player, msg, channel):
                d = random.randint(0, 2)
                if d == 0:
                        channel.reply("^5{}^5 is looking quite sexual tonight. No homo.".format(player))
                elif d == 1:
                        channel.reply("^5{}^5 has had his dung punched on many an occasion.".format(player))
                elif d == 2:
                        channel.reply("^5Want to know how {}^5 is gay? Check the bite marks on his pillow...".format(player))

	def cmd_homosex(self, player, msg, channel):
		channel.reply("^5Father... I am homosex.".format(player))

	def cmd_cake(self, player, msg, channel):
		channel.reply("^5Mmm... fattening.".format(player))

	def cmd_caek(self, player, msg, channel):
		channel.reply("^5The caek is a lie!".format(player))

	def cmd_rape(self, player, msg, channel):
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("^5Now, now. Let's keep things consensual, {}^5.".format(player))
                elif d == 1:
                        channel.reply("^5We're all into it here, {}^5, so how can it be rape?".format(player))

	def cmd_raep(self, player, msg, channel):
		channel.reply("^5Stop right there, criminal scum! You violated my mother!".format(player))

	def cmd_fag(self, player, msg, channel):
                d = random.randint(0, 3)
                if d == 0:
                        channel.reply("^5Now we see {}^5's true colours. Pretty rainbow colours!".format(player))
                elif d == 1:
                        channel.reply("^5Oi mate, can I bum a fag off ya?".format(player))
                elif d == 2:
                        channel.reply("^5Hang on... pot + kettle = black?".format(player))
                elif d == 3:
                        channel.reply("^5{}^5 is a fag hag.".format(player))

	def cmd_faggot(self, player, msg, channel):
		channel.reply("^5{}^5 picks a bundle of sticks.".format(player))

	def cmd_rail(self, player, msg, channel):
		channel.reply("^5{}^5 enjoys being railed hard from behind.".format(player))

	def cmd_shaft(self, player, msg, channel):
		channel.reply("^5{}^5 likes being shafted mightily.".format(player))

	def cmd_smoke(self, player, msg, channel):
                d = random.randint(0, 2)
                if d == 0:
                        channel.reply("^5*cough cough* Ahhhhhh, blessed nicotine...".format(player))
                elif d == 1:
                        channel.reply("^5A pack a day keeps the doctor away.".format(player))
                elif d == 2:
                        channel.reply("^5Smoking is one of the leading causes of statistics.".format(player))

	def cmd_urine(self, player, msg, channel):
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("^5Urine big trouble, mister.".format(player))
                elif d == 1:
                        channel.reply("^5It's also important that you understand why some people choose to urinate on each other.".format(player))

	def cmd_mermaid(self, player, msg, channel):
		channel.reply("^5How the hell do mermaids shit and piss?".format(player))

	def cmd_wank(self, player, msg, channel):
                d = random.randint(0, 5)
                if d == 0:
                        channel.reply("^5Watch out, {}^5... you'll rub it raw.".format(player))
                elif d == 1:
                        channel.reply("^5{}^5 spanks the monkey.".format(player))
                elif d == 2:
                        channel.reply("^5{}^5 tickles the pickle.".format(player))
                elif d == 3:
                        channel.reply("^5{}^5 badgers the witness.".format(player))
                elif d == 4:
                        channel.reply("^5{}^5 flogs the log.".format(player))
                elif d == 5:
                        channel.reply("^5{}^5 frees Willy.".format(player))

	def cmd_jerkoff(self, player, msg, channel):
                d = random.randint(0, 5)
                if d == 0:
                        channel.reply("^5Look at me, jerking off in the shower... This will be the high point of my day.".format(player))
                elif d == 1:
                        channel.reply("^5{}^5 gives a low 5.".format(player))
                elif d == 2:
                        channel.reply("^5{}^5 makes the bald man cry.".format(player))
                elif d == 3:
                        channel.reply("^5{}^5 gives a one gun salute.".format(player))
                elif d == 4:
                        channel.reply("^5{}^5 slams the salami.".format(player))
                elif d == 5:
                        channel.reply("^5{}^5 strains the main vein.".format(player))  

	def cmd_cum(self, player, msg, channel):
		channel.reply("^5Don't sticky up your keyboard, {}^5.".format(player))

	def cmd_discharge(self, player, msg, channel):
		channel.reply("^5Oh dear. It's all milky and creamy.".format(player))

	def cmd_mysperm(self, player, msg, channel):
		channel.reply("^5{}^5's semen contains 0.0007 percent viable sperm. We recommend looser underwear.".format(player))

	def cmd_whore(self, player, msg, channel):
		channel.reply("^5Not everyone needs to pay for it, {}^5.".format(player))

	def cmd_lost(self, player, msg, channel):
		channel.reply("^5It's not about winning or losing, {}^5, but how you camp the rail.".format(player))

	def cmd_bukkake(self, player, msg, channel):
		channel.reply("^5{}^5 surely savours slurping scores of slathering seminal secretions.".format(player))

	def cmd_goldenshower(self, player, msg, channel):
		channel.reply("^5{}^5's singin' in the rain, just singin' in the (golden) rain...".format(player))

	def cmd_bugger(self, player, msg, channel):
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("^5Bugger me sideways!".format(player))
                elif d == 1:
                        channel.reply("^5Bugger off, {}^5.".format(player))

	def cmd_grape(self, player, msg, channel):
		channel.reply("^5In the souls of the people the grapes of wrath are filling and growing heavy.".format(player))

	def cmd_turd(self, player, msg, channel):
                d = random.randint(0, 2)
                if d == 0:
                        channel.reply("^5Little miss {}^5, sat on her tuffet, eating her turds and whey.".format(player))
                elif d == 1:
                        channel.reply("^5Remember, {}^5, you can't polish a turd.".format(player))
                elif d == 2:
                        channel.reply("^5Never kick a fresh turd on a hot day.".format(player))

	def cmd_fark(self, player, msg, channel):
		channel.reply("^5Farken ell. What's the world coming to?".format(player))

	def cmd_headshot(self, player, msg, channel):
		channel.reply("^5I've got your headshot right here *obscene gesture*".format(player))

	def cmd_rekt(self, player, msg, channel):
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("^5Get rekt.".format(player))
                elif d == 1:
                        channel.reply("^5Rekt 'em up the arse.".format(player))

	def cmd_trap(self, player, msg, channel):
		channel.reply("^5IT'S A TRAP!".format(player))

	def cmd_tarp(self, player, msg, channel):
		channel.reply("^5IT'S A CANVAS SHEET!".format(player))

	def cmd_joke(self, player, msg, channel):
                d = random.randint(0, 6)
                if d == 0:
                        channel.reply("^5Yo momma is like weed. Everyone does her but no-one admits it.".format(player))
                elif d == 1:
                        channel.reply("^5Give a man a jacket and he'll be warm in the winter, learn a man to jacket and he'll be warm forever.".format(player))
                elif d == 2:
                        channel.reply("^5Why are gay men so well dressed? They didn't spend all that time in the closet doing nothing.".format(player))
                elif d == 3:
                        channel.reply("^5How many Germans does it take to change a light bulb? One, we are efficient and don't have humour.".format(player))
                elif d == 4:
                        channel.reply("^5When wearing a bikini, women reveal 90% of their body.... men are so polite they only look at the covered parts.".format(player))
                elif d == 5:
                        channel.reply("^5If I had a dollar for every girl that found me unattractive, they would eventually find me attractive.".format(player))
                elif d == 6:
                        channel.reply("^5Why do sumo wrestlers shave their legs? So people don't confuse them with feminists".format(player))

	def cmd_aim(self, player, msg, channel):
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("^5Aim for the stars, {}^5, because you sure as hell can't hit anything here.".format(player))
                elif d == 1:
                        channel.reply("^5Shoot at the green things, {}^5.".format(player))

	def cmd_wut(self, player, msg, channel):
                d = random.randint(0, 2)
                if d == 0:
                        channel.reply("^5I dunno.".format(player))
                elif d == 1:
                        channel.reply("^5Beats me, {}^5.".format(player))
                elif d == 2:
                        channel.reply("^5Haven't the foggiest.".format(player))

	def cmd_wot(self, player, msg, channel):
                d = random.randint(0, 2)
                if d == 0:
                        channel.reply("^5U wot m8?".format(player))
                elif d == 1:
                        channel.reply("^5Sod off, {}^5, ya blimmin' bellend.".format(player))
                elif d == 2:
                        channel.reply("^5Know what you are, {}^5? Yer a bloody minger, that's what you are.".format(player))

	def cmd_milk(self, player, msg, channel):
                d = random.randint(0, 2)
                if d == 0:
                        channel.reply("^5Drink it down, {}^5... every last drop.".format(player))
                elif d == 1:
                        channel.reply("^5Feel the creamy goodness sliding down your throat.".format(player))
                elif d == 2:
                        channel.reply("^5Taste it. Love it.".format(player))

	def cmd_brazilianfartporn(self, player, msg, channel):
		channel.reply("^5I think we're getting a little exotic here, {}^5. I'll stick to my czech voyeur scat, thanks.".format(player)) 

	def cmd_ballsack(self, player, msg, channel):
		channel.reply("^5How's yours hanging, {}^5?".format(player))

	def cmd_scrotum(self, player, msg, channel):
		channel.reply("^5The wrinklier, the better!".format(player))

	def cmd_diarrhea(self, player, msg, channel):
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("^5It's true! You do have a dire rear, {}^5.".format(player))
                elif d == 1:
                        channel.reply("^5Hey Lois! Diarrhea!".format(player))

	def cmd_diarrhoea(self, player, msg, channel):
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("^5Mmm... chocolatey excretions...".format(player))
                elif d == 1:
                        channel.reply("^5Diarrhoea CHA CHA CHA!".format(player))

	def cmd_diahrrea(self, player, msg, channel):
		channel.reply("^5Check your dictionary, {}^5.".format(player))

	def cmd_tard(self, player, msg, channel):
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("^5It ain't hard to be a tard, {}^5.".format(player))
                elif d == 1:
                        channel.reply("^5{}^5 is a refugee from Tardistan..".format(player))

	def cmd_retard(self, player, msg, channel):
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("^5{}^5 seems to be the retarded one around here...".format(player))
                elif d == 1:
                        channel.reply("^5Takes one to know one, {}^5...".format(player))

	def cmd_mongoloid(self, player, msg, channel):
                d = random.randint(0, 2)
                if d == 0:
                        channel.reply("^5I like tulip. Tulip is much better than mongoloid.".format(player))
                elif d == 1:
                        channel.reply("^5Shut up, fuckhead! I hate that mongoloid voice.".format(player))
                elif d == 2:
                        channel.reply("^5I didn't call you a mongoloid, I called you a retard.".format(player))

	def cmd_tosser(self, player, msg, channel):
		channel.reply("^5Toss that salad. Toss it good!".format(player))

	def cmd_tits(self, player, msg, channel):
                d = random.randint(0, 2)
                if d == 0:
                        channel.reply("^5Lubbly jubbly-wubblies!".format(player))
                elif d == 1:
                        channel.reply("^5{}^5 has a breast fixation, it appears...".format(player))
                elif d == 2:
                        channel.reply("^5Show us yer tits, {}^5!".format(player))

	def cmd_boob(self, player, msg, channel):
		channel.reply("^5Only one? Why not a pair?".format(player))

	def cmd_boobs(self, player, msg, channel):
                d = random.randint(0, 2)
                if d == 0:
                        channel.reply("^5More than a handful's a waste.".format(player))
                elif d == 1:
                        channel.reply("^5Big boobs don't make a woman stupid. They make men stupid.".format(player))
                elif d == 2:
                        channel.reply("^5What do you call identical boobs? Identitties.".format(player))

	def cmd_breasts(self, player, msg, channel):
		channel.reply("^5If all the atoms in the universe were transformed into breasts, there would still not be enough breasts.".format(player))

	def cmd_knockers(self, player, msg, channel):
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("^5Hooters should do a home delivery service and call it Knockers.".format(player))
                elif d == 1:
                        channel.reply("^5Please knock firmly, I love firm knockers.".format(player))

	def cmd_minge(self, player, msg, channel):
		channel.reply("^5Seriously {}^5, your minge makes me cringe.".format(player))

	def cmd_cooch(self, player, msg, channel):
		channel.reply("^5I bet {}^5's got a hairy cooch.".format(player))

	def cmd_pussy(self, player, msg, channel):
                d = random.randint(0, 3)
                if d == 0:
                        channel.reply("^5Meow.".format(player))
                elif d == 1:
                        channel.reply("^5Pussy isn't like weed. If you can smell it from across the room, then it isn't the good shit.".format(player))
                elif d == 2:
                        channel.reply("^5I'll have you know there's no PUSSEEEEEEEEEEE!!!!!".format(player))
                elif d == 3:
                        channel.reply("^5Pussies may get mad at dicks once in a while, because pussies get fucked by dicks.".format(player))

	def cmd_clam(self, player, msg, channel):
		channel.reply("^5Clam CHOW-deh!".format(player))

	def cmd_waffles(self, player, msg, channel):
		channel.reply("^5The only good thing to come out of Belgium...".format(player))

	def cmd_pie(self, player, msg, channel):
		channel.reply("^5Any time of the day is a good time for pie.".format(player))

	def cmd_dessert(self, player, msg, channel):
		channel.reply("^5Everybody knows, {}^5 picks his nose. He rubs it in the dirt, and has it for dessert!".format(player))

	def cmd_kuk(self, player, msg, channel):
		channel.reply("^5These nordic types certainly love to talk about their pee-pees.".format(player))

	def cmd_helvete(self, player, msg, channel):
		channel.reply("^5That's where you're going, {}^5.".format(player))

	def cmd_perkele(self, player, msg, channel):
		channel.reply("^5Only in Finland...".format(player))

	def cmd_bussie(self, player, msg, channel):
                d = random.randint(0, 3)
                if d == 0:
                        channel.reply("^5I hear Bussie joined the police force. He's in the Bong Disposal Unit.".format(player))
                elif d == 1:
                        channel.reply("^5Bussie has two spliffs. He's double-jointed.".format(player))
                elif d == 2:
                        channel.reply("^5Bussie's a true stoner. His bong gets washed more than his dishes.".format(player))
                elif d == 3:
                        channel.reply("^5Be lucky to find your penis for a piss, the amount you keep smoking.".format(player))

	def cmd_fucker(self, player, msg, channel):
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("^5Watch yo mouth punk, or I'll fuck yo bitch ass up!".format(player))
                elif d == 1:
                        channel.reply("^5Ain't no-one got time fo' dat.".format(player))

	def cmd_jugs(self, player, msg, channel):
		channel.reply("^5Big, round jugs, overflowing with milk. Delish.".format(player))

	def cmd_monkey(self, player, msg, channel):
                d = random.randint(0, 2)
                if d == 0:
                        channel.reply("^5Watch out! {}^5's about to start flinging his faeces!".format(player))
                elif d == 1:
                        channel.reply("^5The nature of monkey was irrepressible!".format(player))
                elif d == 2:
                        channel.reply("^5{}^5 is the funkiest monkey that ever popped!".format(player))

	def cmd_joint(self, player, msg, channel):
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("^5Let's blow this joint.".format(player))
                elif d == 1:
                        channel.reply("^5{}^5 is the tokin' black guy.".format(player))

	def cmd_spliff(self, player, msg, channel):
		channel.reply("^5Light it up and pass it around, {}^5.".format(player))

	def cmd_smegma(self, player, msg, channel):
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("^5Full of cheesy goodness!".format(player))
                elif d == 1:
                        channel.reply("^5Scrape it off and smear it on your lip, {}^5.".format(player))

	def cmd_jesus(self, player, msg, channel):
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("^5Jesus H. Christ, we've got a fundy.".format(player))
                elif d == 1:
                        channel.reply("^5What would Jesus do? Bring tha fucken smack down, niggaz!".format(player))

	def cmd_christ(self, player, msg, channel):
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("^5Christ on a cream cheese cracker!".format(player))
                elif d == 1:
                        channel.reply("^5{}^5 thinks he's the second coming :P".format(player))

	def cmd_transgenderstriptease(self, player, msg, channel):
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("^5These things are getting more and more specific. Dayum.".format(player))
                elif d == 1:
                        channel.reply("^5Shake dat bootie for us, {}^5.".format(player))

	def cmd_sativa(self, player, msg, channel):
		channel.reply("^5Reckon {}^5 has a craving for that sweet, sweet bud...".format(player))

	def cmd_bitch(self, player, msg, channel):
                d = random.randint(0, 2)
                if d == 0:
                        channel.reply("^5I ain't no-one's bitch, motherfucker.".format(player))
                elif d == 1:
                        channel.reply("^5DOES HE LOOK LIKE A BITCH?!?".format(player))
                elif d == 2:
                        channel.reply("^5Bitch, please...".format(player))

	def cmd_bitches(self, player, msg, channel):
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("^5Bitches ain't got shit on me.".format(player))
                elif d == 1:
                        channel.reply("^5Where mah bitches at?".format(player))

	def cmd_love(self, player, msg, channel):
                d = random.randint(0, 7)
                if d == 0:
                        channel.reply("^5Love. It's apparently all you need.".format(player))
                elif d == 1:
                        channel.reply("^5We love you too, {}^5.".format(player))
                elif d == 2:
                        channel.reply("^5<3".format(player))
                elif d == 3:
                        channel.reply("^5Love is something for people that don't play Quake.".format(player))
                elif d == 4:
                        channel.reply("^5<3".format(player))
                elif d == 5:
                        channel.reply("^5Get ready for {}^5's manlove!".format(player))
                elif d == 6:
                        channel.reply("^5Love is like a carelessly thrown grenade. One misstep and you're fucked.".format(player))
                elif d == 7:
                        channel.reply("^5Five midgets, spanking a man covered with thousand island dressing. Is that making love?".format(player))

	def cmd_fap(self, player, msg, channel):
                d = random.randint(0, 3)
                if d == 0:
                        channel.reply("^5*fapfapfapfapfap*".format(player))
                elif d == 1:
                        channel.reply("^5BRB. Gotta fap.".format(player))
                elif d == 2:
                        channel.reply("^5Remember to keep your tissues handy, {}^5.".format(player))
                elif d == 3:
                        channel.reply("^5{}^5 is good friends with Mrs Palmer and her five daughters.".format(player))

	def cmd_flange(self, player, msg, channel):
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("^5Arrange your flange, {}^5.".format(player))
                elif d == 1:
                        channel.reply("^5{}^5 has a strange flange.".format(player))

	def cmd_fart(self, player, msg, channel):
                d = random.randint(0, 6)
                if d == 0:
                        channel.reply("^5{}^5 let one rip.".format(player))
                elif d == 1:
                        channel.reply("^5{}^5 let fluffy off the chain.".format(player))
                elif d == 2:
                        channel.reply("^5{}^5 cut the cheese.".format(player))
                elif d == 3:
                        channel.reply("^5{}^5 is a lean, mean, bean machine.".format(player))
                elif d == 4:
                        channel.reply("^5{}^5 toots the trouser trumpet.".format(player))
                elif d == 5:
                        channel.reply("^5{}^5 is sorry. No, he's SORRY...".format(player))
                elif d == 6:
                        channel.reply("^5{}^5 dropped a stink bomb.".format(player))

	def cmd_puke(self, player, msg, channel):
                d = random.randint(0, 2)
                if d == 0:
                        channel.reply("^5{}^5 gave a technicolour yawn.".format(player))
                elif d == 1:
                        channel.reply("^5{}^5 blew chunks.".format(player))
                elif d == 2:
                        channel.reply("^5{}^5 prayed to the porcelain god.".format(player))

	def cmd_barf(self, player, msg, channel):
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("^5{}^5 made a pavement pizza.".format(player))
                elif d == 1:
                        channel.reply("^5{}^5 chundered mightily.".format(player))

	def cmd_burp(self, player, msg, channel):
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("^5Manners, {}^5.".format(player))
                elif d == 1:
                        channel.reply("^5Better out than in, amirite {}^5?".format(player))

	def cmd_buff(self, player, msg, channel):
                d = random.randint(0, 2)
                if d == 0:
                        channel.reply("^5{}^5 is lookin' all buff n' swole.".format(player))
                elif d == 1:
                        channel.reply("^5{}^5 lost his buff.".format(player))
                elif d == 2:
                        channel.reply("^5{}^5 buffs the bentley.".format(player))

	def cmd_gangbang(self, player, msg, channel):
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("^5The more the merrier!".format(player))
                elif d == 1:
                        channel.reply("^5We're sorry! Back in the pile!".format(player))

	def cmd_spank(self, player, msg, channel):
                self._channel = channel
                name = self.clean_text(msg[1]).lower()
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("{}^5 spanks {} real hard!".format(player, name))
                elif d == 1:
                        channel.reply("^5{}'s been a bad bot, daddy. Will you take him over your knee and spank him?".format(name))

	def cmd_gg(self, player, msg, channel):
                d = random.randint(0, 11)
                if d == 0:
                        channel.reply("^5I liked it too, {}^5!".format(player))
                elif d == 1:
                        channel.reply("^5Who won, {}^5?".format(player))
                elif d == 2:
                        channel.reply("^5That was just epic, {}^5!".format(player))
                elif d == 3:
                        channel.reply("^5Well that was rather pleasant.".format(player))
                elif d == 4:
                        channel.reply("^5Y'all happy now?".format(player))
                elif d == 5:
                        channel.reply("^5Gangrenous Gonads?".format(player))
                elif d == 6:
                        channel.reply("^5Gere's Gerbil?".format(player))
                elif d == 7:
                        channel.reply("^5Anyway, fuck it. The battle is over and the war is won.".format(player))
                elif d == 8:
                        channel.reply("^5Gary Glitter?".format(player))
                elif d == 9:
                        channel.reply("^5Leave the money on the nightstand, {}^5.".format(player))
                elif d == 10:
                        channel.reply("^5Giggling Gigolo?".format(player))
                elif d == 11:
                        channel.reply("^5Genital Grinding?".format(player))

	def cmd_naked(self, player, msg, channel):
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("^5{}^5 naked: a sight I wouldn't wish on my worst enemy.".format(player))
                elif d == 1:
                        channel.reply("^5Get yer kit off, {}^5. We could do with a laugh.".format(player))

	def cmd_nude(self, player, msg, channel):
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("^5I heard {}^5 visited a nude beach. Those poor, poor people.".format(player))
                elif d == 1:
                        channel.reply("^5Leave your clothes on, {}^5. We don't need to be traumatised further.".format(player))

	def cmd_dicksize(self, player, msg, channel):
                d = random.randint(0, 2)
                if d == 0:
                        channel.reply("^5{}^5's penis size is well below the median. Bad luck, brah.".format(player))
                elif d == 1:
                        channel.reply("^5{}^5 has a tiny tockley. Our condolences.".format(player))
                elif d == 2:
                        channel.reply("^5{}^5 needs tweezers to take a leak.".format(player))

	def cmd_peepee(self, player, msg, channel):
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("^5...and suddenly we're in kindergarten again.".format(player))
                elif d == 1:
                        channel.reply("^5Grab your peepee, {}^5, before it runs away again!".format(player))

	def cmd_lust(self, player, msg, channel):
		channel.reply("^5Ich habe keine Lust.".format(player))

	def cmd_juice(self, player, msg, channel):
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("^5It's running down my leg.".format(player))
                elif d == 1:
                        channel.reply("^5Hitler didn't like fruit. You could say he... hated juice *badumm tish*".format(player))

	def cmd_cheese(self, player, msg, channel):
		channel.reply("^5{}^5's mum is like blue cheese. Both smell worse the older they get.".format(player))

	def cmd_fitte(self, player, msg, channel):
		channel.reply("^5Hold kjeft, {}^5, og kom deg ut!".format(player))

	def cmd_fail(self, player, msg, channel):
                d = random.randint(0, 2)
                if d == 0:
                        channel.reply("^5{}^5's used to failure.".format(player))
                elif d == 1:
                        channel.reply("^5No, {}^5. YOU fail.".format(player))
                elif d == 2:
                        channel.reply("^5{}^5 never ceases to fail.".format(player))

	def cmd_surprisepoopydick(self, player, msg, channel):
		channel.reply("^5Bloody hell! Me knob's covered in shit!".format(player))

	def cmd_surprisepoopypenis(self, player, msg, channel):
		channel.reply("^5Bloody hell! Me peen's all brown and stinky!".format(player))

	def cmd_stark(self, player, msg, channel):
		channel.reply("^5Winter is Coming. And so am I.".format(player))

	def cmd_targaryen(self, player, msg, channel):
		channel.reply("^5Fire and Blood. And semen.".format(player))

	def cmd_tyrell(self, player, msg, channel):
		channel.reply("^5Growing Strong. And big and veiny.".format(player))

	def cmd_lannister(self, player, msg, channel):
		channel.reply("^5Hear Me Roar. As I cum in your arse.".format(player))

	def cmd_greyjoy(self, player, msg, channel):
		channel.reply("^5We Do Not Sow. Except our wild oats in your daughters.".format(player))

	def cmd_arryn(self, player, msg, channel):
		channel.reply("^5As High as Honor. As high as Bussie.".format(player))

	def cmd_baratheon(self, player, msg, channel):
		channel.reply("^5Ours is the Fury. And the depravity.".format(player))

	def cmd_martell(self, player, msg, channel):
		channel.reply("^5Unbowed, Unbent, Unbroken, Undressed.".format(player))

	def cmd_tully(self, player, msg, channel):
		channel.reply("^5Family, Duty, Honor, Debauchery.".format(player))

	def cmd_tarly(self, player, msg, channel):
		channel.reply("^5First in Battle. Last to discharge.".format(player))

	def cmd_bolton(self, player, msg, channel):
		channel.reply("^5Our Blades Are Sharp. And our members long.".format(player))

	def cmd_tourettes(self, player, msg, channel):
                d = random.randint(0, 11)
                if d == 0:
                        channel.reply("^5Fuck!".format(player))
                elif d == 1:
                        channel.reply("^5Shit!".format(player))
                elif d == 2:
                        channel.reply("^5Cunt!".format(player))
                elif d == 3:
                        channel.reply("^5Bastard!".format(player))
                elif d == 4:
                        channel.reply("^5Prick!".format(player))
                elif d == 5:
                        channel.reply("^5Arse!".format(player))
                elif d == 6:
                        channel.reply("^5Knob!".format(player))
                elif d == 7:
                        channel.reply("^5Bollocks!".format(player))
                elif d == 8:
                        channel.reply("^5Wanker!".format(player))
                elif d == 9:
                        channel.reply("^5Cack!".format(player))
                elif d == 10:
                        channel.reply("^5Bitch!".format(player))
                elif d == 11:
                        channel.reply("^5Bellend!".format(player))

	def cmd_vaseline(self, player, msg, channel):
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("^5Get it all lubed up {}^5, I'm coming in!".format(player))
                elif d == 1:
                        channel.reply("^5With no vaseline. Just a match and a little bit of gasoline.".format(player))

	def cmd_rimming(self, player, msg, channel):
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("^5{}^5 sure knows where to put his tongue...".format(player))
                elif d == 1:
                        channel.reply("^5Lick that puckered freckle, {}^5!".format(player))

	def cmd_rimjob(self, player, msg, channel):
		channel.reply("^5Oooh {}^5, your tongue feels all rough on my sphincter!".format(player))

	def cmd_sphincter(self, player, msg, channel):
		channel.reply("^5I'm gaping just for you, {}^5.".format(player))

	def cmd_goatse(self, player, msg, channel):
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("^5hello.jpg".format(player))
                elif d == 1:
                        channel.reply("^5Are you the wide receiver, {}^5?".format(player))

	def cmd_coprophilia(self, player, msg, channel):
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("^5Shittles: Taste the Brown Rainbow".format(player))
                elif d == 1:
                        channel.reply("^5Smear it all over, {}^5!".format(player))

	def cmd_scat(self, player, msg, channel):
                d = random.randint(0, 2)
                if d == 0:
                        channel.reply("^5Diddly bop dop boo doo dee wop wop badaaaaa!!!".format(player))
                elif d == 1:
                        channel.reply("^5I'm the scat man.".format(player))
                elif d == 2:
                        channel.reply("^5If the scatman can do it, so can you.".format(player))

	def cmd_feels(self, player, msg, channel):
                d = random.randint(0, 3)
                if d == 0:
                        channel.reply("^5Dem feels.".format(player))
                elif d == 1:
                        channel.reply("^5Why can't I hold all these feels?".format(player))
                elif d == 2:
                        channel.reply("^5Feels good man.".format(player))
                elif d == 3:
                        channel.reply("^5Right in the feels.".format(player))

	def cmd_moin(self, player, msg, channel):
		channel.reply("^5Moin moin, {}^5.".format(player))

	def cmd_win(self, player, msg, channel):
                d = random.randint(0, 3)
                if d == 0:
                        channel.reply("^5Winning at Quake is like winning at the special Olympics, blah blah blah...".format(player))
                elif d == 1:
                        channel.reply("^5Without losing, winning isn't so great.".format(player))
                elif d == 2:
                        channel.reply("^5Winning is only half of it. Having fun is the other half.".format(player))
                elif d == 3:
                        channel.reply("^5There are more important things in life than winning or losing a game - Lionel Messi".format(player))

	def cmd_lmao(self, player, msg, channel):
                d = random.randint(0, 3)
                if d == 0:
                        channel.reply("^5Licking Multiple Anal Openings?".format(player))
                elif d == 1:
                        channel.reply("^5Lasciviously Making Amoral Observations?".format(player))
                elif d == 2:
                        channel.reply("^5Love Me All Over?".format(player))
                elif d == 3:
                        channel.reply("^5Liberal Meatheads Appoint Obama?".format(player))

	def cmd_lol(self, player, msg, channel):
                d = random.randint(0, 3)
                if d == 0:
                        channel.reply("^5Loving Old Ladies?".format(player))
                elif d == 1:
                        channel.reply("^5Leaking Out Liquids?".format(player))
                elif d == 2:
                        channel.reply("^5Lobotomised Or Laggard?".format(player))
                elif d == 3:
                        channel.reply("^5Leaving Objectionable Lumps?".format(player))

	def cmd_lag(self, player, msg, channel):
                d = random.randint(0, 2)
                if d == 0:
                        channel.reply("^5Don't blame it on the lag, {}^5. You just suck.".format(player))
                elif d == 1:
                        channel.reply("^5Stop downloading that gay midget porn then, {}^5.".format(player))
                elif d == 2:
                        channel.reply("^5It's not lag, {}^5. Your PC is just late to the party.".format(player))

	def cmd_lube(self, player, msg, channel):
                d = random.randint(0, 2)
                if d == 0:
                        channel.reply("^5Get it all moist, {}^5.".format(player))
                elif d == 1:
                        channel.reply("^5Mmm... slippery...".format(player))
                elif d == 2:
                        channel.reply("^5Oooh, cherry flavoured!".format(player))

	def cmd_rage(self, player, msg, channel):
                d = random.randint(0, 2)
                if d == 0:
                        channel.reply("^5Chill the fuck out, {}^5.".format(player))
                elif d == 1:
                        channel.reply("^5{}^5 needs to take a chill pill.".format(player))
                elif d == 2:
                        channel.reply("^5Someone needs to book {}^5 into anger management therapy...".format(player))

	def cmd_minkyn(self, player, msg, channel):
                d = random.randint(0, 4)
                if d == 0:
                        channel.reply("^5Minky, musky, sly old stoaty stoaty stoat.".format(player))
                elif d == 1:
                        channel.reply("^5Just kidding, there's loads of cool things in Belgium. Just not Minky.".format(player))
                elif d == 2:
                        channel.reply("^5When I'm thinkin' of Minkyn, my knob ends up shrinkin'".format(player))
                elif d == 3:
                        channel.reply("^5What's that stinkin'? Oh, it's just Minkyn...".format(player))
                elif d == 4:
                        channel.reply("^5I just can't stop drinkin', to forget about Minkyn...".format(player))

	def cmd_scorpse(self, player, msg, channel):
                d = random.randint(0, 2)
                if d == 0:
                        channel.reply("^5Not over my cold, dead scorpse!".format(player))
                elif d == 1:
                        channel.reply("^5There's no money, there's no weed. It's all been replaced by a pile of scorpses.".format(player))
                elif d == 2:
                        channel.reply("^5There's no money, there's no weed. It's all been replaced by a pile of scorpses.".format(player))

	def cmd_whahaha(self, player, msg, channel):
                d = random.randint(0, 2)
                if d == 0:
                        channel.reply("^5Let him put his rocket in your pocket.".format(player))
                elif d == 1:
                        channel.reply("^5He apparently likes your sister.".format(player))
                elif d == 2:
                        channel.reply("^5All your mums are belong to him!".format(player))

	def cmd_iosys(self, player, msg, channel):
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("^5An error has occurred. Press CTRL+ALT+DEL to restart your computer. Error: 03 :016F".format(player))
                elif d == 1:
                        channel.reply("^5The sissiest sys on the station!".format(player))

	def cmd_hurzhurz(self, player, msg, channel):
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("^5It hurz so good...".format(player))
                elif d == 1:
                        channel.reply("^5HurzHurz is a big fat poopyhead. Do I win the Nobel Prize now?".format(player))

	def cmd_railgunnar(self, player, msg, channel):
                d = random.randint(0, 5)
                if d == 0:
                        channel.reply("^5Gunnis smakar falukorv. Smakar skit.".format(player))
                elif d == 1:
                        channel.reply("^5Dirty Swedes, done dirt cheap.".format(player))
                elif d == 2:
                        channel.reply("^5Har du hoert om svensken som omkom naar han skulle drikke melk? Kua satte seg paa ham!".format(player))
                elif d == 3:
                        channel.reply("^5Man kjenner igjen svensk toalettpapir fordi instruksjonene er trykket paa hvert blad!".format(player))
                elif d == 4:
                        channel.reply("^5Hvorfor bruker alltid Gunnis lue? For at kunne samle tankene :P".format(player))
                elif d == 5:
                        channel.reply("^5Anger! Violence! Jaywalking!".format(player))

	def cmd_d1jon(self, player, msg, channel):
                d = random.randint(0, 4)
                if d == 0:
                        channel.reply("^5Check out his little mustard pickle :D".format(player))
                elif d == 1:
                        channel.reply("^5Smear it on yer meat.".format(player))
                elif d == 2:
                        channel.reply("^5He's shit, leave him alone.".format(player))
                elif d == 3:
                        channel.reply("^5d1jon doesn't quite cut the mustard...".format(player))
                elif d == 4:
                        channel.reply("^5Another familiar face... for me to Poupon".format(player))

	def cmd_crash7(self, player, msg, channel):
		channel.reply("^5Dou-te esta flor um beijo a ti...".format(player))

	def cmd_crash(self, player, msg, channel):
		channel.reply("^5Get rekt? Nah, get crashed ;)".format(player))

	def cmd_pestenoire(self, player, msg, channel):
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("^5Woe! The black death descends upon us!".format(player))
                elif d == 1:
                        channel.reply("^5Pustules? Boils? Gangrene? Yep, it's the plague ;)".format(player))

	def cmd_psych(self, player, msg, channel):
		channel.reply("^5Just another word for a horrible, lingering death.".format(player))

	def cmd_kikindas(self, player, msg, channel):
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("^5Yeah, yeah, he's a good boy.".format(player))
                elif d == 1:
                        channel.reply("^5Kiki's Delivery Service: Bringing The Ass-Kicking".format(player))

	def cmd_milkydischarge(self, player, msg, channel):
                d = random.randint(0, 3)
                if d == 0:
                        channel.reply("^5Drink it down, {}^5... every last drop.".format(player))
                elif d == 1:
                        channel.reply("^5Feel the creamy goodness sliding down your throat.".format(player))
                elif d == 2:
                        channel.reply("^5Taste it. Love it.".format(player))
                elif d == 3:
                        channel.reply("^5Oh dear. It's all milky and creamy.".format(player))

	def cmd_papryk(self, player, msg, channel):
                d = random.randint(0, 2)
                if d == 0:
                        channel.reply("^5Our dear old Pappy.".format(player))
                elif d == 1:
                        channel.reply("^5Lie back and spread your legs... Here comes the Pap smear!".format(player))
                elif d == 2:
                        channel.reply("^5No one listens to what old Pap's got to say, on account of his deformity.".format(player))

	def cmd_fiszek(self, player, msg, channel):
                d = random.randint(0, 2)
                if d == 0:
                        channel.reply("^5Get some fizz in ya.".format(player))
                elif d == 1:
                        channel.reply("^5It's all fizzy on my tongue :P".format(player))
                elif d == 2:
                        channel.reply("^5Do you like fiszsticks? Then you're a gay fisz ;)".format(player))

	def cmd_forthewin(self, player, msg, channel):
		channel.reply("^5'I don't feel very much like Pooh today,' said Pooh ".format(player))

	def cmd_eveshka(self, player, msg, channel):
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("^5We curse ideals of he and she.".format(player))
                elif d == 1:
                        channel.reply("^5Our radiant resident rusalka...".format(player))

	def cmd_groberunfug(self, player, msg, channel):
		channel.reply("^5Unfug yer grobes.".format(player))

	def cmd_obiarshi(self, player, msg, channel):
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("^5Biggest pervert on the Station.".format(player))
                elif d == 1:
                        channel.reply("^5Totallyunawaregreatwhitesharkinapoolwithadog".format(player))

	def cmd_ogopogo(self, player, msg, channel):
		channel.reply("^5Oh noes it's pogos!".format(player))

	def cmd_roleplayer(self, player, msg, channel):
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("^5Kickin' Arsch and takin' names".format(player))
                elif d == 1:
                        channel.reply("^5Donate to the 'Buy Roley a new mouse and keyboard' fund!".format(player))

	def cmd_woolph(self, player, msg, channel):
		channel.reply("^5Mmm... so soft and wooly...".format(player))

	def cmd_p0lymer(self, player, msg, channel):
                d = random.randint(0, 2)
                if d == 0:
                        channel.reply("^5The swiss miss :P".format(player))
                elif d == 1:
                        channel.reply("^5Hide your toblerones, it's poly!".format(player))
                elif d == 2:
                        channel.reply("^5Poly wanna cracker?".format(player))

	def cmd_feck(self, player, msg, channel):
		channel.reply("^5Feck orf ya daft twat.".format(player))

	def cmd_queef(self, player, msg, channel):
                d = random.randint(0, 5)
                if d == 0:
                        channel.reply("^5{}^5 lets out a big ol' pussy fart.".format(player))
                elif d == 1:
                        channel.reply("^5The Good, The Bad and the Sloppy, starring Lee Van Queef".format(player))
                elif d == 2:
                        channel.reply("^5Gee, {}^5, that one really ruffled your beef curtains!".format(player))
                elif d == 3:
                        channel.reply("^5If boys could queef, it'd look like a snake sneezing.".format(player))
                elif d == 4:
                        channel.reply("^5{}^5 joined yoga classes just to hear chicks queef.".format(player))
                elif d == 5:
                        channel.reply("^5If a cat farts, is that considered a queef?".format(player))

	def cmd_bullshit(self, player, msg, channel):
                d = random.randint(0, 2)
                if d == 0:
                        channel.reply("^5I've had enough of your bullshit, {}^5.".format(player))
                elif d == 1:
                        channel.reply("^5My bullshit detector just beeped.".format(player))
                elif d == 2:
                        channel.reply("^5That was complete and utter bullshit, {}^5.".format(player))

	def cmd_iouonegirl(self, player, msg, channel):
                d = random.randint(0, 4)
                if d == 0:
                        channel.reply("^5Still waiting for that one girl you owe me...".format(player))
                elif d == 1:
                        channel.reply("^5You're not my real One!".format(player))
                elif d == 2:
                        channel.reply("^5Shut up, Minkyn!".format(player))
                elif d == 3:
                        channel.reply("^5Repeated usage of 'Aah aah ahh!' will result in perma-ban. You have been warned.".format(player))
                elif d == 4:
                        channel.reply("^5It's the real One, yes, the phuncky feel One.".format(player))

	def cmd_chillin1(self, player, msg, channel):
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("^5Mmm... chilli con carne...".format(player))
                elif d == 1:
                        channel.reply("^5Whassup? Chillin, havin' a bud...".format(player))

	def cmd_crumbsucker(self, player, msg, channel):
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("^5Suckin' up those crumbs...".format(player))
                elif d == 1:
                        channel.reply("^5Get ready to be sucked, it's crummy!".format(player))

	def cmd_robo(self, player, msg, channel):
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("^5Domo arigato, Mr Robo".format(player))
                elif d == 1:
                        channel.reply("^5I'm not perfect; I'm not a robo   -Justin Bieber".format(player))

	def cmd_enema(self, player, msg, channel):
                d = random.randint(0, 2)
                if d == 0:
                        channel.reply("^5Enemas scare the shit out of me.".format(player))
                elif d == 1:
                        channel.reply("^5{}^5 is an enema of the state.".format(player))
                elif d == 2:
                        channel.reply("^5{}^5 heard that coffee enemas were beneficial. He's no longer welcome in Starbucks.".format(player))

	def cmd_fragstealer(self, player, msg, channel):
                d = random.randint(0, 3)
                if d == 0:
                        channel.reply("^5That wasn't stealing, {}^5. Your team mate just wasn't quick enough.".format(player))
                elif d == 2:
                        channel.reply("^5Oh noes! Some criminal mastermind has been going around stealing frags!".format(player))
                elif d == 3:
                        channel.reply("^5It seems some team mate didn't like your support, {}^5".format(player))

	def cmd_condom(self, player, msg, channel):
                d = random.randint(0, 2)
                if d == 0:
                        channel.reply("^5How's a woman like a condom? They spend more time in your wallet than on yer dick.".format(player))
                elif d == 1:
                        channel.reply("^5{}^5 is so cheap he recycles condoms.".format(player))
                elif d == 2:
                        channel.reply("^5Difference between a woman and condoms? It's easier to piss a woman off.".format(player))

	def cmd_bareback(self, player, msg, channel):
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("^5{}^5 once tried it bareback. He made a whole lotta money that night.".format(player))
                elif d == 1:
                        channel.reply("^5{}^5 never goes bareback. He heard that's how arse-babies are made :P".format(player))

	def cmd_pedestrian(self, player, msg, channel):
                d = random.randint(0, 2)
                if d == 0:
                        channel.reply("^5Varldens langsammaste fotgangare".format(player))
                elif d == 1:
                        channel.reply("^5Why did Pedestrian cross the road? Wait for it... Ah fuck it, lame joke anyway :P".format(player))
                elif d == 2:
                        channel.reply("^5Insert pedo joke here.".format(player))

	def cmd_equality4all(self, player, msg, channel):
                d = random.randint(0, 2)
                if d == 0:
                        channel.reply("^5He really does suck best.".format(player))
                elif d == 1:
                        channel.reply("^5Don't be a gay wossname.".format(player))
                elif d == 2:
                        channel.reply("^5Aww so cute! He brought his own bucket!".format(player))

	def cmd_crexx(self, player, msg, channel):
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("^5Mmm... sexy Crexxy".format(player))
                elif d == 1:
                        channel.reply("^5RAWR! Tyrannosaurus Crexx!".format(player))

	def cmd_crexx_chaos(self, player, msg, channel):
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("^5Mmm... sexy Crexxy".format(player))
                elif d == 1:
                        channel.reply("^5RAWR! Tyrannosaurus Crexx!".format(player))

	def cmd_staycool(self, player, msg, channel):
		channel.reply("^5I stay cool, and dig all jive. That's the way I stay alive.".format(player))

	def cmd_nemesis(self, player, msg, channel):
		channel.reply("^5Do you know what 'nemesis' means? A righteous infliction of retribution manifested by an appropriate agent. Personified in this case by an 'orrible tnuc... me.".format(player))

	def cmd_stupid(self, player, msg, channel):
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("^5You should never underestimate the predictability of stupidity.".format(player))
                elif d == 1:
                        channel.reply("^5Your stupidity may be your one saving grace.".format(player)) 

	def cmd_asshole(self, player, msg, channel):
		channel.reply("^5Get your tongue out my asshole.".format(player))   

	def cmd_virgin(self, player, msg, channel):
		channel.reply("^5In the quiet words of virgin Mary, come again.".format(player))   

	def cmd_fuckface(self, player, msg, channel):
		channel.reply("^5Fuckface... I like that one. I'll have to remember that one next time I'm climbing off yer mum.".format(player))   

	def cmd_curry(self, player, msg, channel):
		channel.reply("^5The sight of a chopped-up body will look like curry to a pisshead.".format(player))   

	def cmd_bg(self, player, msg, channel):
		channel.reply("^5Yeah, well, you know, that's just, like, your opinion, man.".format(player))   

	def cmd_fu(self, player, msg, channel):
		channel.reply("^5Kung fu!".format(player))   

	def cmd_herpes(self, player, msg, channel):
		channel.reply("^5Her pees are better than your poos.".format(player))   

	def cmd_milky(self, player, msg, channel):
		channel.reply("^5If the milk turns out to be sour, I ain't the kind of pussy to drink it.".format(player))

	def cmd_dildo(self, player, msg, channel):
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("^5Arse Tickler's Faggots Fan Club: the latest in arse-intruding dildos!".format(player))
                elif d == 1:
                        channel.reply("^5This bloke's dildos.".format(player))   

	def cmd_tea(self, player, msg, channel):
		channel.reply("^5The entire British Empire was built on cups of tea... and if you think I'm going to war without one, mate, you're mistaken.".format(player))   

	def cmd_doublepenetration(self, player, msg, channel):
		channel.reply("^5sometimes when a woman has sex with more than one man, each man makes love to a different orifice.".format(player))

	def cmd_flirt(self, player, msg, channel):
                d = random.randint(0, 14)
                if d == 0:
                        channel.reply("^5Do you frag here very often?".format(player))
                elif d == 1:
                        channel.reply("^5I'm not drunk, I'm just intoxicated by YOU.".format(player))
                elif d == 2:
                        channel.reply("^5Did you sit in a pile of sugar? Cause you have a pretty sweet ass.".format(player))
                elif d == 3:
                        channel.reply("^5I wanna live in your socks so I can be with you every step of the way.".format(player))
                elif d == 4:
                        channel.reply("^5I seem to have lost my phone number. Can I have yours?".format(player))
                elif d == 5:
                        channel.reply("^5I was feeling a little off today, but you definitely turned me on.".format(player))
                elif d == 6:
                        channel.reply("^5Is your daddy a Baker? Because you've got some nice buns!".format(player))
                elif d == 7:
                        channel.reply("^5Are you a parking ticket? 'Cause you've got fine written all over you.".format(player))
                elif d == 8:
                        channel.reply("^5I'm not staring at your boobs. I'm staring at your heart.".format(player))
                elif d == 9:
                        channel.reply("^5That rocket launcher really brings out the colour in your eyes.".format(player))
                elif d == 10:
                        channel.reply("^5Are you carrying a lightning gun? 'Cause I'm seeing sparks fly.".format(player))
                elif d == 11:
                        channel.reply("^5Good thing I brought my depleted uranium slugs, 'cause I wanna rail you so hard.".format(player))
                elif d == 12:
                        channel.reply("^5Don't worry about that bang. That was just my shotgun going off in my pants.".format(player))
                elif d == 13:
                        channel.reply("^5Are you packing a gauntlet? 'Cause you've just knocked me out.".format(player))
                elif d == 14:
                        channel.reply("^5Is that a grenade launcher? 'Cause you just launched me into the clouds.".format(player))

	def cmd_jaxzii(self, player, msg, channel):
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("^5Gottim right up the jaxzii.".format(player))
                elif d == 1:
                        channel.reply("^5What a jaxzoff :P".format(player))

	def cmd_ratamahatta(self, player, msg, channel):
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("^5He's got an Itchy Phallus.".format(player))
                elif d == 1:
                        channel.reply("^5Vamo detona essa porra!".format(player))

	def cmd_stalls(self, player, msg, channel):
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("^5He's still pedo in my mind...".format(player))
                elif d == 1:
                        channel.reply("^5Stalpikk!".format(player)) 

	def cmd_qwasyx(self, player, msg, channel):
		channel.reply("^5Qwa Qwa Qwa!".format(player))

	def cmd_beanz(self, player, msg, channel):
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("^5Beanz, beanz, the musical fruit; The more you eat, the more you toot.".format(player))
                elif d == 1:
                        channel.reply("^5Loves bathing in the delicious milk.".format(player))   

	def cmd_featuredib(self, player, msg, channel):
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("^5Gettin' dibby with it.".format(player))
                elif d == 1:
                        channel.reply("^5Ain't nuthin' but a kurwa.".format(player))

	def cmd_oshcovoq(self, player, msg, channel):
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("^5Oh gosh, it's Osh!".format(player))
                elif d == 1:
                        channel.reply("^5How many coqs could oshcovoq suq if oshcovoq could suq coq?".format(player))

	def cmd_tape(self, player, msg, channel):
                d = random.randint(0, 3)
                if d == 0:
                        channel.reply("^5So called because he duct-tapes his victims and throws them in his van.".format(player))
                elif d == 1:
                        channel.reply("^5Load'cheesepizza',8,1    Press play on tape.".format(player))
                elif d == 2:
                        channel.reply("^5Has finally stopped eating stuff off the ground.".format(player))
                elif d == 3:
                        channel.reply("^5Riddled with tapeworm.".format(player))   

	def cmd_daime(self, player, msg, channel):
                d = random.randint(0, 2)
                if d == 0:
                        channel.reply("^5It's time for some daime!".format(player))
                elif d == 1:
                        channel.reply("^5Delicious chocolatey goodness.".format(player))
                elif d == 2:
                        channel.reply("^5Is like the best farts: silent but deadly..".format(player))

	def cmd_tjtjtjtj(self, player, msg, channel):
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("^5Come Mr. TJ won't you turn the music up".format(player))
                elif d == 1:
                        channel.reply("^5It ain't kosher!".format(player))

	def cmd_danielhjorvar(self, player, msg, channel):
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("^5Eg tala ekki islenska".format(player))
                elif d == 1:
                        channel.reply("^5Modern day viking in da house!".format(player))   

	def cmd_barbarossa(self, player, msg, channel):
		channel.reply("^5Come join us in Barbie's Malibu Dreamhouse!".format(player))

	def cmd_hansgruber(self, player, msg, channel):
                d = random.randint(0, 5)
                if d == 0:
                        channel.reply("^5Look ma! No Hans!".format(player))
                elif d == 1:
                        channel.reply("^5I deleted all the German names from my phone. It's now Hans-free.".format(player))
                elif d == 2:
                        channel.reply("^5Holy fuck, heres the Jennifer Grubez!".format(player))
                elif d == 3:
                        channel.reply("^5Grab your lube, here comes the Grube!".format(player))
                elif d == 4:
                        channel.reply("^5The emperor's new Grube.".format(player))
                elif d == 5:
                        channel.reply("^5How Stella got her Grube back.".format(player))

	def cmd_spermi(self, player, msg, channel):
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("^5Get your umbrellas out for the spermshower!".format(player))
                elif d == 1:
                        channel.reply("^5He ain't got germs, just oodles of sperms :P".format(player))

	def cmd_revilian(self, player, msg, channel):
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("^5The reviled Revilian...".format(player))
                elif d == 1:
                        channel.reply("^5He ain't worth a million, he's only Revilian...".format(player))

	def cmd_omek(self, player, msg, channel):
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("^5He's the alpha and omega :P".format(player))
                elif d == 1:
                        channel.reply("^5Chillin' wit' mah 'omie.".format(player))   

	def cmd_ranzige(self, player, msg, channel):
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("^5Just like a rancid bitch.".format(player))
                elif d == 1:
                        channel.reply("^5Sounds like a queef, but it's just the teef.".format(player))

	def cmd_boobsize(self, player, msg, channel):
                d = random.randint(0, 3)
                if d == 0:
                        channel.reply("^5{}^5 has teeny tiny tittties.".format(player))
                elif d == 1:
                        channel.reply("^5Don't worry, {}^5, more than a handful's a waste.".format(player))
                elif d == 2:
                        channel.reply("^5Want some bacon with your fried eggs?".format(player))
                elif d == 3:
                        channel.reply("^5{}^5's breasts are like the desert: dry and flat.".format(player))

	def cmd_crap(self, player, msg, channel):
                d = random.randint(0, 2)
                if d == 0:
                        channel.reply("^5Don't talk crap, {}^5.".format(player))
                elif d == 1:
                        channel.reply("^5That's a load of crap.".format(player))
                elif d == 2:
                        channel.reply("^5You're so full of crap you could pass for a toilet.".format(player))   

	def cmd_gebakkengarnaal(self, player, msg, channel):
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("^5Shrimp pimpin'".format(player))
                elif d == 1:
                        channel.reply("^5Deep fried genocide.".format(player))   

	def cmd_goenigoegoe(self, player, msg, channel):
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("^5Check out those hairy goenads!".format(player))
                elif d == 1:
                        channel.reply("^5Goeni goeni goen...".format(player))   

	def cmd_gelenkbusfahrer(self, player, msg, channel):
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("^5Some old fart who runs a server or something.".format(player))
                elif d == 1:
                        channel.reply("^5Our fearless leader.".format(player))   

	def cmd_bus(self, player, msg, channel):
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("^5Want a ride? Hop on the bus.".format(player))
                elif d == 1:
                        channel.reply("^5We all ride the short bus around here.".format(player))   

	def cmd_station(self, player, msg, channel):
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("^5It's where all the cool kids stay away from.".format(player))
                elif d == 1:
                        channel.reply("^5Now with 120 percent more gaiety!".format(player))   

	def cmd_whitefeather(self, player, msg, channel):
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("^5The whitest of the white.".format(player))
                elif d == 1:
                        channel.reply("^5Tarred and feathered.".format(player))   

	def cmd_timescar(self, player, msg, channel):
                d = random.randint(0, 5)
                if d == 0:
                        channel.reply("^5Oh, is that the time? I have to go...".format(player))
                elif d == 1:
                        channel.reply("^5Contender for sickest motherfucker on the station.".format(player))
                elif d == 2:
                        channel.reply("^5Fat chick connoisseur.".format(player))
                elif d == 3:
                        channel.reply("^5Seriously scarred and running out of time.".format(player))
                elif d == 4:
                        channel.reply("^5The man with the huge chinko.".format(player))
                elif d == 5:
                        channel.reply("^5Has all the features a woman wants, but his face is a potato.".format(player))   

	def cmd_darkmo(self, player, msg, channel):
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("^5The darkest mo that ever mooed.".format(player))
                elif d == 1:
                        channel.reply("^5Mo' money mo' problems.".format(player))   

	def cmd_masturbate(self, player, msg, channel):
                d = random.randint(0, 4)
                if d == 0:
                        channel.reply("^5{}^5 shakes hands with the bishop.".format(player))
                elif d == 1:
                        channel.reply("^5{}^5 chokes the chicken.".format(player))
                elif d == 2:
                        channel.reply("^5{}^5 does the five finger shuffle.".format(player))
                elif d == 3:
                        channel.reply("^5{}^5 gets trigger happy.".format(player))
                elif d == 4:
                        channel.reply("^5{}^5 jerks the gherkin.".format(player))   

	def cmd_killerboy(self, player, msg, channel):
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("^5Not a boy, not yet a killer.".format(player))
                elif d == 1:
                        channel.reply("^5A Dane pretending to be a Swede.".format(player))

	def cmd_jimmyvulgar(self, player, msg, channel):
                d = random.randint(0, 3)
                if d == 0:
                        channel.reply("^5Really hits the g-spot.".format(player))
                elif d == 1:
                        channel.reply("^5Pornstar in training.".format(player))
                elif d == 2:
                        channel.reply("^5Vulgarity begins when imagination succumbs to the explicit.".format(player))
                elif d == 3:
                        channel.reply("^5Vulgarity is life.".format(player))

	def cmd_angelripper(self, player, msg, channel):
                d = random.randint(0, 2)
                if d == 0:
                        channel.reply("^5Rippin' angels wide open since 1997.".format(player))
                elif d == 1:
                        channel.reply("^5Going AFK in 3... 2... 1...".format(player))
                elif d == 2:
                        channel.reply("^5Just call him daddy.".format(player))

	def cmd_satanclaws(self, player, msg, channel):
                d = random.randint(0, 2)
                if d == 0:
                        channel.reply("^5Leaves nasty little parcels under your tree at christmas.".format(player))
                elif d == 1:
                        channel.reply("^5Kissing him under the mistletoe is not recommended.".format(player))
                elif d == 2:
                        channel.reply("^5Don't let your kids sit in his lap.".format(player))   

	def cmd_bane(self, player, msg, channel):
                d = random.randint(0, 1)
                if d == 0:
                        channel.reply("^5The bane of our existence.".format(player))
                elif d == 1:
                        channel.reply("^5Now's not the time for fear. That comes later.".format(player))