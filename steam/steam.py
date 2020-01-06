import re
import json
from datetime import datetime
from difflib import get_close_matches
import requests
import string
from bs4 import BeautifulSoup

def get_title_for_box(steam_reference, username):
    steamid_regex = re.compile("STEAM_[0-1]:\d{1, 20}")
    steamid3_regex = re.compile("U:[0-9]:\d{1,20}")
    steamid64_regex = re.compile("\d{17}")

    if steamid_regex.match(steam_reference):
        return steam_reference + " recognized as a STEAMID and found user **" + username + "**"

    elif steamid3_regex.match(steam_reference.strip("[").strip("]")):
        return steam_reference + " recognized as a STEAMID3 and found user **" + username + "**"

    elif steamid64_regex.match(steam_reference):
        return steam_reference + " recognized as a STEAMID64 and found user **" + username + "**"

    else:
        # customurl
        return steam_reference + " recognized as a customURL and found user **" + username + "**"



def get_real_date(ts):
    return datetime.utcfromtimestamp(ts).strftime('%d-%m-%Y %H:%M:%S')

def get_profile_by_int64(int64):
    return json.loads(requests.get("http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=42514013F7D8A322C42DD6488F22D20C&format=json" + "&steamids=" + str(int64)).text)["response"]["players"][0]

def get_bans_by_int64(int64):
    return json.loads(requests.get("http://api.steampowered.com/ISteamUser/GetPlayerBans/v1/?key=42514013F7D8A322C42DD6488F22D20C&format=json" + "&steamids=" + str(int64)).text)["response"]["players"][0]

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
        "steamid":values[0].replace("0:0", "1:0").replace("0:1", "1:1"),
        "steamid3":values[1],
        "steamid64":values[2],
        "custom_url":values[3],
        "profile_name":profilename,
        "profile_state":profilestate,
        "profile_created":created,
        "location":values[7],
        # "status":values[8],
        "last_logoff":lastlogoff,
        "profile_url":values[9+i]
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
            await self.bot.delete_message(ctx.message) # delete message when done

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
                embed = Embed(title=get_title_for_box(steam_reference, result["profile_name"]), url=result["profile_url"], color=0xd6c8ff)
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

                    if amount_of_game:
                        vac_embed.title = "Warning {} has {} game bans!".format(result["profile_name"], amount_of_game)
                        vac_embed.colour = 0xFFFF00

                    if bans["VACBanned"]:
                        vac_embed.title = "Warning {} has {} vac bans!".format(result["profile_name"], amount_of_vac) + ("And {} Game bans!".format(amount_of_game) if amount_of_game else "")
                        vac_embed.colour = 0xFF0000
                    
                    vac_embed.add_field(name="VAC bans on record", value=str(amount_of_vac), inline=False)
                    vac_embed.add_field(name="Game bans on record", value=str(amount_of_game), inline=False)
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


def setup(bot):
    bot.add_cog(steam(bot))  
