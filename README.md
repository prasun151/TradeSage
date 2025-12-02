# TradeSage 🔮

TradeSage is a lightweight, non-agentive market-analysis module embedded in a Streamlit application. It provides trend analysis, forecasts, Buffett-style interpretations, and risk flags for financial assets based on data provided by a simulated backend.

## Architecture & Principles

TradeSage operates under strict guidelines:
- **Non-Agentive**: It does not act autonomously or initiate web fetches.
- **Backend-Driven**: All data (price history, fundamentals, news, sentiment, metadata) is supplied exclusively by the backend layer.
- **Gemini-Powered Reasoning**: Utilizes the Google Gemini API for all forecasting and interpretation, adhering to a strict persona and output format.

The flow is explicit: `Frontend` → `Backend` (simulating EXA AI MCP) → `TradeSage` (Gemini LLM).

## Features

-   **Trend Analysis**: Identifies Upward / Sideways / Downward trends with concise evidence.
-   **Forecast**: Simple forward projections over a user-defined horizon using trend continuation, momentum, and volatility cues.
-   **Buffett-Style Interpretation**: Long-term intrinsic-value reasoning, including margin of safety, earnings stability, moat, and balance-sheet health. Avoids interpretation for non-fundamental assets.
-   **Recommendation**: A single label (Buy / Hold / Avoid) with crisp justification.
-   **Risk Flags**: Lists critical risks and concerns about missing data.
-   **Concise TL;DR Summary**.

## How to Run

Follow these steps to set up and run the TradeSage application locally.

### 1. Navigate to the Project Directory

Open your terminal or command prompt and change your current directory to the `TradeSage` project folder:

```bash
cd TradeSage
```

### 2. Install Dependencies

Install the required Python packages using `pip`:

```bash
pip install -r requirements.txt
```

### 3. Set Your API Keys

TradeSage requires Google Gemini and Exa AI API keys to function fully.

1.  **Obtain API Keys**:
    *   **Google Gemini**: Get a free key from [Google AI Studio](https://aistudio.google.com/app/apikey).
    *   **Exa AI**: Get a key from [Exa.ai](https://exa.ai/).
2.  **Create a `.env` file**: In the `TradeSage` directory, create a file named `.env`.
3.  **Add Your Keys**: Open the `.env` file and add the following lines, replacing the placeholders with your actual keys:

    ```
    GOOGLE_API_KEY=your_gemini_api_key_here
    EXA_API_KEY=your_exa_api_key_here
    ```

    _For reference, an `.env.example` file is provided._

### 4. Launch the Streamlit Application

Once the dependencies are installed and your API key is set, you can run the application:

```bash
streamlit run app.py
```

This command will open the TradeSage web application in your default browser. You can then enter an asset ticker (e.g., `AAPL` for Apple Inc., `BTC-USD` for Bitcoin) and click "Analyze Asset" to get the market analysis.

---

**Disclaimer**: This is an AI-generated analysis for informational purposes only and should not be considered financial advice. Always conduct your own research and consult with a financial professional before making any investment decisions.
