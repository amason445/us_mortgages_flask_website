"""
This file acts as a module which contains logic for the folium dashboards.
The data is wrangled from the CountyGeo model and a dashboard is rendered using folium.
It is extremely similar to the script in ShapesETL except that it is parameterized by state, year, loan term and a given datapoint.
It takes two shape files from the US Census website and joins them to the CFPB data with pandas.
Once this data is merged, geopandas and folium are used to render visualizations.
For this initial build, I only built the Colorado maps from a CSV to prototype it. I didn't access the CouchDB model since unit testing would be done later.
https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html

Below is an article explaining a folium choropleth:
https://towardsdatascience.com/creating-choropleth-maps-with-pythons-folium-library-cfacfb40f56a
"""

import app.models as mdl
import app.utilities as utl

import geopandas as gp
import pandas as pd

import folium

def geo_dashboard(state_name, year, loan_term, datapoint):

    # accesses the CountyGeo model and returns a dataframe
    county_data_df = mdl.CountyGeo(state_name= state_name).return_df()
    county_data_df['County'] = county_data_df['County'].astype(str)

    # pull shapes df and drop unnecessary columns
    state_shapes_df = gp.read_file('app//data//state_shapes//tl_rd22_us_state.shp')
    county_shapes_df = gp.read_file('app//data//county_shapes//tl_rd22_us_county.shp')

    # filter state df and combine it with county dfs to pull state counties
    state_shapes_df = state_shapes_df[(state_shapes_df['STUSPS'] == state_name)]
    state_shapes_df = state_shapes_df[['STUSPS', 'STATEFP']]
    county_shapes_df = state_shapes_df.merge(county_shapes_df, how = 'inner', on = 'STATEFP')
    county_shapes_df = county_shapes_df[['STUSPS', 'STATEFP', 'GEOID', 'NAMELSAD', 'geometry']]

    # merge state counties with state mortgage data
    county_shapes_merge = county_shapes_df.merge(county_data_df, how = 'inner', left_on = 'GEOID', right_on = 'County')

    # converted string columns to integer columns. logic is added to enforce the year column as a string in pandas
    numeric_columns = ['Loan Volume', 'Average Interest Rate', 'Total Loan Amount', 'Average Loan to Value']
    county_shapes_merge[numeric_columns] = county_shapes_merge[numeric_columns].apply(pd.to_numeric, errors='coerce')
    county_shapes_merge['Average Interest Rate'] = county_shapes_merge['Average Interest Rate'].round(2)
    county_shapes_merge['Average Loan to Value'] = county_shapes_merge['Average Loan to Value'].round(2)
    county_shapes_merge['Year'] = county_shapes_merge['Year'].astype(str)

    # converted the pandas dataframe to a geopandas dataframe then added paramterization from the year and the loan term
    gdf = gp.GeoDataFrame(county_shapes_merge, geometry='geometry')
    gdf = gdf[(gdf['Year'] == year) & (gdf['Loan Term'] == loan_term)]

    # built folium map then added the choropleth and map marker layer
    m = folium.Map(location= utl.state_capital_coordinates(state_name), zoom_start= 7)

    folium.Choropleth(
        geo_data= gdf,
        data = gdf,
        columns= ['NAMELSAD', datapoint],
        key_on= 'feature.properties.NAMELSAD',
        fill_color= "YlGn",
        fill_opacity= 0.7,
        line_opacity= 0.2,
        legend_name= f'{datapoint} for {state_name}',   
    ).add_to(m)

    for _, row in gdf.iterrows():
        sim_geo = gp.GeoSeries(row['geometry']).simplify(tolerance = 0.001)
        geo_j = sim_geo.to_json()
        geo_j = folium.GeoJson(data=geo_j)
        popup_html = f"<br>{row['NAMELSAD']}<br>{datapoint}: {row[datapoint]}<br>Year: {year}<br>Loan Term: {loan_term}"
        folium.Popup(popup_html, max_width=400).add_to(geo_j)
        geo_j.add_to(m)

    return m