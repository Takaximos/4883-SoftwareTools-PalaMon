import pandas
from gui import buildWeatherURL
from gui import daily_filter
from get_weather import asyncGetWeather
from bs4 import BeautifulSoup
import json
import PySimpleGUI as sg

if __name__ == '__main__':
    
    url, filter = buildWeatherURL()
    
    if filter == "daily":
        web = asyncGetWeather(url)
        
        daily_filter(web)
        
    # Read the JSON file
    with open('daily_data.json', 'r') as f:
        data = json.load(f)

    # Prepare the table data
    table_data = []
    for key, value in data.items():
        table_data.append([key, str(value)])

    # Create the layout for the window
    layout = [
        [sg.Table(values=table_data,
                headings=['Key', 'Value'],
                max_col_width=75,
                auto_size_columns=True,
                display_row_numbers=True,
                justification='left',
                num_rows=min(25, len(table_data))  # Display maximum 25 rows
                )],
        [sg.Button('Close')]
    ]

    # Create the window
    window = sg.Window('JSON Viewer', layout)

    # Event loop to process events
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Close':
            break

    # Close the window
    window.close()