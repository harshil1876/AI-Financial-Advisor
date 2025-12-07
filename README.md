# AI Investment Advisor

The **AI Investment Advisor** is an intelligent agent-based system designed to assist users in making informed investment decisions. By leveraging the power of Large Language Models (LLMs) and real-time financial data, this tool analyzes stock performance, company news, and financial statements to provide comprehensive investment recommendations.

## 🚀 Features

*   **Automated Financial Research**: Fetches detailed company profiles and annual income statements using `yfinance`.
*   **Real-time News Analysis**: Searches the web for the latest news and business updates related to the company using DuckDuckGo.
*   **Intelligent Data Analysis**: Consolidates financial data and news to assess financial health, stock valuation, and potential risks.
*   **Tailored Recommendations**: Provides actionable "Buy", "Hold", or "Sell" advice backed by reasoning and current market data.
*   **Indian Market Support**: Automatically handles Indian stock symbols (e.g., converts "TATA MOTORS" to "TATAMOTORS.NS") and uses Indian numbering units (Lakh/Crore) where applicable.
*   **Multi-Agent Architecture**: Uses **CrewAI** to orchestrate specialized agents (Data Researcher, News Researcher, Analyst, Financial Expert) for a streamlined workflow.

## 🛠️ Prerequisites

Before running the application, ensure you have the following installed:

*   **Python 3.10+**
*   **pip** (Python package manager)

You will also need a valid **Google API Key** to use the Gemini LLM.

## 📦 Installation

1.  **Clone the repository** (or download the source code):
    ```bash
    git clone <repository-url>
    cd "Investment Advisor"
    ```

2.  **Install the required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up Environment Variables**:
    *   Create a `.env` file in the root directory.
    *   Add your Google API Key:
        ```env
        GOOGLE_API_KEY=your_google_api_key_here
        ```

## 💻 Usage

1.  **Run the application**:
    ```bash
    python AI_Investment_Advisor.py
    ```

2.  **Enter a Stock Symbol** when prompted:
    *   For US stocks: `AAPL`, `MSFT`, `TSLA`
    *   For Indian stocks: `RELIANCE.NS`, `TATASTEEL.NS` (or simply `RELIANCE`, `TATA STEEL`)

3.  **View the Results**:
    *   The agents will perform their tasks sequentially, displaying progress in the console.
    *   **Final Output**: A detailed recommendation will be printed to the console.
    *   **Generated Files**:
        *   `Analysis.md`: Contains the comprehensive analysis of the stock.
        *   `Recommendation.md`: Contains the final investment advice.

## 🤖 How It Works

The system employs a crew of four AI agents working in sequence:

1.  **Data Researcher**: Uses `yfinance` to gather company profile and financial statements.
2.  **News and Info Researcher**: Uses `DuckDuckGo` to find the latest relevant news.
3.  **Data Analyst**: Synthesizes the financial data and news into a coherent health report.
4.  **Financial Expert**: Reviews the analysis and current stock price to formulate a final recommendation.

## ⚠️ Disclaimer

This tool is for **informational purposes only** and does not constitute professional financial advice. Always conduct your own research or consult with a qualified financial advisor before making investment decisions. The creators of this software are not responsible for any financial losses incurred.