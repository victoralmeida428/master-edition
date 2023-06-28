import plotly
import dash_bootstrap_components as dbc
from dash import html, dcc
import dash
from django_plotly_dash import DjangoDash
from geopy.geocoders import ArcGIS
import plotly.graph_objects as go
import multiprocessing
import re
import pandas as pd

class Mapa:
    def __init__(self, df):
        self.df = df

    def criar_mapa(self):
        app = DjangoDash("mapa",
                add_bootstrap_links=True)

        app.layout = html.Div(
            dcc.Graph(id='mapa', figure=self.gerar_grafico()))
        return app
    
    def encontrar_coordenadas(self, x):
        nom = ArcGIS()
        coordenada = nom.geocode(x)
        if coordenada:
            return coordenada.latitude, coordenada.longitude

    def tratar_cep(self):
        """Padronizando o cep: Retirando o que não é numérico e preenchendo com 0's, se necessário, no início"""
        df = self.df
        df['CEP'] = df['CEP'].astype(str)
        df['CEP'] = df['CEP'].apply(lambda x: re.sub('[^0-9]', '', x).zfill(8))
        df['CEP'] = df['CEP'].apply(lambda x: f'{x[:5]}-{x[-3:]}')
        return df
    
    def requisicao(self, df):
        df[['Latitude', 'Longitude']] = df['CEP'].apply(lambda x: pd.Series(self.encontrar_coordenadas(x)))
        return df
    def gerar_grafico(self):
        # Cria o mapa usando o Plotly
        df = self.tratar_cep()
        df = self.requisicao(df)
        fig = go.Figure(go.Scattermapbox(
            lat=(df['Latitude']),
            lon=(df['Longitude']),
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=15,
                color='rgb(0, 100, 58)',
                opacity=0.7
            ),
            text=df['CEP'],
        ))
        # Configura o layout do mapa
        fig.update_layout(
            mapbox_style='open-street-map',
            mapbox_center_lon=0,
            margin={'r': 0, 't': 0, 'l': 0, 'b': 0}
        )
        return fig