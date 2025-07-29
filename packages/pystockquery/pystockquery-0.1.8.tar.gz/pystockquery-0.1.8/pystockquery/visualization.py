import re
import matplotlib.pyplot as plt
import seaborn as sns

class Visualizer:
    def create_visualization(self, df, query_string, save_path=None, show=True, **kwargs):
        """
        Create visualization based on natural language description.
        """
        query_string = query_string.lower()
        
        # Extract column names more robustly
        if 'vs' in query_string:
            # Handle scatter plots
            return self._create_scatter_plot(df, query_string, save_path, show, **kwargs)
        elif 'compare' in query_string:
            # Handle bar charts
            return self._create_bar_plot(df, query_string, save_path, show, **kwargs)
        elif 'distribution' in query_string or 'histogram' in query_string:
            # Handle histograms
            return self._create_histogram(df, query_string, save_path, show, **kwargs)
        else:
            # Default to scatter plot
            return self._create_scatter_plot(df, query_string, save_path, show, **kwargs)
    
    def _extract_columns(self, query_string):
        """
        Extract column names from query string.
        Returns: (x_var, y_var, color_var, size_var)
        """
        # Normalize the query string
        query_string = query_string.lower()
        
        # Pattern to match "Plot X vs Y colored by Z"
        pattern = r'(?:plot|show|create)\s+([a-z\s]+)\s+vs\s+([a-z\s]+)(?:\s+colou?red\s+by\s+([a-z\s]+))?'
        match = re.search(pattern, query_string)
        
        if match:
            x_var = match.group(1).strip()
            y_var = match.group(2).strip()
            color_var = match.group(3).strip() if match.group(3) else None
            return x_var, y_var, color_var, None
        
        # If no match, try to extract single variable for histograms
        hist_pattern = r'(?:show|plot)\s+(?:distribution|histogram)\s+of\s+([a-z\s]+)'
        hist_match = re.search(hist_pattern, query_string)
        if hist_match:
            return hist_match.group(1).strip(), None, None, None
            
        return None, None, None, None
    
    def _map_column_name(self, col_name):
        """
        Map natural language column names to actual dataframe columns.
        """
        col_name = col_name.strip().lower()
        
        # Basic mappings - expand this with your actual column names
        mappings = {
            'roe': 'returnOnEquity',
            'beta': 'beta',
            'sector': 'sector',
            'pe': 'trailingPE',
            'price to earnings': 'trailingPE',
            'market cap': 'marketCap',
            'return on equity': 'returnOnEquity',
            # Add all your column mappings here
        }
        
        return mappings.get(col_name, col_name)
    
    def _create_scatter_plot(self, df, query_string, save_path=None, show=True, **kwargs):
        """
        Create a scatter plot based on query description.
        """
        x_var, y_var, color_var, _ = self._extract_columns(query_string)
        
        if not x_var or not y_var:
            raise ValueError("Could not extract X and Y variables from query string")
        
        # Map to actual column names
        x_col = self._map_column_name(x_var)
        y_col = self._map_column_name(y_var)
        color_col = self._map_column_name(color_var) if color_var else None
        
        # Verify columns exist in dataframe
        for col in [x_col, y_col]:
            if col not in df.columns:
                raise ValueError(f"Column '{col}' not found in dataframe. Available columns: {list(df.columns)}")
        
        # Create plot
        plt.figure(figsize=kwargs.get('figsize', (10, 6)))
        sns.scatterplot(
            data=df,
            x=x_col,
            y=y_col,
            hue=color_col,
            alpha=0.7,
            palette='viridis'
        )
        plt.title(f"{y_var.upper()} vs {x_var.upper()}" + (f" by {color_var}" if color_var else ""))
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        if show:
            plt.show()
        
        return plt.gcf()

    def _create_bar_plot(self, df, query_string, save_path=None, show=True, **kwargs):
        """Create bar plot based on query."""
        # Implementation similar to scatter plot
        pass

    def _create_histogram(self, df, query_string, save_path=None, show=True, **kwargs):
        """Create histogram based on query."""
        # Implementation similar to scatter plot
        pass