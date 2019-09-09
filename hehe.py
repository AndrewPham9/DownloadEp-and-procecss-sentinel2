

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
def main ():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", dest = "shp" , help = "put lowLeftLong here", type = str)
    parser.add_argument("-d", dest = "date" ,help = "put lowLeftLat here", type = str)
    parser.add_argument("-p", dest = "province" ,help = "put upRightLong here", type = str)

    args = parser.parse_args()
    print (args.shp)
    print (args.date)
    print (args.province)

if __name__=='__main__':
    main()  