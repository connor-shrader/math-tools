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
    count = 0
    scroll = None

    if form.add_entry.data:
        form.coordinates.append_entry()
        length += 1
        scroll = 'coordinates-{}-x_coordinate'.format(length - 1)

    elif form.remove_entry.data:
        form.coordinates.pop_entry()
        length -= 1

    elif form.clear.data:
        return redirect(url_for('statistics.linear_regression'))

    elif form.validate_on_submit():
        print('validated')
        data = {'x': [], 'y': []}
        for entry in form.coordinates.entries:
            x = entry.x_coordinate.data
            y = entry.y_coordinate.data
            if x and y:
                data['x'].append(x)
                data['y'].append(y)
            elif x or y:
                count += 1
            data_json = json.dumps(data)
            form.plot_json.data = data_json

    if count > 1:
        flash('Several failed')
    elif count == 1:
        flash('One fail')

    print(length)
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
    sns.regplot(data = df, x='x', y='y', ax=axes)
    strIO = BytesIO()
    plt.savefig(strIO, dpi=300, bbox_inches='tight')
    strIO.seek(0)
    return send_file(strIO, mimetype='image/png')
