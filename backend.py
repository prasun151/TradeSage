import os
import yfinance as yf
import pandas as pd
from dotenv import load_dotenv
from exa_py import Exa
from datetime import datetime, timedelta
import re
from urllib.parse import unquote

load_dotenv()

def get_ticker_from_exa(query_name: str):
    """
    Uses Exa AI to find the Yahoo Finance URL and extract the ticker.
    """
    exa_api_key = os.getenv("EXA_API_KEY")
    if not exa_api_key:
        return None

    try:
        exa = Exa(api_key=exa_api_key)
        # Search for the Yahoo Finance quote page
        search_query = f"site:finance.yahoo.com/quote {query_name}"
        
        # Removed 'use_autoprompt' as it caused errors
        response = exa.search(
            search_query,
            num_results=1,
            type="neural"
        )
        
        if response.results:
            url = response.results[0].url
            # Extract ticker from URL like https://finance.yahoo.com/quote/AAPL/ or .../quote/%5ENSEI
            match = re.search(r'/quote/([^/?]+)', url)
            if match:
                # Unquote handles %5E -> ^
                ticker = unquote(match.group(1))
                return ticker
    except Exception as e:
        print(f"Exa ticker resolution error: {e}")
    
    return None

def fetch_market_data(user_input: str):
    """
    1. Tries to fetch data directly.
    2. If failed, tries to resolve ticker via Exa and fetch again.
    3. Fetches Web Data/News via Exa AI.
    """
    try:
        ticker = user_input.upper().strip()
        stock = yf.Ticker(ticker)
        history = stock.history(period="6mo")
        
        # --- INTELLIGENT RESOLUTION ---
        # If direct fetch failed (empty history), assume it's a name and search for ticker
        if history.empty:
            print(f"Direct fetch failed for '{ticker}'. Attempting resolution...")
            resolved_ticker = get_ticker_from_exa(user_input)
            
            if resolved_ticker and resolved_ticker != ticker:
                print(f"Resolved '{user_input}' to '{resolved_ticker}'")
                ticker = resolved_ticker
                stock = yf.Ticker(ticker)
                history = stock.history(period="6mo")
            
            if history.empty:
                return None, f"Could not find market data for '{user_input}'. Try entering the exact ticker (e.g., AAPL)."

        # Data confirmed valid
        current_price = history['Close'].iloc[-1]
        
        # Prepare data for Chart (pass the full DataFrame)
        # We'll just keep 'Close' and 'Volume' for simplicity in the chart
        chart_data = history[['Close', 'Volume']]
        
        # Format history string for the LLM (text summary)
        recent_history_df = history.tail(14)[['Close', 'Volume']]
        recent_history_str = recent_history_df.to_string()
        
        # 2. Fundamentals
        info = stock.info
        fundamentals = {
            "Long Name": info.get("longName"),
            "Business Summary": info.get("longBusinessSummary"),
            "Market Cap": info.get("marketCap"),
            "Trailing PE": info.get("trailingPE"),
            "Forward PE": info.get("forwardPE"),
            "ROE": info.get("returnOnEquity"),
            "Debt to Equity": info.get("debtToEquity"),
            "Free Cashflow": info.get("freeCashflow"),
            "Gross Margins": info.get("grossMargins"),
            "Operating Margins": info.get("operatingMargins"),
        }
        
        # 3. Web Data / News via Exa AI
        exa_api_key = os.getenv("EXA_API_KEY")
        web_data_str = ""

        if exa_api_key:
            try:
                exa = Exa(api_key=exa_api_key)
                one_week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
                
                name = info.get('longName', ticker)
                query = f"competitive advantage, economic moat analysis, and recent financial news for {name} ({ticker})"
                
                # Removed 'use_autoprompt' here too
                search_response = exa.search_and_contents(
                    query,
                    type="neural",
                    num_results=5,
                    text=True,
                    start_published_date=one_week_ago,
                    category="news"
                )
                
                exa_results = []
                for result in search_response.results:
                    content = result.text[:1000] + "..." if result.text and len(result.text) > 1000 else result.text
                    published = result.published_date if result.published_date else "Unknown Date"
                    exa_results.append(
                        f"Title: {result.title}\n"
                        f"Source: {result.url}\n"
                        f"Date: {published}\n"
                        f"Content: {content}\n"
                    )
                
                if exa_results:
                    web_data_str = "--- Exa AI Web Search Results ---\n" + "\n---".join(exa_results)
                else:
                    web_data_str = "Exa AI search returned no results."
                    
            except Exception as exa_error:
                print(f"Exa AI Error: {exa_error}")
                web_data_str = "" 
        
        if not web_data_str:
            news_items = stock.news
            web_data_summary = []
            if news_items:
                for item in news_items[:5]:
                    title = item.get('title')
                    publisher = item.get('publisher')
                    web_data_summary.append(f"- {title} ({publisher})")
            
            fallback_str = "\n".join(web_data_summary) if web_data_summary else "No recent news fetched."
            web_data_str = f"--- Fallback Source (yfinance) ---\n{fallback_str}"

        return {
            "asset": ticker,
            "name": info.get("longName", ticker),
            "current_price": current_price,
            "price_history": recent_history_str, # Text for LLM
            "chart_data": chart_data,            # DataFrame for UI
            "fundamentals": fundamentals,
            "web_data": web_data_str
        }, None

    except Exception as e:
        return None, str(e)
