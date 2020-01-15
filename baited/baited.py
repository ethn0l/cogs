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

BAITED_RULES = [
    {"name":"Rule 1", "value":"Speak only English via voice or text chat to maintain clear channels of communication."},
    {"name":"Rule 2", "value":"Do not Grief, Cheat, Script or Exploit. If found to be in breach of this rule, bans received will be **permanent** and **unappealable**."},
    {"name":"Rule 3", "value":"Do not impersonate any players or baited Staff."},
    {"name":"Rule 4", "value":"No alternative accounts on Baited.\n\n **NOTE: In a rising trend on our servers, alternative accounts are frequently being used to throw, cheat, or evade previous bans, therefore, if caught using an alternative account, it will be permanently banned from the servers. Bans for this do not carry across accounts. Accounts with VAC / Game Bans received over 365 days ago are exempt from this rule.**"},
    {"name":"Rule 5", "value":"Do not abuse !calladmin. The feature is pivotal for moderating the servers and abuse of the system is dealt with promtly and bans will not be overturned."},
    {"name":"Rule 6", "value":"Advertisements of any kind are forbidden. Soliciting the sales of services (hacks, boosting, etc.), linking players to external sites (gambling, free skins etc), or the promotion of servers other than Baited.xyz is strictly prohibited."},
    {"name":"Rule 7", "value":"Treat other players with respect. Instances of malicious racism, sexism or homophobia are frowned upon and when found to be in breach of this rule, bans will progressively increase with each cumulative offence."},
    {"name":"Rule 8", "value":"Do not disrupt the server in any way. Acts of disruption can include, but are not limited to:\n\n - Mic/Chat spam\n - Trolling\n - Team flashing \n - Blocking\n - Ghosting\n - Shooting allies to reveal their position"}
]

BAITED_RANKS = [
    {"name":"Silver 1", "value":"150 Points", "key":"s1"},
    {"name":"Gold Nova 1", "value":"1150 Points", "key":"gn1"},
    {"name":"Master Guardian Elite", "value":"3150 Points", "key":"mge"},
    {"name":"Silver 2", "value":"250 Points", "key":"s2"},
    {"name":"Gold Nova 2", "value":"1350 Points", "key":"gn2"},
    {"name":"Distinguished Master Guardian", "value":"3750 Points", "key":"dmg"},
    {"name":"Silver 3", "value":"450 Points", "key":"s3"},
    {"name":"Gold Nova 3", "value":"1550 Points", "key":"gn3"},
    {"name":"Legendary Eagle", "value":"4500 Points", "key":"le"},
    {"name":"Silver 4", "value":"650 Points", "key":"s4"},
    {"name":"Gold Nova Master", "value":"1750 Points", "key":"gnm"},
    {"name":"Legendary Eagle Master", "value":"6000 Points", "key":"lem"},
    {"name":"Silver Elite", "value":"800 Points", "key":"se"},
    {"name":"Master Guardian 1", "value":"2250 Points", "key":"mg1"},
    {"name":"Supreme Master First Class", "value":"10000 Points", "key":"smfc"},
    {"name":"Silver Elite Master", "value":"950 Points", "key":"sem"},
    {"name":"Master Guardian 2", "value":"2750 Points", "key":"mg2"},
    {"name":"The Global Elite", "value":"17500 Points", "key":"ge"}
]

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
        !rules implemented as [p]rules. Takes [Rule Number] as an argument.
        """
        embed = Embed(title="**RULES**", color=0xfffff0)

        # Check if a specific rule was been chosen
        args = ctx.message.content.split(" ")
        rule_n = 0

        for arg in args:
            if arg.isnumeric() and len(arg) == 1:
                rule_n = int(arg)
                break
            else:
                continue

        if rule_n in range(1, 9):
            embed.add_field(name=BAITED_RULES[rule_n - 1]["name"], value=BAITED_RULES[rule_n - 1]["value"], inline=False)
            embed.title = "**RULE {}**".format(str(rule_n))
        else:
            for rule in BAITED_RULES:
                embed.add_field(name=rule["name"], value=rule["value"], inline=False)

        await self.bot.say(embed=embed)
        await self.bot.delete_message(ctx.message)
    
    @commands.command(pass_context=True)
    async def rank(self, ctx):
        """
        !rank implemented as [p]rank. Takes argument [rank key]/[rank name] to get one rank returned.
        """
        embed = Embed(title="**https://baited.xyz/rankme**", url="https://baited.xyz/rankme", description="or https://baited.xyz/rankmena for na rankings.", color=0xfffff0)
        
        # Check if a specific rank was been chosen
        args = ctx.message.content.split(" ")
        rank_x = False

        for arg in args:
            if arg in [x["key"] for x in BAITED_RANKS]:
                rank_x = True
                rank = [rank for rank in BAITED_RANKS if rank["key"] == arg][0]
                embed.add_field(name=rank["name"], value=rank["value"], inline=True)
        
        if len(args) >= 2 and not rank_x:
            arg = " ".join(args[1:]).lower()

            if arg in [name["name"].lower() for name in BAITED_RANKS]:
                rank_x = True
                rank = [rank for rank in BAITED_RANKS if rank["name"].lower() == arg][0]
                embed.add_field(name=rank["name"], value=rank["value"], inline=True)

        if not rank_x:
            for rank in BAITED_RANKS:
                embed.add_field(name=rank["name"], value=rank["value"], inline=True)

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
        !servers implemented as [p]connect. Takes 2 arguments [server number] and [server region] the latter is optional.
        """
        embed = Embed(title="No server selected showing connection info :wave~1:", color=0xfffff0)

        args = ctx.message.content.split(" ")[1:]

        valid_numbers_eu = range(1, len(BAITED_SERVERS["eu"]) + 1)
        valid_numbers_na = range(1, len(BAITED_SERVERS["na"]) + 1)
        server_number = 0
        server_region = "na" if "na" in args else "eu"

        for arg in args:
            if arg.isnumeric():
                if int(arg) in (valid_numbers_na if server_region == "na" else valid_numbers_eu):
                    server_number = int(arg)

        if not server_number:
            for i, eu_ip in enumerate(BAITED_SERVERS["eu"]):
                embed.add_field(name=BAITED_SERVERS["meta"]["eu"].format(str(i+1)), value=eu_ip, inline=True)

            for i, na_ip in enumerate(BAITED_SERVERS["na"]):
                embed.add_field(name=BAITED_SERVERS["meta"]["na"].format(str(i+1)), value=na_ip, inline=True)
        
        else:
            server_ip = BAITED_SERVERS[server_region][server_number - 1]
            server_name = BAITED_SERVERS["meta"][server_region].format(str(server_number))
            ip_con = BAITED_SERVERS["meta"]["ip"].format(server_ip)
            embed.title = "{}\n({})".format(server_name, ip_con)
        
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
