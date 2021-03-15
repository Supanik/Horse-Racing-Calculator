import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import time
import sqlite3
import statistics
import operator
import csv
import scipy.stats

def scrub(name):
    return ''.join( chr for chr in name if chr.isalnum() )

class Horse():

    def __init__(self, name = None):

        self.name = name
        self.url = "https://www.horseracingnation.com/horse/"

        namelist = []
        furlongs = {'4 1/2 f': 4.5, '5  f':5, '5 f':5,'5 1/2 f':5.5, '6 f':6, '6 1/2 f':6.5, '7 f':7, '1 mile':8, '1 1/16 m':8.5, '1 1/8 m':9}

        for letter in self.name:

            if letter == " ":
                templetter = "_"
                namelist.append(templetter)
            else:
                namelist.append(letter)

        self.name = ""

        for letter in namelist:
            self.name = self.name + letter

        try:
            self.df = pd.read_sql_query('SELECT * from ' + scrub(self.name), sql)
        except:
            self.get_data()
            self.html_clean()
            self.df = pd.DataFrame.from_dict(self.table)
            time.sleep(2)
            try:
                self.df.to_sql(scrub(self.name), sql, if_exists='replace', index = False)
                sql.commit()
            except:
                pass

        if self.df.empty:
            self.name = self.name + "_1"

            try:
                t = (self.name,)
                self.df = pd.read_sql_query('SELECT * from ' + scrub(self.name), sql)
            except:
                pass

            if self.df.empty:
                self.get_data()
                self.html_clean()
                self.df = pd.DataFrame.from_dict(self.table)
                time.sleep(2)
            try:
                time.strftime(self.df['Time'], format="%M:%S.%f")
                self.df.to_sql(scrub(self.name), sql, if_exists='replace', index = False)
                sql.commit()
            except:
                pass

            
            self.get_data()
            self.html_clean()
            self.df = pd.DataFrame.from_dict(self.table)
        for item in self.df['Distance']:
            if item in furlongs:
                self.df['Distance'].replace({item:furlongs[item]}, inplace = True)

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
            self.win_percent = round ((self.win / len(self.df.Finish))*100, 2)
        except:
            pass
        try:
            self.place_percent = round ((((self.place + self.win) / 2) / len(self.df.Finish))*100, 2)
        except:
            pass
        try:
            self.show_percent = round ((((self.show + self.place + self.win) / 3) / len(self.df.Finish))*100, 2)
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
                    , "Angel_S_Arroyo":"Angel_Arroyo", "Hector_Isaac_Berrios":"Hector_I_Berrios", "Joseph_Talamo": "Joe_Talamo", "Travis_Wales":"T_Wales", "Florent_Geroux":"Geroux_F"
                    , "Alex_L_Canchari":"A_Canchari", "Jose_Andres_Guerrero":"J_Guerrero", "Eguard_Andres_Tejera":"E_A_Tejera", "Marco_Meneses":"Marcos_Meneses#", "Cassidy_D_B_Fletcher":"Cassidy_Fletcher"}

        if self.name in altnames.keys():
            self.name = altnames[self.name]

        try:
            self.df = pd.read_sql_query('SELECT * from ' + scrub(self.name), sql)
        except:
            self.get_data()
            self.html_clean()
            self.df = pd.DataFrame.from_dict(self.table)
            time.sleep(2)
            try:
                self.df.to_sql(scrub(self.name), sql, if_exists='replace', index = False)
                sql.commit()
            except:
                pass
            

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
            self.win_percent = round ((self.win / len(self.df.Finish))*100, 2)
        except:
            print("cannot calculate win percentage")
        try:
            self.place_percent = round ((((self.place + self.win) / 2) / len(self.df.Finish))*100, 2)
        except:
            print("cannot calculate place percentage")
        try:
            self.show_percent = round ((((self.show + self.place + self.win) / 3) / len(self.df.Finish))*100, 2)
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

        self.sub1m = ['Three Furlongs', 'Four Furlongs', 'Five Furlongs', 'Six Furlongs', 'Seven Furlongs', '3F', '4F', '412F', '5F','512F', '6F', '612F', '7F']
        self.over1m = ['Eight Furlongs', '1M', '1116M', '118M']

        self.parkpp = {"oaklawn-park":{"sub1m":{"1":1.119, "2":1.1061, "3": 1.1254, "4":1.965, "5":1.10, "6":1.1010, "7":1.1237, "8":1.934, "9": 1.1324, "10":1.658,
                  "11":1.808, "12":1.1064}, "over1m":{"1":1.1224, "2":1.1582, "3": 1.1122, "4":1.1378, "5":1.1071, "6":1.1237, "7":1.968, "8":1.979, "9":1.917, "10":1.909,
                  "11":1.513, "12":1.625}}}

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

        if self.park == "oaklawn-park":

            try:
                tempdate = ""
                for letter in self.date:
                    templetter = letter
                    if letter == "-":
                        templetter = "/"
                    tempdate = tempdate + templetter 
                self.get_oaklawn_wo(date = tempdate)
            except Exception as e:
                print (e)
                
        self.url = "https://entries.horseracingnation.com/entries-results/" + self.park + "/" + self.date
        self.get_data()
        self.clean_names()
        print("---------------------------------------------------------------")
        print("")
        

    def get_oaklawn_wo(self, date = "2021/03/12"):

        url = "https://oaklawn-equibase.herokuapp.com/workouts/"

        page = requests.get(url + date + "/")
        data = BeautifulSoup(page.text, features="html.parser")
        horse = {"Date":[], "Distance":[], "Track":[], "Horse":[], "Sex":[], "Age":[], "Rank":[], "Timing":[], "Notes":[]}
