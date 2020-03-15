#Since my VS compiler has a problem, I could get it work on this, so I also attached jupyternotebook. The project is the following, given the 
#day and the number of confirmed cases in a model country, decision tree make a model for deaths based on day and confirmed cases. 
# You can give it a try, set a country as a model and then another country for comparison.  

#Data is downloaded from https://www.ecdc.europa.eu/en/publications-data 

from  sklearn import tree
import csv
from datetime import date

#for organising the file
rows = []
with open("corona.csv", "r") as read:
    lines = read.readlines()
    first_day = date(2019, 12, 31)
    for row in lines:
        content = row.split(",")
        current = content[0].split("/")
        new_date = str((date(int(current[2]), int(current[1]), int(current[0])) - first_day).days)
        rows.append((new_date, content[1], content[2], content[3]))

with open("new_corona.csv", "w") as output:
    for row in rows:
       output.write(row[0]+","+row[1]+","+row[2]+","+row[3])
     

class main():

    def __init__(self, country):
        self.country = country
    
    def lines(self):
        with open("new_corona.csv", "r") as f:
            lines = f.readlines()
        return lines

    def data(self):
        line = self.lines()
        info = []
        for row in line:
            data = row.split(",")
            if data[1] == self.country:
                 info.append([data[0], data[2].strip()])
        return info
    
    def death(self):
        line = self.lines()
        death = []
        for row in line:
            data = row.split(",")
            if data[1] == self.country:
                death.append(data[3].strip())
        return death

    def model(self):
        fitting = tree.DecisionTreeClassifier()
        fitting1= fitting.fit(self.data(), self.death())
        return fitting1


def call():
    with open("new_corona.csv", "r") as f:
        lines = f.readlines()
        countries = [row.split(",")[1] for row in lines]
        countries_fun = {}
    for count in set(countries):
            countries_fun [count] = main(count)
            
    def predicted(data, model):
        predicted_death = []
        for num in range(0, 74):
            death = model.predict(data)
            predicted_death.append(death[num])
        return predicted_death

    def comparison(death, data, model):
        predicted_death = predicted(data, model)
        difference = []
        for num in range(0, 74):
            difference.append([num, int(death[num])-int(predicted_death[num])])
        return difference
    
    count_model = input("Country You Want to Set as the Model: ")
    count_compar = input("Country You Want to Compare the Model with: ")
    day = int(input("Day between 0 to 74: "))
    count1 = countries_fun[count_model]
    count2= countries_fun[count_compar]
    difference = comparison(count2.death(), count2.data(), count1.model())
    predicted_death = predicted(count2.data(), count1.model())
    death = count2.death()
    
    print("Death in the day %i of Corona based on the predicted model is %i and the actual death is %i" %(day, int(predicted_death[day]), int(death[day])))

call()


# In[ ]:




