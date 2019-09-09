from osgeo import gdal
from osgeo import ogr
import os
import copy
import subprocess
import shutil
import configparser
dirname = os.path.dirname(__file__)
def config (configFile = dirname + '/config/config.txt', section=None):
    parser = configparser.ConfigParser()
    parser.read(configFile)
    return dict(parser.items(section))

def getFoldTiff (folder):
    folders = copy.copy(folder)
    TIFs = []
    allFiles = os.listdir(folders)
    for i in allFiles:
        if '.tif' in i:
            i = folder+'//' + i
            TIFs.append(i)
    return TIFs


def clip (shp, inRaster, outRaster):
    cmdLine2 = "gdalwarp -cutline " +shp + " -crop_to_cutline -of Gtiff -dstnodata 0 -overwrite " + inRaster + ' ' + outRaster 
    p1 = subprocess.Popen(cmdLine2,shell=True)
    p1.wait()


def MosaicFolder (inFolder = None, outFolder = None):
    py = config(section='py_machine')
    py_scripts = py['py_3_scripts']
    alpha = '0'
    inRaster = str()

    Tifs =  getFoldTiff (inFolder)
    print (Tifs)
    for Tif in Tifs:
        inRaster = inRaster + ' ' + Tif                
    outRaster = outFolder + '/' + os.path.basename(inFolder)
    print (inRaster)
    command="py -3 "+py_scripts+"/gdal_merge.py -o "+outRaster+".TIF -of GTiff -ot Float32 -n " + alpha + " -a_nodata NaN"+ inRaster
    p1 = subprocess.Popen(command,shell=True)
    p1.wait()
