import requests
from bs4 import BeautifulSoup
from pandas import DataFrame
import datetime
import time
import sqlite3
import statistics
import operator

class Horse():

    def __init__(self, name = None):

        self.name = name
        self.url = "https://www.horseracingnation.com/horse/"

        namelist = []

        for letter in self.name:

            if letter == " ":
                templetter = "_"
                namelist.append(templetter)
            else:
                namelist.append(letter)

        self.name = ""

        for letter in namelist:
            self.name = self.name + letter

        """ insert the database check and creation here """

        self.get_data()
        self.html_clean()
        self.df = DataFrame.from_dict(self.table)

        if self.df.empty:
            self.name = self.name + "_1"
            self.get_data()
            self.html_clean()
            self.df = DataFrame.from_dict(self.table)

        self.win = 0
        self.place = 0
        self.show = 0

        for place in self.df.Finish:
            if place == "1st":
                self.win += 1

            if place == "2nd":
                self.place += 1

            if place == "3rd":
                self.show += 1

        try:
            self.win_percent = round ((self.win / 100)*100, 2)
        except:
            pass
        try:
            self.place_percent = round (((self.place + self.win) / 100)*100, 2)
        except:
            pass
        try:
            self.show_percent = round (((self.show + self.place + self.win) / 100)*100, 2)
        except:
            pass

    def get_data(self):

        try:
            self.page = requests.get(self.url + self.name + "#")
            self.data = BeautifulSoup(self.page.text, features="html.parser")
            self.table = {"Date":[],"Horse":[],"Finish":[],"Track":[],"Distance":[],"Sf":[],"Race":[],"Cnd":[],"1st":[],"2nd":[],"3rd":[],"Time":[]}
            self.resultstable = self.data.find(id = "theracegrid")
            self.results = self.resultstable.findAll(class_="dxgv")

            length = len(self.results) / 13

            place = 0
            check = False
            for item in self.results:
                if place == 0 and check == False:
                    place = 1
                    check = True
                if place == 1 and check == False:
                    self.table["Date"].append(item)
                    del (item)
                    place = 2
                    check = True
                if place == 2 and check == False:
                    self.table["Horse"].append(item)
                    del (item)
                    place = 3
                    check = True
                if place == 3 and check == False:
                    self.table["Finish"].append(item)
                    del (item)
                    place = 4
                    check = True
                if place == 4 and check == False:
                    self.table["Track"].append(item)
                    del (item)
                    place = 5
                    check = True
                if place == 5 and check == False:
                    self.table["Distance"].append(item)
                    del (item)
                    place = 6
                    check = True
                if place == 6 and check == False:
                    self.table["Sf"].append(item)
                    del (item)
                    place = 7
                    check = True
                if place == 7 and check == False:
                    self.table["Race"].append(item)
                    del (item)
                    place = 8
                    check = True
                if place == 8 and check == False:
                    self.table["Cnd"].append(item)
                    del (item)
                    place = 9
                    check = True
                if place == 9 and check == False:
                    self.table["1st"].append(item)
                    del (item)
                    place = 10
                    check = True
                if place == 10 and check == False:
                    self.table["2nd"].append(item)
                    del (item)
                    place = 11
                    check = True
                if place == 11 and check == False:
                    self.table["3rd"].append(item)
                    del (item)
                    place = 12
                    check = True
                if place == 12 and check == False:
                    self.table["Time"].append(item)
                    del (item)
                    place = 0
                check = False
        except:
            pass
            
    def html_clean(self):             
        for key in self.table:
            tempval = 0
            for list_item in self.table[key]:
                hold = False
                tempkey = ""
                for item in list_item:
                    for letter in item:
                        if letter == "<":
                            hold = True
                        if hold == False:
                            tempkey = tempkey + letter
                        if letter == ">":
                            hold = False
                    self.table[key][tempval] = tempkey
                    tempkey = ""
                    tempval += 1

