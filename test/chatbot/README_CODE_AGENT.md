# Multi-Agent System with Text-to-Python

## 📋 Description

Advanced multi-agent system that combines **text-to-python** for precise data analysis without hallucinations.

### Components:
- **1 Supervisor Agent**: Analyzes queries and determines if they need code
- **13 Municipality Agents with Python**: Generate and execute code for data analysis
- **1 General Agent**: Answers conceptual questions without code
- **Safe Python REPL**: Secure code execution environment

## 🎯 Advantages over Text-to-Text

| Feature | Text-to-Text | Text-to-Python (This System) |
|---|---|---|
| Numerical precision | ❌ Can hallucinate data | ✅ Zero hallucinations |
| Complex analysis | ❌ Limited | ✅ On-demand analysis |
| Transparency | ❌ Black box | ✅ Visible code |
| Scalability | ❌ Limited by prompt | ✅ Full data access |
| API Cost | ✅ Lower | ❌ Higher (GPT-4) |

## 🏗️ Architecture

```
User: "What is the average wind speed in Riohacha?"
   ↓
┌─────────────────────────────────────────────────┐
│ Supervisor Agent                                │
│ Analysis: DATA_QUERY | riohacha | CODE: YES   │
└────────────────┬────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────┐
│ Code Municipality Agent (Riohacha)              │
│                                                  │
│ 1. Generates Python code:                       │
│    df_riohacha['wind_speed_10m'].mean()         │
│                                                  │
│ 2. Executes in Safe REPL                        │
│    → Result: 6.45                               │
│                                                  │
│ 3. Formats response:                            │
│    "The average wind speed in Riohacha          │
│     is 6.45 m/s"                                │
└─────────────────────────────────────────────────┘
```

## 🚀 Usage

### Run the System

```bash
cd test/chatbot
python supervisor_code_agent_test.py
```

### Example Session

```
👤 What is the average wind speed in Riohacha?

🔍 Supervisor analyzing query...
📋 Type: data_query
📍 Municipalities: ['riohacha']
🐍 Needs code: Yes

📊 Routing to Riohacha agent...

🐍 Executing code:
print(f"Average speed: {df_riohacha['wind_speed_10m'].mean():.2f} m/s")

🤖 Bot:
The average wind speed in Riohacha is 6.45 m/s, 
calculated over 43,825 historical records.
```

## 📊 Supported Query Types

### 1. Simple Data Queries

```python
# Examples that automatically generate code:
"What is the average wind in Maicao?"
"What is the maximum temperature in Albania?"
"How many records are there for Uribia?"
"What is the average humidity in Fonseca?"
```

**Typical generated code:**
```python
# For average
mean_wind = df_maicao['wind_speed_10m'].mean()
print(f"Average: {mean_wind:.2f} m/s")

# For maximum
max_temp = df_albania['temperature_2m'].max()
print(f"Maximum temperature: {max_temp:.1f}°C")

# For count
count = len(df_uribia)
print(f"Total records: {count:,}")
```

### 2. Statistical Analysis

```python
"What is the standard deviation of wind in Riohacha?"
"Give me the 25th, 50th, and 75th percentiles of wind in Maicao"
"What is the coefficient of variation in Albania?"
```

**Typical generated code:**
```python
# Standard deviation
std = df_riohacha['wind_speed_10m'].std()
print(f"Standard deviation: {std:.2f} m/s")

# Percentiles
percentiles = df_maicao['wind_speed_10m'].quantile([0.25, 0.5, 0.75])
print("Percentiles:")
print(f"25%: {percentiles[0.25]:.2f} m/s")
print(f"50%: {percentiles[0.50]:.2f} m/s")
print(f"75%: {percentiles[0.75]:.2f} m/s")
```

### 3. Temporal Queries

```python
"What was the average wind in Riohacha in 2023?"
"Which month has the most wind in Maicao?"
"What is the average wind by hour of day in Albania?"
```

**Typical generated code:**
```python
# Filter by year
df_2023 = df_riohacha[df_riohacha['datetime'].dt.year == 2023]
mean_2023 = df_2023['wind_speed_10m'].mean()
print(f"2023 Average: {mean_2023:.2f} m/s")

# Group by month
monthly = df_maicao.groupby(df_maicao['datetime'].dt.month)['wind_speed_10m'].mean()
max_month = monthly.idxmax()
print(f"Windiest month: {max_month} ({monthly[max_month]:.2f} m/s)")
```

### 4. Multi-Municipality Comparisons

```python
"Compare average wind between Riohacha and Maicao"
"Which municipality has the highest wind speed?"
"Rank municipalities by average temperature"
```

**Typical generated code:**
```python
# Simple comparison
riohacha_mean = df_riohacha['wind_speed_10m'].mean()
maicao_mean = df_maicao['wind_speed_10m'].mean()
print(f"Riohacha: {riohacha_mean:.2f} m/s")
print(f"Maicao: {maicao_mean:.2f} m/s")
print(f"Difference: {abs(riohacha_mean - maicao_mean):.2f} m/s")
```