##        horse = {}
        horses = []
        workoutheaders = data.findAll(class_="workout-header")
        data = data.findAll(class_="horse-data-table")
        place = 0
        workoutsdb = sqlite3.connect("workouts.db")
        workoutsdbc = sql.cursor()

        try:
            workouts.df = pd.read_sql_query('SELECT * from ' + scrub(date), workoutsdb)

        except:

            try:
                for item in data:
                    temp = item.findAll("tr")
                    del temp[0]
                    for subitem in temp:
                        subdata = subitem.findAll("td")
                        horse["Date"].append(date)
                        horse["Horse"].append(subdata[0].text)
                        horse["Sex"].append(subdata[1].text)
                        horse["Age"].append(subdata[2].text)
                        horse["Rank"].append(subdata[3].text)
                        horse["Timing"].append(subdata[4].text)
                        horse["Notes"].append(subdata[5].text)
                        horse["Distance"].append(workoutheaders[place].find("h2").text)
                        horse["Track"].append(self.park)

##                        horse[subdata[0].text] = {}
##                        horse[subdata[0].text]["Date"] = date
##                        horse[subdata[0].text]["Name"] = subdata[0].text
##                        horse[subdata[0].text]["Sex"] = subdata[1].text
##                        horse[subdata[0].text]["Age"] = subdata[2].text
##                        horse[subdata[0].text]["Rank"] = subdata[3].text
##                        horse[subdata[0].text]["Timing"] = subdata[4].text
##                        horse[subdata[0].text]["Notes"] = subdata[5].text
##                        horse[subdata[0].text]["Distance"] = workoutheaders[place].find("h2").text
##                        horse[subdata[0].text]["Track"] = self.park
                        
                    horse = pd.DataFrame.from_dict(horse)
                    horse.to_sql(scrub(date), workoutsdb, if_exists='replace', index = False)
                    sql.commit()
                    horses.append(horse)
                    horse = {"Date":[], "Distance":[], "Track":[], "Horse":[], "Sex":[], "Age":[], "Rank":[], "Timing":[], "Notes":[]}
##                    horse = {}
                    place += 1

                    
