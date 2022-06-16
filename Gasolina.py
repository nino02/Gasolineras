#!/usr/bin/env python
# coding: utf-8

# # Precio de la gasolina

# In[1]:


import pandas as pd
import requests


# In[2]:


file = requests.get('https://geoportalgasolineras.es/resources/files/preciosEESS_es.xls')
guardar = open('espanya_gasolina.xls','wb').write(file.content)


# In[3]:


Municipio = input('Insertar Municipio: ')
try:
    data = pd.read_excel('espanya_gasolina.xls',skiprows=3,index_col=4,decimal=',')
    data = data[data.Localidad.eq(Municipio)]
    Iprecio = data['Precio gasolina 95 E5'].idxmin()
    Media_latitud = data['Latitud'].mean()
    Media_longitud = data['Longitud'].mean()
except:
    data = pd.read_excel('espanya_gasolina.xls',skiprows=3,index_col=4,decimal=',')
    f = lambda x: True if Municipio in x else False
    data = data[data['Localidad'].apply(f)]
    Iprecio = data['Precio gasolina 95 E5'].idxmin()


# In[4]:


print('Precio mas bajo:')
print(Iprecio)                                     #CALLE DE LA GASOLINERA
print(f"{data['Precio gasolina 95 E5'].min()} €")  #PRECIO MINIMO
print(data.iloc[data.index.get_loc(Iprecio),7])    #FECHA DE ACTUALIZACION 
print(data.iloc[data.index.get_loc(Iprecio),25])   #ROTULO
print(f"Precio para el deposito de la moto: {data['Precio gasolina 95 E5'].min()*7} €\n")
if Municipio == 'ASPE': print(f"Precio de la gasolina REPSOL: {data[data.Rótulo.eq('LEVANTINA')]['Precio gasolina 95 E5'][0]} €")


# In[5]:


data[['Precio gasolina 95 E5','Rótulo','Toma de datos','Tipo servicio']]


# ### Buscar por gasolinera

# In[6]:


gasolinera = input('Insertar gasolinera: ')
f = lambda x: True if gasolinera in x else False
data[data['Rótulo'].apply(f)]


# ### Toda la tabla

# In[7]:


data.describe()


# ## Las gasolineras mas cercanas

# In[19]:


import math
data = pd.read_excel('espanya_gasolina.xls',skiprows=3,index_col=4,decimal=',')
dis = input('Km a la redonda(aconsejable 10): ')

def Haversine(Latitud,Longitud):
    R = 6373
    a = math.pow(math.sin(math.radians(Latitud - Media_latitud)/2),2) + math.cos(math.radians(Media_latitud))*math.cos(math.radians(Latitud))*math.pow(math.sin(math.radians(Longitud-Media_longitud)/2),2)
    c = 2*math.atan2(math.sqrt(a),math.sqrt(1-a))
    
    return (R*c) <float(dis)

vec = []
for i in range(len(data['Latitud'].tolist())):
    Lat = data['Latitud'].tolist()[i]
    Long = data['Longitud'].tolist()[i]
    vec.append(Haversine(Lat,Long))

data = data[vec]


# In[20]:


print(data[data.Localidad.eq('HONDON DE LOS FRAILES')])

