# QGIS_Customization_s3853274
 
#The final outcome of the customization is to find out - What is the Ground Parrot species movement pattern since 2000 (distance between ground parrot records of the previous and the following year)? 
#Pre-processing: The relevant shapefiles for this customization have been manually saved in GDA 2020 Map Grid of Australia Zone 55, EPSG: 7855 CRS. Click OK for Inverse Transformation from EPSG: 7855 to EPSG: 3111 for the East Gippsland Study Area shapefile

#Check the Data_3 zip file to access the relevant data used for this code

Data used:

The following shapefiles will be used to analyze both the geographic questions. First, the shapefile representing the fire history data that contains the recent 2019-2020 burnt severity. This shapefile is taken from the http://datashare.vic.gov/ website. The layer includes features of the last time an area has been burnt by wildfire or prescribed burning and represents a sequential overlay of all FIRE_HISTORY layers, from older fire seasons (1900) to the most recent fire seasons (2021). Another layer required for the tasks is the shapefile that contains the Wet Heathland patches. This data must be extracted from the Ecological Vegetation classes shapefile (2005) from the following link https://discover.data.vic.gov.au/dataset/native-vegetation-modelled-2005-ecological-vegetation-classes-with-bioregional-conservation-sta 
The Ground Parrot records shapefile has been taken from the NatureKit website, which contains records dating from 1804 to 2019. The 2019 records are only dated until the 18th November, just before the bushfire event of 2019/2020 (21st November). 

**Summary of the customization**

The customization for the project is to rename the survey date field attributes by creating a new field that contains only the year of the ground parrot survey records in the NatureKit shapefile. This renaming will ensure that the original data will not be disturbed, and it is easy to classify the features based on the survey year. Furthermore, this step is performed as it is unnecessary to track the movement of the species according to a specific date. After the new field is created, a separate shapefile will be made for each year from 2000 to 2019. Therefore, 20 shapefiles have been created in the end. These layers will be used to calculate the distances between each point layer for the first task of the analysis. 
This customization reduces the end-user's time and effort in performing repetitive tasks such as renaming the attributes and creating multiple shapefile outputs. Such tasks often take many actions as the end-user must look into several features within a shapefile and manually enter the corresponding desired field value. This task can take several hours, but using queries and expressions of PyQGIS can automatically update the field values by running the script. The customization will potentially facilitate a GIS Principles Project that focuses on assessing the Eastern Ground Parrot habitat following the 2019/20 bushfires and a real-world project on identifying the remaining patches of the Eastern Ground Parrot suitable habitat that one of the group members is undertaking.


