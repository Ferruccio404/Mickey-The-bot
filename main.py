import discord
from better_profanity import profanity
from discord.ext import commands
import logging
from dotenv import load_dotenv
import random
from datetime import datetime
import os
import webserver
 
load_dotenv()
token = os.getenv('DISCORD_TOKEN')
handler = logging.FileHandler(filename='discord.log', encoding='utf-8',mode='w')
intents = discord.Intents.default()
intents.message_content=True
intents.members=True
bot = commands.Bot(command_prefix='!', intents=intents)
secrole ="Gamer"
puzzles = [
    {
        "question": "What comes once in a minute, twice in a moment, but never in a thousand years?",
        "answer": "m"
    },
    {
        "question": "I speak without a mouth and hear without ears. I have nobody, but I come alive with wind. What am I?",
        "answer": "echo"
    },
    {
        "question": "What has keys but can’t open locks?",
        "answer": "piano"
    },
    {
        "question": "The more of this there is, the less you see. What is it?",
        "answer": "darkness"
    },
    {
        "question": "What can travel around the world while staying in the same corner?",
        "answer": "stamp"
    },
    {
        "question": "What gets wetter the more it dries?",
        "answer": "towel"
    },
    {
        "question": "What has hands but can’t clap?",
        "answer": "clock"
    },
    {
        "question": "I’m tall when I’m young, and I’m short when I’m old. What am I?",
        "answer": "candle"
    },
    {
        "question": "What has one eye, but can’t see?",
        "answer": "needle"
    },
    {
        "question": "What invention lets you look right through a wall?",
        "answer": "window"
    },
    {
        "question": "What has a head, a tail, is brown, and has no legs?",
        "answer": "penny"
    },
    {
        "question": "What building has the most stories?",
        "answer": "library"
    },
    {
        "question": "What has to be broken before you can use it?",
        "answer": "egg"
    },
    {
        "question": "What begins with T, ends with T, and has T in it?",
        "answer": "teapot"
    },
    {
        "question": "What has four wheels and flies?",
        "answer": "garbage truck"
    },
    {
        "question": "Forward I am heavy, but backward I’m not. What am I?",
        "answer": "ton"
    },
    {
        "question": "What comes down but never goes up?",
        "answer": "rain"
    },
    {
        "question": "What can you catch but not throw?",
        "answer": "cold"
    },
    {
        "question": "What has a neck but no head?",
        "answer": "bottle"
    },
    {
        "question": "What kind of band never plays music?",
        "answer": "rubber band"
    },
    {
        "question": "What has many teeth but can’t bite?",
        "answer": "comb"
    },
    {
        "question": "What can fill a room but takes up no space?",
        "answer": "light"
    },
    {
        "question": "What can’t talk but will reply when spoken to?",
        "answer": "echo"
    },
    {
        "question": "What has legs but doesn’t walk?",
        "answer": "table"
    },
    {
        "question": "What runs but never walks, has a bed but never sleeps, and has a mouth but never eats?",
        "answer": "river"
    },
    {
        "question": "What can’t be used until it’s broken?",
        "answer": "egg"
    },
    {
        "question": "What belongs to you, but others use it more than you do?",
        "answer": "your name"
    },
    {
        "question": "What has one head, one foot, and four legs?",
        "answer": "bed"
    },
    {
        "question": "What gets bigger the more you take away from it?",
        "answer": "hole"
    },
    {
        "question": "What goes up but never comes down?",
        "answer": "age"
    },
    {
        "question": "What kind of tree can you carry in your hand?",
        "answer": "palm"
    },
    {
        "question": "What has an eye but cannot see?",
        "answer": "storm"
    },
    {
        "question": "What comes in a minute, twice in a moment, but never in a thousand years?",
        "answer": "m"
    },
    {
        "question": "What is full of holes but still holds water?",
        "answer": "sponge"
    },
    {
        "question": "What has cities, but no houses; forests, but no trees; and rivers, but no water?",
        "answer": "map"
    },
    {
        "question": "What gets sharper the more you use it?",
        "answer": "brain"
    },
    {
        "question": "What begins with an E but only has one letter in it?",
        "answer": "envelope"
    },
    {
        "question": "What can you break, even if you never pick it up or touch it?",
        "answer": "promise"
    },
    {
        "question": "Where does today come before yesterday?",
        "answer": "dictionary"
    },
    {
        "question": "What is always in front of you but can’t be seen?",
        "answer": "future"
    },
    {
        "question": "What has 13 hearts, but no other organs?",
        "answer": "deck of cards"
    },
    {
        "question": "What word is spelled incorrectly in every dictionary?",
        "answer": "incorrectly"
    },
    {
        "question": "What has 88 keys but can’t open a single door?",
        "answer": "piano"
    },
    {
        "question": "What is so fragile that saying its name breaks it?",
        "answer": "silence"
    },
    {
        "question": "What flies without wings?",
        "answer": "time"
    },
    {
        "question": "What can you hold in your right hand, but not in your left?",
        "answer": "your left hand"
    },
    {
        "question": "What can’t be put in a saucepan?",
        "answer": "its lid"
    },
    {
        "question": "What has a thumb and four fingers, but is not alive?",
        "answer": "glove"
    },
    {
        "question": "What has words, but never speaks?",
        "answer": "book"
    },
    {
        "question": "What is easy to lift but hard to throw?",
        "answer": "feather"
    }
]