class Jockey():
        
    def __init__(self, name = None):

        self.name = name
        self.url = "https://www.horseracingnation.com/person/"

        namelist = []

        for letter in self.name:

            if letter == " ":
                templetter = "_"
                namelist.append(templetter)
            else:
                namelist.append(letter)

        self.name = ""

        for letter in namelist:
            self.name = self.name + letter

        altnames = {"Francisco_Arrieta":"Franciso_Arrieta", "Cristian_A_Torres":"Cristian_Torres", "Samuel_Camacho_Jr":"S_Camacho_Jr", "Paco_Lopez":"Pascacio_Lopez", "Edgard_J_Zayas":"Edgard_Zayas"
                    , "Angel_S_Arroyo":"Angel_Arroyo", "Hector_Isaac_Berrios":"Hector_I_Berrios"}

        if self.name in altnames.keys():
            self.name = altnames[self.name]

        self.get_data()
        self.html_clean()
        self.df = DataFrame.from_dict(self.table)

        self.win = 0
        self.place = 0
        self.show = 0

        for place in self.df.Finish:
            if place == "1st":
                self.win += 1

            if place == "2nd":
                self.place += 1

            if place == "3rd":
                self.show += 1

        try:
            self.win_percent = round ((self.win / 100)*100, 2)
        except:
            print("cannot calculate win percentage")
        try:
            self.place_percent = round (((self.place + self.win) / 100)*100, 2)
        except:
            print("cannot calculate place percentage")
        try:
            self.show_percent = round (((self.show + self.place + self.win) / 100)*100, 2)
        except:
            print("cannot calculate show percentage")
            

    def get_data(self):
        try:
            self.page = requests.get(self.url + self.name + "#")
            self.data = BeautifulSoup(self.page.text, features="html.parser")
            self.table = {"Date":[],"Horse":[],"Finish":[],"Trainer":[],"Track":[],"#":[],"Distance":[],"Sf":[],"Race":[],"$":[],"Cnd":[],"1st":[],"2nd":[],"3rd":[],"Time":[]}
            self.resultstable = self.data.find(class_= "hrdb-race-grid")
            self.results = self.resultstable.findAll(class_="dxgv")

            length = len(self.results) / 15

            place = 0
            check = False
            for item in self.results:
                if place == 0 and check == False:
                    place = 1
                    check = True
                if place == 1 and check == False:
                    self.table["Date"].append(item)
                    del (item)
                    place = 2
                    check = True
                if place == 2 and check == False:
                    self.table["Horse"].append(item)
                    del (item)
                    place = 3
                    check = True
                if place == 3 and check == False:
                    self.table["Finish"].append(item)
                    del (item)
                    place = 4
                    check = True
                if place == 4 and check == False:
                    self.table["Trainer"].append(item)
                    del (item)
                    place = 5
                    check = True
                if place == 5 and check == False:
                    self.table["Track"].append(item)
                    del (item)
                    place = 6
                    check = True
                if place == 6 and check == False:
                    self.table["#"].append(item)
                    del (item)
                    place = 7
                    check = True
                if place == 7 and check == False:
                    self.table["Distance"].append(item)
                    del (item)
                    place = 8
                    check = True
                if place == 8 and check == False:
                    self.table["Sf"].append(item)
                    del (item)
                    place = 9
                    check = True
                if place == 9 and check == False:
                    self.table["Race"].append(item)
                    del (item)
                    place = 10
                    check = True
                if place == 10 and check == False:
                    self.table["$"].append(item)
                    del (item)
                    place = 11
                    check = True
                if place == 11 and check == False:
                    self.table["Cnd"].append(item)
                    del (item)
                    place = 12
                    check = True
                if place == 12 and check == False:
                    self.table["1st"].append(item)
                    del (item)
                    place = 13
                    check = True
                if place == 13 and check == False:
                    self.table["2nd"].append(item)
                    del (item)
                    place = 14
                    check = True
                if place == 14 and check == False:
                    self.table["3rd"].append(item)
                    del (item)
                    place = 15
                    check = True
                if place == 15 and check == False:
                    self.table["Time"].append(item)
                    del (item)
                    place = 0
                check = False
        except:
            print ("Invalid Entry? No Data")

    def html_clean(self):             
        for key in self.table:
            tempval = 0
            for list_item in self.table[key]:
                hold = False
                tempkey = ""
                for item in list_item:
                    for letter in item:
                        if letter == "<":
                            hold = True
                        if hold == False:
                            tempkey = tempkey + letter
                        if letter == ">":
                            hold = False
                    self.table[key][tempval] = tempkey
                    tempkey = ""
                    tempval += 1

