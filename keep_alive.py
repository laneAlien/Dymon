from flask import Flask, render_template 
from threading import Thread 
import os
import schedule
import time
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
  return "Я снова живу"

def run():
  app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

def keep_alive():
  t = Thread(target=run)
  t.start()

def restart_bot():
  print("Перезапуск бота...")
  os._exit(0)

if __name__ == '__main__':
  keep_alive()

  # Запуск перезапуска бота каждые 1 минут
  schedule.every(5).minutes.do(restart_bot)

  while True:
    schedule.run_pending()
    time.sleep(5)