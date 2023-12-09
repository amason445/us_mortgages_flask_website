"""
I wrote this script to build and prototype the geographical visualizations for my project.
It takes two shape files from the US Census website and joins them to the CFPB data with pandas.
Once this data is merged, geopandas and folium are used to render visualizations.
For this initial build, I only built the Colorado maps from a CSV to prototype it. I didn't access the CouchDB model since unit testing would be done later.
https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html
"""

import geopandas as gp
import pandas as pd

import folium

import itertools

# this function maps the state abbreviation to the lattitude and longitudinal coordinates for each state capital in scope. I googled these coordinate pairs.
def state_capital_coordinates(abbreviation):
        match abbreviation:
            case 'AZ':
                return [33.4484, -112.0740]
            case 'CO':
                return [39.7392,-104.991531]
            case 'NM':
                return [35.691544, -105.944183]
            case 'UT':
                return [40.758701, -111.876183]

def geo_dashboard(state_name, year, loan_term, datapoint):

    # accesses a raw csv file of the colorado geo model.
    county_data_df = pd.read_csv('tests/models/county_geo/CO_county_geo.csv', dtype= 'object')
    county_data_df['County'] = county_data_df['County'].astype(str)

    # pull shapes df and drop unnecessary columns
    state_shapes_df = gp.read_file('app//data//state_shapes//tl_rd22_us_state.shp')
    county_shapes_df = gp.read_file('app//data//county_shapes//tl_rd22_us_county.shp')

    # filter state df and combine it with county dfs to pull state counties
    state_shapes_df = state_shapes_df[(state_shapes_df['STUSPS'] == state_name)]
    state_shapes_df = state_shapes_df[['STUSPS', 'STATEFP']]
    county_shapes_df = state_shapes_df.merge(county_shapes_df, how = 'inner', on = 'STATEFP')
    county_shapes_df = county_shapes_df[['STUSPS', 'STATEFP', 'GEOID', 'NAMELSAD', 'geometry']]

    #merge state counties with state mortgage data
    county_shapes_merge = county_shapes_df.merge(county_data_df, how = 'inner', left_on = 'GEOID', right_on = 'County')

    # converted string columns to integer columns
    numeric_columns = ['Loan Volume', 'Average Interest Rate', 'Total Loan Amount', 'Average Loan to Value']
    county_shapes_merge[numeric_columns] = county_shapes_merge[numeric_columns].apply(pd.to_numeric, errors='coerce')
    county_shapes_merge['Average Interest Rate'] = county_shapes_merge['Average Interest Rate'].round(2)
    county_shapes_merge['Average Loan to Value'] = county_shapes_merge['Average Loan to Value'].round(2)

    # converted the pandas dataframe to a geopandas dataframe then added paramterization from the year and the loan term
    gdf = gp.GeoDataFrame(county_shapes_merge, geometry='geometry')
    gdf = gdf[(gdf['Year'] == year) & (gdf['Loan Term'] == loan_term)]

    # built folium map then added the choropleth and map marker layer
    m = folium.Map(location= state_capital_coordinates(state_name), zoom_start= 6)

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
        popup_html = f"<br>{row['NAMELSAD']}<br>{datapoint}: {row[datapoint]}"
        folium.Popup(popup_html).add_to(geo_j)
        geo_j.add_to(m)

    m.save(f'tests/dashboards/{state_name}_{year}_{loan_term}_{datapoint}.html')

# the main method contains logic to prototype the rendering functions above
if __name__ == "__main__":
    #defines testing scope
    
    # state_list = ['AZ', 'CO', 'NM', 'UT']
    state_list = ['CO']
    year_list = ['2018', '2019', '2020', '2021', '2022']
    term_list = ['15-year','30-year']
    datapoint_list = ['Loan Volume', 'Average Interest Rate', 'Total Loan Amount', 'Average Loan to Value']
    
    state_shapes_df = gp.read_file('ShapeETL//state_shapes//tl_rd22_us_state.shp')
    county_shapes_df = gp.read_file('app//data//county_shapes//tl_rd22_us_county.shp')

    state_shapes_df = state_shapes_df[state_shapes_df['STUSPS'] == 'NM']
    state_shapes_df = state_shapes_df[['STUSPS', 'STATEFP']]

    county_shapes_df = state_shapes_df.merge(county_shapes_df, how = 'inner', left_on = 'STATEFP', right_on = 'STATEFP')
    

    print(state_shapes_df)

    print(county_shapes_df)

    #iterates through testing scope
    try:
        for element in itertools.product(state_list, year_list, term_list, datapoint_list):
            geo_dashboard(element[0],element[1], element[2], element[3])

    except Exception as e:
        print(e)