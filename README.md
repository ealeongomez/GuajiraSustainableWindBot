# 🌬️ ChatBot for Sustainable Energy Planning through Wind Forecasting in La Guajira

**Explainable Deep Learning ChatBot for Wind Speed Forecasting and Sustainable Energy Planning in La Guajira, Colombia.**

Advanced wind forecasting system powered by AI and conversational chatbots. The project integrates climate data from multiple sources to provide accurate and accessible predictions through both console and Telegram interfaces, with full conversation persistence and context management.


## 📂 Project Structure  

```bash
GuajiraSustainableWindBot/
│── docs/       # Technical documentation, manuals, and user guides
│── examples/   # Example implementations and use cases
│── infra/      # Infrastructure scripts (deployment, Docker, CI/CD, AWS/Azure configs)
│── models/     # Deep learning and explainability models (trained and under development)
│── src/        # Main source code of the ChatBot
│   ├── data_ingestion/   # Data API and ingestion modules
│   └── prompt_template/  # LLM prompt templates (windbot_prompt.txt, etc.)
│── test/       # Unit and integration tests
│   ├── chatbot/    # Chatbot tests (console, Telegram prototypes)
│   └── smoke/      # Smoke tests for data and models
│── .env        # Environment variables (Snowflake, APIs, OpenAI, etc.)
│── .gitignore  # Files and folders ignored by Git
│── README.md   # This file
```

## ✨ Main Features

### 🤖 Conversational AI
- **Intelligent Chatbot**: Multi-platform chatbot (Console + Telegram) using LangChain and OpenAI
- **Context-Aware**: Maintains conversation history with automatic loading of last 10 interactions
- **User-Specific Memory**: Each user has isolated, persistent conversation history
- **Natural Language**: Understands and responds in Spanish about wind predictions

### 💾 Data Persistence
- **MongoDB Integration**: All conversations stored with unique IDs (UUID)
- **Cloud-Ready**: MongoDB Atlas support for scalable storage
- **Conversation Search**: Advanced filtering by user, date, and content
- **Analytics Ready**: Query and analyze conversation patterns

### 📊 Monitoring & Tracing
- **LangSmith Integration**: Full tracing of LLM interactions
- **Performance Metrics**: Track response times, tokens, and user engagement
- **Debug Support**: Comprehensive logging and error tracking

### 🌐 Wind Prediction (In Development)
- **Machine Learning Models**: LSTM-based models for wind speed forecasting
- **Multi-Source Data**: Integration with Open-Meteo and other climate APIs
- **13 Municipalities**: Coverage of all La Guajira municipalities

## 🚀 Installation

### 1. Clone the repository:
```bash
git clone <repository-url>
cd GuajiraSustainableWindBot
```

### 2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies:
```bash
pip install -r requirements.txt
```

**Required packages:**
- `langchain` - LLM framework
- `langchain-openai` - OpenAI integration
- `langsmith` - Tracing and monitoring
- `python-telegram-bot` - Telegram bot API
- `pymongo` - MongoDB driver
- `python-dotenv` - Environment management
- `colorama` - Console colors (for console chatbot)

### 4. Configure environment variables:

Create a `.env` file with your credentials:

```bash
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Telegram Bot (get from @BotFather)
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here

# LangSmith (optional - for tracing)
LANGCHAIN_API_KEY=your_langsmith_api_key_here
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_PROJECT=GuajiraSustainableWindBot-Telegram

# MongoDB Atlas (optional - for conversation persistence)
MONGODB_URI=mongodb+srv://user:password@cluster.mongodb.net/?retryWrites=true&w=majority
MONGODB_DATABASE=windbot_telegram
```

**Note**: The bot works without MongoDB (conversations stored in RAM only) and without LangSmith (no tracing).

## 💬 Usage

### Test the Chatbots:

#### 🖥️ Console Chatbot (Terminal):

Simple terminal-based chatbot for quick testing.

```bash
cd test/chatbot
python console_chatbot_test.py
```

**Features:**
- 🎨 Colored output with emoticons
- 💬 Interactive conversation loop
- 🧠 Session-based memory (resets on restart)
- ⚡ Fast and lightweight

**Requirements:** Only `OPENAI_API_KEY` in `.env`

#### 📱 Telegram Chatbot (Production-Ready):

Full-featured Telegram bot with persistent memory and advanced features.

