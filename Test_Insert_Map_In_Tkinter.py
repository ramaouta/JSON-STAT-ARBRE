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


# https://stackoverflow.com/questions/5444438/display-google-map-api-in-python-tkinter-window
# https://github.com/TomSchimansky/TkinterMapView


import tkinter
from tkintermapview import TkinterMapView

root_tk = tkinter.Tk()
root_tk.geometry(f"{600}x{400}")
root_tk.title("map_view_simple_example.py")

# create map widget
map_widget = TkinterMapView (root_tk, width=600, height=400, corner_radius=0)
map_widget.pack(fill="both", expand=True)


# google normal tile server
map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

#map_widget.set_address("Paris France", marker=False)

# Zone affichée de la carte
map_widget.set_position(48.860381, 2.338594)

# Zoom
map_widget.set_zoom(11.5)

# Marqueurs
map_widget.set_marker(48.867, 2.323, text="2eme")
map_widget.set_marker(48.8417, 2.2586, text="15eme")


root_tk.mainloop()