from flask_wtf import FlaskForm
from wtforms import StringField, DateField
from wtforms.validators import DataRequired, Length


class FeatureForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=20)])
    description = StringField('Description', validators=[DataRequired()])
    client = StringField('Client', validators=[DataRequired()])
    client_priority = StringField('ClientPriority', validators=[DataRequired()])
    targetDate = DateField('TargetDate', validators=[DataRequired()], format='%Y-%m-%d')
    productArea = StringField('ProductArea', validators=[DataRequired()])
