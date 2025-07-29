import re

class QueryParser:
    def __init__(self):
            self.condition_map = {
    # Stock / Financial Metrics
    "Stock Industry": "industry",
    "Dividend Payout Ratio": "payoutRatio",
    "Five Year Avg Dividend Yield": "fiveYearAvgDividendYield",
    "Price to Sales Trailing 12 Months": "priceToSalesTrailing12Months",
    "Trailing Annual Dividend Rate": "trailingAnnualDividendRate",
    "Profit Margins": "profitMargins",
    "% Held by Insiders": "heldPercentInsiders",
    "% Held by Institutions": "heldPercentInstitutions",
    "Volume": "volume",
    "Regular Market Volume": "regularMarketVolume",
    "Average Volume": "averageVolume",
    "Average Volume 10 days": "averageVolume10days",
    "Average Daily Volume 10 Day": "averageDailyVolume10Day",
    "Return on Assets": "returnOnAssets",
    "Return on Assets (ttm)": "returnOnAssets",
    "Return on Equity (ttm)": "returnOnEquity",
    "Total Value": "totalValue",
    "Correlation with NSEI": "Correlation with ^NSEI",
    "Annualized Alpha (%)": "Annualized Alpha (%)",
    "Annualized Volatility (%)": "Annualized Volatility (%)",
    "Sharpe Ratio": "Sharpe Ratio",
    "Treynor Ratio": "Treynor Ratio",
    "Sortino Ratio": "Sortino Ratio",
    "Maximum Drawdown": "Maximum Drawdown",
    "R-Squared": "R-Squared",
    "Downside Deviation": "Downside Deviation",
    "Annualized Tracking Error (%)": "Annualized Tracking Error (%)",
    "VaR (95%)": "VaR (95%)",
    "50-Day Moving Average": "50-Day Moving Average",
    "200-Day Moving Average": "200-Day Moving Average",
    "New Haircut Margin": "New Haircut Margin",
    "Rating": "Rating",
    "Combined Score": "Combined Score",
    "New Collateral Value Percentage": "New Collateral Value Percentage",
    "Market Cap": "marketCap",
    "Enterprise Value": "enterpriseValue",
    "Trailing P/E": "trailingPE",
    "Forward P/E": "forwardPE",
    "PEG Ratio": "pegRatio",
    "Price/Sales": "priceToSalesTrailing12Months",
    "Price/Book": "priceToBook",
    "Enterprise Value/Revenue": "enterpriseToRevenue",
    "Enterprise Value/EBITDA": "enterpriseToEbitda",
    "Beta": "beta",
    "52-Week High": "fiftyTwoWeekHigh",
    "52-Week Low": "fiftyTwoWeekLow",
    "50-Day Average": "fiftyDayAverage",
    "200-Day Average": "twoHundredDayAverage",
    "Short Ratio": "shortRatio",
    "Short % of Float": "shortPercentOfFloat",
    "Shares Outstanding": "sharesOutstanding",
    "Float": "floatShares",
    "Shares Short": "sharesShort",
    "Short Ratio": "shortRatio",
    "Book Value": "bookValue",
    "Price/Book": "priceToBook",
    "EBITDA": "ebitda",
    "Revenue": "revenue",
    "Revenue Per Share": "revenuePerShare",
    "Gross Profit": "grossProfit",
    "Free Cash Flow": "freeCashflow",
    "Operating Cash Flow": "operatingCashflow",
    "Earnings Growth": "earningsGrowth",
    "Revenue Growth": "revenueGrowth",
    "Current Ratio": "currentRatio",
    "Quick Ratio": "quickRatio",
    "Debt to Equity": "debtToEquity",
    "Total Debt": "totalDebt",
    "Total Cash": "totalCash",
    "Total Cash Per Share": "totalCashPerShare",
    "CAGR": "CAGR",
    "ROI": "ROI",
    "EPS": "trailingEps",
    "EPS Growth": "epsGrowth",

    # Interpretations
    "Correlation with NSEI Interpretation": "Correlation with ^NSEI Interpretation",
    "Alpha Interpretation": "Annualized Alpha (%) Interpretation",
    "Volatility Interpretation": "Annualized Volatility (%) Interpretation",
    "Sharpe Ratio Interpretation": "Sharpe Ratio Interpretation",
    "Treynor Ratio Interpretation": "Treynor Ratio Interpretation",
    "Sortino Ratio Interpretation": "Sortino Ratio Interpretation",
    "Maximum Drawdown Interpretation": "Maximum Drawdown Interpretation",
    "R-Squared Interpretation": "R-Squared Interpretation",
    "Downside Deviation Interpretation": "Downside Deviation Interpretation",
    "Tracking Error Interpretation": "Annualized Tracking Error (%) Interpretation",
    "VaR Interpretation": "VaR (95%) Interpretation",
    "Moving Average Interpretation": "Moving Average Interpretation",
    "Valuation Interpretation": "Valuation Interpretation",

    # Company Info
    "Address": "address1",
    "City": "city",
    "Zip": "zip",
    "Country": "country",
    "Website": "website",
    "Sector": "sector",
    "Industry": "industry",
    "Business Summary": "longBusinessSummary",
    "Full Time Employees": "fullTimeEmployees",
    "Company Name": "shortName",
    "Exchange": "exchange",
    "Currency": "currency",
    "Quote Type": "quoteType",

    # Financial Statements
    "Income Statement (Quarterly)": "incomeStatementQuarterly",
    "Income Statement (Annual)": "incomeStatementAnnual",
    "Balance Sheet (Quarterly)": "balanceSheetQuarterly",
    "Balance Sheet (Annual)": "balanceSheetAnnual",
    "Cash Flow (Quarterly)": "cashflowStatementQuarterly",
    "Cash Flow (Annual)": "cashflowStatementAnnual",

    # Industry Comparisons
    "Industry Forward PE": "industry_forwardPE",
    "Industry Trailing PE": "industry_trailingPE",
    "Industry Debt to Equity": "industry_debtToEquity",
    "Industry Current Ratio": "industry_currentRatio",
    "Industry Quick Ratio": "industry_quickRatio",
    "Industry EBITDA": "industry_ebitda",
    "Industry Total Debt": "industry_totalDebt",
    "Industry Return on Assets": "industry_returnOnAssets",
    "Industry Return on Equity": "industry_returnOnEquity",
    "Industry Revenue Growth": "industry_revenueGrowth",
    "Industry Gross Margins": "industry_grossMargins",
    "Industry EBITDA Margins": "industry_ebitdaMargins",
    "Industry Operating Margins": "industry_operatingMargins",
    "Industry PEG Ratio": "industry_pegRatio",
    "Industry Price/Sales": "industry_priceToSales",
    "Industry Price/Book": "industry_priceToBook",

    # Technical Indicators
    "RSI": "rsi",
    "MACD": "macd",
    "Bollinger Bands": "bollingerBands",
    "Stochastic Oscillator": "stochasticOscillator",
    "ATR": "averageTrueRange",
    "OBV": "onBalanceVolume",
    "ADX": "averageDirectionalIndex",
    "CCI": "commodityChannelIndex",
    "Money Flow Index": "moneyFlowIndex",
    "Parabolic SAR": "parabolicSAR",
    "Ichimoku Cloud": "ichimokuCloud",

    # Alternative Names
    "PE Ratio": "trailingPE",
    "Price to Earnings": "trailingPE",
    "Price to Book Ratio": "priceToBook",
    "Price to Sales Ratio": "priceToSalesTrailing12Months",
    "Debt/Equity": "debtToEquity",
    "Current Assets": "totalCurrentAssets",
    "Current Liabilities": "totalCurrentLiabilities",
    "Total Assets": "totalAssets",
    "Total Liabilities": "totalLiabilities",
    "Shareholders Equity": "totalStockholderEquity",
    "Operating Income": "operatingIncome",
    "Net Income": "netIncome",
    "Diluted EPS": "trailingEps",
    "Basic EPS": "trailingEps",
    "Dividend Yield": "dividendYield",
    "Payout Ratio": "payoutRatio",
    "Enterprise Value to EBITDA": "enterpriseToEbitda",
    "Enterprise Value to Revenue": "enterpriseToRevenue",
    "EV/EBITDA": "enterpriseToEbitda",
    "EV/Revenue": "enterpriseToRevenue",
    "Quick Ratio": "quickRatio",
    "Acid Test Ratio": "quickRatio",
    "Working Capital": "workingCapital"
}
        
        self.comparison_operators = {
            '>': 'gt',
            '<': 'lt',
            '>=': 'ge',
            '<=': 'le',
            '=': 'eq',
            '!=': 'ne',
            'is': 'eq',
            'greater than': 'gt',
            'less than': 'lt',
            'at least': 'ge',
            'at most': 'le',
            'equals': 'eq',
            'not equals': 'ne'
        }
    
    def parse_query(self, query_string):
        """
        Parse a natural language query into pandas-compatible conditions.
        
        Args:
            query_string (str): Natural language query
            
        Returns:
            tuple: (conditions, sort_by, ascending)
                   conditions: list of query conditions
                   sort_by: column to sort by
                   ascending: sort order
        """
        # Normalize query string
        query_string = query_string.lower()
        
        # Initialize variables
        conditions = []
        sort_by = None
        ascending = True
        
        # Extract top N if specified
        top_n_match = re.search(r'top\s+(\d+)', query_string)
        top_n = int(top_n_match.group(1)) if top_n_match else None
        
        # Extract sort conditions
        if 'sort by' in query_string or 'order by' in query_string:
            sort_pattern = r'(?:sort by|order by)\s+([a-z\s]+)(?:\s+(asc|ascending|desc|descending))?'
            sort_match = re.search(sort_pattern, query_string)
            if sort_match:
                sort_field = sort_match.group(1).strip()
                sort_by = self._map_condition(sort_field)
                if sort_match.group(2) and sort_match.group(2).startswith('desc'):
                    ascending = False
        
        # Split query into conditions
        condition_parts = re.split(r',|\band\b|\bwith\b|\bwhere\b', query_string)
        
        for part in condition_parts:
            part = part.strip()
            if not part or 'top' in part or 'sort by' in part or 'order by' in part:
                continue
                
            # Parse condition
            condition = self._parse_condition(part)
            if condition:
                conditions.append(condition)
        
        return conditions, sort_by, ascending
    
    def _parse_condition(self, condition_str):
        """
        Parse a single condition string into a pandas query string.
        """
        # Match patterns like "P/E > 10", "Volatility < 20%", "positive ROI"
        pattern = r'([a-z/\s%]+)\s*(>|<|>=|<=|=|!=|is|greater than|less than|at least|at most|equals|not equals|positive|negative)\s*([\d.%]+)?'
        match = re.match(pattern, condition_str)
        
        if not match:
            return None
            
        field = match.group(1).strip()
        operator = match.group(2).strip()
        value = match.group(3).strip() if match.group(3) else None
        
        # Map field to actual column name
        column = self._map_condition(field)
        if not column:
            return None
            
        # Handle special cases
        if operator in ['positive', 'negative']:
            if operator == 'positive':
                return f"{column} > 0"
            else:
                return f"{column} < 0"
        
        # Map operator
        op = self.comparison_operators.get(operator, 'eq')
        
        # Clean value
        if value:
            value = value.replace('%', '')
            try:
                value = float(value)
            except ValueError:
                pass
        
        return f"{column} {op} {value}" if value is not None else None
    
    def _map_condition(self, condition_str):
        """
        Map natural language condition to actual column name.
        """
        # Try exact match first
        for key, value in self.condition_map.items():
            if key.lower() == condition_str.lower():
                return value
                
        # Try partial match
        for key, value in self.condition_map.items():
            if condition_str.lower() in key.lower():
                return value
                
        return None