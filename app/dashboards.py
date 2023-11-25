import app.models as mdl

import geopandas as gp
import pandas as pd

import holoviews as hv
from holoviews import opts
import panel as pn

hv.extension('bokeh')

def geo_dashboard(state_name):

    county_data_df = mdl.CountyGeo(state_name= state_name).return_df()
    
    #pull shapes df and drop unnecessary columns
    county_shapes_df = gp.read_file('app//data//county_shapes//tl_rd22_us_county.shp')
    county_shapes_df = county_shapes_df[['GEOID', 'NAME', 'geometry']]

    merge_gdf = pd.merge(left = county_shapes_df, right = county_data_df, how = 'inner', left_on = 'GEOID', right_on ='County')

    geo_overlay = hv.Polygons(merge_gdf, vdims=['Average Loan to Value'])

    options = dict(width=800, height=600, tools=['hover'], xaxis=None, yaxis=None)
    geo_overlay.opts(opts.Polygons(**options))
    
    heatmap_app = pn.Column(f"Heat Map of Average Loan to Volume", geo_overlay)

    return hv.render(heatmap_app, backend= 'bokeh')