```bash
cd test/chatbot
python telegram_chatbot.py
```

**Key Features:**

🤖 **Multi-User Support**
- Isolated conversation context per user
- Unique user identification via Telegram ID
- No cross-contamination of conversations

💾 **Intelligent Persistence**
- MongoDB Atlas cloud storage
- Each conversation has unique UUID
- Auto-loads last 10 conversations on startup
- Maintains context across bot restarts

📚 **Context Management**
- History automatically included in LLM context
- Smart memory: RAM (fast) + MongoDB (durable)
- `/clear` command to reset and reload from database

📊 **Monitoring & Analytics**
- LangSmith integration for LLM tracing
- Query conversation history by user/date
- Built-in analytics scripts

🔧 **Commands:**
- `/start` - Initialize bot and load history
- `/help` - Show available commands and examples
- `/clear` - Clear memory and reload from database

**Requirements:**
- `OPENAI_API_KEY` (required)
- `TELEGRAM_BOT_TOKEN` (required - get from [@BotFather](https://t.me/botfather))
- `MONGODB_URI` (optional - for persistence)
- `LANGCHAIN_API_KEY` (optional - for tracing)

**MongoDB Setup:**
1. Create free account at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register)
2. Create M0 cluster (free tier, 512MB)
3. Get connection string
4. Add to `.env`: `MONGODB_URI=mongodb+srv://...`

**Testing Scripts:**
```bash
cd test/chatbot

# Query saved conversations
python query_conversations.py

# Test history loading
python test_history_loading.py

# Verify context inclusion
python verify_history_in_context.py
```

## 🏗️ Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                    TELEGRAM USER                            │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────┐
│              TELEGRAM BOT (telegram_chatbot.py)             │
│  • User authentication (Telegram ID)                        │
│  • Command handlers (/start, /help, /clear)                │
│  • Message routing                                          │
└────────────────────────┬────────────────────────────────────┘
                         │
         ┌───────────────┴───────────────┐
         ↓                               ↓
┌──────────────────┐          ┌──────────────────────┐
│  USER MEMORIES   │          │  MONGODB MANAGER     │
│  (RAM Cache)     │←────────→│  (Persistence)       │
│                  │          │                      │
│  • Fast access   │          │  • Cloud storage     │
│  • Per-user      │          │  • Unique IDs        │
│  • Temporary     │          │  • History queries   │
└────────┬─────────┘          └──────────────────────┘
         │
         ↓
┌─────────────────────────────────────────────────────────────┐
│                    LANGCHAIN (LLMChain)                     │
│  • ConversationBufferMemory (last 10 messages)              │
│  • PromptTemplate (windbot_prompt.txt)                      │
│  • Context injection {history} + {pregunta}                 │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────┐
│                 OPENAI GPT-3.5-TURBO                        │
│  • Receives full context (system + history + question)     │
│  • Generates contextual response                            │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────┐
│                    LANGSMITH (Optional)                     │
│  • Traces every LLM call                                    │
│  • Monitors tokens, latency, errors                         │
│  • User-level analytics                                     │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

```
New Message → Load History (if not in RAM) → Include in Context → 
    LLM Response → Save to MongoDB → Return to User
```

## 📊 Technical Details

### Memory System

The bot uses a **two-tier memory architecture**:

1. **RAM Layer** (Fast, Temporary)
   - `USER_MEMORIES` dictionary
   - One `LLMChain` per active user
   - Lost on bot restart

2. **MongoDB Layer** (Durable, Permanent)
   - All conversations with UUID
   - Indexed by user_id and timestamp
   - Automatically reloaded on restart

**On First Message**: Load last 10 conversations from MongoDB → Populate memory → Generate response

**On Subsequent Messages**: Use existing memory (faster)

**On /clear**: Delete from RAM → Next message reloads from MongoDB

### Prompt Template Structure

Located in `src/prompt_template/windbot_prompt.txt`:

```
System Instructions (Who you are)
    ↓
Context (What you do)
    ↓
{history} ← Last 10 conversations injected here
    ↓
{pregunta} ← Current user question
    ↓
Response format
```

### Conversation Document (MongoDB)

```javascript
{
  "_id": ObjectId("..."),
  "conversation_id": "a7b3c4d5-1234-5678-90ab-cdef12345678",  // UUID
  "user_id": 123456789,                                       // Telegram ID
  "user_name": "Juan Pérez",
  "user_message": "¿Cómo está el viento en Riohacha?",
  "bot_response": "En Riohacha, la velocidad promedio...",
  "timestamp": ISODate("2025-10-19T10:30:00Z"),
  "platform": "telegram",
  "metadata": {
    "username": "@juanito",
    "chat_id": 987654321
  }
}
```

## 🛠️ Development

### Project Structure Details

```
src/
├── prompt_template/
│   ├── __init__.py           # load_prompt() function
│   └── windbot_prompt.txt    # LLM system prompt
└── telegram_bot/
    ├── __init__.py           # Package exports
    ├── config.py             # Configuration, LLM initialization
    ├── handlers.py           # Telegram command/message handlers
    ├── utils.py              # get_user_chain, history loading
    └── mongodb_manager.py    # MongoDB operations

test/chatbot/
├── console_chatbot_test.py       # Console interface
├── telegram_chatbot.py           # Telegram bot main
├── query_conversations.py        # MongoDB query examples
├── test_history_loading.py       # Test history feature
└── verify_history_in_context.py  # Verify LLM context
```

### Adding New Features

**1. New Telegram Command:**

Edit `src/telegram_bot/handlers.py`:

```python
async def new_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Response")
```

Register in `telegram_chatbot.py`:

```python
application.add_handler(CommandHandler("new", new_command))
```

**2. Custom Prompt:**

Create `src/prompt_template/my_prompt.txt` and use:

```python
prompt_template = load_prompt("my_prompt")
```

**3. Different Memory Strategy:**

In `src/telegram_bot/utils.py`:

```python
from langchain.memory import ConversationBufferWindowMemory

memory = ConversationBufferWindowMemory(k=5)  # Last 5 only
```

## 📈 Performance & Costs

### Estimated Costs (GPT-3.5-turbo)

| Metric | Value |
|--------|-------|
| Input tokens per message | ~2,500 (with 10 msg history) |
| Output tokens per response | ~300 |
| Cost per message | ~$0.0017 |
| Cost per 1,000 messages | ~$1.70 |
| Monthly cost (100 users, 10 msgs/day) | ~$51 |

### Database Storage (MongoDB Atlas Free Tier)

- **Capacity**: 512 MB (free)
- **Estimated**: ~1 million conversations
- **Sufficient for**: Most small-to-medium deployments

## 🔒 Security & Privacy

- ✅ No phone numbers collected
- ✅ User identified by Telegram ID only
- ✅ Per-user data isolation
- ✅ `.env` credentials not committed (in `.gitignore`)
- ✅ MongoDB with authentication
- ⚠️ Implement data retention policy for GDPR/LGPD compliance

## 🐛 Troubleshooting

### Bot doesn't respond

1. Check `.env` has `OPENAI_API_KEY` and `TELEGRAM_BOT_TOKEN`
2. Verify bot is running: `ps aux | grep telegram_chatbot`
3. Check logs for errors

### MongoDB connection failed

- Message: `⚠️ MongoDB no disponible`
- **Solution**: Bot works without MongoDB (RAM-only mode)
- **To fix**: Verify `MONGODB_URI` in `.env` and cluster is running

### History not loading

- Run: `python test/chatbot/test_history_loading.py`
- Check MongoDB has conversations for user
- Verify `conversation_id` field exists in documents

## 🚧 Roadmap

- [ ] Integration with real wind prediction models (LSTM)
- [ ] Web dashboard for conversation analytics
- [ ] Multi-language support (English, Portuguese)
- [ ] Voice message support
- [ ] Export conversations to CSV/PDF
- [ ] Admin panel for bot management
- [ ] Integration with Open-Meteo real-time data
- [ ] Scheduled wind reports via Telegram

## 📝 License

This project is under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Contact

- **Author**: E. A. León Gómez
- **Email**: ealeongomez@unal.edu.co
- **Institution**: Universidad Nacional de Colombia
- **Project**: GuajiraSustainableWindBot

## 🙏 Acknowledgments

- **OpenAI** - GPT-3.5 Turbo API
- **LangChain** - LLM framework
- **MongoDB** - Database services
- **Telegram** - Bot platform

---

**Status**: 🟢 Active Development | **Version**: 0.2.0 (Chatbot MVP)

*This project is under active development. Features and structure may evolve.* 