# 🎓 Smart Class Bot

A Telegram bot for managing teacher attendance and notifying students — powered by AI-generated messages via OpenAI.

---

## ✅ Features

| Feature | Description |
|---|---|
| Teacher attendance | `/coming`, `/notcoming`, `/late` commands |
| AI notifications | Auto-generates professional absence/late messages |
| Group broadcast | Sends notifications to all registered student groups |
| Admin panel | Add/remove teachers, view attendance, logs |
| Student portal | Register, view daily status, report issues |
| SQLite database | Zero-config local storage |
| Structured logging | All actions are logged |

---

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.10+
- A Telegram bot token (from [@BotFather](https://t.me/BotFather))
- An OpenAI API key (for AI-generated messages)

### 2. Create your bot on Telegram

1. Open Telegram → search `@BotFather`
2. Send `/newbot` and follow the steps
3. Copy the **bot token** you receive

### 3. Get your Telegram user ID

1. Search `@userinfobot` on Telegram
2. Send `/start` — it will reply with your numeric ID
3. Copy it — this is your `ADMIN_IDS` value

### 4. Clone / unzip the project

```bash
unzip smart-class-bot.zip
cd smart-class-bot-improved
```

### 5. Set up the environment

```bash
cp .env.example .env
```

Edit `.env`:

```env
BOT_TOKEN=your_telegram_bot_token_here
ADMIN_IDS=123456789          # Your Telegram user ID (comma-separate for multiple admins)
OPENAI_API_KEY=sk-...        # Your OpenAI key (get one at platform.openai.com)
```

### 6. Install dependencies

```bash
pip install -r requirements.txt
```

### 7. Run the bot

```bash
python bot.py
```

You should see:
```
INFO - Database initialized.
INFO - Bot starting...
```

Open Telegram, find your bot, and send `/start` ✅

---

## 👤 User Roles

### 🔑 Admin
Must be listed in `ADMIN_IDS` in `.env`.

| Command | Description |
|---|---|
| `/adminhelp` | Show all admin commands |
| `/addteacher <id> <Name> [section]` | Register a teacher |
| `/removeteacher <id>` | Deactivate a teacher |
| `/teachers` | List active teachers |
| `/addgroup <chat_id> [name]` | Register a student group |
| `/groups` | List all groups |
| `/attendance` | Today's attendance summary |
| `/logs` | Recent bot activity |

### 👩‍🏫 Teacher
Must be registered by admin via `/addteacher`.

| Command | Description |
|---|---|
| `/teacherhelp` | Show all teacher commands |
| `/coming` | Mark yourself as present |
| `/notcoming [reason]` | Report absence (notifies all groups via AI message) |
| `/late [minutes]` | Report you'll be late |
| `/mystatus` | View your profile |

### 🎓 Student

| Command | Description |
|---|---|
| `/start` | Welcome message |
| `/register <Full Name>` | Join the notification system |
| `/today` | See today's attendance status |
| `/report <message>` | Report an issue to admin |
| `/help` | Show all commands |

---

## 🏫 Setup Workflow (Step by Step)

```
1. Admin starts bot and runs /addteacher 111222333 "Dr. Ahmed" "Math"
2. Admin runs /addgroup -100123456789 "Year 2 - Group A"
   (Add the bot to the group first, then use that group's chat_id)
3. Teacher opens bot and sends /coming  →  attendance logged
4. Teacher sends /notcoming exam conflict  →  AI message sent to all groups
5. Students in the group receive: "📢 Dr. Ahmed (Math) will not be attending..."
6. Students can check /today to see all updates
```

### How to get a group's chat_id

1. Add your bot to the Telegram group
2. Send any message in the group
3. Visit: `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
4. Find `"chat": {"id": -100XXXXXXXXX}` — that negative number is the chat_id

---

## 📁 Project Structure

```
smart-class-bot/
├── bot.py                  # Entry point
├── config.py               # Environment variables
├── database.py             # SQLite helpers (teachers, students, attendance, logs)
├── ai_service.py           # OpenAI message generation
├── scheduler.py            # APScheduler (for future daily reminders)
├── requirements.txt
├── .env.example
├── handlers/
│   ├── admin.py            # Admin commands
│   ├── teacher.py          # Teacher commands
│   └── student.py          # Student commands
└── utils/
    └── notifications.py    # Group broadcast helper
```

---

## 🔧 Troubleshooting

| Problem | Fix |
|---|---|
| `BOT_TOKEN is not set` | Make sure `.env` exists and has your token |
| `⛔ You are not registered as a teacher` | Admin must run `/addteacher` with your Telegram ID first |
| `⛔ Access denied. Admins only.` | Your ID is not in `ADMIN_IDS` in `.env` |
| Bot doesn't send to group | Make sure the bot is an admin in the group |
| OpenAI error | Check your API key and usage limits at platform.openai.com |

---

## 🔮 Future Enhancements

- [ ] Daily 8 AM reminder for teachers to mark attendance
- [ ] Weekly attendance report PDF export
- [ ] PostgreSQL support for production
- [ ] Docker deployment
- [ ] FastAPI dashboard for web-based admin view
