from . import main
from app import visualizations as vis
from app import csv_export as csv_exp
from app import utilities as utl
from flask import render_template, Response

@main.route('/')
def index():
    return  render_template('index.html')

@main.route('/sky_color/<color>')
def sky_color(color):
    return render_template('sky_color.html', color = color)

@main.route('/state_level/dummy_data', endpoint = 'dummy_data')
def dummy_data():

    state = 'DEMO_PAGE'

    plot = vis.dummy_plot()

    return render_template('visualization_template.html', state = state, plot = plot)

@main.route('/state_level/download_dummy_csv', endpoint = 'dummy_csv')
def download_dummy_data():

    raw_data = csv_exp.generate_dummy_csv()

    return Response(raw_data, content_type= 'text/csv', headers={'Content-Disposition': 'attachment; filename=dummy_data.csv'})

@main.route('/state_level/<state>', endpoint = 'state_data')
def state_level(state):

    state_long_name = utl.state_abbreviation_mapping(state)

    loan_volume_plot = vis.state_loan_volumes(state)
    interest_plot = vis.state_interest_rates(state)

    return render_template('state_pages.html', state = state, loan_volume_plot = loan_volume_plot, interest_plot = interest_plot, state_long_name = state_long_name)