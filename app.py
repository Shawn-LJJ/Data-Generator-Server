from flask import Flask, render_template, redirect, url_for, send_file, flash, request
from flask_cors import CORS
import pandas as pd
import os
from forms import DataForm, ArchiveForm, SaveForm
from functions.get_mockaroo import main as get_mockaroo_data
from functions.customer import main as cust_transformer
from functions.merchant import main as merc_transformer
from functions.address import main as address_maker
from functions.credit_card import main as cc_transformer
from functions.write_zip import main as zip_writter

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24).hex()
CORS(app)

os.makedirs('./zip', exist_ok=True) # making sure the zip directory is there to store zip data

def get_zips():
    return [f for f in os.listdir('./zip') if f.endswith('.zip')]

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
@app.route('/home', methods=['GET'])
def home():
    data_form = DataForm()
    archive_form = ArchiveForm()
    save_form = SaveForm()
    archive_form.savedData.choices = get_zips()
    return render_template('index.html', data_form=data_form, archive_form=archive_form, save_form=save_form)

@app.route('/generate', methods=['POST'])
def user_input():
    form = DataForm()
    if form.validate_on_submit():
        cust_df = get_mockaroo_data('customer', form.customerRows.data)
        merc_df = get_mockaroo_data('merchant', form.merchantRows.data)
        cc_df = get_mockaroo_data('credit_card', len(cust_df) + round(len(cust_df) * form.twoCCPercent.data / 100))

        cust_df = cust_transformer(cust_df)
        merc_df = merc_transformer(merc_df)
        add_df = address_maker(cust_df, merc_df, form.foreignMerchantPercent.data, form.onlineMerchantPercent.data)
        banks_list = merc_df[merc_df['merchant_category'] == 'Bank'].values[:,2]
        cc_df = cc_transformer(cc_df, len(cust_df), banks_list)

        zip_file = zip_writter(cust_df, merc_df, add_df, cc_df)
        return send_file(zip_file, as_attachment=True)
    return redirect(url_for('home'))

@app.route('/archive', methods=['POST'])
def archive():
    form = ArchiveForm()
    form.savedData.choices = get_zips()
    if form.validate_on_submit():

        file_path = f'./zip/{form.savedData.data}'

        if form.retrieve.data:
            if os.path.isfile(file_path):
                return send_file(file_path, as_attachment=True)
            flash('Zip file does not exists', 'error')

        elif form.delete.data:
            if not os.path.isfile(file_path):
                flash('Zip file does not exists', 'error')
            else:
                os.remove(file_path)

    return redirect(url_for('home'))

@app.route('/save', methods=['POST'])
def save():
    form = SaveForm()
    if form.validate_on_submit():
        file = request.files['zipFile']
        file_path = f'./zip/{file.filename}'
        file.save(file_path)
    else:
        flash([str(error) for error in form.errors.values()], 'error')
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run()