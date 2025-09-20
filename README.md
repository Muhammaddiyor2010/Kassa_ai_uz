# 🤖 Kassa AI Bot

Telegram bot for managing income and expenses with AI-powered voice and text processing.

## ✨ Features

- 🎤 **Voice Processing**: Send voice messages to record expenses/income
- ✍️ **Text Processing**: Type messages to record transactions
- 📊 **Reports**: View detailed financial reports
- 🔐 **User Management**: Separate data for each user
- 🤖 **AI Integration**: Powered by Google Gemini AI
- 📱 **Easy to Use**: Simple and intuitive interface

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Telegram Bot Token
- Google Gemini API Key

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Muhammaddiyor2010/Kassa_ai_uz.git
cd Kassa_ai_uz
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements/base.txt
```

4. **Configure environment variables**
```bash
# Copy environment template
cp .env.dist .env

# Edit .env file with your actual tokens
# BOT_TOKEN=your_telegram_bot_token
# GEMINI_API_KEY=your_gemini_api_key
```

5. **Run the bot**
```bash
python bot.py
```

## 📋 Commands

- `/start` - Start the bot
- `/help` - Show help information

## 🎯 Usage

### Voice Messages
1. Press the microphone button
2. Say your transaction: "I spent 50000 som on food"
3. Bot will process and save the transaction
4. View your report

### Text Messages
1. Type your transaction: "I earned 500000 som from work"
2. Bot will process and save the transaction
3. View your report

## 📊 Categories

### Expenses (Chiqim)
- ovqat (food)
- kiyim (clothing)
- mashina (car)
- ta'lim (education)

### Income (Kirim)
- ish (work)
- savdo (sales)
- investitsiya (investment)
- boshqa (other)

## 🛠️ Configuration

### Environment Variables

Copy `.env.dist` to `.env` and fill in your actual tokens:

```bash
cp .env.dist .env
```

Then edit `.env` file with your actual values:

```env
BOT_TOKEN=your_telegram_bot_token
GEMINI_API_KEY=your_gemini_api_key
```

### Database

The bot uses SQLite database (`main.db`) to store:
- User information
- Income transactions
- Expense transactions

## 📁 Project Structure

```
kassa_ai_uz/
├── bot.py                 # Main bot file
├── loader.py              # Bot and database loader
├── config/                # Configuration files
├── handlers/              # Message handlers
│   ├── start.py          # Start and help commands
│   ├── chiqim.py         # Expense processing
│   ├── kirim.py          # Income processing
│   └── report.py         # Report generation
├── keyboards/             # Keyboard layouts
├── states/                # User states
├── tables/                # Database operations
├── utils/                 # Utilities (AI integration)
├── requirements/          # Dependencies
└── .env                   # Environment variables
```

## 🔧 Development

### Adding New Features

1. Create new handlers in `handlers/` directory
2. Add new states in `states/` directory
3. Update database schema in `tables/sqlite.py`
4. Test with your bot token

### Database Schema

#### Users Table
- id (PRIMARY KEY)
- Name
- language
- phone
- kirim
- chiqim

#### Chiqim Table (Expenses)
- id (PRIMARY KEY)
- summa
- izoh
- kategoriya
- user_id

#### Kirim Table (Income)
- id (PRIMARY KEY)
- summa
- izoh
- kategoriya
- user_id

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 Support

If you have any questions or need help, please contact:
- GitHub Issues: [Create an issue](https://github.com/Muhammaddiyor2010/Kassa_ai_uz/issues)
- Telegram: @Kassa_aiuz_bot

## 🙏 Acknowledgments

- [Aiogram](https://github.com/aiogram/aiogram) - Telegram Bot Framework
- [Google Gemini](https://ai.google.dev/) - AI Processing
- [SQLite](https://www.sqlite.org/) - Database

---

Made with ❤️ by [Muhammaddiyor2010](https://github.com/Muhammaddiyor2010)