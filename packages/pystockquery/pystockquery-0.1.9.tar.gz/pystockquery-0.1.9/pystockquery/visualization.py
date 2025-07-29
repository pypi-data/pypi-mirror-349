import re
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class Visualizer:
    def create_visualization(self, df, query_string, save_path=None, show=True, **kwargs):
        """
        Create visualization based on natural language description.
        """
        query_string = query_string.lower()
        
        # First check if the query is asking for a specific plot type
        if 'scatter' in query_string or 'vs' in query_string:
            return self._create_scatter_plot(df, query_string, save_path, show, **kwargs)
        elif 'bar' in query_string or 'compare' in query_string:
            return self._create_bar_plot(df, query_string, save_path, show, **kwargs)
        elif 'histogram' in query_string or 'distribution' in query_string:
            return self._create_histogram(df, query_string, save_path, show, **kwargs)
        else:
            # Default to scatter plot
            return self._create_scatter_plot(df, query_string, save_path, show, **kwargs)
    
    def _map_column_name(self, col_name, df_columns):
        """
        Map natural language column names to actual dataframe columns.
        """
        col_name = col_name.strip().lower()
        
        # Comprehensive mapping based on your dataset columns
        mappings = {
            # Financial Metrics
            'pe': 'P/E_Ratio',
            'p/e': 'P/E_Ratio',
            'price to earnings': 'P/E_Ratio',
            'pb': 'P/B_Ratio',
            'p/b': 'P/B_Ratio',
            'price to book': 'P/B_Ratio',
            'beta': 'Beta',
            'volatility': 'Volatility',
            'return on investment': 'Return_on_Investment',
            'cagr': 'CAGR',
            'debt to equity': 'Debt_to_Equity_Ratio',
            'eps': 'EPS',
            'dividend yield': 'Dividend_Yield',
            'market cap': 'Market_Cap',
            
            # Technical Indicators
            '50 day ma': 'Fifty_MA',
            '200 day ma': 'Two_Hundred_MA',
            'rsi': 'RSI',
            'macd': 'MACD',
            'bollinger band': 'Bollinger_Band',
            'current price': 'Current_Price',
            
            # Categories
            'sector': 'sector',
            'industry': 'Stock Industry',
            'category': 'Category',
            
            # Other important columns
            'score': 'Total_Score',
            'correlation': 'Correlation_with_event',
            'price': 'Latest_Close_Price'
        }
        
        # First try exact match (case insensitive)
        for actual_col in df_columns:
            if col_name.lower() == actual_col.lower():
                return actual_col
                
        # Then try our mappings
        mapped = mappings.get(col_name, None)
        if mapped and mapped in df_columns:
            return mapped
            
        # Try to find partial matches
        for actual_col in df_columns:
            if col_name in actual_col.lower():
                return actual_col
                
        raise ValueError(f"Column '{col_name}' not found in dataframe. Available columns: {list(df_columns)}")

    def _extract_plot_components(self, query_string, df_columns):
        """
        Extract components from visualization query.
        Returns: (plot_type, x_col, y_col, hue_col, title)
        """
        query_string = query_string.lower()
        
        # Scatter plot pattern
        scatter_pattern = r'(?:plot|show|create)\s+(?:scatter\s*)?([a-z\s]+)\s+vs\s+([a-z\s]+)(?:\s+colou?red\s+by\s+([a-z\s]+))?'
        scatter_match = re.search(scatter_pattern, query_string)
        
        if scatter_match:
            x_var = scatter_match.group(1).strip()
            y_var = scatter_match.group(2).strip()
            color_var = scatter_match.group(3).strip() if scatter_match.group(3) else None
            
            x_col = self._map_column_name(x_var, df_columns)
            y_col = self._map_column_name(y_var, df_columns)
            hue_col = self._map_column_name(color_var, df_columns) if color_var else None
            
            title = f"{y_col} vs {x_col}"
            if hue_col:
                title += f" by {hue_col}"
                
            return 'scatter', x_col, y_col, hue_col, title
            
        # Bar plot pattern
        bar_pattern = r'(?:compare|show)\s+([a-z\s]+)\s+(?:across|by)\s+([a-z\s]+)'
        bar_match = re.search(bar_pattern, query_string)
        
        if bar_match:
            value_var = bar_match.group(1).strip()
            category_var = bar_match.group(2).strip()
            
            value_col = self._map_column_name(value_var, df_columns)
            category_col = self._map_column_name(category_var, df_columns)
            
            title = f"{value_col} by {category_col}"
            return 'bar', category_col, value_col, None, title
            
        # Histogram pattern
        hist_pattern = r'(?:show|plot)\s+(?:distribution|histogram)\s+of\s+([a-z\s]+)'
        hist_match = re.search(hist_pattern, query_string)
        
        if hist_match:
            var = hist_match.group(1).strip()
            col = self._map_column_name(var, df_columns)
            return 'histogram', col, None, None, f"Distribution of {col}"
            
        raise ValueError("Could not interpret visualization query. Try patterns like: "
                        "'Plot X vs Y', 'Compare A across B', or 'Show distribution of Z'")

    def _create_scatter_plot(self, df, query_string, save_path=None, show=True, **kwargs):
        """Create scatter plot from query."""
        plot_type, x_col, y_col, hue_col, title = self._extract_plot_components(query_string, df.columns)
        
        plt.figure(figsize=kwargs.get('figsize', (10, 6)))
        sns.scatterplot(
            data=df,
            x=x_col,
            y=y_col,
            hue=hue_col,
            palette='viridis',
            alpha=0.7,
            size=kwargs.get('size', None),
            sizes=kwargs.get('sizes', (20, 200))
        )
        
        plt.title(title)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        if show:
            plt.show()
            
        return plt.gcf()

    def _create_bar_plot(self, df, query_string, save_path=None, show=True, **kwargs):
        """Create bar plot from query."""
        plot_type, x_col, y_col, hue_col, title = self._extract_plot_components(query_string, df.columns)
        
        plt.figure(figsize=kwargs.get('figsize', (12, 6)))
        sns.barplot(
            data=df,
            x=x_col,
            y=y_col,
            hue=hue_col,
            palette='coolwarm'
        )
        
        plt.title(title)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        if show:
            plt.show()
            
        return plt.gcf()

    def _create_histogram(self, df, query_string, save_path=None, show=True, **kwargs):
        """Create histogram from query."""
        plot_type, x_col, y_col, hue_col, title = self._extract_plot_components(query_string, df.columns)
        
        plt.figure(figsize=kwargs.get('figsize', (10, 6)))
        sns.histplot(
            data=df,
            x=x_col,
            hue=hue_col,
            bins=kwargs.get('bins', 20),
            kde=kwargs.get('kde', True),
            palette='pastel'
        )
        
        plt.title(title)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        if show:
            plt.show()
            
        return plt.gcf()