class Park_Data():

    def __init__(self, date = "2021-02-19", park = "gulfstream-park"):

        self.park = park
        parklist = []

        for letter in self.park:

            if letter == " ":
                templetter = "-"
                parklist.append(templetter)
            else:
                parklist.append(letter)

        self.park = ""

        for letter in parklist:
            self.park = self.park + letter

        self.date = date    
        self.url = "https://entries.horseracingnation.com/entries-results/" + self.park + "/" + self.date
        self.get_data()
        self.clean_names()
        race = int(input("What race? "))
        print("---------------------------------------------------------------")
        print("")
        self.get_contestant_data(race)

    def get_contestant_data(self, race = 2, jockeyvalue = 1, horsevalue = 1, trainervalue = 1, ppvalue = 1):
        race -= 1
        itemcount = 0

        prediction = {}
        
        for item in self.tables[race]["Horse"]:
            self.tables[race]['Horse'][itemcount]= Horse(str(item))
            try:
                time.sleep(2)
                self.tables[race]['Jockey'][itemcount]= Jockey(str(self.tables[race]['Jockey'][itemcount]))
            except:
                pass
            print ("# " + str(itemcount + 1) + " Horse: " + self.tables[race]['Horse'][itemcount].name)
            try:
                winscore = ((self.tables[race]['Horse'][itemcount].win_percent * horsevalue) + (self.tables[race]['Jockey'][itemcount].win_percent * jockeyvalue) / 2)
                placescore = ((self.tables[race]['Horse'][itemcount].place_percent * horsevalue) + (self.tables[race]['Jockey'][itemcount].place_percent * jockeyvalue) / 2)
                showscore = ((self.tables[race]['Horse'][itemcount].show_percent * horsevalue) + (self.tables[race]['Jockey'][itemcount].show_percent * jockeyvalue) / 2)
                aggregatescore = round(statistics.mean([winscore, placescore, showscore]),2)
                prediction[self.tables[race]['Horse'][itemcount].name] = aggregatescore
##                print(str(aggregatescore) + " Prediction Score")
                print(str(prediction[self.tables[race]['Horse'][itemcount].name]) + " Prediction Score")
                print("")
            except:
                print ("No Prediction Data")
                print ("")
                pass
            try:
                print(str(len(self.tables[race]['Horse'][itemcount].df.Finish)) + " Starts")
                print(str(self.tables[race]['Horse'][itemcount].win_percent) + "% Win")
                print(str(self.tables[race]['Horse'][itemcount].place_percent) + "% Place or Better")
                print(str(self.tables[race]['Horse'][itemcount].show_percent) + "% Show or Better")
                print("")
            except:
                print ("No Horse Data")
                print ("")
                pass
            
            try:
                print ("Jockey: " + self.tables[race]['Jockey'][itemcount].name)
                print(str(len(self.tables[race]['Jockey'][itemcount].df.Finish)) + " Starts")
                print(str(self.tables[race]['Jockey'][itemcount].win_percent) + "% Win")
                print(str(self.tables[race]['Jockey'][itemcount].place_percent) + "% Place or Better")
                print(str(self.tables[race]['Jockey'][itemcount].show_percent) + "% Show or Better")
                print("")
            except:
                print ("No Jockey Data")
                pass
            print("---------------------------------------------------------------")
            itemcount += 1
            time.sleep(2)
        
        print("Race " + str(race + 1) + " Results")
        try:
            print("Win- " + self.placestables[race]["Win"])
            print("Place- " + self.placestables[race]["Place"])
            print("Show- " + self.placestables[race]["Show"])
            
        except:
            print("No Results")
        print("")
        print("---------------------------------------------------------------")
        print(str(max(prediction.items(), key=operator.itemgetter(1))[0]) + " To Win")

    def get_data(self):
        
        self.page = requests.get(self.url)
        self.data = BeautifulSoup(self.page.text, features="html.parser")
        self.table = {"P#":[],"PP":[],"Horse":[],"A/S":[],"Med/EQ":[],"Jockey":[],"WGT":[],"Trainer":[],"ML":[]}
        self.places = {"Win":"", "Place":"", "Show":""}
        self.placestables = []
        self.resultstable = self.data.find(class_= "col col-md-8")
        self.results = self.resultstable.findAll(class_="my-5")
        self.tables = []

        listloc = 0

        for item in self.results:

            foundlist = []
            foundtrainer = None
            foundjockey = None
            foundml = None

            try:
                placesdata = self.results[listloc].find(class_="race-with-results row")
                placesdata = placesdata.find(class_="table table-hrn table-payouts")
                placesdata = placesdata.findAll("tr")
                del placesdata[0]
                self.places["Win"] = placesdata[0].find("td").text
                self.places["Place"] = placesdata[1].find("td").text
                self.places["Show"] = placesdata[2].find("td").text
                self.placestables.append(self.places)
                self.places = {"Win":"", "Place":"", "Show":""}
                
            except:
