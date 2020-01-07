import re
import json
from datetime import datetime
from difflib import get_close_matches
import requests
import string
from bs4 import BeautifulSoup

def get_title_for_box(steam_reference, username):
    steamid_regex = re.compile(r"STEAM_[0-1]:[0-1]:\d+")
    steamid3_regex = re.compile(r"U:[0-9]:\d{1,20}")
    steamid64_regex = re.compile(r"\d{17}")

    if steamid_regex.match(steam_reference):
        return steam_reference + " recognized as a STEAMID and found user " + username

    elif steamid3_regex.match(steam_reference.strip("[").strip("]")):
        return steam_reference + " recognized as a STEAMID3 and found user " + username

    elif steamid64_regex.match(steam_reference):
        return steam_reference + " recognized as a STEAMID64 and found user " + username

    else:
        # customurl
        return steam_reference + " recognized as a customURL and found user " + username



def get_real_date(ts):
    return datetime.utcfromtimestamp(ts).strftime('%d-%m-%Y %H:%M:%S')

def get_profile_by_int64(int64):
    return json.loads(requests.get("http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=42514013F7D8A322C42DD6488F22D20C&format=json" + "&steamids=" + str(int64)).text)["response"]["players"][0]

def get_bans_by_int64(int64):
    return json.loads(requests.get("http://api.steampowered.com/ISteamUser/GetPlayerBans/v1/?key=42514013F7D8A322C42DD6488F22D20C&format=json" + "&steamids=" + str(int64)).text)["players"][0]

def get_profile_by_steamio(inp):
    url = "https://steamid.io/lookup/" + str(inp)
    req = requests.get(url)
    if req.status_code != 200:
        print(req.text)
        return False

    html = req.text
    parsed = BeautifulSoup(html, 'html.parser')
    values = [re.sub("<[^>]*>", "", str(x.find("a"))) for x in parsed.find_all(attrs={"class":"value"})]

    i = 0

    if len(values) < 10:
        return False

    elif len(values) > 10:
        i = len(values) - 10

    # STEAM API
    steam_api = get_profile_by_int64(values[2])
    custom_url = steam_api["profileurl"].split("/")[:-1].pop()
    created = get_real_date(steam_api["timecreated"]) if "timecreated" in steam_api.keys() else "None"
    profilestate = "public" if steam_api["communityvisibilitystate"] - 1 else "private"
    profilename = steam_api["personaname"] if "personaname" in steam_api.keys() else "None"
    lastlogoff = get_real_date(steam_api["lastlogoff"]) if "lastlogoff" in steam_api.keys() else "None"

    if not custom_url.isnumeric():
        values[3] = custom_url

    return {
        "steamid":values[0].replace("0:0:", "1:0:").replace("0:1:", "1:1:"),
        "steamid3":values[1],
        "steamid64":values[2],
        "custom_url":values[3],
        "profile_name":profilename,
        "profile_state":profilestate,
        "profile_created":created,
        "location":values[7],
        # "status":values[8],
        "last_logoff":lastlogoff,
        "profile_url":values[9+i],
        "avatar":steam_api["avatarfull"]
    }

# SETUP RED SUPPORT HERE.
from discord import Embed
from discord.ext import commands

