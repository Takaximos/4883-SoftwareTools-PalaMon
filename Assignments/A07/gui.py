""" 
Description:
    This is an example gui that allows you to enter the appropriate parameters to get the weather from wunderground.
TODO:
    - You will need to change the text input boxes to drop down boxes and add the appropriate values to the drop down boxes.
    - For example the month drop down box should have the values 1-12.
    - The day drop down box should have the values 1-31.
    - The year drop down box should have the values ??-2023.
    - The filter drop down box should have the values 'daily', 'weekly', 'monthly'.
"""
import os
import PySimpleGUI as sg
import tkinter as tk
from tkinter import ttk   
import json
import get_weather
import webbrowser
import pandas
from bs4 import BeautifulSoup
from lxml import etree
from bs4 import BeautifulSoup as bs

months = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
days = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"]
years = ["2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023"]
dic = dict()
itt = 0

with open('airports-better.json') as file:
    json_data = json.load(file)
    
countries = []
cities = []

for item in json_data:
    country_name = item['country']
    city_name = item['city']
    if country_name not in countries:
        countries.append(country_name)
    if city_name not in cities:
        cities.append(city_name)
    
countries.sort()
cities.sort()

base_url = "https://wunderground.com/history"

def currentDate(returnType='tuple'):
    """ Get the current date and return it as a tuple, list, or dictionary.
    Args:
        returnType (str): The type of object to return.  Valid values are 'tuple', 'list', or 'dict'.
    """
    from datetime import datetime
    if returnType == 'tuple':
        return (datetime.now().month, datetime.now().day, datetime.now().year)
    elif returnType == 'list':
        return [datetime.now().month, datetime.now().day, datetime.now().year]

    return {
        'day':datetime.now().day,
        'month':datetime.now().month,
        'year':datetime.now().year
    }

def buildWeatherURL(month=None, day=None, year=None, code=None, filter=None):
    """ A gui to pass parameters to get the weather from the web.
    Args:
        month (int): The month to get the weather for.
        day (int): The day to get the weather for.
        year (int): The year to get the weather for.
    Returns:
        Should return a URL like this, but replace the month, day, and year, filter, and airport with the values passed in.
        https://www.wunderground.com/history/daily/KCHO/date/2020-12-31
    """
    current_month,current_day,current_year = currentDate('tuple')
    
    if not month:
        month = current_month
    if not day:
        day = current_day
    if not year:
        year = current_year
    
    # Create the gui's layout using text boxes that allow for user input without checking for valid input
    layout = [
        [sg.Text('Month')],[sg.InputCombo(months)],
        [sg.Text('Day')],[sg.InputCombo(days)],
        [sg.Text('Year')],[sg.InputCombo(years)],
        [sg.Text('Country')],[sg.InputCombo(countries)],
        [sg.Text('City')],[sg.InputCombo(cities)],
        [sg.Text('Daily / Weekly / Monthly')],[sg.InputText()],
        [sg.Submit(), sg.Cancel()]
    ]      

    window = sg.Window('Get The Weather', layout)    

    event, values = window.read()
    window.close()
        
    month = values[0]
    day = values[1]
    year = values[2]
    country = values[3]
    city = values[4]
    filter = values[5]
    
    for item in json_data:
        if item['country'] == country:
            if item['city'] == city:
                code = item['icao']


    sg.popup('You entered', f"Month: {month}, Day: {day}, Year: {year}, Country: {country}, City: {city}, Code: {code}, Filter: {filter}")

    url = f"{base_url}/{filter}/{code}/{'date'}/{year}-{month}-{day}"
    
    # return the URL to pass to get appropriate weather data
    return url, filter
    
if __name__=='__main__':
    pass
    

def daily_filter(rendered_html):
    
    counter = 1
    column_tit = {
        1: "time",
        2: "temp",
        3: "dew",
        4: "humidity",
        5: "wind",
        6: "wspeed",
        7: "wgust",
        8: "pressure",
        9: "precip",
        10: "condition"
    }
    
    pull_data = {
        "time": [

        ],
        "temp": [

        ],
        "dew": [

        ],
        "humidity": [

        ],
        "wind": [

        ],
        "wspeed": [

        ],
        "wgust": [

        ],
        "pressure": [

        ],
        "precip": [

        ],
        "condition": [

        ]
    }
    
    page = BeautifulSoup(rendered_html, 'html.parser')
    table = page.find_all('lib-city-history-observation')
    tbody = table[0].find('table')
    rowgroup = tbody.find('tbody')
    rows = tbody.find_all("tr")
    
    """for row in tbody.find_all('tr'):  # Find all table rows
        for cell in row.find_all('td'):  # Find all cells in each row
            print(cell.text)  # Access the cell content
        print('---')"""
    
    for row in rows:
        columns = row.find_all("td")
        for column in columns:
            if counter in [1, 5, 10]:
                data_tag = column.find("span")
                pull_data[column_tit[counter]].append(data_tag.get_text())
            else:
                lib = column.find("lib-display-unit")
                span = lib.find("span")
                data_tag = span.find("span")
                pull_data[column_tit[counter]].append(data_tag.get_text())
            counter += 1
        counter = 1
    
    with open("daily_data.json","w") as f:
        json.dump(pull_data,f)
        
