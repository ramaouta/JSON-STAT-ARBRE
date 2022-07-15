#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      emman
#
# Created:     08/07/2022
# Copyright:   (c) emman 2022
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import pandas
from tkinter import *
from tkintermapview import TkinterMapView

localisation= {
    'PARIS 20E ARRDT': [48.8625565,2.3791177],
    'PARIS 19E ARRDT':[48.8871247,2.3702572],
    'PARIS 18E ARRDT': [48.8919626,2.331184],
    'PARIS 17E ARRDT': [48.8874353,2.2875386],
    'PARIS 16E ARRDT': [48.8572065,2.2279586] ,
    'PARIS 15E ARRDT': [48.8417055,2.2586112],
    'PARIS 14E ARRDT': [48.829721,2.3054438],
    'PARIS 13E ARRDT': [48.8302919,2.3480624] ,
    'PARIS 12E ARRDT': [48.8351159,2.3821336] ,
    'PARIS 11E ARRDT': [48.8601,2.36405] ,
    'PARIS 10E ARRDT':[48.8759882,2.3448933] ,
    'PARIS 9E ARRDT':[48.877097,2.3291154] ,
    'PARIS 8E ARRDT':[48.8732641,2.2935887] ,
    'PARIS 7E ARRDT': [48.8548603,2.2939732],
    'PARIS 6E ARRDT':[48.8495301,2.3131637] ,
    'PARIS 5E ARRDT': [48.8454734,2.3338198],
    'PARIS 4E ARRDT': [48.8541126,2.3393264],
    'PARIS 3E ARRDT': [48.8625682,2.3505515],
    'PARIS 2E ARRDT': [ 48.8677006,2.3323497],
    'PARIS 1ER ARRDT':[48.8620317,2.3183917],
    'CENTRE DE PARIS' : [48.8589465,2.2768229],
    'HAUTS-DE-SEINE':[48.828508,2.2188068]
}


data = ["TOUS", "TOUS","Quantité"]
new_df = pandas.read_csv(r"D:\Manu\FORMATIONS\PYTHON\JsonStatArbres\new_arbres.csv" , sep = "," , header= 0)


if data[0]== "TOUS" and data[1]== "TOUS" and data[2]== "Quantité":
    reponse =[]
    nom_arrond_max = new_df["ARRONDISSEMENT"].value_counts().idxmax(axis=0)
    nom_arrond_min = new_df["ARRONDISSEMENT"].value_counts().idxmin(axis=0)
    if nom_arrond_max in localisation:

        reponse.append(localisation[nom_arrond_max])
        reponse[0].append(nom_arrond_max)

    if nom_arrond_min in localisation:
        reponse.append(localisation[nom_arrond_min])
        reponse[1].append(nom_arrond_min)





        root_tk = Tk()
        root_tk.geometry(f"{600}x{400}")
        root_tk.title("map_view_simple_example.py")

        # create map widget
        map_widget = TkinterMapView(root_tk, width=600, height=400, corner_radius=0)
        map_widget.pack(fill="both", expand=True)


        # google normal tile server
        self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

        #map_widget.set_address("Paris France", marker=False)

        # Zone affichée de la carte
        map_widget.set_position(48.860381, 2.338594)

        # Zoom
        map_widget.set_zoom(11.5)

        # Marqueurs
        map_widget.set_marker(reponse[0][0], reponse[0][1], text = reponse[0][2], marker_color_circle="#3a0ca3", marker_color_outside="#4361ee")
        map_widget.set_marker(reponse[1][0], reponse[1][1], text = reponse[1][2], marker_color_circle="#a4161a", marker_color_outside="#df7373")

        root_tk.mainloop()

        # strg = ""
        # tmp = ""
        # for i in reponse:
            # strg=tmp+str(i[0])+","+str(i[1])+"%7C"
            # tmp = strg
            # map(strg)
else:
    print("autre Question")