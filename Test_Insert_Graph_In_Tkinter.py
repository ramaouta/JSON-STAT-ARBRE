#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      emman
#
# Created:     07/07/2022
# Copyright:   (c) emman 2022
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from tkinter import *
from tkinter import messagebox
import pandas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)
import seaborn as sns
import numpy as np
import random





def plot():

    sns.set(style="white")

    '''
    rs = np.random.RandomState(33)
    d = pandas.DataFrame(data=rs.normal(size=(100, 26)), columns=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26])

    corr = d.corr()

    mask = np.zeros_like(corr, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True

    #data = pandas.read_csv(r"D:\Manu\FORMATIONS\PYTHON\JsonStatArbres\new_arbres.csv")
    #f = sns.catplot(x="ARRONDISSEMENT", kind="count", palette="ch:.25", data=data)

    f, ax = plt.subplots(figsize=(11, 9))

    cmap = sns.diverging_palette(220, 10, as_cmap=True)
    '''

    dataQ1 = pandas.read_csv(r"D:\Manu\FORMATIONS\PYTHON\JsonStatArbres\new_arbres.csv")
    dataQ1 = dataQ1.assign(COUNT=1)
    dataQ1 = (pandas.crosstab  ( dataQ1['ARRONDISSEMENT'], dataQ1['COUNT'] ))
    dataQ1.columns=['COUNT']
    listeArrdt = dataQ1.index.tolist()
    dataQ1.insert(0, "ARRONDISSEMENT", listeArrdt)


    plt.figure(figsize = (20, 20))
    f, ax = plt.subplots(figsize=(12, 9))
    f.subplots_adjust(bottom=0.50)
    plt.xticks(rotation=80)
    plt.gcf().set_size_inches(5, 5)
    sns.barplot(x = 'ARRONDISSEMENT', y = 'COUNT',data = dataQ1)

    #sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0, square=True, linewidths=.5, cbar_kws={"shrink": .5})

    return f



window = Tk()

window.title('Plotting in Tkinter')

window.geometry("800x800")



fig = plot()
canvas = FigureCanvasTkAgg(fig, master = window)
canvas.draw()
canvas.get_tk_widget().pack()

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        window.destroy()
        window.quit()

window.protocol("WM_DELETE_WINDOW", on_closing)

window.mainloop()