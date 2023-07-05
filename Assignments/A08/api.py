from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import csv
from funct import *


description = """🚀
## 4883 Software Tools
### Where awesomeness happens
"""


app = FastAPI(

    description=description,

)


@app.get("/")
async def docs_redirect():
    """Api's base route that displays the information created above in the ApiInfo section."""
    return RedirectResponse(url="/docs")



@app.get("/casesByRegion/")
async def casesByRegion(year:int = None):
    """
    Returns the number of cases by region

    """

    # create a dictionary as a container for our results
    # that will hold unique regions. Why, because there 
    # cannot be duplicate keys in a dictionary.
    cases = {}
    db = []

    # return {'success':False,'message':'no database exists'}

    # loop through our db list
    for row in db:
        
        # If there is a year passed in and that year is not equal to this row
        # then skip the rest of code
        if year != None and year != int(row[0][:4]):
            continue
            
        # this line guarantees that the dictionary has the region as a key
        if not row[3] in cases:
            cases[row[3]] = 0
        
        # this line adds the case count to whatever is at that key location
        cases[row[3]] += int(row[4])    

    # return cases

    return {"data":cases,"success":True,"message":"Cases by Region","size":len(cases),"year":year}


@app.get("/get_countries/")
async def countries():
    countries = []
    countries = get_countries()
    
    return {"data":countries,"success":True,"message":"Countries"}
    
@app.get("/get_regions/")
async def regions():
    regions = []
    regions = get_regions()
    
    return {"data":regions,"success":True,"message":"Regions"}

@app.get("/get_deaths/")
async def deaths():
    deaths = get_deaths()
    
    return {"data":deaths,"success":True,"message":"Number of deaths"}

@app.get("/get_count_deaths/{country}")
async def count_deaths(country):
    try:
        deaths = get_count_deaths(country)
        
        return {"data":deaths,"success":True,"message":"Number of deaths in " + country}
    except:
        return{"success" : False, "message" : "Issues with the country implemented"}


@app.get("/get_reg_deaths/{region}")
async def reg_deaths(region):
    try:
        deaths = get_reg_deaths(region)
        
        return {"data":deaths,"success":True,"message":"Number of deaths in " + region}
    except:
        return{"success" : False, "message" : "Issues with the region implemented"}

@app.get("/get_count_year_deaths/{country}/{year}")
async def count_year_deaths(country, year):
    try:
        deaths = get_count_year_deaths(country, year)
        
        return {"data":deaths,"success":True,"message":"Number of deaths in " + country + " on " + year}
    except:
        return{"success" : False, "message" : "Issues with the country or year implemented"}

@app.get("/get_reg_year_deaths/{reg}/{year}")
async def reg_year_deaths(region, year):
    try:
        deaths = get_reg_year_deaths(region)
        
        return {"data":deaths,"success":True,"message":"Number of deaths in " + region + " on " + year}
    except:
        return{"success" : False, "message" : "Issues with region or year implemented"}

@app.get("/get_max_deaths/")
async def max_deaths():
    deaths = get_max_death()
    
    return {"data":deaths,"success":True,"message":"Maximum number of deaths"}

@app.get("/get_max_year_deaths/")
async def get_max_year_deaths(year1, year2):
    try:
        deaths, date = get_max_year_death(year1, year2)
        
        return {"data":deaths,"success":True,"message":"Maximum number of deaths was on " + date}
    except:
        return{"success" : False, "message" : "Issues with the years implemented"}

@app.get("/get_min_deaths/")
async def _min_deaths():
    deaths = get_min_death()
    
    return {"data":deaths,"success":True,"message":"Minimum number of deaths"}

@app.get("/get_min_year_deaths/")
async def min_year_deaths(year1, year2):
    try:
        deaths, date = get_min_year_death(year1, year2)
        
        return {"data":deaths,"success":True,"message":"Minimum number of deaths was on " + date}
    except:
        return{"success" : False, "message" : "Issues with the years implemented"}

@app.get("/get_avg_deaths/")
async def avg_death():
    average = get_avg_deaths()
    
    return {"data":average,"success":True,"message":"Average number of deaths"}

if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=5000, log_level="debug", reload=True) #host="127.0.0.1"