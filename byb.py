import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL de la página web que deseas descargar
url = r'https://www.airbnb.es/s/Comunidad-de-Madrid--Espa%C3%B1a/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2023-12-01&monthly_length=3&price_filter_input_type=0&channel=EXPLORE&query=Comunidad%20de%20Madrid%2C%20Espa%C3%B1a&place_id=ChIJuTPgQHqBQQ0RgMhLvvNAAwE&date_picker_type=calendar&source=structured_search_input_header&search_type=autocomplete_click'

# Realizar la solicitud GET para obtener el contenido HTML de la página
response = requests.get(url, verify=False)

# Verificar si la solicitud fue exitosa (código de estado 200)
if response.status_code == 200:
    # Obtener el contenido HTML de la página
    html_content = response.text

    # Crear un objeto BeautifulSoup para analizar el HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Crear una lista para almacenar los datos de las casas
    casas_data = []

    # Encontrar todas las tarjetas de listado de casas en la página
    listing_cards = soup.find_all('div', class_='_8ssblpx')

    for card in listing_cards:
        # Extraer información de cada tarjeta de listado
        link = 'https://www.airbnb.es' + card.find('a', class_='_gjfol0').get('href')

        # Crear un nuevo objeto BeautifulSoup para analizar el contenido de cada enlace
        sopa = BeautifulSoup(requests.get(link, verify=False).text, 'html.parser')

        # Aquí puedes continuar extrayendo más información específica del enlace, según tus necesidades

        # Agregar datos a la lista
        casas_data.append({
            'Enlace': link,
            'Precio': card.find('span', class_='_doc79r').text,
            'Habitaciones': card.find('div', class_='_3hmsj')['aria-label'].split()[0],
            'Dirección': card.find('div', class_='_oq1k89').text.strip()
        })

    # Crear un DataFrame de pandas con los datos
    df = pd.DataFrame(casas_data)

    print (df)

    # Guardar el DataFrame en un archivo Excel
    df.to_excel(r'C:\Users\cesar\OneDrive\Escritorio\turismo\casas_airbnb.xlsx', index=False)

    print('Datos guardados en casas_airbnb.xlsx')
else:
    print(f'Error al descargar la página. Código de estado: {response.status_code}')