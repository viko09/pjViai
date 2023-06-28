# Import mne data
import mne
import os
import pandas as pd
import matplotlib.pyplot as plt

data_path = '/Users/vikoluna/Apps/PyCharm/classifEGG1/codes/data/Ale_piloto_1/'
vhdr_file = os.path.join(data_path, 'Ale_piloto_1.vhdr')

# MNE Workspace
# Import the BrainVision data into an MNE Raw object
raw = mne.io.read_raw_brainvision(vhdr_file, preload=True)

# Obtener el canal
chN1 = 'Ch1'  # Reemplaza 'nombre_del_canal' con el nombre del canal que deseas extraer
datos_canal = raw[chN1][0]

chN2 = 'Ch2'
datos_canal2 = raw[chN2][1]

# Crear un DataFrame
df = pd.DataFrame(datos_canal.T, columns=['Canal'])
# Transponer los datos y agregar una columna 'Canal'

# Guardar el DataFrame en un archivo CSV
df.to_csv('brainChannel1.csv', index=False)

# Leer el archivo CSV
df = pd.read_csv('brainChannel1.csv')

# Imprimir el DataFrame
print(df.head())

df.plot(color='green', alpha=0.70)
plt.title("Actividad eléctrica del cerebro")
plt.xlabel("Tiempo")
plt.ylabel("Voltaje")
plt.legend()
plt.locator_params()
plt.grid()
plt.show()