##                print ("error getting race results or no results")
                pass
            
            for found in item.findAll("h4"):
                self.table["Horse"].append(found.text)
            for found in item.findAll("p"):
                foundlist.append(found)
            del foundlist[0]
            
            while len(foundlist) > 0:
                del foundlist[0]
                self.table["Trainer"].append(foundlist.pop(0).text)
                self.table["Jockey"].append(foundlist.pop(0).text)
                self.table["ML"].append(foundlist.pop(0).text)
                del foundlist[0]
            
            
            self.tables.append(self.table)
            self.table = {"P#":[],"PP":[],"Horse":[],"A/S":[],"Med/EQ":[],"Jockey":[],"WGT":[],"Trainer":[],"ML":[]}
            listloc += 1

            placecount = -1
            
            for table in self.placestables:
                placecount += 1
                for item in table:
                    tempitem = ""
                    spacecount = False
                    toggle = False
                    charlist = ["'", ".", ",", " ", "\n"]
                    
                    for letter in self.placestables[placecount][item]:
                        if letter == " " and spacecount == True:
                            spacecount = False
                            toggle = True
                        if letter not in charlist:
                            spacecount = False
                            tempitem = tempitem + letter

                        if spacecount == False and letter == " " and toggle == False:
                            tempitem = tempitem + letter
                            spacecount = True

                        toggle = False


                    self.placestables[placecount][item] = tempitem
                    if self.placestables[placecount][item][-1] in charlist:
                        self.placestables[placecount][item] = self.placestables[placecount][item][:-1]
                
    def clean_names(self):

        for table in self.tables:
            for key in table:
                itemcount = -1
                for item in table[key]:
                    itemcount += 1
                    tempitem = ""
                    spacecount = False
                    toggle = False
                    charlist = ["'", ".", ",", " "]
                    for letter in item:
                            
                        if letter == " " and spacecount == True:
                            spacecount = False
                            toggle = True
                            
                        if letter not in charlist:
                            spacecount = False
                            tempitem = tempitem + letter

                        if spacecount == False and letter == " " and toggle == False:
                            tempitem = tempitem + letter
                            spacecount = True

                        toggle = False


                    table[key][itemcount] = tempitem
                        
                    

sql = sqlite3.connect("horses.db")
sqlc = sql.cursor()


print("Horse Racing Calculator")
print("")

raceagain = True

while raceagain == True:
    
    try:
        date = str(input("What is the race date? example '2021-02-11' "))
        park = str(input("What is the name of the Park? "))
        print("")
        races = Park_Data(date, park)
    except:
        print("Invalid Data")

    raceagain = str(input("Do you want to calculate another race? 'y' or 'n' "))
    print("")

    if raceagain == "n":
        raceagain = False
    else:
        raceagain = True
       
##quit()

##try:
##    date = str(input("What is the race date? example '2021-02-11' "))
##    park = str(input("What is the name of the Park? "))
##    print("")
##    races = Park_Data(date, park)
##except Exception as e:
##    print(e)



