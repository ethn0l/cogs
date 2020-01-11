from discord import Embed
from discord.ext import commands

BAITED_SERVERS = {
    "meta":{
        "eu":":flag_eu: #{} Baited 5v5 Competitive !knife !ws !gloves ",
        "na":":flag_us: #{} Baited 5v5 Competitive !knife !ws !gloves ",
        "ip":"steam://connect/{}"
    },
    "eu":[
        "145.239.254.11:27015",
        "145.239.254.11:27025",
        "145.239.254.11:27035",
        "145.239.254.11:27045",
        "145.239.254.11:27055",
        "145.239.254.11:27065",
        "145.239.254.11:27075",
        "145.239.254.11:27085",
        "145.239.254.11:27095",
        "145.239.254.11:27105",
        "145.239.254.11:27115",
        "145.239.254.11:27125",
        "145.239.254.11:27135",
        "145.239.254.11:27145",
        "145.239.254.11:27155",
        "145.239.254.11:27165",
        "145.239.254.11:27175",
        "145.239.254.11:27185",
        "145.239.254.11:27195",
        "145.239.254.11:27205"
    ],
    "na":[
        "74.91.119.107:27015",
        "69.4.90.243:27075"
    ]
}

class baited:
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def report(self, ctx):
        """
        !report implemented as [p]report
        """
        embed=Embed(title="**THIS CHANNEL IS FOR EVIDENCE ONLY**", description="- Post the EVIDENCE\n - Post their steam profile link\n  - Mention what server they are on\n - And let us know what they are doing (cheating, trolling, griefing, etc)", color=0xe06100)
        embed.add_field(name="To report a player in-game", value="- Type !calladmin in-game\n - Select a player you would like to report\n - Type the reason for this report then press enter", inline=False)
        await self.bot.say(embed=embed)
        await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True)
    async def rules(self, ctx):
        """
        !rules implemented as [p]rules
        """
        embed = Embed(title="**RULES**", color=0xfffff0)
        embed.add_field(name="Rule 1", value="Speak only English via voice or text chat to maintain clear channels of communication.", inline=False)
        embed.add_field(name="Rule 2 ", value="Do not Grief, Cheat, Script or Exploit. If found to be in breach of this rule, bans received will be **permanent** and **unappealable**.", inline=False)
        embed.add_field(name="Rule 3 ", value="Do not impersonate any Players or Baited Staff.", inline=False)
        embed.add_field(name="Rule 4", value="No 'Smurf'/alt accounts on Baited.\n\n **NOTE: In a rising trend on our Servers, Alts/Smurfs are being frequently used to throw, cheat, or evade previous bans, therefore, if caught using an Alt/Smurf account, it will be permanently banned from the Servers. Bans for this do not carry across accounts. Accounts with VAC / Game Bans received over __365 days__ ago are exempt from this rule.**", inline=False)
        embed.add_field(name="Rule 5", value="Do not abuse !calladmin. This feature is pivotal for Moderating the Servers, abuse of this system will be dealt with promptly and bans will not be overturned.", inline=False)
        embed.add_field(name="Rule 6", value="Advertisements of any kind are forbidden, Soliciting the sales of services (hacks, boosting, etc.), linking players to external sites (Gambling free skins etc), or the promotion of Servers other than Baited.xyz is strictly prohibited.", inline=False)
        embed.add_field(name="Rule 7", value="Treat other players with respect. Instances of malicious racism, sexism or homophobia are frowned upon and when found to be in breach of this rule, bans will progressively increase with each cumulative offence.", inline=False)
        embed.add_field(name="Rule 8", value="Do not disrupt the Server in any way. Acts of disruption can include, but are not limited to:\n\n - Mic/Chat Spam\n - Trolling\n - Team Flashing \n - Blocking\n - Ghosting\n - Shooting allies to reveal their position", inline=False)
        await self.bot.say(embed=embed)
        await self.bot.delete_message(ctx.message)
    
    @commands.command(pass_context=True)
    async def rank(self, ctx):
        """
        !rank implemented as [p]rank
        """
        embed = Embed(title="**https://baited.xyz/rankme**", url="https://baited.xyz/rankme", description="or https://baited.xyz/rankmena for na rankings.", color=0xfffff0)
        embed.add_field(name="Silver 1 ", value="150 Points", inline=True)
        embed.add_field(name="Gold Nova 1", value="1150 Points", inline=True)
        embed.add_field(name="Master Guardian Elite", value="3150 Points", inline=True)
        embed.add_field(name="Silver 2", value="250 Points", inline=True)
        embed.add_field(name="Gold Nova 2", value="1350 Points", inline=True)
        embed.add_field(name="Distinguished Master Guardian", value="3750 Points", inline=True)
        embed.add_field(name="Silver 3", value="450 Points", inline=True)
        embed.add_field(name="Gold Nova 3", value="1550 Points", inline=True)
        embed.add_field(name="Legendary Eagle", value="4500 Points", inline=True)
        embed.add_field(name="Silver 4", value="650 Points", inline=True)
        embed.add_field(name="Gold Nova Master", value="1750 Points", inline=True)
        embed.add_field(name="Legendary Eagle Master ", value="6000 Points", inline=True)
        embed.add_field(name="Silver Elite", value="800 Points", inline=True)
        embed.add_field(name="Master Guardian 1", value="2250 Points", inline=True)
        embed.add_field(name="Supreme Master First Class", value="10000 Points", inline=True)
        embed.add_field(name="Silver Elite Master", value="950 Points", inline=True)
        embed.add_field(name="Master Guardian 2", value="2750 Points", inline=True)
        embed.add_field(name="The Global Elite", value="17500 Points", inline=True)
        await self.bot.say(embed=embed)
        await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True)
    async def apply(self, ctx):
        """
        !admin and !apply implemented as [p]apply
        """
        embed=Embed(title="https://www.baited.xyz/dashboard/dash.php?apply", url="https://www.baited.xyz/dashboard/dash.php?apply", color=0xfffff0)
        embed.set_author(name="Apply for admin here!")
        await self.bot.say(embed=embed)
        await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True)
    async def activity(self, ctx):
        """
        !activity implemnted as [p]activity
        """
        embed=Embed(title="**https://baited.xyz/activity/**", url="https://baited.xyz/activity/", color=0x00e1ff)
        embed.set_author(name="See your activity on")
        await self.bot.say(embed=embed)
        await self.bot.delete_message(ctx.message)

  
    @commands.command(pass_context=True)
    async def appeal(self, ctx):
        """
        !appeal implemented as [p]appeal
        """
        embed=Embed(title="**How to appeal your ban?**", description="- Post your steam profile link\n- Wait for an admin to reply\n- Do NOT tag admins or owners", color=0xfffff0)
        await self.bot.say(embed=embed)
        await self.bot.delete_message(ctx.message)

   
    @commands.command(pass_context=True)
    async def group(self, ctx):
        """
        !group implemented as [p]group
        """
        embed = Embed(title="Steam Community :: Group :: Baited Community", url="http://steamcommunity.com/groups/BaitedCommunity", description="Welcome to Baited Community, the most popular 5v5 community servers in the UK. We boast 1 Gbps Networking on all of our servers and our website guaranteeing a flawless CS:GO experience, we are even branching into America. In our very active Discord, our active admin team are ...", color=0xfdfaff)
        embed.set_thumbnail(url="https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/b0/b0b14a6aa94c4089a5eca3dc7c492522bb3edc61_full.jpg")
        await self.bot.say("http://steamcommunity.com/groups/BaitedCommunity", embed=embed)

    
    @commands.command(pass_context=True)
    async def connect(self, ctx):
        """
        !servers implemented as [p]connect
        """
        embed = Embed(title="Connection Info", color=0xfffff0)

        for i, eu_ip in enumerate(BAITED_SERVERS["eu"]):
            embed.add_field(name=BAITED_SERVERS["meta"]["eu"].format(str(i+1)), value=BAITED_SERVERS["meta"]["ip"].format(eu_ip), inline=True)

        for i, na_ip in enumerate(BAITED_SERVERS["na"]):
            embed.add_field(name=BAITED_SERVERS["meta"]["na"].format(str(i+1)), value=BAITED_SERVERS["meta"]["ip"].format(na_ip), inline=True)
        
        await self.bot.say(embed=embed)
        await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True)
    async def store(self, ctx):
        """
        !vip implemted as [p]store
        """
        embed = Embed(title="https://baited.xyz/", url="https://baited.xyz/", color=0x00e1ff)
        embed.set_author(name="Buy VIP now on")
        await self.bot.say(embed=embed)
        await self.bot.delete_message(ctx.message)
    
    @commands.command(pass_context=True)
    async def unprivate(self, ctx):
        """
        Command on insolence requests sharing a gif on how to unprivate. [p]unprivate
        """
        embed = Embed(title="Unprivating game details", color=0x00e1ff)
        embed.set_image(url="https://s.put.re/ZYs3eYf4.gif")
        await self.bot.say(embed=embed)
        await self.bot.delete_message(ctx.message)

def setup(bot):
    bot.add_cog(baited(bot))  
