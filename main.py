# -------------- import --------------

import nextcord
from nextcord.ext import commands
import json
from datetime import datetime
import requests
from time import sleep

# -------------- config or setting --------------

config = json.load(open('config.json'))

token = config['token']

host = config['rbx-host']
port = config['rbx-port']
webpass = config['rbx-webpass']
timeout = config['time-out']

# -------------- bot setting --------------

embedtextfooter = "[ bot by nyaouu#2917 ]"
embedtitle = "Nao"
embediconurl = "https://media.discordapp.net/attachments/1033775510909620227/1033797043275178045/super.jpg?width=688&height=683"

intents = nextcord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!",help_command=None,intents=intents)

# -------------- function --------------

class Launch(nextcord.ui.Modal):
    def __init__(self):
        super().__init__("Launch")
        self.username = nextcord.ui.TextInput(
            label = "Username",
            placeholder = "Enter your username",
            style = nextcord.TextInputStyle.short,
            required = True
        )
        self.placeid = nextcord.ui.TextInput(
            label = "Place Id",
            placeholder = "Enter your placeid",
            style = nextcord.TextInputStyle.short,
            required = True
        )
        self.jobid = nextcord.ui.TextInput(
            label = "Job Id",
            placeholder = "Enter your jobid",
            style = nextcord.TextInputStyle.short,
            required = False
        )
        self.add_item(self.username)
        self.add_item(self.placeid)
        self.add_item(self.jobid)

    async def callback(self, interaction: nextcord.Interaction):
        username = self.username.value
        placeid = self.placeid.value
        jobid = self.jobid.value

        usernamerbxlist = []

        for usernamerbx in requests.get(f"http://{host}:{port}/GetAccounts?Password={webpass}").text.split(','):
            usernamerbx = usernamerbx.strip()
            usernamerbxlist.append(usernamerbx)

        embed = nextcord.Embed(title = embedtitle, description = f'User | <@{interaction.user.id}>\n```fix\n- Checking\n```', color = 16776960, timestamp = datetime.now())
        embed.set_footer(text = str(embedtextfooter), icon_url= embediconurl)
        await interaction.send(embed=embed, ephemeral=True)

        r = requests.get(f'https://api.roblox.com/users/get-by-username?username={username}')
        if "Username" in r.json():
            if username in usernamerbxlist:
                userid = r.json()['Id']
                on = requests.get(f'https://api.roblox.com/users/{userid}/onlinestatus/')
                if on.json()['IsOnline'] == True:
                    embed = nextcord.Embed(title = embedtitle, description = f'User | <@{interaction.user.id}>\n```diff\n+ Username is online\n```', color = 0x2ecc71, timestamp = datetime.now())
                    embed.set_footer(text = str(embedtextfooter), icon_url= embediconurl)
                    await interaction.edit_original_message(embed=embed)
                elif on.json()['IsOnline'] == False:
                    requests.get(f"http://{host}:{port}/LaunchAccount?Account={username}&PlaceId={placeid}&Password={webpass}&JobId={jobid}")
                    embed = nextcord.Embed(title = embedtitle, description = f'User | <@{interaction.user.id}>\n```fix\n- Launching\n```', color = 16776960, timestamp = datetime.now())
                    embed.set_footer(text = str(embedtextfooter), icon_url= embediconurl)
                    await interaction.edit_original_message(embed=embed)
                    sleep(int(timeout))
                    onnow = requests.get(f'https://api.roblox.com/users/{userid}/onlinestatus/')
                    if onnow.json()['IsOnline'] == True:
                        embed = nextcord.Embed(title = embedtitle, description = f'User | <@{interaction.user.id}>\n```diff\n+ Launch Success\n```', color = 0x2ecc71, timestamp = datetime.now())
                        embed.set_footer(text = str(embedtextfooter), icon_url= embediconurl)
                        await interaction.edit_original_message(embed=embed)
                    else :
                        embed = nextcord.Embed(title = embedtitle, description = f'User | <@{interaction.user.id}>\n```fix\n- Launch Timeout\n```', color = 16776960, timestamp = datetime.now())
                        embed.set_footer(text = str(embedtextfooter), icon_url= embediconurl)
                        await interaction.edit_original_message(embed=embed)
            else:
                embed = nextcord.Embed(title = embedtitle, description = f'User | <@{interaction.user.id}>\n```diff\n- Username not found in Roblox Account Manager\n```', color = 0xe74c3c, timestamp = datetime.now())
                embed.set_footer(text = str(embedtextfooter), icon_url= embediconurl)
                await interaction.edit_original_message(embed = embed)
        else:
            embed = nextcord.Embed(title = embedtitle, description = f'User | <@{interaction.user.id}>\n```diff\n- Username not found in roblox\n```', color = 0xe74c3c, timestamp = datetime.now())
            embed.set_footer(text = str(embedtextfooter), icon_url= embediconurl)
            await interaction.edit_original_message(embed = embed)

