# 🍽️ AI 食物熱量估算機器人（Discord Bot）

這是一個基於 **Discord + OpenAI Vision API** 的機器人，能夠：
- 📷 **辨識食物圖片**，透過 **GPT-4 Turbo Vision** 分析食物名稱
- 🔍 **根據食物名稱估算熱量**（每 100 克的卡路里值）
- 📊 **支援多種食物辨識**，一次回應多個食物的熱量資訊
- 🛠️ **無需 Google Vision API**，全程使用 **OpenAI Vision API**

---

## 🚀 **安裝步驟**

### 1️⃣ **設定 Discord Bot**
1. 前往 **[Discord Developer Portal](https://discord.com/developers/applications)** 並創建一個 **新應用程式**。
2. 在 **Bot 分頁**，點擊「Add Bot」來建立機器人。
3. 取得 **Bot Token**（這個 Token 之後要用來與 Discord 進行 API 通訊）。
4. 在 **OAuth2 → URL Generator**，選擇 `bot` 和 `applications.commands` 權限。
5. 在 **Bot 權限** 中，勾選：
   - `Read Messages`
   - `Send Messages`
   - `Attach Files`
   - `Read Message History`
6. **複製產生的邀請連結**，將機器人加入你的 **Discord 伺服器**。

---

### 2️⃣ **設定 OpenAI API**
1. **註冊 OpenAI 帳戶**：[點此註冊](https://platform.openai.com/signup/)
2. **產生 API Key**：[前往 API Key 頁面](https://platform.openai.com/account/api-keys)
3. **複製 API Key**，這將用於 `.env` 檔案設定

---

### 3️⃣ **運行機器人**
1. **在專案目錄執行**：python AI_Food_Calorie_Calculator.py
2. **在後台執行：**：nohup python AI_Food_Calorie_Calculator.py &


### 4️⃣ **功能與使用方式**
1. **📷 上傳食物圖片**：
   - 在 Discord 頻道中，上傳一張食物的圖片
   - 使用 GPT-4 Turbo Vision 辨識圖片中的食物
   - 取得食物名稱，並估算其熱量
   - 回應結果
2. **直接輸入食物名稱**：

### 5️⃣ **技術架構**
1. **Discord Bot**：接收使用者訊息與圖片
2. **OpenAI GPT-4 Turbo Vision**：解析食物圖片，辨識食物名稱
3. **OpenAI GPT-3.5 Turbo**：透過語言模型提供熱量估算
4. **requests**：處理 Discord 上傳的圖片



