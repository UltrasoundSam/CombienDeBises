#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  MapData.py
#  
#  Copyright 2018 Samuel Hill <sam@huygens>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
import sys
import matplotlib.pyplot as plt
import matplotlib.cm
import numpy as np
import pandas as pd
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.colors import Normalize
from DataCollect import departements, bises

def draw_map():
    '''
    Draw basemap and add départments onto it
    '''
    m = Basemap(resolution='i', # c, l, i, h, f or None
                projection='merc', 
                lat_0=47.05, lon_0=2.23,
                llcrnrlon=-5.68, llcrnrlat=42.31,urcrnrlon=8.47, urcrnrlat=51.39)
     
    m.bluemarble()
    m.drawcoastlines()
    m.drawcountries()
    
    # Read in Départements shape file and add to graph
    m.readshapefile('./Data/departements-20180101', 'areas')
    
    df_poly = pd.DataFrame({
        'shapes': [Polygon(np.array(shape), True) for shape in m.areas],
        'area': [area['nom'] for area in m.areas_info]
        })
    return (m, df_poly)

def plot_data(bise, dataframe, ax):
    # Create colourmap, fill in constituency polygons with % First-class travel
    cmap = plt.get_cmap('hot')   
    pc = PatchCollection(dataframe.shapes, zorder=2)
    norm = Normalize()
    
    pc.set_facecolor(cmap(norm(dataframe[str(bise)].fillna(0).values)))
    ax.add_collection(pc)
    
    mapper = matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap)
    
    mapper.set_array(dataframe[str(bise)])
    cbar = plt.colorbar(mapper, ticks=range(0, 101, 10))
    cbar.set_clim(0, 100)
    cbar.set_label('Percentage of People who give {0} bises'.format(bise))


def main(args):
    fig, ax = plt.subplots(figsize=(10,20))
    m, df_poly = draw_map()
    
    # Get list of departements
    Departements = departements()
    
    # Get Bises data and put into dataframe
    Info = {dep: bises(code) for dep, code in Departements.items()}
    Info = pd.DataFrame(Info).transpose().fillna(0)
    Info = Info.reset_index()
    Info = Info.rename(columns={'index': 'area'})
    
    # Merge Bises and shapefile data
    df_poly = df_poly.merge(Info, on='area', how='left')
    
    plot_data(args, df_poly, ax)
    plt.show()


if __name__ == '__main__':
    main(sys.argv[1])

