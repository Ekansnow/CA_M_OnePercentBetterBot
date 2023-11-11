import nextcord, random
from nextcord.ext import commands
import pandas as pd
from datetime import datetime as dt

intents = nextcord.Intents.default()
intents.message_content = True

bot = nextcord.Client(intents=intents)

"""Tells that Bot is up and running"""


@bot.event
async def on_ready():
    print("Bot is ready!")


"""Extract data from excel sheet"""


def todays_data_from_excel():
    file = "computer words.xlsx"
    sheet1 = pd.read_excel(file, sheet_name=0, index_col=None, header=None)
    sheet2 = pd.read_excel(file, sheet_name=1, index_col=None)

    """This is done to get particular row for a particular day"""
    todays_row_beginner = (
        dt.strptime(str(dt.now())[:10], "%Y-%m-%d")
        - dt.strptime("2023-01-01", "%Y-%m-%d")
    ).days

    """This is done to get particular row amongst 214 Bonus words for a particular day
    Remember using seed fixed the result random function generates"""
    random.seed(sheet1.loc[todays_row_beginner][2])
    todays_row_intermediate = random.randint(0, 214)
    return sheet1.loc[todays_row_beginner], sheet2.loc[todays_row_intermediate]


"""Get word in magic/hidden form"""


def magic_word_hidden(x):
    magic_word = []
    for i in x:
        if i in ["a", "e", "i", "o", "u"]:
            magic_word.append(i)
            magic_word.append(" ")
        else:
            magic_word.append("—")
            magic_word.append(" ")
    return "".join(magic_word)


"""What to do when Reveal button is clicked"""


async def level_one(interaction, sheet1_row, sheet2_row):
    # Do something when the button is clicked

    newEmbed = nextcord.Embed(
        title="One Percent Better Everyday",
        description="Today's magic tech word is....🪄💫\n😁",
        color=nextcord.Colour.dark_blue(),
    )
    newEmbed.set_thumbnail(
        url="https://s3-ap-southeast-1.amazonaws.com/ghost-production-blog/2023/03/Scaler_Logo_WhiteBG.jpg"
    )

    newEmbed.add_field(
        name=f"**{sheet1_row[0]}**",
        value=f"{sheet1_row[1]}\n\n_Challenge What's Possible 🚀_",
        inline=False,
    )
    """Some day bonus word will be displayed other days, it won't be, as intended"""
    random.seed(sheet1_row[2])
    if random.choice(("", "1")):
        newEmbed.add_field(
            name=f"\n\nBonus Word....💎\n\n**{sheet2_row[0]}**",
            value=f"\n\n{sheet2_row[1]}\n\n_See you tomorrow ❤️_",
            inline=False,
        )

    # embed updated
    await interaction.edit(embed=newEmbed , view = None)


class Menu(nextcord.ui.View):
    def __init__(self, sheet1_row, sheet2_row):
        super().__init__()
        self.value = None
        self.sheet1_row = sheet1_row
        self.sheet2_row = sheet2_row

    """Place reveal button which calls level_one function when clicked"""

    @nextcord.ui.button(
        label="Reveal", emoji="👐", style=nextcord.ButtonStyle.blurple)
    async def menu1(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        # await interaction.response.send_message("Check your DM", ephemeral=True)
        await level_one(interaction, self.sheet1_row, self.sheet2_row)


@bot.event
async def on_message(msg):
    if msg.content.lower() == "onepercentbetter":
        # await msg.channel.send("Let's Begin!")
        # Get row details for that day from both the sheets in a workbook
        sheet1_row, sheet2_row = todays_data_from_excel()

        # Get magic/hidden word
        todays_word_hidden = magic_word_hidden(sheet1_row[0])

        # Get hint that describes magic word
        todays_word_hint = sheet1_row[1].split(": ")[1]

        MyEmbed = nextcord.Embed(
            title="One Percent Better Everyday",
            description="Today's magic tech word is....🪄💫\n😈",
            color=nextcord.Colour.dark_blue(),
        )

        MyEmbed.set_thumbnail(
            url="https://s3-ap-southeast-1.amazonaws.com/ghost-production-blog/2023/03/Scaler_Logo_WhiteBG.jpg"
        )
        MyEmbed.add_field(
            name=f"**{todays_word_hidden}**",
            value=f"**{todays_word_hint}**\n\nAre you thinking what I am thinking? 💭",
            inline=False,
        )

        view = Menu(sheet1_row, sheet2_row)


        # to avoid other community members from accessing the game chat we use dm channel
        await msg.author.send(embed=MyEmbed, view=view)



bot.run("MTE2MzM3ODY5MzIzODk1NjAzMg.Bot Token")
