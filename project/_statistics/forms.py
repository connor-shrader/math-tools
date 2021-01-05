from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, FormField, FieldList, FloatField, HiddenField
from wtforms.validators import DataRequired, Optional
from wtforms import ValidationError

class CoordinateForm(FlaskForm):
    x_coordinate = FloatField('x', validators=[Optional()])
    y_coordinate = FloatField('y', validators=[Optional()])

    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False
        FlaskForm.__init__(self, *args, **kwargs)

class LinearRegressionForm(FlaskForm):
    coordinates = FieldList(FormField(CoordinateForm), min_entries = 2, max_entries=1000)

    # This field will be set to true after the form is created, and will
    # always stay true. The purpose of this field is to create 9 extra
    # coordinate forms after the form is initialized.
    form_initialized = HiddenField() 
    data_json = HiddenField()

    add_entry = SubmitField('Add row')
    remove_entry = SubmitField('Remove row')
    clear = SubmitField('Clear')
    submit = SubmitField('Calculate')

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)

        # Adds 8 more entries when the form is first created.
        if not self.form_initialized.data:
            for i in range(0, 8):
                self.coordinates.append_entry()
            self.form_initialized.data = 'True'
        
