from . import main
from . import visualizations as vis
from . import csv_export as csv_exp
from flask import render_template, Response

@main.route('/')
def index():
    return  render_template('index.html')

@main.route('/sky_color/<color>')
def sky_color(color):
    return render_template('sky_color.html', color = color)

@main.route('/state_level/<state>')
def state_level(state):

    plot = vis.dummy_plot()

    return render_template('visualization_template.html', state = state, plot = plot)

@main.route('/state_level/download_dummy_csv', endpoint = 'dummy_csv')
def download_dummy_data():

    raw_data = csv_exp.generate_dummy_csv()

    return Response(raw_data, content_type= 'text/csv', headers={'Content-Disposition': 'attachment; filename=dummy_data.csv'})