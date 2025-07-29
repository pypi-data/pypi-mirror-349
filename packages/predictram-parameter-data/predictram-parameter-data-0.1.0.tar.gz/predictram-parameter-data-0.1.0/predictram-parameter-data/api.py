# predictram-parameter-data/api.py
from .query_parser import parse_query
from .data_handler import filter_stocks, get_stock_data
from .visualization import create_visualization
import pandas as pd

def query(query_string, limit=20):
    """
    Query stocks based on the provided criteria
    
    Args:
        query_string (str): The query string (e.g., "CAGR > 15% and ROE > 20%")
        limit (int): Maximum number of results to return
        
    Returns:
        list: List of stocks matching the criteria
    """
    conditions = parse_query(query_string)
    filtered_stocks = filter_stocks(conditions)
    return filtered_stocks[:limit]

def visualize(visualization_string, stocks=None):
    """
    Generate a visualization based on the provided specification
    
    Args:
        visualization_string (str): Description of visualization to create
        stocks (list): Optional list of stocks to visualize
        
    Returns:
        matplotlib.figure.Figure: The generated figure
    """
    return create_visualization(visualization_string, stocks)

def export(query_string, filename, format='xlsx'):
    """
    Export query results to a file
    
    Args:
        query_string (str): The query to execute
        filename (str): Output filename
        format (str): Export format ('xlsx' or 'csv')
    """
    results = query(query_string)
    df = pd.DataFrame(results)
    
    if format == 'xlsx':
        df.to_excel(filename, index=False)
    elif format == 'csv':
        df.to_csv(filename, index=False)
    else:
        raise ValueError("Unsupported format. Use 'xlsx' or 'csv'")