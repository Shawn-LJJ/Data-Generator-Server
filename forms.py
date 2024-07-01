from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, NumberRange
from flask_wtf.file import FileAllowed, FileField, FileRequired

class DataForm(FlaskForm):
    customerRows = IntegerField('Number of customers', validators=[DataRequired(), NumberRange(10, 50_000)])
    merchantRows = IntegerField('Number of merchants', validators=[DataRequired(), NumberRange(10, 10_000)])
    foreignMerchantPercent = IntegerField('Percentage of foreign physical merchants (%)', validators=[DataRequired(), NumberRange(1, 90)])
    onlineMerchantPercent = IntegerField('Percentage of online merchants (%)', validators=[DataRequired(), NumberRange(1, 90)])
    twoCCPercent = IntegerField('Percentage of customers with two credit cards (%)', validators=[DataRequired(), NumberRange(0, 100)])
    submit = SubmitField('Generate')

class ArchiveForm(FlaskForm):
    savedData = SelectField('Select any ZIP file and click retrieve to download', validators=[DataRequired()])
    retrieve = SubmitField('Retrieve')
    delete = SubmitField('Delete')

class SaveForm(FlaskForm):
    zipFile = FileField('Upload zip file', validators=[
        FileAllowed(['zip'], 'Please upload zip file only!'),
        FileRequired('Please upload a zip file!')])
    submit = SubmitField('Save')