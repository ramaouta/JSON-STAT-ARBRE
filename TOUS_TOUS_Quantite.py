#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      kev97
#
# Created:     12/07/2022
# Copyright:   (c) kev97 2022
# Licence:     <your licence>
#-------------------------------------------------------------------------------

if data[0] == 'TOUS' and data[1] == 'TOUS' and data[2] == "Quantité":

        #CREATION DU GRAPH------------------------------------------------------
        font = {'family' : 'normal','size'   : 5}
        sns.set(style="white")
        dataQ1 = new_df
        dataQ1 = dataQ1.assign(COUNT=1)
        dataQ1 = (pandas.crosstab(dataQ1['ARRONDISSEMENT'], dataQ1['COUNT']))
        dataQ1.columns=['COUNT']
        listeArrdt = dataQ1.index.tolist()
        dataQ1.insert(0, "ARRONDISSEMENT", listeArrdt)
        plt.figure(figsize = (16, 9))
        plt.rc('font', **font)
        f, ax = plt.subplots(figsize=(12, 9))
        f.subplots_adjust(bottom=0.30)
        plt.xticks(rotation=80)
        plt.gcf().set_size_inches(5, 5)
        plt.xlabel('ARRONDISSEMENT')
        sns.barplot(x = 'ARRONDISSEMENT', y = 'COUNT',data = dataQ1)

        AfficheframeCanvas()


        #CREATION DE LA MAP ----------------------------------------------------
        # create map widget
        dataQ1 = new_df
        map_widget = TkinterMapView(frameTheMap, width=400, height=400, corner_radius=0)
        map_widget.pack(  pady = 10, padx = 10, side=RIGHT)

        map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

        # Zone affichée de la carte = PARIS
        map_widget.set_position(48.860381, 2.338594)

        # Zoom
        map_widget.set_zoom(11)

        #marqueurs =[]
        marqueurs = {}
        zone = []
        nom_arrond_max = dataQ1["ARRONDISSEMENT"].value_counts().idxmax(axis=0)
        nom_arrond_min = dataQ1["ARRONDISSEMENT"].value_counts().idxmin(axis=0)
        if nom_arrond_max in localisation:

            marqueurs[nom_arrond_max] = localisation[nom_arrond_max]
            zone.append(appartenance[nom_arrond_max])

        if nom_arrond_min in localisation:
            marqueurs[nom_arrond_min] = localisation[nom_arrond_min]
            zone.append(appartenance [nom_arrond_min])

        affiche_map(marqueurs, zone)


        #CREATION DU TEXTE -----------------------------------------------------
        nbr_arrMax = new_df["ARRONDISSEMENT"].value_counts().max()
        nbr_arrMin = dataQ1["ARRONDISSEMENT"].value_counts().min()

        answer = f"L'arrondissement avec le plus d'arbre est {nom_arrond_max} comptant un total de {nbr_arrMax} arbre.\n\nCelui avec le moins d'arbre est {nom_arrond_min} avec un total de {nbr_arrMin} arbre."
        AfficheframeLabelText()