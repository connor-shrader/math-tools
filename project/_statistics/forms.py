from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, FormField, FieldList, DecimalField, HiddenField
from wtforms.validators import DataRequired, Optional
from wtforms import ValidationError

class CoordinateForm(FlaskForm):
    x_coordinate = DecimalField('x', validators=[Optional()])
    y_coordinate = DecimalField('y', validators=[Optional()])

    def validate(self):
        if not FlaskForm.validate(self):
            return False

        x = self.x_coordinate.data
        y = self.y_coordinate.data

        if (x and not y) or (y and not x):
            return False

        return True

    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False
        FlaskForm.__init__(self, *args, **kwargs)

class LinearRegressionForm(FlaskForm):
    coordinates = FieldList(FormField(CoordinateForm), min_entries = 1, max_entries=100)
    plot_success = HiddenField('False')
    plot_json = HiddenField()

    add_entry = SubmitField('Add entry')
    remove_entry = SubmitField('Remove entry')
    submit = SubmitField('Submit')
        
