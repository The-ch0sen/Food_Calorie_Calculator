import discord
import openai
import os
import requests
from dotenv import load_dotenv
from google.cloud import vision
import io

# 載入 .env 檔案
load_dotenv()

# 讀取環境變數
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

print(f"讀取的 Discord Token: {TOKEN}")

# 設定 Bot 權限
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # 重要，確保能讀取訊息內容
intents.guilds = True
intents.typing = False
intents.presences = False

bot = discord.Client(intents=intents)

# 設定 OpenAI API
client = openai.Client(api_key=OPENAI_API_KEY)



def analyze_food_image(image_url):
    """使用 OpenAI Vision API 分析圖片內容，並回傳主要食物名稱"""
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "你是一位食物辨識專家。請仔細分析圖片，並且只列出主要的食物名稱。不要提供詳細描述。"},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "請列出圖片中所有的食物名稱，每個食物名稱用逗號分隔，例如：'炒飯, 牛肉麵, 涼拌黃瓜'"},
                    {"type": "image_url", "image_url": {"url": image_url}}
                ]
            }
        ]
    )

    # 取得 AI 回傳的純食物名稱
    food_names = response.choices[0].message.content.strip()

    # 確保 AI 只回傳主要的食物名稱
    return [food.strip() for food in food_names.split(",") if food.strip()]

def get_calorie_estimation(food_name):
    """向 OpenAI 取得食物熱量估算"""
    prompt = f"請幫我估算以下食物的熱量：{food_name}。請給出大約的數據（每 100 克的熱量）。"

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

@bot.event
async def on_ready():
    print(f'已登入為 {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.attachments:
        image_url = message.attachments[0].url  # 取得圖片網址
        await message.channel.send("📷 正在分析圖片，請稍候...")

        try:
            # 讓 OpenAI Vision API 辨識圖片
            food_names = analyze_food_image(image_url)

            if not food_names:
                await message.channel.send("⚠️ 無法辨識圖片中的食物，請確認圖片清晰，並且是食物圖片！")
                return

            await message.channel.send(f"🔍 我辨識到這些食物：**{', '.join(food_names)}**")

            # 逐一查詢每種食物的熱量
            for food in food_names:
                calorie_estimate = get_calorie_estimation(food)
                await message.channel.send(f"🍽 **{food}** 的熱量估算為：\n{calorie_estimate}")

        except Exception as e:
            await message.channel.send("⚠️ 無法分析圖片，請確認圖片清晰，並且是食物圖片！")
            print(e)

    else:
        # 如果是文字，則直接查詢熱量
        user_input = message.content.strip()

        # 確保使用者輸入不是空白
        if len(user_input) == 0:
            return

        calorie_estimate = get_calorie_estimation(user_input)
        await message.channel.send(f"{user_input} 的熱量估算為：\n{calorie_estimate}")

bot.run(TOKEN)
