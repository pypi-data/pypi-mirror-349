import matplotlib.pyplot as plt
import seaborn as sns
import re

class Visualizer:
    def create_visualization(self, df, query_string, save_path=None, show=True, **kwargs):
        """
        Create visualization based on natural language description.
        
        Args:
            df (pd.DataFrame): Data to visualize
            query_string (str): Visualization description
            save_path (str, optional): Path to save the visualization
            show (bool): Whether to display the visualization
            **kwargs: Additional visualization parameters
            
        Returns:
            matplotlib.figure.Figure: Created figure
        """
        query_string = query_string.lower()
        
        # Determine plot type
        if 'scatter' in query_string or 'vs' in query_string:
            return self._create_scatter_plot(df, query_string, save_path, show, **kwargs)
        elif 'bar' in query_string or 'compare' in query_string:
            return self._create_bar_plot(df, query_string, save_path, show, **kwargs)
        elif 'histogram' in query_string or 'distribution' in query_string:
            return self._create_histogram(df, query_string, save_path, show, **kwargs)
        elif 'bubble' in query_string:
            return self._create_bubble_chart(df, query_string, save_path, show, **kwargs)
        else:
            # Default to scatter plot
            return self._create_scatter_plot(df, query_string, save_path, show, **kwargs)
    
    def _create_scatter_plot(self, df, query_string, save_path=None, show=True, **kwargs):
        """
        Create a scatter plot based on query description.
        """
        # Extract x and y variables
        vs_match = re.search(r'([a-z\s]+)\s+vs\s+([a-z\s]+)', query_string)
        if vs_match:
            x_var = vs_match.group(1).strip()
            y_var = vs_match.group(2).strip()
        else:
            # Default to ROE vs Beta if pattern not found
            x_var = 'returnOnEquity'
            y_var = 'beta'
            
        # Extract color variable if specified
        color_var = None
        color_match = re.search(r'colou?red by\s+([a-z\s]+)', query_string)
        if color_match:
            color_var = color_match.group(1).strip()
            
        # Create plot
        plt.figure(figsize=kwargs.get('figsize', (10, 6)))
        sns.scatterplot(data=df, x=x_var, y=y_var, hue=color_var)
        plt.title(f"{y_var} vs {x_var}" + (f" by {color_var}" if color_var else ""))
        
        if save_path:
            plt.savefig(save_path)
        if show:
            plt.show()
            
        return plt.gcf()
    
    def _create_bar_plot(self, df, query_string, save_path=None, show=True, **kwargs):
        """
        Create a bar plot based on query description.
        """
        # Extract variable and group by
        compare_match = re.search(r'compare\s+([a-z\s]+)\s+across\s+([a-z\s]+)', query_string)
        if compare_match:
            value_var = compare_match.group(1).strip()
            group_var = compare_match.group(2).strip()
        else:
            # Default to P/E ratios across sectors
            value_var = 'trailingPE'
            group_var = 'sector'
            
        # Create plot
        plt.figure(figsize=kwargs.get('figsize', (12, 6)))
        sns.barplot(data=df, x=group_var, y=value_var)
        plt.title(f"Comparison of {value_var} by {group_var}")
        plt.xticks(rotation=45)
        
        if save_path:
            plt.savefig(save_path)
        if show:
            plt.show()
            
        return plt.gcf()
    
    def _create_histogram(self, df, query_string, save_path=None, show=True, **kwargs):
        """
        Create a histogram based on query description.
        """
        # Extract variable
        dist_match = re.search(r'distribution of\s+([a-z\s]+)', query_string)
        if dist_match:
            var = dist_match.group(1).strip()
        else:
            # Default to profit margins
            var = 'profitMargins'
            
        # Create plot
        plt.figure(figsize=kwargs.get('figsize', (10, 6)))
        sns.histplot(data=df, x=var, bins=kwargs.get('bins', 20))
        plt.title(f"Distribution of {var}")
        
        if save_path:
            plt.savefig(save_path)
        if show:
            plt.show()
            
        return plt.gcf()
    
    def _create_bubble_chart(self, df, query_string, save_path=None, show=True, **kwargs):
        """
        Create a bubble chart based on query description.
        """
        # Extract variables
        bubble_match = re.search(r'([a-z\s]+)\s+vs\s+([a-z\s]+)\s+colou?red by\s+([a-z\s]+)', query_string)
        if bubble_match:
            x_var = bubble_match.group(1).strip()
            y_var = bubble_match.group(2).strip()
            color_var = bubble_match.group(3).strip()
            size_var = kwargs.get('size_var', 'marketCap')
        else:
            # Default to ROE vs Beta colored by sector
            x_var = 'returnOnEquity'
            y_var = 'beta'
            color_var = 'sector'
            size_var = 'marketCap'
            
        # Create plot
        plt.figure(figsize=kwargs.get('figsize', (12, 8)))
        scatter = sns.scatterplot(
            data=df,
            x=x_var,
            y=y_var,
            hue=color_var,
            size=size_var,
            sizes=(20, 200),
            alpha=0.6
        )
        plt.title(f"Bubble Chart: {y_var} vs {x_var} (Size: {size_var}, Color: {color_var})")
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        if save_path:
            plt.savefig(save_path, bbox_inches='tight')
        if show:
            plt.show()
            
        return plt.gcf()