class LaunchAll(nextcord.ui.Modal):
    def __init__(self):
        super().__init__("Launch All")
        self.placeid = nextcord.ui.TextInput(
            label = "Place Id",
            placeholder = "Enter your placeid",
            style = nextcord.TextInputStyle.short,
            required = True
        )
        self.jobid = nextcord.ui.TextInput(
            label = "Job Id",
            placeholder = "Enter your jobid",
            style = nextcord.TextInputStyle.short,
            required = False
        )
        self.add_item(self.placeid)
        self.add_item(self.jobid)

    async def callback(self, interaction: nextcord.Interaction):
        placeid = self.placeid.value
        jobid = self.jobid.value

        usernamerbxlist = []
        usernametextlist = []

        for usernamerbx in requests.get(f"http://{host}:{port}/GetAccounts?Password={webpass}").text.split(','):
            usernamerbx = usernamerbx.strip()
            usernamerbxlist.append(usernamerbx)

        for usernametext in open('account.txt'):
            usernametext = usernametext.strip()
            usernametextlist.append(usernametext)

        embed = nextcord.Embed(title = embedtitle, description = f'User | <@{interaction.user.id}>\n```fix\n- Checking\n```', color = 16776960, timestamp = datetime.now())
        embed.set_footer(text = str(embedtextfooter), icon_url= embediconurl)
        await interaction.send(embed=embed, ephemeral=True)

        for username in usernametextlist:
            r = requests.get(f'https://api.roblox.com/users/get-by-username?username={username}')
            if "Username" in r.json():
                if username in usernamerbxlist:
                    userid = r.json()['Id']
                    on = requests.get(f'https://api.roblox.com/users/{userid}/onlinestatus/')
                    if on.json()['IsOnline'] == True:
                        embed = nextcord.Embed(title = embedtitle, description = f'User | <@{interaction.user.id}>\n```diff\n+ {username} | Username is online\n```', color = 0x2ecc71, timestamp = datetime.now())
                        embed.set_footer(text = str(embedtextfooter), icon_url= embediconurl)
                        await interaction.edit_original_message(embed=embed)
                    elif on.json()['IsOnline'] == False:
                        requests.get(f"http://{host}:{port}/LaunchAccount?Account={username}&PlaceId={placeid}&Password={webpass}&JobId={jobid}")
                        embed = nextcord.Embed(title = embedtitle, description = f'User | <@{interaction.user.id}>\n```fix\n- {username} | Launching\n```', color = 16776960, timestamp = datetime.now())
                        embed.set_footer(text = str(embedtextfooter), icon_url= embediconurl)
                        await interaction.edit_original_message(embed=embed)
                        sleep(int(timeout))
                        onnow = requests.get(f'https://api.roblox.com/users/{userid}/onlinestatus/')
                        if onnow.json()['IsOnline'] == True:
                            embed = nextcord.Embed(title = embedtitle, description = f'User | <@{interaction.user.id}>\n```diff\n+ {username} | Launch Success\n```', color = 0x2ecc71, timestamp = datetime.now())
                            embed.set_footer(text = str(embedtextfooter), icon_url= embediconurl)
                            await interaction.edit_original_message(embed=embed)
                        else :
                            embed = nextcord.Embed(title = embedtitle, description = f'User | <@{interaction.user.id}>\n```fix\n- {username} | Launch Timeout\n```', color = 16776960, timestamp = datetime.now())
                            embed.set_footer(text = str(embedtextfooter), icon_url= embediconurl)
                            await interaction.edit_original_message(embed=embed)
                else:
                    embed = nextcord.Embed(title = embedtitle, description = f'User | <@{interaction.user.id}>\n```diff\n- {username} | Username not found in Roblox Account Manager\n```', color = 0xe74c3c, timestamp = datetime.now())
                    embed.set_footer(text = str(embedtextfooter), icon_url= embediconurl)
                    await interaction.edit_original_message(embed = embed)
            else:
                embed = nextcord.Embed(title = embedtitle, description = f'User | <@{interaction.user.id}>\n```diff\n- {username} | Username not found in roblox\n```', color = 0xe74c3c, timestamp = datetime.now())
                embed.set_footer(text = str(embedtextfooter), icon_url= embediconurl)
                await interaction.edit_original_message(embed = embed)

class Button(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(label="Launch", style=nextcord.ButtonStyle.green, custom_id="launch")
    async def Launch(self, button: nextcord.Button, interaction: nextcord.Interaction):
        if interaction.user.guild_permissions.administrator:
            await interaction.response.send_modal(Launch())
        else:
            embed = nextcord.Embed(title = embedtitle, description = f"User | <@{interaction.user.id}>\n```diff\n- Don't Have Permission\n```", color = 0xe74c3c, timestamp = datetime.now())
            embed.set_footer(text = str(embedtextfooter), icon_url= embediconurl)
            await interaction.send(embed=embed, ephemeral=True)

    @nextcord.ui.button(label="Launch All", style=nextcord.ButtonStyle.green, custom_id="launch-all")
    async def LaunchAll(self, button: nextcord.Button, interaction: nextcord.Interaction):
        if interaction.user.guild_permissions.administrator:
            await interaction.response.send_modal(LaunchAll())
        else:
            embed = nextcord.Embed(title = embedtitle, description = f"User | <@{interaction.user.id}>\n```diff\n- Don't Have Permission\n```", color = 0xe74c3c, timestamp = datetime.now())
            embed.set_footer(text = str(embedtextfooter), icon_url= embediconurl)
            await interaction.send(embed=embed, ephemeral=True)

# -------------- bot --------------

@bot.event
async def on_ready():
    bot.add_view(Button())
    print(f"Login as : {bot.user}")
    await bot.change_presence(activity = nextcord.Streaming(name="nyaouu#2917",url="https://www.twitch.tv/twitch"))

@bot.command(pass_context = True)
async def setup(ctx):
    if ctx.author.guild_permissions.administrator:
        await ctx.message.delete()
        embed = nextcord.Embed(title = f"{embedtitle} | Roblox",color = 0x2ecc71, description="", timestamp=datetime.now())
        embed.set_image(url = "https://media.discordapp.net/attachments/1033775510909620227/1033788231151525970/5786fa2b5b25a36e.png?width=832&height=468")
        embed.set_footer(text = str(embedtextfooter), icon_url = embediconurl)
        await ctx.send(embed = embed, view = Button())
    else:
        pass

# -------------- run bot --------------

bot.run(token)