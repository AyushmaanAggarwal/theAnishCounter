from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, RadioField, DateField, IntegerField, \
    SelectMultipleField, widgets, FloatField, TimeField, DateTimeField
from wtforms.validators import DataRequired, Length


class MultiCheckboxField(SelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.

    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.
    """
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


days_of_week = ['Mo', 'Tu', 'We', 'Th', 'Fr']


class CourseForm(FlaskForm):
    name = StringField("Name of Course", validators=[DataRequired()])
    url_link = TextAreaField("Course Link", validators=[DataRequired()])
    submit = SubmitField('Submit')


class AddSection(FlaskForm):
    week_days = MultiCheckboxField("Week Days", validators=[DataRequired()], choices=days_of_week)
    start_time = TimeField("Start Time", validators=[DataRequired()])
    end_time = TimeField("End Time", validators=[DataRequired()])
    location = StringField("Location", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()])
    submit = SubmitField('Submit')
