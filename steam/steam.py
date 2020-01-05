import re
import requests
from bs4 import BeautifulSoup

def get_profile_by_steamio(inp):
    url = "https://steamid.io/lookup/" + str(inp)
    req = requests.get(url)

    if req.status_code != 200:
        return False

    html = req.text
    parsed = BeautifulSoup(html, 'html.parser')
    values = [re.sub("<[^>]*>", "", str(x.find("a"))) for x in parsed.find_all(attrs={"class":"value"})]
    
    if len(values) != 10:
        return False

    return {
        "steamid":values[0],
        "steamid3":values[1],
        "steamid64":values[2],
        "customurl":values[3],
        "profile_state":values[4],
        "profile_created":values[5],
        "name":values[6],
        "location":values[7],
        "status":values[8],
        "profile_url":values[9]
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
            
        print(dir(ctx.bot))
        
        steam_reference = ctx.message.content

        result = get_profile_by_steamio(steam_reference)

        if result:
            response = ">>> "

            for kn in result.keys():
                if result[kn] != "None":
                    response += "**{}**: {}\n".format(kn.upper(), result[kn])
            
            await ctx.bot.send_message(ctx.message.channel, response)

        else:
            await ctx.bot.send_message(ctx.message.channel, "> Invalid input.")

def setup(bot):
    bot.add_cog(steam(bot))  
