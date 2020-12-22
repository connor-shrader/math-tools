import simplejson as json
from io import StringIO, BytesIO

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def validate_inputs():
    pass

def process_coordinates(coordinates):
    '''
    This function inputs the coordinates field in the LinearRegressionForm
    and outputs the tuple (data_json, partial_entry_count):

    -   data_json is a json string containing the values of all of the valid
        ordered pairs that were passed into this function. This json string will
        be used to generate the plot.
    -   partial_entry_count is the number of coordinate fields that only
        had one entry (and so they were missing a value). This information
        is used to alert the user that their input was faulty.
    '''
    data = {'x': [], 'y': []}
    entry_count = 0
    partial_entry_count = 0
    for entry in coordinates:
        x = entry.x_coordinate.data
        y = entry.y_coordinate.data
        if x and y:
            # The coordinate is valid, so we add it to the data dictionary
            data['x'].append(x)
            data['y'].append(y)
        elif x or y:
            # The coordinate is invalid. We note this so we can flash it to
            # the user later
            partial_entry_count += 1

    return data, partial_entry_count

def json_to_dataframe(data_json):
    data = json.load(StringIO(data_json))
    df = pd.DataFrame(data = data)
    return df

def compute_linear_fit(data):
    df = pd.DataFrame(data = data)
    x_variance, y_variance = df.var()
    covariance = df.cov()['x'].loc['y']

    beta = covariance / x_variance
    alpha = df['y'].mean() - beta * df['x'].mean()
    
    if y_variance != 0:
        r = covariance / np.sqrt(x_variance * y_variance)
    else:
        # All the y-values are the same, so the correlation is perfect.
        r = 1

    r2 = r ** 2

    print(r2)
    return alpha, beta, r2

def format_best_fit(alpha, beta):
    return_string = 'y = '

    if beta < 0:
        return_string += '- '
        beta = -1 * beta
    
    if beta != 0:
        return_string += (str(round(beta, 5)) + 'x')

    if alpha < 0:
        return_string += ' - '
        alpha = -1 * alpha
    elif alpha > 0 and beta != 0:
        return_string += ' + '
    
    if alpha != 0:
        return_string += str(round(alpha, 5))

    return return_string

def plot_data(df, alpha, beta):
    fig, axes = plt.subplots(figsize = (2, 2))
    axes.set_xlabel('x')
    axes.set_ylabel('y')

    # Scatterplot
    sns.scatterplot(
        data = df,
        x = 'x',
        y = 'y',
        ax = axes,
        color = 'black',
        s = 5               # marker size
    )
    
    # Linear Fit
    lower_x = df['x'].min()
    upper_x = df['x'].max()

    lower_plot = lower_x - 0.1 * (upper_x - lower_x)
    upper_plot = upper_x + 0.1 * (upper_x - lower_x)

    axes.plot(
        [lower_plot, upper_plot],
        [alpha + lower_plot * beta, alpha + upper_plot * beta],
        linewidth = 0.5
    )

    axes.set_xlim(lower_plot, upper_plot)
    strIO = BytesIO()
    plt.savefig(strIO, dpi=300, bbox_inches='tight')
    return strIO