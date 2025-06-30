import discord
from discord.ext import commands
import openai
import json
import os
import schedule
import time
from keep_alive import keep_alive

keep_alive()

# Загрузка конфигурации из файла config.json
with open('config.json', 'r') as file:
    config = json.load(file)

# Получение токенов из встроенных секретов Replit
DISCORD_TOKEN = os.environ['DISCORD_TOKEN']
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
OPENAI_ORG_ID = os.environ['OPENAI_ORG_ID']

intents = discord.Intents.all()

# Устанавливаем префиксы
prefixes = [config['prefix']]
bot = commands.Bot(command_prefix=prefixes, intents=intents)

@bot.event
async def on_ready():
    print('Спящий пробудился')

@bot.command(name='/')
async def gpt_command(ctx: commands.Context, *, args):
    openai.api_key = OPENAI_API_KEY
    openai.organization = OPENAI_ORG_ID

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": args}
        ]
    )

    await ctx.send(embed=discord.Embed(description=response['choices'][0]['message']['content']))

# Расписание для перезапуска каждые 1 минут
def job():
    print("Перезапуск через 6 минут")
    os.execv(sys.executable, ['python'] + sys.argv)

# Запуск задачи каждые 1 минут
schedule.every(6).minutes.do(job)

  
# Запуск бота
bot.run(DISCORD_TOKEN)