active_puzzles = {}
@bot.event 
async def on_ready():
    print(f"Hello Sir We are ready to nuke, {bot.user.name}")

@bot.event
async def on_member_join(member):
    await member.send(f"Wellcome to the server Sergant {member.name} ")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    content = message.content.lower()

    # Check if the user has an active puzzle
    if message.author.id in active_puzzles:
        expected_answer = active_puzzles[message.author.id]
        if content == expected_answer:
            await message.channel.send(f"✅ Correct, {message.author.mention}! Well done!")
        else:
            await message.channel.send(f"❌ Incorrect, {message.author.mention}. Try again or use `!puzzle` for a new one.")
        del active_puzzles[message.author.id]
        return

    # Profanity check
    if profanity.contains_profanity(content):
        await message.delete()
        await message.channel.send(f"{message.author.mention} Don't use that word Homie 🧼")
        return

    await bot.process_commands(message)

@bot.command()
async def hello(ctx):
   await ctx.send(f" Hello {ctx.author.mention} Sergant!")

@bot.command()
async def time(ctx):
    current_time = datetime.now().strftime("%H:%M:%S")  # 24-hour format
    await ctx.send(f"Hello {ctx.author.mention}, Sergeant! ⏰ Current time is {current_time}")

@bot.command()
async def commands(ctx):
   await ctx.send("Following commands are available \n 1.Hello \n 2.Time \n 3.Assign \n 4.Remove \n 5.DM \n 6.Reply \n 7.Puzzle")

@bot.command()
async def assign(ctx):
   role=discord.utils.get(ctx.guild.roles, name=secrole)
   if role:
      await ctx.author.add_roles(role)
      await ctx.send(f"{ctx.author.mention} is now assigned {secrole} !")
   else:
      await ctx.send("No role")

@bot.command()
async def remove(ctx):
   role=discord.utils.get(ctx.guild.roles, name=secrole)
   if role:
      await ctx.author.remove_roles(role)
      await ctx.send(f"{ctx.author.mention} Had the {secrole} Role, Now removed !")
   else:
      await ctx.send("No role")

@bot.command()
async def dm(ctx, * , msg):
   await ctx.author.send(f"You said {msg} ")

@bot.command()
async def reply(ctx):
   await ctx.reply("This is a reply you asked for")
   
@bot.command()
async def poll(ctx,*,msg):
   embed=discord.Embed(title="New Poll", description=msg)
   poll_message=await ctx.send(embed=embed)
   await poll_message.add_reaction("👍")
   await poll_message.add_reaction("👎")

@bot.command()
async def puzzle(ctx):
    puzzle = random.choice(puzzles)
    active_puzzles[ctx.author.id] = puzzle["answer"].lower()

    await ctx.send(
        f"🧩 Puzzle for {ctx.author.mention}:\n{puzzle['question']}\n\nType your answer below:"
    )


webserver.keep_alive()
bot.run(token, log_handler=handler, log_level=logging.DEBUG)