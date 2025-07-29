import pandas as pd
import os
from pathlib import Path

class DataHandler:
    def __init__(self, data_path=None):
        """
        Initialize the data handler with optional custom data path.
        
        Args:
            data_path (str, optional): Path to custom data file. Defaults to package data.
        """
        self.data_path = data_path
        
    def load_data(self):
        """
        Load the stock data from Excel file.
        
        Returns:
            pd.DataFrame: Loaded stock data
        """
        if self.data_path:
            if not os.path.exists(self.data_path):
                raise FileNotFoundError(f"Data file not found: {self.data_path}")
            df = pd.read_excel(self.data_path)
        else:
            # Load package default data
            package_dir = Path(__file__).parent
            default_data_path = package_dir / 'data' / 'merged_stock_data.xlsx'
            if not default_data_path.exists():
                raise FileNotFoundError("Default data file not found in package")
            df = pd.read_excel(default_data_path)
            
        # Clean column names
        df.columns = df.columns.str.strip()
        
        return df