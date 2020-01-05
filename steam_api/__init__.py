from .steam_api import steam_api

def setup(bot):
    bot.add_cog(steam_api(bot))
