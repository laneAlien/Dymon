import sys
import asyncio
import discord
from discord.ext import commands
from openai import OpenAI, OpenAIError
import json
import os
import schedule
import time
from threading import Thread
from keep_alive import keep_alive

keep_alive()

# Загрузка конфигурации из файла config.json
with open('config.json', 'r') as file:
    config = json.load(file)

# Получение токенов из встроенных секретов Replit
DISCORD_TOKEN = os.environ['DISCORD_TOKEN']
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
OPENAI_ORG_ID = os.environ.get('OPENAI_ORG_ID')

# Инициализируем клиент один раз при запуске
openai_client = OpenAI(api_key=OPENAI_API_KEY, organization=OPENAI_ORG_ID)

intents = discord.Intents.all()

# Устанавливаем префиксы
prefixes = [config['prefix']]
bot = commands.Bot(command_prefix=prefixes, intents=intents)

@bot.event
async def on_ready():
    print('Спящий пробудился')

@bot.command(name='ask')
async def gpt_command(ctx: commands.Context, *, args):
    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": args}
            ]
        )
        reply = response.choices[0].message.content
        await ctx.send(embed=discord.Embed(description=reply))
    except OpenAIError as e:
        await ctx.send(f"Ошибка API: {e}")
    except Exception:
        await ctx.send("Произошла ошибка при обработке запроса.")

# Перезапуск процесса через os.execv
def restart_process():
    print("Перезапуск бота...")
    os.execv(sys.executable, ['python'] + sys.argv)

def run_schedule():
    schedule.every(6).minutes.do(restart_process)
    while True:
        schedule.run_pending()
        time.sleep(1)

# Запуск планировщика в отдельном потоке, чтобы не блокировать bot.run
Thread(target=run_schedule, daemon=True).start()

# Запуск бота
bot.run(DISCORD_TOKEN)
