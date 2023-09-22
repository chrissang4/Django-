from django.shortcuts import render
from django.contib.auth.models import User
from django.contrib.auth import authenticate, login

# # Create your views here.
# from django.shortcuts import render

# # generic base view
# from django.views.generic import TemplateView

# # import Geocoder 
# # import geocoder
# # location1 = 'Kenya'
# # loc = geocoder.osm(location1)

# #Define coordinates of where we want to center our map
# # boulder_coords = [loc.lat, loc.lng] 

# #folium
# import folium
# from folium import plugins


# #gee
# import ee
# import geemap
# import geemap.eefolium

# ee.Initialize()


# #home
# class home(TemplateView):
#     template_name = 'index.html'

#     # Define a method for displaying Earth Engine image tiles on a folium map.
#     def get_context_data(self, **kwargs):

#         figure = folium.Figure()
#         roi = ee.FeatureCollection('users/collinsasegaca/Counties/Kakamega')
#         AOI = roi
#         region1 = AOI.first().getInfo()['geometry']['coordinates'][0][5]
        
#         Map = geemap.Map()
#         #create Folium Object
#         m = folium.Map(
#             location=[region1[1], region1[0]],
#             zoom_start=12
#         )

#         #add map to figure
#         m.add_to(figure)
        
#         # Select Region of interest
#         roi = ee.FeatureCollection('users/collinsasegaca/Counties/Kakamega')


#         #// Load Sentinel-1 C-band SAR Ground Range collection (log scale, VV, descending)
#         collectionVV = ee.ImageCollection('COPERNICUS/S1_GRD') \
#         .filter(ee.Filter.eq('instrumentMode', 'IW')) \
#         .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV')) \
#         .filter(ee.Filter.eq('orbitProperties_pass', 'DESCENDING')) \
#         .filterMetadata('resolution_meters','equals' , 10) \
#         .filterBounds(roi) \
#         .select('VV')

#         #// Load Sentinel-1 C-band SAR Ground Range collection (log scale, VH, descending)
#         collectionVH = ee.ImageCollection('COPERNICUS/S1_GRD') \
#         .filter(ee.Filter.eq('instrumentMode', 'IW')) \
#         .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VH')) \
#         .filter(ee.Filter.eq('orbitProperties_pass', 'DESCENDING')) \
#         .filterMetadata('resolution_meters','equals' , 10) \
#         .filterBounds(roi) \
#         .select('VH') \

#         #//Filter by date
#         first2019VV = collectionVV.filterDate('2021-01-01', '2021-01-31').mosaic().clip(roi)
#         second2020VV = collectionVV.filterDate('2021-02-01', '2021-02-31').mosaic().clip(roi)
#         third2020VV = collectionVV.filterDate('2020-03-01', '2020-03-20').mosaic().clip(roi)
#         first2019VH = collectionVH.filterDate('2018-01-01', '2018-05-31').mosaic().clip(roi)
#         second2020VH = collectionVH.filterDate('2021-01-01', '2021-05-31').mosaic().clip(roi)
#         third2020VH = collectionVH.filterDate('2021-03-01', '2021-03-20').mosaic().clip(roi)



#         # Apply filter to reduce speckle
#         SMOOTHING_RADIUS = 50
#         first2019VV_filtered = first2019VV.focal_mean(SMOOTHING_RADIUS, 'circle', 'meters')
#         first2019VH_filtered = first2019VH.focal_mean(SMOOTHING_RADIUS, 'circle', 'meters')
#         second2020VV_filtered = second2020VV.focal_mean(SMOOTHING_RADIUS, 'circle', 'meters')
#         second2020VH_filtered = second2020VH.focal_mean(SMOOTHING_RADIUS, 'circle', 'meters')
#         third2020VV_filtered = third2020VV.focal_mean(SMOOTHING_RADIUS, 'circle', 'meters')
#         third2020VH_filtered = third2020VH.focal_mean(SMOOTHING_RADIUS, 'circle', 'meters')

#         # Calculate the ratio between before and after
#         ratio1920VH= first2019VH_filtered.subtract(second2020VH_filtered)
#         ratio1920VV= first2019VV_filtered.subtract(second2020VV_filtered)
#         ratio2020_marchVH= second2020VH_filtered.subtract(third2020VH_filtered)
#         ratio2020_marchVV= second2020VV_filtered.subtract(third2020VV_filtered)

