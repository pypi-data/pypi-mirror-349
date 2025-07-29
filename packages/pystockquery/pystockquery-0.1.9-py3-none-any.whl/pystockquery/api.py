import pandas as pd
from .query_parser import QueryParser
from .data_handler import DataHandler
from .visualization import Visualizer

class StockQueryAPI:
    def __init__(self, data_path=None):
        """
        Initialize the StockQueryAPI with optional custom data path.
        
        Args:
            data_path (str, optional): Path to the Excel data file. Defaults to package data.
        """
        self.data_handler = DataHandler(data_path)
        self.parser = QueryParser()
        self.visualizer = Visualizer()
        self.df = self.data_handler.load_data()
        
    def query(self, query_string, top_n=None):
        """
        Execute a query against the stock data.
        
        Args:
            query_string (str): Natural language query string
            top_n (int, optional): Number of top results to return
            
        Returns:
            pd.DataFrame: Filtered and sorted results
        """
        conditions, sort_by, ascending = self.parser.parse_query(query_string)
        
        # Apply conditions
        result = self.df.copy()
        for condition in conditions:
            result = result.query(condition)
            
        # Sort results
        if sort_by:
            result = result.sort_values(by=sort_by, ascending=ascending)
            
        # Limit results
        if top_n:
            result = result.head(top_n)
            
        return result
    
    def visualize(self, query_string, save_path=None, show=True, **kwargs):
        """
        Generate visualizations based on the query.
        
        Args:
            query_string (str): Visualization description
            save_path (str, optional): Path to save the visualization
            show (bool): Whether to display the visualization
            **kwargs: Additional visualization parameters
        """
        return self.visualizer.create_visualization(self.df, query_string, save_path, show, **kwargs)
    
    def export(self, query_string, output_path, format='excel', **kwargs):
        """
        Export query results to a file.
        
        Args:
            query_string (str): Query to execute
            output_path (str): Path to save the results
            format (str): Output format ('excel', 'csv', 'json')
            **kwargs: Additional export parameters
        """
        result = self.query(query_string)
        
        if format == 'excel':
            result.to_excel(output_path, **kwargs)
        elif format == 'csv':
            result.to_csv(output_path, **kwargs)
        elif format == 'json':
            result.to_json(output_path, **kwargs)
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def get_available_metrics(self):
        """
        Return a list of available metrics/columns in the dataset.
        
        Returns:
            list: Available metrics
        """
        return sorted(self.df.columns.tolist())