from flask import render_template, url_for, redirect, request, Blueprint, request, flash
from project._statistics.forms import LinearRegressionForm
from flask import Blueprint, render_template, redirect, url_for, send_file

from .linear_regression import process_coordinates, json_to_dataframe, plot_data

statistics = Blueprint('statistics', __name__, template_folder='templates/_statistics')

@statistics.route('/linear-regression', methods=['GET', 'POST'])
def linear_regression():
    form = LinearRegressionForm()

    data_json = form.data_json.data
    scroll = None

    if form.add_entry.data:
        form.coordinates.append_entry()
        scroll = 'coordinates-{}-x_coordinate'.format(len(form.coordinates) - 1)

    elif form.remove_entry.data:
        form.coordinates.pop_entry()

    elif form.clear.data:
        # Resets the form, but preserves the data_json field
        # (so that the image does not go away)
        data_json = form.data_json.data
        form = LinearRegressionForm(formdata=None)
        form.data_json.data = data_json

    elif form.submit.data:
        form.data_json.data, partial_entry_count = process_coordinates(form.coordinates)
        
        if partial_entry_count > 1:
            flash('Several of your ordered pairs are missing one of their coordinates, so they were ignored.')
        elif partial_entry_count == 1:
            flash('One of your ordered pairs is missing one of its coordinates, so it was ignored.')

    return render_template('linear-regression.html',
                            form = form, 
                            length = len(form.coordinates),
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
    df = json_to_dataframe(data_json)
    strIO = plot_data(df)
    print(strIO)
    strIO.seek(0)
    return send_file(strIO, mimetype='image/png')