#         #Calculate the mean and standard deviation for each ratio image
#         mean_1920 = ratio1920VH.select('VH').reduceRegion(
#             ee.Reducer.mean(), roi, scale= 300).get('VH').getInfo()
#         variance_1920 = ratio1920VH.select('VH').reduceRegion(
#             ee.Reducer.variance(), roi, scale=300).get('VH').getInfo()
#         std_1920 = ratio1920VH.select('VH').reduceRegion(
#             ee.Reducer.stdDev(), roi, scale=300).get('VH').getInfo()
#         #Mean for the ratio2020_march
#         mean_2020_march = ratio2020_marchVH.select('VH').reduceRegion(
#             ee.Reducer.mean(), roi, scale= 300).get('VH').getInfo()
#         variance_2020_march = ratio2020_marchVH.select('VH').reduceRegion(
#             ee.Reducer.variance(), roi, scale=300).get('VH').getInfo()

#         std_2020_march = ratio2020_marchVH.select('VH').reduceRegion(
#             ee.Reducer.stdDev(), roi, scale=300).get('VH').getInfo()
# # compute treshold
#         thresh1920 = std_1920*5 + mean_1920
#         thresh2020_march = std_2020_march*2 + mean_2020_march

#         # Apply threshold The threshold is calculated by multiplying the Standard deviation by 1.5 and adding the Mean

#         RATIO_UPPER_THRESHOLD1920 = thresh1920
#         RATIO_UPPER_THRESHOLD2020_march = thresh2020_march
#         ratio1920VH_thresholded = ratio1920VH.gt(RATIO_UPPER_THRESHOLD1920)
#         ratio2020_marchVH_thresholded = ratio2020_marchVH.gt(RATIO_UPPER_THRESHOLD2020_march)

#         legend_dict = {
#         'Vegetation Loss Dec 2019/2020 Jan': 'FF0000',
#         'Vegetation Loss Jan 2020/2020 march': '140b13'
#         }


        
#         #select the Dataset Here's used the MODIS data
        

#         dataset = (ee.ImageCollection('MODIS/006/MOD13Q1')
#                   .filter(ee.Filter.date('2019-07-01', '2019-11-30'))
#                   .first())
#         modisndvi = dataset.select('NDVI').clip(roi)

#         #Styling 
#         vis_paramsNDVI = {
#             'min': 0,
#             'max': 9000,
#             'palette': [ 'FE8374', 'C0E5DE', '3A837C','034B48',]}

        
#         #add the map to the the folium map
#         first2019VH_filtered_dic = ee.Image(first2019VH_filtered).getMapId({'min':-15,max:0})
#         map_id_dict = ee.Image(modisndvi).getMapId(vis_paramsNDVI)
#         map_id_dic1 = ee.Image(ratio1920VH_thresholded).getMapId({'min':-15,max:0})
#         threshoded_2019 = ratio1920VH_thresholded.updateMask(ratio1920VH_thresholded)

#         map_id_dic_veglos_2019 = ee.Image(threshoded_2019).getMapId({'palette':"FF0000"})
       
#         #GEE raster data to TileLayer
#         # folium.raster_layers.TileLayer(
#         #             tiles =  map_id_dict['tile_fetcher'].url_format,
#         #             attr = 'LocateIT',
#         #             name = 'NDVI',
#         #             overlay = True,
#         #             control = True
#         #             ).add_to(m)



#         # folium.raster_layers.TileLayer(
#         #             tiles =  map_id_dic_veglos_2019['tile_fetcher'].url_format,
#         #             attr = 'LocateIT',
#         #             name = 'Veg los 2019',
#         #             overlay = True,
#         #             control = True
#         #             ).add_to(m)

        
#         def maap(map_id_dic, name):
#             folium.raster_layers.TileLayer(
#                         tiles =  map_id_dic['tile_fetcher'].url_format,
#                         attr = 'LocateIT',
#                         name = name,
#                         overlay = True,
#                         control = True
#                         ).add_to(m)
#             return folium.raster_layers.TileLayer
#         filterted_2021 = maap(first2019VH_filtered_dic, 'Filtered 2021 08 to 12')
#         Radar_vh = maap(map_id_dic1, 'Ratio image ' ) 
#         veg_loss = maap(map_id_dic_veglos_2019, 'Vegetation loss 2021')
        
#         # ndvi = maap(map_id_dict, 'NDVI')
        
#         #add Layer control
#         m.add_child(folium.LayerControl())
 
#         #figure 
#         figure.render()
         
#         #return map
#         return {"map": figure}