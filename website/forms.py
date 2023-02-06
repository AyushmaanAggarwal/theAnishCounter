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
    name = StringField("Name of Course", validators=[DataRequired()],
                       render_kw={'class': 'form-control', 'placeholder': 'Course Name'})
    url_link = TextAreaField("Course Link", validators=[DataRequired()],
                             render_kw={'class': 'form-control', 'placeholder': 'Course Link'})
    submit = SubmitField('Submit')


class AddSection(FlaskForm):
    week_days = MultiCheckboxField("Week Days", choices=days_of_week,
                                   render_kw={'class': 'form-control'})
    start_time = TimeField("Start Time", validators=[DataRequired()],
                           render_kw={'class': 'form-control'})
    end_time = TimeField("End Time", validators=[DataRequired()],
                         render_kw={'class': 'form-control'})
    location = StringField("Location",
                           render_kw={'class': 'form-control', 'placeholder': 'Location (Optional)'})
    description = StringField("Description", validators=[DataRequired()],
                              render_kw={'class': 'form-control', 'placeholder': 'Section Type'})
    submit = SubmitField('Submit')
