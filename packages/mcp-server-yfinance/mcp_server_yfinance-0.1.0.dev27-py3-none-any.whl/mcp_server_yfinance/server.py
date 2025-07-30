"""MCP Server Markets - YFinance integration"""

import json

import yfinance as yf
from mcp.server import FastMCP

app = FastMCP("Market Data Server", "1.0.0")


@app.tool()
async def get_stock_info(ticker: str) -> str:
    """Get basic information about a stock.

    Args:
        ticker: Stock ticker symbol (e.g. 'AAPL')

    Returns:
        JSON string containing stock information
    """
    stock = yf.Ticker(ticker)
    info = stock.info
    relevant_info = {
        "symbol": info.get("symbol"),
        "shortName": info.get("shortName"),
        "sector": info.get("sector"),
        "industry": info.get("industry"),
        "marketCap": info.get("marketCap"),
        "currentPrice": info.get("currentPrice"),
    }
    return json.dumps(relevant_info, indent=2)


@app.tool()
async def get_historical_data(ticker: str, period: str = "1mo", interval: str = "1d") -> str:
    """Get historical price data for a stock.

    Args:
        ticker: Stock ticker symbol
        period: Data period (1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max)
        interval: Data interval (1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo)

    Returns:
        JSON string containing historical price data
    """
    stock = yf.Ticker(ticker)
    hist = stock.history(period=period, interval=interval)
    return hist.to_json(date_format="iso")


@app.tool()
async def get_recommendations(ticker: str) -> str:
    """Get analyst recommendations for a stock.

    Args:
        ticker: Stock ticker symbol

    Returns:
        JSON string containing analyst recommendations
    """
    stock = yf.Ticker(ticker)
    recs = stock.recommendations
    if recs is not None:
        return recs.to_json(date_format="iso")
    return json.dumps({"error": "No recommendations available"})


@app.tool()
async def get_multiple_tickers(tickers: list[str], period: str = "1d") -> str:
    """Get current data for multiple stock tickers.

    Args:
        tickers: list of stock ticker symbols. (e.g. ['AAPL', 'GOOGL'])
        period: Data period (1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max)

    Returns:
        JSON string containing data for all requested tickers
    """
    tickers_str = " ".join(tickers)
    data = yf.download(
        tickers_str,
        period=period,
        group_by="ticker",
        auto_adjust=True,
    )
    if data is None or data.empty:
        return json.dumps({"error": "No data available for the given tickers"})
    return data.to_json(date_format="iso")


@app.tool()
async def get_dividends(ticker: str) -> str:
    """Get dividend history for a stock.

    Args:
        ticker: Stock ticker symbol

    Returns:
        JSON string containing dividend history
    """
    stock = yf.Ticker(ticker)
    dividends = stock.dividends
    if dividends is not None:
        return dividends.to_json(date_format="iso")
    return json.dumps({"error": "No dividend data available"})


def main():
    """Main function to start the MCP server."""

    app.run()


if __name__ == "__main__":
    main()
