
#The final outcome of the customization is to find out - What is the Ground Parrot species movement pattern since 2000 (distance between ground parrot records of the previous and the following year)? 
#Pre-processing: The relevant shapefiles for this customization have been manually saved in GDA 2020 Map Grid of Australia Zone 55, EPSG: 7855 CRS. Click OK for Inverse Transformation from EPSG: 7855 to EPSG: 3111 for the East Gippsland Study Area shapefile

from qgis.core import *
from qgis.utils import iface
from qgis.PyQt.QtCore import QVariant
import processing
from processing.tools import *
import os
import glob
#--------------------------
#Step 1: IMPORTING LAYERS
#--------------------------

#set file path variable for the study area vector layer- East Gippsland
egStudyAreaPath= 'S:\MC265_RMIT\Sem_2\Geospatial_Programming\Project\Data_3\east_gippsland.shp'
#use iface to add layer to the QGIS interface
egStudyAreaLayer = iface.addVectorLayer(egStudyAreaPath, 'East Gippsland', 'ogr')

#set file path variable for the Fire History vector layer
firehistoryPath= 'S:\MC265_RMIT\Sem_2\Geospatial_Programming\Project\Data_3\hist_fire.shp'
#use iface to add vector layer to the QGIS interface
firehistoryLayer=iface.addVectorLayer(firehistoryPath,'','ogr')

#set file path variable for the Ground Parrot Records pre fire vector layer
GroundParrotPrefire_Path='S:\MC265_RMIT\Sem_2\Geospatial_Programming\Project\Data_3\pre_fire_gp.shp'
#use iface to add vector layer to the QGIS interface
GroundParrotPrefire_Layer=iface.addVectorLayer(GroundParrotPrefire_Path,'','ogr')

#set file path variable for the Ground Parrot Records post fire vector layer
GroundParrotPostfire_Path='S:\MC265_RMIT\Sem_2\Geospatial_Programming\Project\Data_3\post_fire_gp.shp'
#use iface to add vector layer to the QGIS interface
GroundParrotPostfire_Layer=iface.addVectorLayer(GroundParrotPostfire_Path,'','ogr')

#set file path variable for the Wet HeathLand (suitable habitat for ground parrots) vector layer
wetHeathland_Path='S:\MC265_RMIT\Sem_2\Geospatial_Programming\Project\Data_3\heath.shp'
#use iface to add vector layer to the QGIS interface
wetHeathland_Layer=iface.addVectorLayer(wetHeathland_Path,'','ogr')


#--------------------------------------------------------------------
#Step 2: CLIPPING OF THE LAYERS TO THE STUDY AREA EXTENT
#--------------------------------------------------------------------

#add all the output paths including the potential shapefile names
fireClip="S:\MC265_RMIT\Sem_2\Geospatial_Programming\Project\Data\Outputs\history_fire_clip.shp"
preGPClip="S:\MC265_RMIT\Sem_2\Geospatial_Programming\Project\Data\Outputs\pre_fire_gp_clip.shp"
postGPClip="S:\MC265_RMIT\Sem_2\Geospatial_Programming\Project\Data\Outputs\post_fire_gp_clip.shp"
wetHeathClip="S:\MC265_RMIT\Sem_2\Geospatial_Programming\Project\Data\Outputs\wet_heathland_clip.shp"

#the clip processing algorithm has been chosen to clip all the layers to the study area extent 'egStudyAreaPath'. This is used as an overlay for all other input shapefiles 
processing.run("native:clip", {'INPUT':firehistoryPath,'OVERLAY':egStudyAreaPath,'OUTPUT': fireClip})

processing.run("native:clip", {'INPUT':GroundParrotPrefire_Path, 'OVERLAY':egStudyAreaPath, 'OUTPUT':preGPClip})

processing.run("native:clip", {'INPUT':GroundParrotPostfire_Path,'OVERLAY':egStudyAreaPath, 'OUTPUT':postGPClip})

processing.run("native:clip", {'INPUT':wetHeathland_Path,'OVERLAY':egStudyAreaPath,'OUTPUT':wetHeathClip})

#add the clipped shapefiles to the QGIS project instance 
iface.addVectorLayer(fireClip , '', 'ogr')
#do not yet add the clipped pre fire ground parrot records shapefile to the instance as this will be further used for other operations
pre_fire_Clip=QgsVectorLayer(preGPClip, 'pre_fire_Ground Parrots_clip', 'ogr')
#add the clipped shapefiles to the QGIS project instance 
iface.addVectorLayer(postGPClip, '', 'ogr')
#add the clipped shapefiles to the QGIS project instance 
iface.addVectorLayer(wetHeathClip, '', 'ogr')

