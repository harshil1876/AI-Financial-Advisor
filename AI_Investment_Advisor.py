import os
import json
import requests
import yfinance as yf
from datetime import datetime
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

# Load environment variables
load_dotenv()

# Check for API Keys
if not os.getenv("GOOGLE_API_KEY"):
    print("Warning: GOOGLE_API_KEY not found. Ensure it is set for Gemini.")

# Current date for context
Now = datetime.now()
Today = Now.strftime("%d-%b-%Y")

# --- Tools ---

@tool("DuckDuckGo Search")
def search_tool(search_query: str):
    """Search the internet for information on a given topic"""
    return DuckDuckGoSearchRun().run(search_query)

@tool("Get current stock price")
def get_current_stock_price(symbol: str) -> str:
    """Use this function to get the current stock price for a given symbol using Yfinance.
    
    Args:
        symbol (str): The stock symbol (e.g., AAPL, RELIANCE.NS).
    
    Returns:
        str: The current stock price or error message.
    """
    try:
        ticker = yf.Ticker(symbol)
        price = ticker.fast_info.last_price
        return f"{price}" if price else f"Could not fetch price for {symbol}"
            
    except Exception as e:
        return f"Error fetching stock price for {symbol}: {e}"

@tool("Get Company Profile")
def get_company_info(symbol: str):
    """Use this function to get company information and profile for a given stock symbol using Yfinance.
    
    Args:
        symbol (str): The stock symbol.
    
    Returns:
        JSON string containing company profile.
    """
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        return json.dumps(info, indent=2)
            
    except Exception as e:
        return f"Error fetching company info for {symbol}: {e}"

@tool("Get Income Statements")
def get_income_statements(symbol: str):
    """Use this function to get annual income statements for a given stock symbol using Yfinance.
    
    Args:
        symbol (str): The stock symbol.
    
    Returns:
        JSON string containing income statements.
    """
    try:
        ticker = yf.Ticker(symbol)
        financials = ticker.financials
        # Convert DataFrame to JSON
        return financials.to_json()
            
    except Exception as e:
        return f"Error fetching income statements for {symbol}: {e}"


# --- Agents ---

# Agent for gathering company news and information
news_info_explorer = Agent(
    role='News and Info Researcher',
    goal='Gather and provide the latest news and information about a company from the internet',
    llm='gemini/gemini-2.5-flash-lite',
    verbose=True,
    backstory=(
        'You are an expert researcher, who can gather detailed information about a company. '
        f'Consider you are on: {Today}'
    ),
    tools=[search_tool],
    cache=True,
    max_iter=5,
)

# Agent for gathering financial data
data_explorer = Agent(
    role='Data Researcher',
    goal='Gather and provide financial data and company information about a stock',
    llm='gemini/gemini-2.5-flash-lite',
    verbose=True,
    backstory=(
        'You are an expert researcher, who can gather detailed information about a company or stock. '
        'You use the Yahoo Finance (yfinance) tools. '
        'For Indian stocks, use the suffix ".NS" and remove any spaces (e.g., "TATA MOTORS" becomes "TATAMOTORS.NS"). '
        f'Consider you are on: {Today}'
    ),
    tools=[get_company_info, get_income_statements],
    cache=True,
    max_iter=5,
)

# Agent for analyzing data
analyst = Agent(
    role='Data Analyst',
    goal='Consolidate financial data, stock information, and provide a summary',
    llm='gemini/gemini-2.5-flash-lite',
    verbose=True,
    backstory=(
        'You are an expert in analyzing financial data, stock/company-related current information, and '
        'making a comprehensive analysis. Use Indian units for numbers (lakh, crore) if the stock is Indian, otherwise standard units. '
        f'Consider you are on: {Today}'
    ),
)

# Agent for financial recommendations
fin_expert = Agent(
    role='Financial Expert',
    goal='Considering financial analysis of a stock, make investment recommendations',
    llm='gemini/gemini-2.5-flash-lite',
    verbose=True,
    tools=[get_current_stock_price],
    max_iter=5,
    backstory=(
        'You are an expert financial advisor who can provide investment recommendations. '
        'Consider the financial analysis, current information about the company, current stock price, '
        'and make recommendations about whether to buy/hold/sell a stock along with reasons. '
        f'Consider you are on: {Today}'
    ),
)


# --- Tasks ---

# Task to gather financial data of a stock
get_company_financials = Task(
    description="Get financial data like income statements and company profile for stock: {stock}",
    expected_output="Detailed information from income statement, key ratios for {stock}. "
                    "Indicate also about current financial status and trend over the period.",
    agent=data_explorer,
)

# Task to gather company news
get_company_news = Task(
    description="Get latest news and business information about company: {stock}",
    expected_output="Latest news and business information about the company. Provide a summary also.",
    agent=news_info_explorer,
)

# Task to analyze financial data and news
analyse = Task(
    description="Make thorough analysis based on given financial data and latest news of a stock",
    expected_output="Comprehensive analysis of a stock outlining financial health, stock valuation, risks, and news. "
                    "Mention currency information and number units in Indian context (lakh/crore) if applicable.",
    agent=analyst,
    context=[get_company_financials, get_company_news],
    output_file='Analysis.md',
)

# Task to provide financial advice
advise = Task(
    description="Make a recommendation about investing in a stock, based on analysis provided and current stock price. "
                "Explain the reasons.",
    expected_output="Recommendation (Buy / Hold / Sell) of a stock backed with reasons elaborated."
                    "Response in Markdown format.",
    agent=fin_expert,
    context=[analyse],
    output_file='Recommendation.md',
)


# --- Crew ---

# Define the crew with agents and tasks in sequential process
crew = Crew(
    agents=[data_explorer, news_info_explorer, analyst, fin_expert],
    tasks=[get_company_financials, get_company_news, analyse, advise],
    verbose=True,
    process=Process.sequential,
)

# --- Main Execution ---

if __name__ == "__main__":
    print("## Welcome to the AI Investment Advisor ##")
    print("------------------------------------------")
    stock_symbol = input("Enter the stock symbol (e.g., AAPL, RELIANCE.NS): ")
    
    if stock_symbol:
        result = crew.kickoff(inputs={'stock': stock_symbol})
        print("\n\n########################")
        print("## Final Result ##")
        print("########################\n")
        print(result)
    else:
        print("No stock symbol entered. Exiting.")