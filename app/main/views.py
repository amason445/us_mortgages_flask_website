"""
This script contains the view rendering functions. It renders Jinja2 templates using HTML, CSS and the other modules.
For the HTML templates, it accesses the templated folder and renders them. The CSS is stored in static.
Finally, this script also acts at the hyperlink architecture for the website.
Each route function serves one web page or a download link.
To write the HTML, CSS and route functions, I used a combination of online research, OpenAI's ChatGPT and Miguel Grinberg's Flask Web Development: Developing Web Applications with Python.
I still had to customize each HTML template, the CSS and the route functions to access the models.
Additionally, I used the below color pallette in the CSS.
https://colorhunt.co/palette/f3eeeaebe3d5b0a695776b5d
"""

from . import main
from app import visualizations as vis
from app import dashboards as dbs
from app import csv_export as csv_exp
from app import utilities as utl
from flask import render_template, Response, request, redirect, url_for

# initial landing page
@main.route('/')
def index():
    return  render_template('index.html')

# this was a demo page I created to initially learn flask and its hyperlink paramterization.
@main.route('/sky_color/<color>')
def sky_color(color):
    return render_template('sky_color.html', color = color)

# this page contains my project references for this project
@main.route('/references/', endpoint = 'references')
def references_page():
    return render_template('references.html')

# this page is a demo page I wrote during week 2
@main.route('/state_level/dummy_data', endpoint = 'dummy_data')
def dummy_data():

    state = 'DEMO_PAGE'

    plot = vis.dummy_plot()

    return render_template('visualization_template.html', state = state, plot = plot)

# this acts as a download link for the demo data
@main.route('/state_level/download_dummy_csv', endpoint = 'dummy_csv')
def download_dummy_data():

    raw_data = csv_exp.generate_dummy_csv()

    return Response(raw_data, content_type= 'text/csv', headers={'Content-Disposition': 'attachment; filename=dummy_data.csv'})

# this link acts as a download link for the state data
@main.route('/state_level/<state>/state_averages_csv', endpoint = 'averages_csv')
def download_state_averages(state):

    raw_data = csv_exp.mortgage_averages(state_name=state)

    return Response(raw_data, content_type= 'text/csv', headers={'Content-Disposition': f'attachment; filename={state}_data.csv'})


# this link renders and serves the state time series pages
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


# this link renders and servers the state geography dashboard page
# it contains a post request that allows the user to render state dashboards
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
    