#------------------------------------------------------------------------
#Step 3: ADD AN YEAR FIELD TO THE CLIPPED PRE FIRE GROUND PARROT RECORDS SHAPEFILE
#------------------------------------------------------------------------

#Now we’ll get the layer capabilities. This will allow us to make sure we can add fields of the layer. This is done by calling capabilities() on the layer’s data provider.
caps = pre_fire_Clip.dataProvider().capabilities()
#start editing the required layer
pre_fire_Clip.startEditing()
#loop through each feature in the layer and add attributes using the addAttributes method and the QgsField, mention the type of the data field using the Qvariant 
#the reason for chosing integer as the type of data field for the YEAR field as the expression(metioned in the following lines of codes) outputs year length as an integer and not as a date
if caps & QgsVectorDataProvider.AddAttributes:
    res = pre_fire_Clip.dataProvider().addAttributes([QgsField("YEAR", QVariant.Int)])
    #do not forget to update the fields
    pre_fire_Clip.updateFields() 
else:
    print("Error")
#commit changes to the layer to permanently reflect the changes which cannot be edited.
pre_fire_Clip.commitChanges()

#---------------------------------------------------------------------------------------------------------------------
#Step 4: ADD ONLY THE YEAR FROM THE STARTDATE FIELD TO THE YEAR FIELD IN THE CLIPPED PRE FIRE GROUND PARROT RECORDS SHAPEFILE
#---------------------------------------------------------------------------------------------------------------------

#Expression used ADD ONLY THE YEAR FROM THE STARTDATE FIELD TO THE YEAR FIELD IN THE CLIPPED PRE FIRE GROUND PARROT RECORDS SHAPEFILE
#'year(STARTDATE)': year is an inbuilt QGIS function readily available for use. It takes a date argument and outputs the length, therefore, the field STARTDATE from the pre_fire_Clip has been chosen as an argument
year_exp = QgsExpression('year(STARTDATE)')
#Now we need to specify which layer to perform the expression on. This is done by creating a QgsExpressionContext object, which we will pass to when we calculate the expression.
#First create the QgsExpressionContext object. Then give it the scope of the layer you’re working with.
context = QgsExpressionContext()
context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(pre_fire_Clip))
#start editing the layer using with edit(pre_fire_Clip): and running a for loop within that to access the features and evaluate the expressions.
with edit(pre_fire_Clip):
    for f in pre_fire_Clip.getFeatures():
        context.setFeature(f)
        f['YEAR'] = year_exp.evaluate(context)
        pre_fire_Clip.updateFeature(f)
pre_fire_Clip.commitChanges()
#now adding the clipped pre fire gp layer with modifications to the QGIS Project instance.This layer will have an additional YEAR field with only the years from the STARTDATE field as an integer
QgsProject.instance().addMapLayer(pre_fire_Clip)


#---------------------------------------------------------------------------------------------------------------------
#Step 5: REMOVING NULL VALUES and all the year values which are below 2000 in the YEAR field from pre_fire_Clip
#---------------------------------------------------------------------------------------------------------------------
#access pre_fire_Clip by layer name
layers = QgsProject.instance().mapLayersByName('pre_fire_Ground Parrots_clip')
layer = layers[0]
#Now we’ll get the layer capabilities. This will allow us to make sure we can modify fields of the layer. This is done by calling capabilities() on the layer’s data provider.
caps = layer.dataProvider().capabilities()
#get all the features form the layer
feats = layer.getFeatures()
dfeats = []

#delete null features and features below 2000 in the YEAR field using comparison operators and if statement
if caps & QgsVectorDataProvider.DeleteFeatures:
    for feat in feats:
        if feat['YEAR'] == NULL or feat['YEAR'] < 2000:
            dfeats.append(feat.id())
    res = layer.dataProvider().deleteFeatures(dfeats)
    layer.triggerRepaint()
#---------------------------------------------------------------------------------------------------------------------
#Step 6: SEPERATE PRE FIRE GROUND PARROT RECORDS SHAPEFILE BASED ON THE YEAR FIELD
#---------------------------------------------------------------------------------------------------------------------
output_directory= 'S:/MC265_RMIT/Sem_2/Geospatial_Programming/Project/Data/Outputs'
#Provide File type as 1 which is shapefile, input the preGPClip layer and not the QGIS instance layer, provide YEAR as the field to identify unique attributes, and finally provide the output path to save all the seperate shapefiles
processing.run('qgis:splitvectorlayer',{ 'FIELD' : 'YEAR', 'FILE_TYPE' : 1, 'INPUT' : preGPClip, 'OUTPUT' : output_directory })