##                horses = pd.DataFrame.from_dict(horses)
                self.workouts = horses

            except Exception as e:
                print(e)
                pass
            

    def get_contestant_data(self, race = 2, jockeyvalue = .1, horsevalue = 1, trainervalue = 1, ppvalue = 1.375, winweight = 3, placeweight = 2, showweight = 1):
        global wins
        global datatracker
        race -= 1
        itemcount = 0

        starts = []
        medianstartslist = []
        prediction = {}
        prediction1 = {}
        
        for item in self.tables[race]["Horse"]:
            self.tables[race]['Horse'][itemcount]= Horse(str(item))
            try:
                time.sleep(2)
                self.tables[race]['Jockey'][itemcount]= Jockey(str(self.tables[race]['Jockey'][itemcount]))
            except:
                pass

            try:
                print("")
                print("---------------------------------------------------------------")
                print("Current Accuracy " + str(round((wins.count(1)/len(wins)) * 100,2)) + "%")
                print("---------------------------------------------------------------")
                print("")

            except:
                pass
            
            print ("# " + str(itemcount + 1) + " Horse: " + self.tables[race]['Horse'][itemcount].name)
            
            try:
                winscore = (((self.tables[race]['Horse'][itemcount].win_percent * winweight) * horsevalue) + ((self.tables[race]['Jockey'][itemcount].win_percent * winweight) * jockeyvalue) / 2)
                placescore = (((self.tables[race]['Horse'][itemcount].place_percent * placeweight) * horsevalue) + ((self.tables[race]['Jockey'][itemcount].place_percent * placeweight) * jockeyvalue) / 2)
                showscore = (((self.tables[race]['Horse'][itemcount].show_percent * showweight) * horsevalue) + ((self.tables[race]['Jockey'][itemcount].show_percent * showweight) * jockeyvalue) / 2)
                aggregatescore = round(statistics.mean([winscore, placescore, showscore]),2)
                
                if self.park in self.parkpp.keys():
                    
                    try:

                        winscore = winscore * (((self.parkpp[self.park]["over1m"][self.tables[race]["PP"][itemcount]] + self.parkpp[self.park]["over1m"][self.tables[race]["PP"][itemcount]]) /2) * ppvalue)
                        placescore = placescore * (((self.parkpp[self.park]["over1m"][self.tables[race]["PP"][itemcount]] + self.parkpp[self.park]["over1m"][self.tables[race]["PP"][itemcount]]) /2) * ppvalue)
                        showscore = showscore * (((self.parkpp[self.park]["over1m"][self.tables[race]["PP"][itemcount]] + self.parkpp[self.park]["over1m"][self.tables[race]["PP"][itemcount]]) /2) * ppvalue)
                        aggregatescore = aggregatescore * (((self.parkpp[self.park]["over1m"][self.tables[race]["PP"][itemcount]] + self.parkpp[self.park]["over1m"][self.tables[race]["PP"][itemcount]]) /2) * ppvalue)

                        for item in self.sub1m:
                            if item in self.tables[race]["Info"][0]:
                                winscore = winscore * (self.parkpp[self.park]["sub1m"][self.tables[race]["PP"][itemcount]] * ppvalue)
                                placescore = placescore * (self.parkpp[self.park]["sub1m"][self.tables[race]["PP"][itemcount]] * ppvalue)
                                showscore = showscore * (self.parkpp[self.park]["sub1m"][self.tables[race]["PP"][itemcount]] * ppvalue)
                                aggregatescore = aggregatescore * (self.parkpp[self.park]["sub1m"][self.tables[race]["PP"][itemcount]] * ppvalue)

##                                print("Race is less than 1 mile")
                                
                        for item in self.over1m:
                            if item in self.tables[race]["Info"][0]:
                                winscore = winscore * (self.parkpp[self.park]["over1m"][self.tables[race]["PP"][itemcount]] * ppvalue)
                                placescore = placescore * (self.parkpp[self.park]["over1m"][self.tables[race]["PP"][itemcount]] * ppvalue)
                                showscore = showscore * (self.parkpp[self.park]["over1m"][self.tables[race]["PP"][itemcount]] * ppvalue)
                                aggregatescore = aggregatescore * (self.parkpp[self.park]["over1m"][self.tables[race]["PP"][itemcount]] * ppvalue)

##                                print("Race is greater than 1 mile")
                            
                    except Exception as e:
                        print(e)
                        
                prediction[self.tables[race]['Horse'][itemcount].name] = aggregatescore
##                print(str(prediction[self.tables[race]['Horse'][itemcount].name]) + " Prediction Score")
            except Exception as e:
                print ("No Prediction Data")
                print ("")
                pass

                
            try:
                starts.append(len(self.tables[race]['Horse'][itemcount].df.Finish))
                print(str(len(self.tables[race]['Horse'][itemcount].df.Finish)) + " Starts")
                print(str(self.tables[race]['Horse'][itemcount].win_percent) + "% Win")
##                print(str(self.tables[race]['Horse'][itemcount].place_percent) + "% Place or Better")
##                print(str(self.tables[race]['Horse'][itemcount].show_percent) + "% Show or Better")
                print("")
            except:
                print ("No Horse Data")
                print ("")
                pass
            
            try:
                print ("Jockey: " + self.tables[race]['Jockey'][itemcount].name)
                print(str(len(self.tables[race]['Jockey'][itemcount].df.Finish)) + " Starts")
                print(str(self.tables[race]['Jockey'][itemcount].win_percent) + "% Win")
