#-----------------------------------------------------------------------
# Name:        tests_huff (huff package)
# Purpose:     Tests for Huff Model package functions
# Author:      Thomas Wieland 
#              ORCID: 0000-0001-5168-9846
#              mail: geowieland@googlemail.com              
# Version:     1.3.0
# Last update: 2025-05-22 05:41
# Copyright (c) 2025 Thomas Wieland
#-----------------------------------------------------------------------


from huff.models import create_interaction_matrix, get_isochrones, load_geodata, load_interaction_matrix
from huff.osm import map_with_basemap
from huff.gistools import buffers, point_spatial_join


# Customer origins (statistical districts):

Haslach = load_geodata(
    "data/Haslach.shp",
    location_type="origins",
    unique_id="BEZEICHN"
    )
# Loading customer origins (shapefile)

Haslach_buf = Haslach.buffers(
    segments_distance=[500,1000,1500],
    save_output=True,
    output_filepath="Haslach_buf.shp",
    output_crs="EPSG:31467"
    )
# Buffers for customer origins

Haslach.summary()
# Summary of customer origins

Haslach.define_marketsize("pop")
# Definition of market size variable

Haslach.define_transportcosts_weighting(
    param_lambda = -2.2
    )
# Definition of transport costs weighting (lambda)

Haslach.summary()
# Summary after update


# Supply locations (supermarkets):

Haslach_supermarkets = load_geodata(
    "data/Haslach_supermarkets.shp",
    location_type="destinations",
    unique_id="LFDNR"
    )
# Loading supply locations (shapefile)

Haslach_supermarkets.summary()
# Summary of supply locations

Haslach_supermarkets.define_attraction("VKF_qm")
# Defining attraction variable

Haslach_supermarkets.define_attraction_weighting(
    param_gamma=0.9
    )
# Define attraction weighting (gamma)

Haslach_supermarkets.isochrones(
    segments_minutes=[5, 10],
    profile = "foot-walking",
    save_output=True,
    ors_auth="5b3ce3597851110001cf62480a15aafdb5a64f4d91805929f8af6abd",
    output_filepath="Haslach_supermarkets_iso.shp",
    output_crs="EPSG:31467"
    )
# Obtaining isochrones for walking (5 and 10 minutes)
# ORS API documentation: https://openrouteservice.org/dev/#/api-docs/v2/

Haslach_supermarkets.summary()
# Summary of updated customer origins

Haslach_supermarkets_isochrones = Haslach_supermarkets.get_isochrones_gdf()
# Extracting isochrones

print(Haslach_supermarkets_isochrones)


# Using customer origins and supply locations for building interaction matrix:

haslach_interactionmatrix = create_interaction_matrix(
    Haslach,
    Haslach_supermarkets
    )
# Creating interaction matrix

interaction_matrix = haslach_interactionmatrix.transport_costs(
    ors_auth="5b3ce3597851110001cf62480a15aafdb5a64f4d91805929f8af6abd"
    #network=False
    )
# Obtaining transport costs (default: driving-car)
# ORS API documentation: https://openrouteservice.org/dev/#/api-docs/v2/

interaction_matrix = interaction_matrix.flows()
# Calculating spatial flows

huff_model = interaction_matrix.marketareas()
# Calculating total market areas

huff_model.summary()
# Summary of Huff model

print(huff_model.get_market_areas_df())
# Showing total market areas

print(interaction_matrix.get_interaction_matrix_df())
# Showing df of interaction matrix


# Multiplicative Competitive Interaction Model:

mci_fit = huff_model.mci_fit()
# Fitting via MCI

mci_fit.summary()
# Summary of MCI model

mci_fit.marketareas()
# MCI model market simulation

mci_fit.get_market_areas_df()
# MCI model market areas


# Loading own interaction matrix:
# Data source: Wieland 2015 (https://nbn-resolving.org/urn:nbn:de:bvb:20-opus-180753)

Wieland2015_interaction_matrix = load_interaction_matrix(
    data="data/Wieland2015.xlsx",
    customer_origins_col="Quellort",
    supply_locations_col="Zielort",
    attraction_col=[
        "VF", 
        "K", 
        "K_KKr"
        ],
    transport_costs_col="Dist_Min2",
    probabilities_col="MA",
    data_type="xlsx"
    )

Wieland2015_interaction_matrix.summary()
# Summary of interaction matrix

Wieland2015_fit = Wieland2015_interaction_matrix.mci_fit(
    cols=[
        "A_j", 
        "t_ij", 
        "K", 
        "K_KKr"
        ]
    )
# Fitting MCI model with four independent variables

Wieland2015_fit.summary()
# MCI model summary


# Buffer analysis:

Haslach_supermarkets_gdf = Haslach_supermarkets.get_geodata_gpd_original()
Haslach_buffers = Haslach_buf.get_buffers()
# Extracting points and buffer polygons

spj_test = point_spatial_join(
    polygon_gdf = Haslach_buffers,
    point_gdf = Haslach_supermarkets_gdf,
    polygon_ref_cols = ["BEZEICHN", "segment"],
    point_stat_col = "VKF_qm"
)
# Spatial join with buffers and points
# Statistics for supermarkets by statistical districts

spj_test[0].to_file("spj_test.shp")
# Save joined points as shapefile

print(spj_test[1])
# Showing df with overlay statistics


# Creating map:

Haslach_gdf = Haslach.get_geodata_gpd_original()
Haslach_supermarkets_gdf = Haslach_supermarkets.get_geodata_gpd_original()
Haslach_supermarkets_gdf_iso = Haslach_supermarkets.get_isochrones_gdf()
# Extracttion geopandas.GeoDataFrames

map_with_basemap(
    layers = [
        Haslach_supermarkets_gdf_iso,
        Haslach_gdf, 
        Haslach_supermarkets_gdf
        ],
    output_filepath = "Haslach_map.png"
    )
# Map with three layers and OSM basemap