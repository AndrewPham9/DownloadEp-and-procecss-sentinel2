from osgeo import gdal
from osgeo import ogr
import subprocess
import os
from glob import glob
import configparser
import shutil
import config_this


def processByXML (infolder, shp ,province, outfolder):
	##config all
	con = config_this.config(section='config')
	wget, gpt, sen2cor = con['wget'], con['gpt'], con['sen2cor']

	processDataset = config_this.config(section='processDataset')
	bat, XML, properties1= processDataset['bat'], processDataset['xml'], processDataset['properties1']
	properties2  =  properties1.replace('ARVI_Subset1','ARVI_Subset2')

	#sen2cor for sourceproduct_1 ---> sourceproduct_2
	Sourceproduct_1 = infolder+'/'+os.listdir(infolder)[0]
	print ('sen2cor...')
	cmdLine = sen2cor + ' --resolution 10 ' + '--output_dir ' + infolder + ' ' + Sourceproduct_1
	p1 = subprocess.Popen(cmdLine,shell=True)
	p1.wait()
	#put sourceproduct_2 as inraster
	for file in os.listdir(infolder):
		if infolder + '/' + file == Sourceproduct_1:
			pass
		else:
			Sourceproduct_2 = infolder + '/' + file
			outRaster = infolder + '/' + file.split('_')[2] + '_' + file.split('_')[1] + '_'+ file.split('_')[5] + province

	# insert geometry of shape file to cutline in SNAP
	driver = ogr.GetDriverByName("ESRI Shapefile")	
	data = driver.Open(shp, 0)
	layer = data.GetLayer()
	for feature in layer:
		geom = feature.GetGeometryRef()

	with open(properties1, 'r') as f1:
		with open (properties2, 'w') as f2:
			lines = f1.readlines()
			print (lines)
			for line in lines:
				if line.startswith('geometry'):
					lines[lines.index(line)] = line.replace(line.split('=')[1],str(geom))
					f2.writelines(lines)

	# caculate NDVI
	cmdLine = "%s %s -p %s -SsourceProduct=%s -t %s -f %s"%(gpt,XML,properties2,Sourceproduct_2,outRaster,'GeotifF')
	# p1 = subprocess.Popen(cmdLine,shell=True)
	p1.wait()

	#clip raster
	inRaster = outRaster + '.tif'
	outRaster = outfolder + '/' + inRaster.replace('.tif','_clipped.tif').split('/')[-1]
	config_this.clip(shp, inRaster, outRaster)

	# os.remove(properties2)
	# shutil.rmtree(infolder)


