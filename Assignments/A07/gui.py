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
    
    # return the URL to pass to wunderground to get appropriate weather data
    return url
if __name__=='__main__':
    
    rendered_html = get_weather.asyncGetWeather(buildWeatherURL())
    
    wunderground_soup = BeautifulSoup(rendered_html, 'html.parser')
    
    soup_container = wunderground_soup.find('lib-city-history-summary')
    soup_data = soup_container.find_all('table', class_='mat-table cdk-table mat-sort ng-star-inserted')
    
    row = []
    for i, dat in enumerate(soup_data):
        # loops through High Temp, Low Temp, etc.
        for j, d in enumerate(dat.find_all('span', class_='ng-star-inserted')):
            # loops through Actual, Historic Avg., Record
            for k in d.find_all('td', class_='ng-star-inserted'):
                tmp = k.text
                tmp = tmp.strip('  ') # remove any extra spaces
                        
                row.append(tmp)
    print(row)
    
    headers = {'Time':[], 'Temperature':[], 'Dew Point':[], 'Humidity':[], 'Wind':[], 'Wind Speed':[], 'Wind Gust':[], 'Pressure':[], 'Percip.':[], 'Condition':[]}
    table = pandas.DataFrame(headers)
    
    headings = list(headers)
    values = table.values.tolist()
    
    sg.theme("DarkBlue3")
    sg.set_options(font=("Courier New", 16))
    
    layout = [[sg.Table(values = values, headings = headings,
    # Set column widths for empty record of table
    auto_size_columns=False,
    col_widths=list(map(lambda x:len(x)+1, headings)))]]

    window = sg.Window('Airport Conditions',  layout)
    event, value = window.read()