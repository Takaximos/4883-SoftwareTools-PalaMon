import csv

results = []

with open("data.csv", 'r') as csvfile:
    reader = csv.reader(csvfile)
    i = 0
    for row in reader: # each row is a list
        if i == 0:
            i += 1
            continue
        
        results.append(row)
        
        
def get_countries(): # get all of the countries in the csv file
    
    global results
    countries = []
    
    for row in results:
        if row[2] not in countries:
            countries.append(row[2])
            
    return countries

def get_regions(): # get all of the regions in the csv file
    global results
    regions = []
    
    for row in results:
        if row[3] not in regions:
            regions.append(row[3])
            
    return regions

def get_deaths(): # get total number of deaths
    global results
    deaths = 0
    
    for row in results:
        deaths += int(row[7])
    
    return deaths
def get_count_deaths(country): # get the number of deaths of a specified country
    global results
    deaths = 0
    
    for row in results:
        
        if row[2] == country:
            deaths += int(row[6])
            
    return deaths

def get_reg_deaths(region): # get the number of deaths of a specified region
    global results
    deaths = 0
    
    for row in results:
        
        if row[3] == region:
            deaths += int(row[6])
            
    return deaths
    
    
def get_count_year_deaths(country, year): # get the number of deaths of a specified country and specified year
    global results
    deaths = 0
    
    for row in results:
        
        if row[2] == country and row[0][:4] == year:
            deaths += int(row[6])
            
    return deaths

def get_reg_year_deaths(region, year): # get the number of deaths of a specified region and year
    global results
    deaths = 0
    
    for row in results:
        
        if row[3] == region and row[0][:4] == year:
            deaths += int(row[6])
            
    return deaths

def get_max_death(): # get max number of deaths
    global results
    temp = 0 
    country = ''
    
    for row in results:
        
        if int(row[7]) > temp:
            temp = int(row[7])
            country = row[2]
            
    return country

def get_max_year_death(year1, year2):   # get max number of deaths from certain years
    global results
    temp = 0 
    date = ''
    for row in results:
        
        if int(row[0][:4]) > year1 and int(row[0][:4]) < year2:
            if row[7] > temp:
                temp = row[7]
                date = row[0]
            
    return date

def get_min_death(): #get min nimber of deaths
    global results
    temp = 0 
    date = ""
    country = ""
    for row in results:
        if int(row[7]) < temp or int(row[7]) == 0:
            
            place = row[2]
            
            if place != country:
                temp = int(row[7])
                country = row[2]
                date = row[0]
            
    return country, date

def get_min_year_death(year1, year2):   # get min number of deaths from certain years
    global results
    temp = 0 
    place = "kirk"
    country = "terp"
    
    for row in results:
        
        if row[0][:4] > year1 and row[0][:4] < year2:
            
            if row[7] < temp and row[7] == 0:
                
                place = row[2]
                
                if place != country:
                    temp = row[7]
                    country = row[2]
                    date = row[0]
            
    return country, date

def get_avg_deaths():   # get average number of deaths from certain years
    global results
    counter = 0
    death = 0
    
    for row in results:
        
        death += int(row[6])
        counter += 1
    
    return death/counter