# Classname should be CamelCase and the same spelling as the folder
class steam:
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    """
    COG that provides the command [p]steam, that can parse steam input and return steamio.io details.
    """

    @commands.command(pass_context=True)
    async def steam(self, ctx):
        """
        Please enter a steamID, steamID3, steamID64, customURL or complete URL.

        Some valid examples:

        a steamID               	STEAM_0:0:11101
        a steamID3	                [U:1:22202]
        a steamID3 without brackets	U:1:22202
        a steamID64	                76561197960287930
        a customURL	                gabelogannewell
        a full URL	                http://steamcommunity.com/profiles/76561197960287930
        a full URL with customURL	http://steamcommunity.com/id/gabelogannewell
        """

        one_message = False
        result_only = None

        try:
            com = ctx.message.content.split(" ")
            steam_reference = ""

            if len(com) <= 1:
                if not one_message:
                    await ctx.bot.send_message(ctx.message.channel, "> No steam reference given.")
                    one_message = True

            elif len(com) == 2:
                steam_reference = com[1]
            
            elif len(com) >= 3:
                steam_reference = com[1]
                result_only = ' '.join(com[2:])

            result = get_profile_by_steamio(steam_reference)
    
            if result:
                icon = result["avatar"]
                del result["avatar"]

                embed = Embed(color=0xd6c8ff)
                embed.set_author(name=get_title_for_box(steam_reference, result["profile_name"]), url=result["profile_url"], icon_url=icon)
                embed.set_footer(text="Results provided by Valve and STEAMID I/O. Author: 4ppl3#0018")

                if not result_only:
                    for kn in result.keys():
                        if result[kn] != "None":
                            embed.add_field(name=kn.upper().replace("_", " "), value=result[kn])
                        else:
                            continue

                elif result_only:
                    opt = list(result.keys())
                    matches = get_close_matches(result_only, opt)
                    if len(matches) >= 1:
                        kn = matches[0]
                        embed.add_field(name=kn.upper().replace("_", " "), value=result[kn])

                        if not one_message:
                            await ctx.bot.send_message(ctx.message.channel, embed=embed)
                            one_message = True
                    else:
                        if not one_message:
                            await ctx.bot.send_message(ctx.message.channel, "> No such return as '" + result_only + "' in this search.")
                            one_message = True

                if not one_message:
                        await ctx.bot.send_message(ctx.message.channel, embed=embed)
                        one_message = True
                
                # CHECK FOR VAC BANS SEPERATE OF THE ONE MESSAGE LOOP
                # Check for vac bans
                bans = get_bans_by_int64(result["steamid64"])
                vac_embed = Embed()

                if bans["VACBanned"] or bans["NumberOfGameBans"]:
                    days_since_last = bans["DaysSinceLastBan"]
                    amount_of_vac = bans["NumberOfVACBans"]
                    amount_of_game = bans["NumberOfGameBans"]
                    vac_word = "bans"
                    game_word = "bans"

                    if amount_of_vac == 1:
                        vac_word = "ban"
                    
                    if amount_of_game == 1:
                        game_word = "ban"
                    

                    if amount_of_game:
                        vac_embed.title = "WARNING {} has {} game {} on record! ".format(result["profile_name"], amount_of_game, game_word)
                        vac_embed.colour = 0xffff00

                    if bans["VACBanned"]:
                        vac_embed.title = "WARNING {} has {} VAC {}".format(result["profile_name"], amount_of_vac, vac_word) + (" and {} game {} on record!".format(amount_of_game, game_word) if amount_of_game else " on record!")
                        vac_embed.colour = 0xff0000

                    vac_embed.set_thumbnail(url="https://cdn2.iconfinder.com/data/icons/freecns-cumulus/32/519791-101_Warning-512.png")
                    
                    vac_embed.add_field(name="VAC bans", value=str(amount_of_vac), inline=True)
                    vac_embed.add_field(name="Game bans", value=str(amount_of_game), inline=True)
                    vac_embed.add_field(name="Days since last ban", value=str(days_since_last), inline=False)

                    await ctx.bot.send_message(ctx.message.channel, embed=vac_embed)

            else:
                if not one_message:
                    await ctx.bot.send_message(ctx.message.channel, "> Steam reference could not be found.")
                    one_message = True

        except Exception as e:
            print(e)
            if not one_message:
                await ctx.bot.send_message(ctx.message.channel, "> Failed to load steam.io")
                one_message = True
        
        await self.bot.delete_message(ctx.message) # delete message when done
    
    # !report implemented as -report
    @commands.command(pass_context=True)
    async def report(self, ctx):
        embed=Embed(title="**THIS CHANNEL IS FOR EVIDENCE ONLY**", description="- Post the EVIDENCE\n - Post their steam profile link\n  - Mention what server they are on\n - And let us know what they are doing (cheating, trolling, griefing, etc)", color=0xe06100)
        embed.add_field(name="To report a player in-game", value="- Type !calladmin in-game\n - Select a player you would like to report\n - Type the reason for this report then press enter", inline=False)
        await self.bot.say(embed=embed)
    
    # !rules implemented as -rules
    @commands.command(pass_context=True)
    async def rules(self, ctx):
        embed = Embed(title="**RULES**", color=0xffffff)
        embed.add_field(name="Rule 1", value="Speak only english via vocie or text chat to maintain clear channels of communication.", inline=False)
        embed.add_field(name="Rule 2 ", value="Do not grief, cheat, script, exploit, or use hacks of any kind. If found to be in breach of this rule, bns recieived will be **permanent** and **unappealable**.", inline=False)
        embed.add_field(name="Rule 3 ", value="Do not impersonate any members or staff.", inline=False)
        embed.add_field(name="Rule 4", value="No smurf accounts/alts.\n\n **NOTE: In a rising trend on our servers, Alts/Smurfs are being frequently used to throw games, cheat, or evade previous bns, therefore, if caught using an Alt/Smurf account, it will be permanently banned from the servers. Bans for this do not carry across accounts. Accounts with VAC / Game Bans received over __365 days__ are exempt from this rule.**", inline=False)
        embed.add_field(name="Rule 5", value="Do not abuse !calladmin. This feature is pivotal for moderating the servers and abuse of the system is dealt with promptly and bans will not be overturned.", inline=False)
        embed.add_field(name="Rule 6", value="Advertisements of any kind are forbidden, Solicitating the sales of services (hacks, boosting, etc.), linking players to external sites (gamling etc.), or the promotion of servers other than Baited.xyz is strictly prohibited.", inline=False)
        embed.add_field(name="Rule 7", value="Treat other players with respect. Inastances of malicious racism, sexism or homophobia are frowned upon and when found to be in breach of this rule, bans will progressively increase with each cumulative offence.", inline=False)
        embed.add_field(name="Rule 8", value="Do not disript the server in any way. Acts of disruption can include, but are not limited to:\n\n  - Mic/Chat Spam\n - Trolling\n   - Team Flashing \n - Blocking\n - Ghosting\n - Shooting allies to reveal their position", inline=False)
        await self.bot.say(embed=embed)

def setup(bot):
    bot.add_cog(steam(bot))  