#---------------------------------------------------------------------------------------------------------------------
#Step 7: calculate MEAN coordinates between each year shapefiles generated from the previous step of splitting
#---------------------------------------------------------------------------------------------------------------------
#provide input and output paths
Select_folder="S:/MC265_RMIT/Sem_2/Geospatial_Programming/Project/Data/Outputs/"
Save_results= "S:/MC265_RMIT/Sem_2/Geospatial_Programming/Project/Data/Outputs/Mean/"

#create an empty list 
listFilterShapes = []

#append all the files from the input folder that contain the terms shp and YEAR according to string slicing 
for item in os.listdir(Select_folder):
    if item[-3:]=='shp' and item[:4]=='YEAR':
        listFilterShapes.append(item)

#print(listFilterShapes)

#create a dictionary to store all the associated files with the shapefiles
dictFilterShapes = {}

#loop through the shapefiles listed in the above list 
for shape in listFilterShapes:
    dictFilterShapes[shape[:-4]] = QgsVectorLayer(Select_folder + shape,shape[:-4],"ogr")

#from the dictionary created, create mean coordinates using the inbuilt algorithm and use the dictionary as the input to generate all the point shapefiles
for layers in dictFilterShapes.keys():
    processing.run("qgis:meancoordinates",{'INPUT':dictFilterShapes[layers],'OUTPUT': Save_results+ layers+'_Mean.shp'})

#a list and dictionary is created to display all the generated mean coordinates for each year
listFilterMeanShapes = []

for item in os.listdir(Save_results):
    if item[-3:]=='shp':
        listFilterMeanShapes.append(item)

#print(listFilterMeanShapes)

#provides all the mean coordinates shapefiles and add them to the QGIS interface
dictFilterMeanShapes = {}

for shape in listFilterMeanShapes:
    dictFilterMeanShapes[shape[:-4]] = iface.addVectorLayer(Save_results + shape,shape[:-4],"ogr")

#access all the mean coordinates of all the years by their layer name added previously by the dictionary loop
LayerName_2000=QgsProject.instance().mapLayersByName("YEAR_2000_Mean")
Layer2000 = LayerName_2000[0]
LayerName_2001 = QgsProject.instance().mapLayersByName("YEAR_2001_Mean")
Layer2001 = LayerName_2001[0]
LayerName_2002= QgsProject.instance().mapLayersByName("YEAR_2002_Mean")
Layer2002 = LayerName_2002[0]
LayerName_2003 =QgsProject.instance().mapLayersByName ("YEAR_2003_Mean")
Layer2003 = LayerName_2003[0]
LayerName_2004=QgsProject.instance().mapLayersByName ("YEAR_2004_Mean")
Layer2004 = LayerName_2004[0]
LayerName_2005 = QgsProject.instance().mapLayersByName("YEAR_2005_Mean")
Layer2005 = LayerName_2005[0]
LayerName_2006=QgsProject.instance().mapLayersByName ("YEAR_2006_Mean")
Layer2006 = LayerName_2006[0]
LayerName_2007 =QgsProject.instance().mapLayersByName( "YEAR_2007_Mean")
Layer2007 = LayerName_2007[0]
LayerName_2008= QgsProject.instance().mapLayersByName("YEAR_2008_Mean")
Layer2008 = LayerName_2008[0]
LayerName_2009 =QgsProject.instance().mapLayersByName ("YEAR_2009_Mean")
Layer2009 = LayerName_2009[0]
LayerName_2013 = QgsProject.instance().mapLayersByName("YEAR_2013_Mean")
Layer2013 = LayerName_2013[0]
LayerName_2014=QgsProject.instance().mapLayersByName ("YEAR_2014_Mean")
Layer2014 = LayerName_2014[0]
LayerName_2016= QgsProject.instance().mapLayersByName("YEAR_2016_Mean")
Layer2016 = LayerName_2016[0]
LayerName_2017 =QgsProject.instance().mapLayersByName ("YEAR_2017_Mean")
Layer2017 = LayerName_2017[0]
LayerName_2018=QgsProject.instance().mapLayersByName ("YEAR_2018_Mean")
Layer2018 = LayerName_2018[0]
LayerName_2019 = QgsProject.instance().mapLayersByName("YEAR_2019_Mean")
Layer2019 = LayerName_2019[0]

