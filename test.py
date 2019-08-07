from usgs import api
import usgs
from usgs import USGS_API
from usgs import xsi, payloads
import requests
import urllib.request as urllib2
import json
import argparse
import numpy as np 
import sys
import math
from osgeo import gdal
from osgeo import ogr
from gdalconst import*
import os
import re
import copy
import shutil
import zipfile
import yu
import gzip
import senDown
import process

def run(shp,date,province):
	if not os.path.exists('NDVI_%s'%(province)):
		os.mkdir('NDVI_%s'%(province))
	else:
		pass
	driver = ogr.GetDriverByName('ESRI Shapefile')
	dataSource = driver.Open(shp, 0)
	layer = dataSource.GetLayer()
	feature = layer[0]
	geom = feature.GetGeometryRef()

	A = geom.GetEnvelope()
	lowLeftLat = A[2] #(y dưới trái)
	lowLeftLong = A[0] #(x dưới trái)
	upRightLat = A[3] #(y trên phải)
	upRightLong = A[1] #(x trên phải)

	print (lowLeftLat)
	print (lowLeftLong)
	print (upRightLat)
	print (upRightLong)
	
	results = list()
	#create a sentinel folder
	#sentinel_folders = senDown.Download_sentinel_2(str(lowLeftLat),str(lowLeftLong),str(upRightLat),str(upRightLong),str(date))
	sentinel_folders = ['L1C_T48PXS_A012256_20190712T032057']
	for sentinel_folder in sentinel_folders:
		path_to_zip_file = sentinel_folder + '.zip'
		with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
			zip_ref.extractall(sentinel_folder)
			process.processByXML(sentinel_folder, shp, province,'NDVI_%s'%(province))



shp = 'D:/python/STAC_intern_project/snappy/HCM/HCM.shp'
date = '20190720'
province = 'HCM'
run (shp, date, province)


