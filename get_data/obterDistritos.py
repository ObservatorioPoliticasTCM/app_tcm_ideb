import os
import pandas as pd
import geopandas as gpd
from json import dumps


def distritos(path_salvo, dfIdebIniciais, dfIdebFinais):

    if os.path.exists(path_salvo):

        geodfDistritos = gpd.read_file(path_salvo)
        #geodfDistritos.to_file('c:\\c2\\myshpfile.geojson', driver='GeoJSON')


        if "Unnamed: 0" in geodfDistritos:
            geodfDistritos.drop("Unnamed: 0", axis=1, inplace=True)

        geodfDistritos.set_crs(epsg=31983, inplace=True)

    if geodfDistritos is not None:
        dfIdebIniciais['coddist'] = dfIdebIniciais['coddist'].astype(int).astype(str)
        geodfAgrupado = dfIdebIniciais.groupby(['tipo_anos', 'coddist'])[['ideb_2019']].mean()


        dfMerged = pd.merge(geodfDistritos, geodfAgrupado,
                          how='left', left_on='ds_codigo', right_on='coddist')

        # ds = dfMerged[dfMerged.columns[0:5]]
        # ds.to_excel("c:\\c2\\ds.xlsx")


        dfIdebFinais['coddist'] = dfIdebFinais['coddist'].astype(int).astype(str)
        geodfAgrupado = dfIdebFinais.groupby(['tipo_anos', 'coddist'])[['ideb_2019']].mean()

        dfMerged2 = pd.merge(dfMerged, geodfAgrupado,
                          how='left', left_on='ds_codigo', right_on='coddist')


        dfMerged2 = dfMerged2.rename(columns={'ideb_2019_x': 'ideb_iniciais', 'ideb_2019_y': 'ideb_finais'})
        dfMerged2['ideb_iniciais'] = dfMerged2['ideb_iniciais'].fillna(0)
        dfMerged2['ideb_finais'] = dfMerged2['ideb_finais'].fillna(0)
        media = dfMerged2['ideb_iniciais'] + dfMerged2['ideb_finais']
        dfMerged2['media_final'] = media / 2

        geodfAgrupadox = dfIdebFinais.groupby(['tipo_anos', 'coddist'])[['ideb_2019']].min()



    return dfMerged2