#---------------------------------------------------------------------------------------------------------------------
#Step 7: calculate distances between each year mean coodinate shapefiles
#---------------------------------------------------------------------------------------------------------------------
#run the distance matrix algorithm by inputting mean coordinate layers and the target layers as the consecutive year's mean coordinate layers
processing.run("qgis:distancematrix",{'INPUT':Layer2000,'INPUT_FIELD':'MEAN_X','TARGET_FIELD':'MEAN_X','TARGET':Layer2001,'MATRIX_TYPE':0,'OUTPUT': Save_results+'Mean_dist_2000_2001.shp'})
processing.run("qgis:distancematrix",{'INPUT':Layer2001,'INPUT_FIELD':'MEAN_X','TARGET_FIELD':'MEAN_X','TARGET':Layer2002,'MATRIX_TYPE':0,'OUTPUT': Save_results+'Mean_dist_2001_2002.shp'})
processing.run("qgis:distancematrix",{'INPUT':Layer2002,'INPUT_FIELD':'MEAN_X','TARGET_FIELD':'MEAN_X','TARGET':Layer2003,'MATRIX_TYPE':0,'OUTPUT': Save_results+'Mean_dist_2002_2003.shp'})
processing.run("qgis:distancematrix",{'INPUT':Layer2003,'INPUT_FIELD':'MEAN_X','TARGET_FIELD':'MEAN_X','TARGET':Layer2004,'MATRIX_TYPE':0,'OUTPUT': Save_results+'Mean_dist_2003_2004.shp'})
processing.run("qgis:distancematrix",{'INPUT':Layer2004,'INPUT_FIELD':'MEAN_X','TARGET_FIELD':'MEAN_X','TARGET':Layer2005,'MATRIX_TYPE':0,'OUTPUT': Save_results+'Mean_dist_2004_2005.shp'})
processing.run("qgis:distancematrix",{'INPUT':Layer2005,'INPUT_FIELD':'MEAN_X','TARGET_FIELD':'MEAN_X','TARGET':Layer2006,'MATRIX_TYPE':0,'OUTPUT': Save_results+'Mean_dist_2005_2006.shp'})
processing.run("qgis:distancematrix",{'INPUT':Layer2006,'INPUT_FIELD':'MEAN_X','TARGET_FIELD':'MEAN_X','TARGET':Layer2007,'MATRIX_TYPE':0,'OUTPUT': Save_results+'Mean_dist_2006_2007.shp'})
processing.run("qgis:distancematrix",{'INPUT':Layer2007,'INPUT_FIELD':'MEAN_X','TARGET_FIELD':'MEAN_X','TARGET':Layer2008,'MATRIX_TYPE':0,'OUTPUT': Save_results+'Mean_dist_2007_2008.shp'})
processing.run("qgis:distancematrix",{'INPUT':Layer2008,'INPUT_FIELD':'MEAN_X','TARGET_FIELD':'MEAN_X','TARGET':Layer2009,'MATRIX_TYPE':0,'OUTPUT': Save_results+'Mean_dist_2008_2009.shp'})
processing.run("qgis:distancematrix",{'INPUT':Layer2009,'INPUT_FIELD':'MEAN_X','TARGET_FIELD':'MEAN_X','TARGET':Layer2013,'MATRIX_TYPE':0,'OUTPUT': Save_results+'Mean_dist_2009_2013.shp'})
processing.run("qgis:distancematrix",{'INPUT':Layer2013,'INPUT_FIELD':'MEAN_X','TARGET_FIELD':'MEAN_X','TARGET':Layer2014,'MATRIX_TYPE':0,'OUTPUT': Save_results+'Mean_dist_2013_2014.shp'})
processing.run("qgis:distancematrix",{'INPUT':Layer2014,'INPUT_FIELD':'MEAN_X','TARGET_FIELD':'MEAN_X','TARGET':Layer2016,'MATRIX_TYPE':0,'OUTPUT': Save_results+'Mean_dist_2014_2016.shp'})
processing.run("qgis:distancematrix",{'INPUT':Layer2016,'INPUT_FIELD':'MEAN_X','TARGET_FIELD':'MEAN_X','TARGET':Layer2017,'MATRIX_TYPE':0,'OUTPUT': Save_results+'Mean_dist_2016_2017.shp'})
processing.run("qgis:distancematrix",{'INPUT':Layer2017,'INPUT_FIELD':'MEAN_X','TARGET_FIELD':'MEAN_X','TARGET':Layer2018,'MATRIX_TYPE':0,'OUTPUT': Save_results+'Mean_dist_2017_2018.shp'})
processing.run("qgis:distancematrix",{'INPUT':Layer2018,'INPUT_FIELD':'MEAN_X','TARGET_FIELD':'MEAN_X','TARGET':Layer2019,'MATRIX_TYPE':0,'OUTPUT': Save_results+'Mean_dist_2018_2019.shp'})

#LIST ALL THE DISTANCE SHAPEFILES
listMeanDistShapes = []

for item in os.listdir(Save_results):
    if item[-3:]=='shp' and item[:4]=='Mean':
        listMeanDistShapes.append(item)

#print(listMeanDistShapes)

#display the final distance coordinate layers by looping through list of the DISTANCE SHAPEFILES
dictMeanDistShapes = {}

for shape in listMeanDistShapes:
    dictMeanDistShapes[shape[:-4]] = iface.addVectorLayer(Save_results + shape,shape[:-4],"ogr")
