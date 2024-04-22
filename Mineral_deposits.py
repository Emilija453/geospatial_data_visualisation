import dash
from dash import html
import geopandas as gpd
import folium
import pandas as pd

# Load GeoDataFrames
countries = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))

china_layer_name = 'CHN_Mineral_Resources_Copper'
gdf_china = gpd.read_file('data/CHN_GIS.gdb', layer=china_layer_name)
china_layer_title = 'China Mineral ResourcesCopper'

africa_layer_name = 'AFR_Mineral_Resources_Copper'
gdf_africa = gpd.read_file('data/Africa_GIS.gdb', layer=africa_layer_name)
africa_layer_title = 'Africa Mineral Resources Copper'

indopac_layer_name = 'INDOPAC_Mineral_Resources_Copper'
gdf_indopac = gpd.read_file('data/INDOPAC_GIS.gdb', layer=indopac_layer_name)
indopac_layer_title = 'Indo-Pacific Mineral Resources Copper'

swasia_layer_name = 'SWA_Mineral_Resources_Copper'
gdf_swasia = gpd.read_file('data/SWAsia_GIS.gdb', layer=swasia_layer_name)
swasia_layer_title= 'Southwest Asi Mineral Resources Copper'

# Merge GeoDataFrames
gdf_merged = gpd.GeoDataFrame(pd.concat([gdf_africa, gdf_china, gdf_indopac, gdf_swasia], ignore_index=True), crs=gdf_africa.crs)

# Create Folium map
m = folium.Map([35, 103], zoom_start=4, tiles='CartoDB dark_matter', attr='CartoDB dark_matter')

# Add countries GeoJSON to Folium map
folium.GeoJson(countries.to_json()).add_to(m)

# Add copper deposits to Folium map
for index, row in gdf_merged.iterrows():
    if index < len(gdf_africa):
        layer_title = africa_layer_title
    elif index < len(gdf_africa) + len(gdf_china):
        layer_title = china_layer_title
    elif index < len(gdf_africa) + len(gdf_china) + len(gdf_indopac):
        layer_title = indopac_layer_title
    else:
        layer_title = swasia_layer_title

    if row['geometry'].geom_type == 'MultiPolygon':
        multi_polygon_geojson = folium.GeoJson(row['geometry'].__geo_interface__,
                                                style_function=lambda x: {'fillColor': '#FF5733', 'color': 'none', 'weight': 1.5},
                                                tooltip=f"{layer_title}")
        multi_polygon_geojson.add_to(m)
    else:
        folium.GeoJson(row['geometry'].__geo_interface__,
                       style_function=lambda x: {'fillColor': '#FF5733', 'color': 'none', 'weight': 1.5},
                       tooltip=f"{layer_title}").add_to(m)

# Convert Folium map to HTML
m.save('map.html')

app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1("Copper Deposits in Africa, China, Indopacific and South West Asia", className="text-center mt-4 mb-4"),
    html.Iframe(id='map', srcDoc=open('map.html', 'r').read(), width='100%', height='600', className="border border-dark rounded"),
    html.Footer([
        html.P("Data by U.S. Geological Survey", className="text-center text-muted mt-3 mb-0"),
        html.P("Visualisation by Emilija Zebrauskaite", className="text-center text-muted mt-0 mb-4")
    ], className="bg-dark text-white p-3 mt-5")
])

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        <!-- Bootstrap CSS -->
        <link href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
        <!-- Custom dark theme CSS -->
        <style>
            body {
                background-color: #1e1e1e; /* Dark background color */
                color: #ffffff; /* Text color */
            }
            .jumbotron {
                background-color: #2a2a2a; /* Jumbotron background color */
            }
            .card {
                background-color: #2a2a2a; /* Card background color */
                color: #ffffff; /* Card text color */
            }
            #map {
                border: 2px solid #ffffff; /* Map border color */
            }
        </style>
        <!-- Required meta tags -->
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <title>{%title%}</title>
        {%favicon%}
        {%metas%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

if __name__ == '__main__':
    app.run_server(debug=True)