##                print(str(self.tables[race]['Jockey'][itemcount].place_percent) + "% Place or Better")
##                print(str(self.tables[race]['Jockey'][itemcount].show_percent) + "% Show or Better")
                print("")
            except:
                print ("No Jockey Data")
                pass
            print("---------------------------------------------------------------")
            itemcount += 1
            time.sleep(.125)
        
        print("Race " + str(race + 1) + " Results")
        try:
            winner = self.placestables[race]["Win"]
            print("Win- " + self.placestables[race]["Win"])
            print("Place- " + self.placestables[race]["Place"])
            print("Show- " + self.placestables[race]["Show"])
            
        except:
            print("No Results")
        print("")
        print("---------------------------------------------------------------")
        try:
            predictedwinner = max(prediction.items(), key=operator.itemgetter(1))[0]
        except:
            print("No Predicted Winner")
        print(str(predictedwinner) + " To Win")
        medianstarts = statistics.median(starts)
        medianstartslist.append(medianstarts)
        print(str(statistics.median(starts)) + " Median Horse Starts")

        win = 0
        try:
            if scrub(predictedwinner) == scrub(winner) or scrub(predictedwinner) == (scrub(winner) + "1"):
                print("You Won!!!")
                win = 1

        except Exception as e:
            print(e)
            pass
        wins.append(win)        
        datatracker.append(statistics.median(starts))
        try:
            print(str(round((wins.count(1)/len(wins)) * 100,2)) + "%")
        except:
            pass

        try:
            r, p = scipy.stats.pearsonr(wins, datatracker)
            print(str(r) + " Data Correlation (R)")
        except:
            pass

    def get_data(self):
        
        self.page = requests.get(self.url)
        self.data = BeautifulSoup(self.page.text, features="html.parser")
        self.table = {"Info":[],"P#":[],"PP":[],"Horse":[],"A/S":[],"Med/EQ":[],"Jockey":[],"WGT":[],"Trainer":[],"ML":[]}
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
                raceinfo = self.results[listloc].find(class_="col-lg-auto flex-grow-1 race-distance")
                raceinfo = scrub(raceinfo.text)
                self.table["Info"].append(raceinfo)
            except Exception as e:
                print(e)

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

            foundlist = []
            for found in item.findAll("td"):
                foundlist.append(found)

            del foundlist[0]
            while len(foundlist) > 0:
                self.table["PP"].append(scrub(foundlist.pop(0).text))
                try:
                    del foundlist[0:5]
                except:
                    pass
            
            
            self.tables.append(self.table)
            self.table = {"Info":[],"P#":[],"PP":[],"Horse":[],"A/S":[],"Med/EQ":[],"Jockey":[],"WGT":[],"Trainer":[],"ML":[]}
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

def backtest():

    with open('backtestdates.txt', newline='') as f:
        reader = csv.reader(f)
        dates = list(reader)
        
    print("")
    park = str(input("What is the name of the Park? "))

    try:
        for item in dates[0]:
            races = Park_Data(date = item, park = park)
            for race in range(len(races.tables)):
                races.get_contestant_data(race = race)
    except Exception as e:
        print(e)
        pass
    
    print(str(round((wins.count(1)/len(wins)) * 100,2)) + "%")
        

sql = sqlite3.connect("data.db")
sqlc = sql.cursor()


print("Horse Racing Calculator")
print("")

raceagain = True
test = str(input("Backtest? 'y' or 'n' "))

date = None
park = None
wins = []
datatracker = []

while raceagain == True:
    
    try:
        if (date == None or park == None) and test == "n":
            date = str(input("What is the race date? example '2021-02-11' "))
            park = str(input("What is the name of the Park? "))
            races = Park_Data(date, park)
        if test == "n":    
            race = int(input("What Race? "))
            print("")
            races.get_contestant_data(race = race)
    except Exception as e:
        pass

    try:
        if test == "y":
            backtest()
            test = "n"
    except:
        pass

    raceagain = str(input("Do you want to calculate another race? 'y' or 'n' "))
    print("")

    if raceagain == "n":
        raceagain = False
    else:
        raceagain = True
       
sql.close()
quit()                     

##try:
##    date = str(input("What is the race date? example '2021-02-11' "))
##    park = str(input("What is the name of the Park? "))
##    print("")
##    races = Park_Data(date, park)
##except Exception as e:
##    print(e)



