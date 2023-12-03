from . import main
from app import visualizations as vis
from app import dashboards as dbs
from app import csv_export as csv_exp
from app import utilities as utl
from flask import render_template, Response, request, redirect, url_for

@main.route('/')
def index():
    return  render_template('index.html')

@main.route('/sky_color/<color>')
def sky_color(color):
    return render_template('sky_color.html', color = color)

@main.route('/references/', endpoint = 'references')
def references_page():
    return render_template('references.html')

@main.route('/state_level/dummy_data', endpoint = 'dummy_data')
def dummy_data():

    state = 'DEMO_PAGE'

    plot = vis.dummy_plot()

    return render_template('visualization_template.html', state = state, plot = plot)

@main.route('/state_level/download_dummy_csv', endpoint = 'dummy_csv')
def download_dummy_data():

    raw_data = csv_exp.generate_dummy_csv()

    return Response(raw_data, content_type= 'text/csv', headers={'Content-Disposition': 'attachment; filename=dummy_data.csv'})

@main.route('/state_level/<state>/state_averages_csv', endpoint = 'averages_csv')
def download_state_averages(state):

    raw_data = csv_exp.mortgage_averages(state_name=state)

    return Response(raw_data, content_type= 'text/csv', headers={'Content-Disposition': f'attachment; filename={state}_averages_data.csv'})


@main.route('/state_level/<state>', endpoint = 'state_data')
def state_level(state):

    state = state

    state_long_name = utl.state_abbreviation_mapping(state)

    loan_volume_plot = vis.state_loan_volumes(state)
    loan_amount_plot = vis.state_loan_amounts(state)
    interest_plot = vis.state_interest_rates(state)
    ltv_plot = vis.state_ltvs(state)

    return render_template('state_pages.html', state = state, loan_volume_plot = loan_volume_plot, loan_amount_plot = loan_amount_plot,
                           interest_plot = interest_plot, state_long_name = state_long_name, ltv_plot = ltv_plot)


@main.route('/state_geography/', methods = ['GET', 'POST'], endpoint = 'state_geo')
def state_geo():
    if request.method == 'POST':
        state_name = request.form.get('state')
        year = request.form.get('year')
        loan_term = request.form.get('loan_term')
        datapoint = request.form.get('datapoint')

        m = dbs.geo_dashboard(state_name= state_name, year= year, loan_term= loan_term, datapoint= datapoint)

        map_html = m.get_root().render()

        return render_template('state_geo.html', map_html= map_html)
    
    return render_template('state_geo.html')
    