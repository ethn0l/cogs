import re
import json
from datetime import datetime
from difflib import get_close_matches
import requests
import string
from bs4 import BeautifulSoup

def get_real_date(ts):
    return datetime.utcfromtimestamp(ts).strftime('%d-%m-%Y')

def get_profile_by_int64(int64):
    return json.loads(requests.get("http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=42514013F7D8A322C42DD6488F22D20C&format=json" + "&steamids=" + str(int64)).text)["response"]["players"][0]

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

    steam_api = get_profile_by_int64(values[2])
    custom_url = steam_api["profileurl"].split("/")[:-1].pop()
    created = get_real_date(steam_api["timecreated"]) if "timecreated" in steam_api.keys() else "None"
    profilestate = "public" if steam_api["communityvisibilitystate"] - 1 else "private"
    profilename = steam_api["personaname"] if "personaname" in steam_api.keys() else "None"

    if not custom_url.isnumeric():
        values[3] = custom_url

    return {
        "steamid":values[0],
        "steamid3":values[1],
        "steamid64":values[2],
        "custom_url":values[3],
        "profile_name":profilename,
        "profile_state":profilestate,
        "profile_created":created,
        "location":values[7],
        "status":values[8],
        "profile_url":values[9+i]
    }

# SETUP RED SUPPORT HERE.
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
                response = ">>> "

                if not result_only:
                    for kn in result.keys():
                        if result[kn] != "None":
                            response += "**{}**: {}\n".format(kn.upper(), result[kn]).replace("_", " ")
                        else:
                            continue

                elif result_only:
                    opt = [e.replace("_", " ") for e in list(result.keys())]
                    matches = get_close_matches(result_only, opt)
                    if len(matches) >= 1:
                        kn = matches[0]
                        response += "**{}**: {}\n".format(kn.upper(), result[kn]).replace("_", " ")

                        if not one_message:
                            await ctx.bot.send_message(ctx.message.channel, response)
                            one_message = True
                    else:
                        if not one_message:
                            await ctx.bot.send_message(ctx.message.channel, "> No such return as '" + result_only + "' in this search.")
                            one_message = True

                if not one_message:
                        await ctx.bot.send_message(ctx.message.channel, response)
                        one_message = True

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
