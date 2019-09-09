import requests
import urllib.request as urllib2
import argparse
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
import senDown
import process
import config_this

def run(shp,date,province):

	if not os.path.exists('NDVI_%s'%(province)):
		os.mkdir('NDVI_%s'%(province))
	else:
		pass

	if not os.path.exists('NDVI_%s_%s'%(province, date)):
		os.mkdir('NDVI_%s_%s'%(province, date))
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

	#create a sentinel 
	sentinel_folders = senDown.Dowfoldernload_sentinel_2(str(lowLeftLat),str(lowLeftLong),str(upRightLat),str(upRightLong),str(date))
	# sentinel_folders = ['L1C_T48PXS_A012256_20190712T032057','L1C_T48PXT_A012256_20190712T032057']
	for sentinel_folder in sentinel_folders:
		path_to_zip_file = sentinel_folder + '.zip'
		with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
			print ('unzipping...')
			zip_ref.extractall(sentinel_folder)
			process.processByXML(sentinel_folder, shp, province,'NDVI_%s_%s'%(province, date))
	
	config_this.MosaicFolder('NDVI_%s_%s'%(province, date), 'NDVI_%s'%(province))
	shutil.rmtree('NDVI_%s_%s'%(province, date))

def main ():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", dest = "shp" , help = "put lowLeftLong here", type = str)
    parser.add_argument("-d", dest = "date" ,help = "put lowLeftLat here", type = str)
    parser.add_argument("-p", dest = "province" ,help = "put upRightLong here", type = str)

    args = parser.parse_args()

    result = run(args.shp,args.date,args.province)


if __name__=='__main__':
    main()  

