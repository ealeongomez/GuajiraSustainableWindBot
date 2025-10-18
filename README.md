# ChatBot for Sustainable Energy Planning through Wind Forecasting in La Guajira

**Explainable Deep Learning ChatBot for Wind Speed Forecasting and Sustainable Energy Planning in La Guajira.**

Wind forecasting system for La Guajira using artificial intelligence and a conversational chatbot. The project integrates climate data from multiple sources to provide accurate and accessible predictions through a conversational interface.


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

## Main Features

- **Wind Prediction**: Machine learning models to forecast wind speeds and directions
- **Intelligent Chatbot**: Conversational interface using LangChain and RAG
- **Multi-Source Integration**: Data from IDEAM, NASA, OpenWeather and other APIs
- **Advanced Visualization**: Interactive charts and automatic reports
- **REST API**: Backend for integration with external applications

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd GuajiraWindForecast
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

## Usage

### Run local server:
```bash
python main.py
```

### Test the Chatbots:

#### Console Chatbot (Terminal):
```bash
# Configure environment first
cp env.example .env
# Edit .env with your OPENAI_API_KEY

# Run the chatbot
cd test/chatbot
python console_chatbot_test.py
```

#### Telegram Chatbot:
```bash
# Configure environment with Telegram token
# Edit .env with your TELEGRAM_BOT_TOKEN (get from @BotFather)

# Run the bot
cd test/chatbot
python telegram_chatbot.py
```

For detailed Telegram setup, see [test/chatbot/TELEGRAM_SETUP.md](test/chatbot/TELEGRAM_SETUP.md)

## License

This project is under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

- **Author**: E. A. León Gómez
- **Email**: [ealeongomez@unal.edu.co]
- **Project**: [https://github.com/user/GuajiraSustainableWindBot]

---

**Note**: This project is under active development. The structure may evolve according to project needs. 