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
    print(form.plot_success.data)
    plot_generated = False
    data = {'x': [], 'y': []}
    data_json = None

    if form.add_entry.data:
        form.coordinates.append_entry()

    elif form.remove_entry.data:
        form.coordinates.pop_entry()

    elif form.validate_on_submit():
        print('validated')
        for entry in form.coordinates.entries:
            x = entry.x_coordinate.data
            y = entry.y_coordinate.data
            if x and y:
                data['x'].append(x)
                data['y'].append(y)
        plot_generated = True
        data_json = json.dumps(data)
        form.plot_success.data = 'True'
        form.plot_json.data = data_json
        print('hi', form.plot_json.data)

    return render_template('linear-regression.html',
                            form = form, 
                            length = len(form.coordinates.entries),
                            plot_generated = plot_generated,
                            data_json = data_json)

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
    print(data_json, "hi")
    data = json.load(StringIO(data_json))
    print(data)
    df = pd.DataFrame(data = data)
    print(df)

    fig = plt.figure()
    axes = fig.add_axes([0, 0, 1, 1])
    fig.tight_layout()
    fig.set_size_inches(2, 2)
    sns.scatterplot(data = data, x='x', y='y', ax=axes, s=10)
    strIO = BytesIO()
    plt.savefig(strIO, dpi=300, bbox_inches='tight')
    strIO.seek(0)
    return send_file(strIO, mimetype='image/png')
