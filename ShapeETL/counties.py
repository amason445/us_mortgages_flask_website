import geopandas as gp
import pandas as pd

import json
from shapely.geometry import Polygon

import folium
from folium import ColorMap

county_data_df = pd.read_csv('tests/models/county_geo/CO_county_geo.csv', dtype= 'object')
county_data_df['County'] = county_data_df['County'].astype(str)

# pull shapes df and drop unnecessary columns
state_shapes_df = gp.read_file('ShapeETL//state_shapes//tl_rd22_us_state.shp')
county_shapes_df = gp.read_file('app//data//county_shapes//tl_rd22_us_county.shp')

state_shapes_df = state_shapes_df[(state_shapes_df['STUSPS'] == 'AZ') | (state_shapes_df['STUSPS'] == 'CO') |
                                  (state_shapes_df['STUSPS'] == 'NM') | (state_shapes_df['STUSPS'] == 'UT')] 

state_shapes_df = state_shapes_df [['STUSPS', 'STATEFP']]

county_shapes_df = state_shapes_df.merge(county_shapes_df, how = 'inner', on = 'STATEFP')

county_shapes_df = county_shapes_df[['STUSPS', 'STATEFP', 'GEOID', 'NAME', 'geometry']]

county_shapes_df = county_shapes_df.merge(county_data_df, how = 'inner', left_on = 'GEOID', right_on = 'County')

numeric_columns = ['Loan Volume', 'Average Interest Rate', 'Total Loan Amount', 'Average Loan to Value']
county_shapes_df[numeric_columns] = county_shapes_df[numeric_columns].apply(pd.to_numeric, errors='coerce')

gdf = gp.GeoDataFrame(county_shapes_df, geometry='geometry')

gdf = gdf[(gdf['Year'] == '2022') & (gdf['Loan Term'] == '30-year')]

m = folium.Map(location= [0,0], zoom_start= 3)

colormap = folium.LinearColormap(['green', 'blue'], vmin=50, vmax=100)

folium.Choropleth(
    geo_data= gdf,
    data = gdf,
    columns= ['NAME', 'Average Loan to Value'],
    key_on= 'feature.properties.NAME',
    fill_color= "YlGn",
    fill_opacity= 0.7,
    line_opacity= 0.2,
    legend_name= 'Heat Map Legend',   
).add_to(m)

# for _, row in gdf.iterrows():
#     sim_geo = gp.GeoSeries(row['geometry']).simplify(tolerance = 0.001)
#     geo_j = sim_geo.to_json()
#     geo_j = folium.GeoJson(data=geo_j, style_function= lambda x: {'fillColor': colormap(row['Average Loan to Value']), 
#                                                                   'color': 'black', 'weight': 1, 'fillOpacity': 0.7})
#     folium.Popup(row['NAME']).add_to(geo_j)
#     geo_j.add_to(m)

m.save('choropleth_map_colored.html')
