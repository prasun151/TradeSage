import streamlit as st
import backend
import agent

st.set_page_config(page_title="TradeSage", page_icon="📈")

st.title("TradeSage 📈")

# Sidebar controls
with st.sidebar:
    st.header("Configuration")
    forecast_horizon = st.slider("Forecast Horizon (Days)", min_value=7, max_value=90, value=30)
    st.markdown("---")
    
    with st.expander("ℹ️ Common Ticker Examples"):
        st.markdown("""
        **Indices:**
        - Nifty 50: `^NSEI`
        - S&P 500: `^GSPC`
        - Sensex: `^BSESN`
        
        **Stocks:**
        - Apple: `AAPL`
        - Reliance: `RELIANCE.NS`
        - Tesla: `TSLA`
        
        **Crypto:**
        - Bitcoin: `BTC-USD`
        - Ethereum: `ETH-USD`
        """)

# Main Input
ticker_input = st.text_input("Enter Company Name, Description, or Ticker (e.g., 'The iphone company', 'Coca Cola', 'BTC')", value="")

if st.button("Ask the Agent"):  
    if not ticker_input:
        st.warning("Please enter a company name or ticker.")
    else:
        with st.spinner(f"Backend: Hunting for market data for '{ticker_input}'..."):
            # 1. Backend Data Fetch (Simulating the EXA AI MCP flow)
            data, error = backend.fetch_market_data(ticker_input)
            
        if error:
            st.error(f"Backend Error: {error}")
        else:
            # SUCCESS: Display Data & Charts
            
            # Title and Price
            st.markdown(f"## {data['name']} ({data['asset']})")
            st.metric("Current Price", f"{data['current_price']:,.2f}")

            # --- GRAPHICAL REPRESENTATION ---
            st.subheader("Price History (6 Months)")
            # Streamlit handles dataframe indices (dates) automatically for the x-axis
            st.line_chart(data['chart_data']['Close'], color="#00FF00") 

            # Detailed Analysis Section
            with st.spinner("TradeSage: Analyzing trends & reasoning (Thinking like Buffett)..."):
                # 2. TradeSage Analysis
                analysis_result = agent.get_tradesage_analysis(data, forecast_horizon)
            
            # Output Report
            st.markdown("### The Agent's Analysis")
            st.markdown("---")
            st.markdown(analysis_result)
            st.markdown("---")
            
            # Raw Data Expander
            with st.expander("View Raw Data Sources"):
                st.json(data["fundamentals"])
                st.text("Web Data Summary:")
                st.text(data["web_data"])
                
            st.caption("Disclaimer: This is an AI-generated analysis for informational purposes only. Not financial advice.")
