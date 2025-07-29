# predictram_parameter_data/data_handler.py
import json
import os
from pathlib import Path

# Load the data
DATA_FILE = Path(__file__).parent / 'data' / 'all_stocks.json'
STOCK_DATA = None

def load_data():
    """
    Load the stock data from JSON file
    
    Returns:
        dict: The loaded stock data
    """
    global STOCK_DATA
    if STOCK_DATA is None:
        with open(DATA_FILE, 'r') as f:
            STOCK_DATA = json.load(f)
    return STOCK_DATA

def filter_stocks(conditions):
    """
    Filter stocks based on the provided conditions
    
    Args:
        conditions (list): List of conditions from parse_query
        
    Returns:
        list: List of stocks that match all conditions
    """
    data = load_data()
    results = []
    
    for symbol, stock in data.items():
        matches_all = True
        
        for condition in conditions:
            metric = condition['metric']
            json_key = condition['json_key']
            operator = condition['operator']
            target_value = condition['value']
            
            # Get the actual value from the stock data
            try:
                # Handle nested keys if needed
                keys = json_key.split('.')
                value = stock
                for key in keys:
                    value = value.get(key, None)
                    if value is None:
                        break
            except (KeyError, AttributeError):
                matches_all = False
                break
                
            if value is None:
                matches_all = False
                break
                
            # Apply the condition
            if operator == '>':
                if not (value > target_value):
                    matches_all = False
                    break
            elif operator == '<':
                if not (value < target_value):
                    matches_all = False
                    break
            elif operator == '>=':
                if not (value >= target_value):
                    matches_all = False
                    break
            elif operator == '<=':
                if not (value <= target_value):
                    matches_all = False
                    break
            elif operator == '=' or operator == '==':
                if not (value == target_value):
                    matches_all = False
                    break
            elif operator == '!=':
                if not (value != target_value):
                    matches_all = False
                    break
            elif operator in ('contains', 'like'):
                if not (str(target_value).lower() in str(value).lower()):
                    matches_all = False
                    break
            else:
                matches_all = False
                break
                
        if matches_all:
            results.append(stock)
    
    return results

def get_stock_data(symbol):
    """
    Get data for a specific stock symbol
    
    Args:
        symbol (str): The stock symbol to look up
        
    Returns:
        dict: The stock data or None if not found
    """
    data = load_data()
    return data.get(symbol, None)