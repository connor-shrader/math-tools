from flask import render_template, url_for, redirect, request, Blueprint, request, flash
from project._statistics.forms import LinearRegressionForm
import simplejson as json
from flask import Blueprint, render_template, redirect, url_for, send_file

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from io import BytesIO, StringIO
import base64

statistics = Blueprint('statistics', __name__, template_folder='templates/_statistics')


@statistics.route('/linear-regression', methods=['GET', 'POST'])
def linear_regression():
    form = LinearRegressionForm()

    length = len(form.coordinates.entries)
    data_json = None
    data = {'x': [], 'y': []}
    scroll = None
    entry_count = 0
    partial_entry_count = 0

    if form.add_entry.data:
        form.coordinates.append_entry()
        length += 1
        scroll = 'coordinates-{}-x_coordinate'.format(length - 1)

    elif form.remove_entry.data:
        form.coordinates.pop_entry()
        length -= 1

    elif form.clear.data:
        data_json = form.data_json.data
        form = LinearRegressionForm(formdata=None)
        form.data_json.data = data_json

    elif form.validate_on_submit():
        for entry in form.coordinates.entries:
            x = entry.x_coordinate.data
            y = entry.y_coordinate.data
            if x and y:
                data['x'].append(x)
                data['y'].append(y)
                entry_count += 1
            elif x or y:
                partial_entry_count += 1

    data_json = json.dumps(data)
    form.data_json.data = data_json

    if partial_entry_count > 1:
        flash('Several of your ordered pairs are missing one of their coordinates, so they were ignored.')
    elif partial_entry_count == 1:
        flash('One of your ordered pairs is missing one of its coordinates, so it was ignored.')

    return render_template('linear-regression.html',
                            form = form, 
                            length = length,
                            data_json = data_json,
                            scroll = scroll)

# @statistics.route('/test_img', methods=['GET', 'POST'])
# def test_image():
#     scalar = float(request.args.get('scalar'))
#     print(type(scalar))
#     fig = plt.figure(figsize=(1,1), dpi=300)
#     axes = fig.add_axes([0, 0, 1, 1])
#     x = np.linspace(0, 10, 101)
#     y = x ** scalar
#     axes.plot(x,y)
    
#     strIO = BytesIO()
#     plt.savefig(strIO, dpi=fig.dpi)
#     strIO.seek(0)
#     return send_file(strIO, mimetype='image/png')

@statistics.route('/linear-regression/plot', methods=['GET', 'POST'])
def linear_regression_plot():
    data_json = request.args.get('data_json')
    data = json.load(StringIO(data_json))
    df = pd.DataFrame(data = data)

    fig = plt.figure()
    axes = fig.add_axes([0, 0, 1, 1])
    fig.set_size_inches(2, 2)
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
    strIO.seek(0)
    return send_file(strIO, mimetype='image/png')
