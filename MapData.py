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
'''
Programme that will collect the bise data and plot it on a map of France,
showing a heat map of popularity of different number of bises.
'''
import sys
import numpy as np
import pandas as pd

import matplotlib.cm
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.colors import Normalize
from DataCollect import departements, bises

def draw_map():
    '''
    Draw basemap and add départments onto it
    '''
    Map = Basemap(resolution='i', # c, l, i, h, f or None
                  projection='merc',
                  lat_0=47.05, lon_0=2.23,
                  llcrnrlon=-5.68, llcrnrlat=42.31, urcrnrlon=8.47, urcrnrlat=51.39)

    Map.bluemarble()
    Map.drawcoastlines()
    Map.drawcountries()

    # Read in Départements shape file and add to graph
    Map.readshapefile('./Data/departements-20180101', 'areas')

    df_poly = pd.DataFrame({
        'shapes': [Polygon(np.array(shape), True) for shape in Map.areas],
        'area': [area['nom'] for area in Map.areas_info]
        })
    df_poly['area'] = df_poly['area'].str.lower()
    return (Map, df_poly)

def plot_data(bise, dataframe, ax):
    '''
    Function that will plot départemental bise data to map
    '''
    # Create colourmap, fill in constituency polygons with % First-class travel
    cmap = plt.get_cmap('hot')
    pc = PatchCollection(dataframe.shapes, zorder=2)
    norm = Normalize(vmin=0, vmax=100)

    pc.set_facecolor(cmap(norm(dataframe[str(bise)].fillna(0).values)))
    ax.add_collection(pc)

    mapper = matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap)

    mapper.set_array(dataframe[str(bise)])
    cbar = plt.colorbar(mapper, ticks=range(0, 101, 10))
    cbar.set_label('Percentage of People who give {0} bises'.format(bise))


def main(args):
    '''
    Main function that links all function together
    '''
    fig, ax = plt.subplots()
    m, df_poly = draw_map()

    # Get list of departements
    Departements = departements()

    # Get Bises data and put into dataframe
    Info = {dep: bises(code) for dep, code in Departements.items()}
    Info = pd.DataFrame(Info).transpose().fillna(0)
    Info = Info.reset_index()
    Info = Info.rename(columns={'index': 'area'})
    Info['area'] = Info['area'].str.lower()

    # Merge Bises and shapefile data
    df_poly = df_poly.merge(Info, on='area', how='left')

    plot_data(args, df_poly, ax)
    plt.show()


if __name__ == '__main__':
    main(sys.argv[1])