### 5. General Queries (No Code)

```python
"What is an LSTM model?"
"How does wind energy work?"
"Explain time series prediction"
"What is La Guajira?"
```

**These are routed to the General Agent (no code generation)**

## 🔧 Configuration

### Environment Variables

```bash
# .env file
OPENAI_API_KEY=sk-...  # Required - uses GPT-4 by default
```

### Dependencies

```bash
pip install langchain langchain-openai langchain-experimental \
    pandas matplotlib colorama python-dotenv
```

## 🧪 Testing

### Automated Tests

```bash
cd test/chatbot
python test_code_agent.py
```

**Included tests:**
1. ✅ Data loading (13 municipalities)
2. ✅ Supervisor routing
3. ✅ Code generation and execution

**Expected output:**
```
🧪 Test 1: Data Availability
✅ riohacha: 43,825 records
✅ maicao: 43,825 records
...

🧪 Test 2: Supervisor Routing
Query: What is the average wind speed in Riohacha?
  ✅ PASS - Correct routing

🧪 Test 3: Code Execution
Query: What is the average wind speed?
🐍 Executing code...
✅ PASS - Code executed successfully
```

## 🔒 Safe Python REPL Security

The system uses a **Safe Python REPL** with:

### Security Restrictions:
- ✅ Only allowed modules: `pandas`, `matplotlib`
- ✅ Limited builtins (no `eval`, `exec`, `import`, `open`, `file`)
- ✅ No file system access (except output)
- ✅ No network access
- ✅ Execution timeout
- ✅ Memory sandbox

### Permitted Access:
- ✅ Pre-loaded DataFrames: `df_riohacha`, `df_maicao`, etc.
- ✅ Full pandas for analysis
- ✅ Matplotlib for graphs (coming soon)
- ✅ Basic mathematical functions

## 📈 Performance and Costs

### Expected Latency:
- Simple query: 5-10 seconds
  - Supervisor: 2-3s
  - Code generation: 3-4s
  - Execution: <1s
  - Formatting: 2-3s

- Complex query: 10-20 seconds

### Costs (GPT-4):
- Routing: ~1,000 tokens = $0.01
- Code generation: ~2,000 tokens = $0.02
- Formatting: ~500 tokens = $0.005
- **Total per query: ~$0.035**

Vs. GPT-3.5 text-to-text: ~$0.002
**Trade-off: 17x more expensive but zero hallucinations**

## 🎨 Advanced Examples

### Correlation Analysis

```python
👤 Is there correlation between temperature and wind in Riohacha?

🤖 Generates and executes:
correlation = df_riohacha[['temperature_2m', 'wind_speed_10m']].corr()
print(f"Correlation: {correlation.iloc[0,1]:.3f}")

→ "The correlation between temperature and wind in Riohacha is -0.156,
   indicating a weak negative correlation."
```

### Hourly Analysis

```python
👤 At what time of day is there more wind in Maicao?

🤖 Generates and executes:
hourly = df_maicao.groupby('hour')['wind_speed_10m'].mean()
max_hour = hourly.idxmax()
print(f"Windiest hour: {max_hour}h ({hourly[max_hour]:.2f} m/s)")

→ "Wind is strongest in Maicao at 14h with an average of 8.3 m/s."
```

### Municipality Ranking

```python
👤 Rank municipalities by average wind speed

🤖 Generates code that iterates over all municipalities, calculates averages,
    and generates a complete ranking.
```

## 🚧 Roadmap

### Phase 1 (Current):
- [x] Python code generation
- [x] Safe execution (Safe REPL)
- [x] Basic statistical analysis
- [x] Multi-municipality comparisons

### Phase 2 (Next):
- [ ] Automatic graph generation
- [ ] Temporal trend analysis
- [ ] Predictions with LSTM models
- [ ] Export results to CSV/PDF

### Phase 3 (Future):
- [ ] Interactive visualizations
- [ ] Heat maps
- [ ] Advanced time series analysis
- [ ] ML model integration

## 🆚 Comparison: Text-to-Text vs Text-to-Python

### Use Case: "What is the average wind in Riohacha?"

**Text-to-Text (previous system):**
```
LLM reads pre-calculated statistics from prompt
→ "The average speed is 6.4 m/s"
✅ Fast (2-3s)
❌ Can hallucinate if data changes
❌ Cannot perform unanticipated analyses
```

**Text-to-Python (current system):**
```
LLM generates: df_riohacha['wind_speed_10m'].mean()
→ Executes code
→ Result: 6.452341
→ Formats: "The average speed is 6.45 m/s"
✅ Absolute precision
✅ Can perform any analysis
❌ Slower (5-8s)
❌ More expensive ($0.035 vs $0.002)
```

**Recommendation:** Use text-to-python when precision is critical (data analysis, official reports, business decisions). Use text-to-text for informal conversations.

## 👨‍💻 Author

Eder Arley León Gómez  
Date: 2025-10-19

---

**Note:** This system represents a significant advancement in precision over traditional conversational systems by completely eliminating hallucinations in numerical data.

