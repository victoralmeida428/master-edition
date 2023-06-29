import pandas as pd
from geopy.geocoders import ArcGIS
import re


nom = ArcGIS()
def encontrar_coordenadas(x: str):
    coordenada = nom.geocode(x)
    if coordenada:
        return coordenada.latitude, coordenada.longitude
    

def ler_mala():
    return pd.read_csv('//Pastor/analytics/MalaDireta.csv', sep=';', encoding='latin1')



class MalaDireta:

    def filtros_mala(self):
        df = ler_mala()
        df = df.loc[(df['ID'] < 8000) | (df['ID'] > 8999)]
        return df.drop_duplicates(subset=['ID'], keep='first')


    def tratar_cep(self):
        """Padronizando o cep: Retirando o que não é numérico e preenchendo com 0's, se necessário, no início"""
        df = self.filtros_mala()
        df['CEP'] = df['CEP'].astype(str)
        df['CEP'] = df['CEP'].apply(lambda x: re.sub('[^0-9]', '', x).zfill(8))
        df['CEP'] = df['CEP'].apply(lambda x: f'{x[:5]}-{x[-3:]}')
        return df
    
    def col_endereco(self):
        df = self.tratar_cep()
        colunas = ['CEP', 'Bairro', 'Cidade', 'UF', 'País', 'Logradouro']
        for coluna in colunas:
            df[coluna].fillna('', inplace=True)

        df.loc[(df['País'] == 'Brasil'), 
            'Endereco'] = 'CEP: ' + df['CEP'] + ', ' + df['Logradouro'] + ', Cidade: ' + df['Cidade'] + ', Estado: ' + df['UF'] + ', ' + df['País']

        df.loc[(df['País'] != 'Brasil'), 
            'Endereco'] = df['Logradouro'] + ', ' + df['Bairro'] + ', ' + df['Cidade'] + ', ' + df['País']
        return df
    
    
    def exportar_mala(self, coordenadas=False):
        if not coordenadas:
            return self.tratar_cep()
        
        else:
            df = self.col_endereco()
            df[['Latitude', 'Longitude']] = df['Endereco'].apply(lambda x: pd.Series(encontrar_coordenadas(x)))
            df.drop('Endereco', axis=1, inplace=True)
            return df
            
    


# class Coordenadas:

#     def __init__(self, df):
#         self.df = df

    
#     def col_endereco(self):
#         colunas = ['CEP', 'Bairro', 'Cidade', 'UF', 'País', 'Logradouro']
#         for coluna in colunas:
#             self.df[coluna].fillna('', inplace=True)

#         self.df.loc[(self.df['País'] == 'Brasil'), 
#             'Endereco'] = 'CEP: ' + self.df['CEP'] + ', ' + self.df['Logradouro'] + ', Cidade: ' + self.df['Cidade'] + ', Estado: ' + self.df['UF'] + ', ' + self.df['País']

#         self.df.loc[(self.df['País'] != 'Brasil'), 
#             'Endereco'] = self.df['Logradouro'] + ', ' + self.df['Bairro'] + ', ' + self.df['Cidade'] + ', ' + self.df['País']
#         return self.df

#     def encontrar_coordenadas(self):
#         df = self.col_endereco()

#         df['Latitude'] = ''
#         df['Longitude'] = ''

#         nom = ArcGIS()

#         for linha in df.itertuples():
#             endereco = linha.Endereco
#             coordenada = nom.geocode(endereco)
#             if coordenada:
#                 df.at[linha.Index, 'Latitude'] = coordenada.latitude
#                 df.at[linha.Index, 'Longitude'] = coordenada.longitude


#         df['Latitude'] = df['Latitude'].astype(str).apply(lambda x: x.replace('.',','))
#         df['Longitude'] = df['Longitude'].astype(str).apply(lambda x: x.replace('.',','))

#         df.drop('Endereco', axis=1, inplace=True)
#         return df
        



    # def encontrar_coordenadas2(self):
    #     latitudes = []
    #     longitudes = []
    #     nom = ArcGIS()
        

    #     for item in self.df.itertuples():
    #         coordenada = nom.geocode(item.Endereco)
    #         try:
    #             lat = coordenada.latitude
    #             lon = coordenada.longitude
    #             latitudes.append(lat)
    #             longitudes.append(lon)
    #         except:
    #             latitudes.append('Erro')
    #             longitudes.append('Erro')

            
    #     self.df['Latitude'] = latitudes
    #     self.df['Longitude'] = longitudes

    #     self.df['Latitude'] = self.df['Latitude'].astype(str).apply(lambda x: x.replace('.',','))
    #     self.df['Longitude'] = self.df['Longitude'].astype(str).apply(lambda x: x.replace('.',','))

    #     self.df.drop('Endereco', axis=1, inplace=True)
    #     return self.df
