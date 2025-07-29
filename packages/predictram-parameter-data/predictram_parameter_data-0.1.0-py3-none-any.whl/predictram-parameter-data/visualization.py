# predictram-parameter-data/visualization.py
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def create_visualization(visualization_string, stocks=None):
    """
    Create a visualization based on the description
    
    Args:
        visualization_string (str): Description of the visualization
        stocks (list): Optional list of stocks to visualize
        
    Returns:
        matplotlib.figure.Figure: The generated figure
    """
    # Parse the visualization string
    if 'scatter' in visualization_string.lower():
        return create_scatter_plot(visualization_string, stocks)
    elif 'bar' in visualization_string.lower():
        return create_bar_chart(visualization_string, stocks)
    elif 'histogram' in visualization_string.lower():
        return create_histogram(visualization_string, stocks)
    else:
        raise ValueError("Unsupported visualization type")

def create_scatter_plot(visualization_string, stocks):
    """
    Create a scatter plot based on the description
    
    Args:
        visualization_string (str): Description of the scatter plot
        stocks (list): List of stocks to plot
        
    Returns:
        matplotlib.figure.Figure: The generated figure
    """
    # Extract x and y axes from the string
    parts = visualization_string.lower().split()
    x_axis = None
    y_axis = None
    
    for i, part in enumerate(parts):
        if part == 'vs' and i > 0 and i < len(parts)-1:
            x_axis = parts[i-1]
            y_axis = parts[i+1]
            break
    
    if not x_axis or not y_axis:
        raise ValueError("Could not parse axes from visualization string")
    
    # Get the data
    df = pd.DataFrame(stocks)
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=df, x=x_axis, y=y_axis, hue='sector', ax=ax)
    ax.set_title(f"{y_axis} vs {x_axis}")
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    return fig

def create_bar_chart(visualization_string, stocks):
    """
    Create a bar chart based on the description
    
    Args:
        visualization_string (str): Description of the bar chart
        stocks (list): List of stocks to plot
        
    Returns:
        matplotlib.figure.Figure: The generated figure
    """
    # Extract the metric to plot
    metric = visualization_string.lower().replace('bar chart of', '').strip()
    
    # Get the data
    df = pd.DataFrame(stocks)
    
    # Sort and limit to top 20
    df = df.sort_values(by=metric, ascending=False).head(20)
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=df, x='shortName', y=metric, ax=ax)
    ax.set_title(f"Bar Chart of {metric}")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    plt.tight_layout()
    
    return fig

def create_histogram(visualization_string, stocks):
    """
    Create a histogram based on the description
    
    Args:
        visualization_string (str): Description of the histogram
        stocks (list): List of stocks to plot
        
    Returns:
        matplotlib.figure.Figure: The generated figure
    """
    # Extract the metric to plot
    metric = visualization_string.lower().replace('histogram of', '').strip()
    
    # Get the data
    df = pd.DataFrame(stocks)
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(data=df, x=metric, kde=True, ax=ax)
    ax.set_title(f"Histogram of {metric}")
    plt.tight_layout()
    
    return fig