import simplejson as json
from io import StringIO, BytesIO

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

        data_json = json.dumps(data)

    return data_json, partial_entry_count

def json_to_dataframe(data_json):
    data = json.load(StringIO(data_json))
    df = pd.DataFrame(data = data)
    return df

def plot_data(df):
    fig, axes = plt.subplots(figsize = (2, 2))
    axes.set_xlabel('x')
    axes.set_ylabel('y')
    sns.regplot(data = df,
                x='x',
                y='y',
                ax=axes,
                ci=None,
                scatter_kws={'color': 'black'},
                line_kws={'color': 'red'})
    strIO = BytesIO()
    plt.savefig(strIO, dpi=300, bbox_inches='tight')
    return strIO