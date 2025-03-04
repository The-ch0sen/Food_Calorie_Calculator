import discord
import openai
import os
from dotenv import load_dotenv

# 載入 .env 檔案
load_dotenv()

# 讀取環境變數
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
print(f"讀取的 Discord Token: {TOKEN}")

# 設定 Bot 權限
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # 重要！確保能讀取訊息內容

bot = discord.Client(intents=intents)

# 設定 OpenAI 客戶端（新版 API 必須這樣做）
client = openai.OpenAI(api_key=OPENAI_API_KEY)

def get_calorie_estimation(food_name):
    """向 OpenAI 取得食物熱量估算"""
    prompt = f"請幫我估算以下食物的熱量：{food_name}。請給出大約的數據（每 100 克的熱量）。"

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "你是一位營養專家，請提供準確的熱量估算。"},
            {"role": "user", "content": prompt}
        ]
    )

    # 取得 AI 回應
    return response.choices[0].message.content

@bot.event
async def on_ready():
    print(f'已登入為 {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    user_input = message.content
    calorie_estimate = get_calorie_estimation(user_input)

    await message.channel.send(f"{user_input} 的熱量估算為：\n{calorie_estimate}")

bot.run(TOKEN)
