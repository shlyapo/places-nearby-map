import os

import branca
import folium
from folium.plugins import MousePosition

from commands.map.get import MapXY


class Map():
    def __init__(self, db_helper):
        self.name_map = f"Map_original.html"
        self.db_helper = db_helper
        self.map = None
        self.original_map = None
        self.dots = []

    def set_map(self, zoom):
        self.original_map = folium.Map(location=[self.map.x_location, self.map.y_location], zoom_start=zoom)
        self.add_group()
        self.add_mouse_position()
        self.original_map.save(self.name_map)

    def add_group(self):
        pick = folium.map.FeatureGroup()
        for pair in self.map.dots:
            html_img = ""
            pick.add_child(
                folium.features.CircleMarker(
                    [float(pair.x_cor), float(pair.y_cor)], radius=8,
                    color='red', fill_color='Red'
                )
            )
            pick.add_child(
                folium.features.CircleMarker(
                    [float(pair.x_cor), float(pair.y_cor)], radius=8,
                    color='red', fill_color='Red'
                )
            )

            for path in pair.paths:
                html_img += f"<img src={path[0]} style='width:150px;height:150px;'>"
            if len(html_img) == 0:
                html_img += "<p> No images </p>"

            """folium.Marker([float(pair.x_cor), float(pair.y_cor)],  # широта и долгота Санкт-Петербурга
            popup = folium.Popup(branca.element.IFrame(html=f"<img src=~/1.png>", width=500, height=400),
                                 max_width=500)).add_to(self.original_map)"""
            folium.Marker(
                location=[float(pair.x_cor), float(pair.y_cor)],
                popup=html_img,
                tooltip=f'{pair.x_cor}, {pair.y_cor}',
                icon=folium.Icon(color="green")).add_to(self.original_map)
        # self.original_map.add_child(pick)

    def add_mouse_position(self):
        formatter = "function(num) {return L.Util.formatNum(num, 5);};"
        mouse_position = MousePosition(
            position='topright',
            separator=' Long: ',
            empty_string='NaN',
            lng_first=False,
            num_digits=20,
            prefix='Lat:',
            lat_formatter=formatter,
            lng_formatter=formatter,
        )

        self.original_map.add_child(mouse_position)

    def run(self, args):
        print(1)
        self.map = MapXY(self.db_helper, args.country)
        self.set_map(args.zoom)

