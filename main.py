#
# CS341 - Project 1
# Roman Moreno
# UIN: 664706090
#

import sqlite3
import matplotlib.pyplot as plt

##################################################################  
#
# print_stats
#
# Given a connection to the CTA database, executes various
# SQL queries to retrieve and output basic stats.
#
def print_stats(dbConn):
    dbCursor = dbConn.cursor()
    
    print("General stats:")
    
    dbCursor.execute("Select count(*) From Stations;")  # will execute the query and obtain the total number of stations in database
    row = dbCursor.fetchone();
    print("  # of stations:", f"{row[0]:,}")  # will print the stations
    
    dbCursor.execute("SELECT COUNT(*) From Stops")  # will obtain the number of stops from database
    rowOfStops = dbCursor.fetchone()
    print("  # of stops:", f"{rowOfStops[0]:,}")

    dbCursor.execute("SELECT COUNT(*) From Ridership")  # will give the total number of ride entries
    rowOfRideEntries = dbCursor.fetchone()
    print("  # of ride entries:", f"{rowOfRideEntries[0]:,}")

    dateRange = """SELECT DATE(MIN(Ride_Date)), DATE(MAX(Ride_Date))  
                   FROM Ridership"""
    dbCursor.execute(dateRange)  # will execute and find the start and finish date of the database
    rowDateRange = dbCursor.fetchone()
    print("  date range:", rowDateRange[0], "-", rowDateRange[1])

    totalRidership = """SELECT SUM(Num_Riders)
                        FROM Ridership"""
    dbCursor.execute(totalRidership)  # will obtain the total number of riders
    rowTotalRidership = dbCursor.fetchone()
    print("  Total ridership:", f"{rowTotalRidership[0]:,}")

    weekdayRidership = """SELECT  SUM(Num_Riders)
                          FROM Ridership
                          WHERE Type_of_Day LIKE ('W')"""
    dbCursor.execute(weekdayRidership)  # will give the total number of riders on the weekdays
    rowWeekdayRidership = dbCursor.fetchone()
    weekdayPercentage =  rowWeekdayRidership[0] / rowTotalRidership[0]  # will divide the number of riders on weekdays and divide it by total riders
    print("  Weekday ridership:",
          f"{rowWeekdayRidership[0]:,}", "("f"{weekdayPercentage:.2%}"")")

    saturdayRidership = """SELECT  SUM(Num_Riders)
                           FROM Ridership
                           WHERE Type_of_Day LIKE ('A')"""
    dbCursor.execute(saturdayRidership)  # obtains the total number of riders on saturdays
    rowSaturdayRidership = dbCursor.fetchone()
    saturdayPercentage = rowSaturdayRidership[0] / rowTotalRidership[0]
    print("  Saturday ridership:",
          f"{rowSaturdayRidership[0]:,}", "("f"{saturdayPercentage:.2%}"")")

    sundayRidership = """SELECT  SUM(Num_Riders)
                         FROM Ridership
                         WHERE Type_of_Day LIKE ('U')"""
    dbCursor.execute(sundayRidership)  # obtains the total number of riders on sundays and holidays
    rowSundayRidership = dbCursor.fetchone()
    sundayPercentage = rowSundayRidership[0] / rowTotalRidership[0]
    print("  Sunday/holiday ridership:",
          f"{rowSundayRidership[0]:,}", "("f"{sundayPercentage:.2%}"")")
  
################################################################## 
#
# commandOne
#
# The following command will take the user's input and retrieve stations
# similar to what is being input in an ascending order.
#
def commandOne(dbConn):
  db1Cursor = dbConn.cursor()
  userStation = input("\nEnter partial station name (wildcards _ and %): ")  # this line will obtain the user's input

  sql = """SELECT  Station_ID, Station_Name
           FROM Stations
           WHERE Station_Name LIKE ?
           ORDER BY Station_Name ASC"""

  rowUserStation = db1Cursor.execute(sql, [userStation]).fetchall()
  
  if not rowUserStation:                      # if the sql query returns nothing, it will notify the user
    print("**No stations found...")
  else:                                       # otherwise it will print the results from the query
    for row in rowUserStation:
      print(row[0], ":", row[1])
      
################################################################## 
#
# commandTwo
#
# The following command will output the total ridership of each
# station in an ascending order followed by a percentage 
# of the total ridership and the station
#
def commandTwo(dbConn):
  db2Cursor = dbConn.cursor()
  dbPercentage = dbConn.cursor()  # will be used in order to obtain total riders
  
  sql = """SELECT  Station_Name, SUM(Num_Riders)
           FROM Ridership
           JOIN Stations ON Ridership.Station_ID = Stations.Station_ID
           GROUP BY Station_Name
           ORDER BY Station_Name ASC"""

  totalRidership = """SELECT SUM(Num_Riders)
                        FROM Ridership"""
  
  rowTotalRiders = db2Cursor.execute(sql).fetchall()  # obtains total ridership for each station
  rowPercentage = dbPercentage.execute(totalRidership).fetchone()
  
  print("** ridership all stations **")
  for row in rowTotalRiders:  # will output number of riders for each station
    totalRiderPercentage = row[1] / rowPercentage[0]
    print(row[0], ":", f"{row[1]:,}", "("f"{totalRiderPercentage:.2%}"")")  # fstring in order to print percentages
    
################################################################## 
#
# commandThree
#
# The following command will output the top-10 most ridden trains 
# in descending order by ridership
#
def commandThree(dbConn):
  db3Cursor = dbConn.cursor()
  dbPercentage = dbConn.cursor()  # will be used to obtain total ridership

  sql = """SELECT  Station_Name, SUM(Num_Riders)
           FROM Ridership
           JOIN Stations ON Ridership.Station_ID = Stations.Station_ID
           GROUP BY Station_Name
           ORDER BY SUM(Num_Riders) DESC
           LIMIT 10"""

  totalRidership = """SELECT SUM(Num_Riders)
                        FROM Ridership"""

  rowTopTen = db3Cursor.execute(sql).fetchall()  # obtains the first 10 querys for busiest stations in terms of ridership
  rowPercentage = dbPercentage.execute(totalRidership).fetchone()  # value obtained will be divided by each station ridership to get percentage

  print("** top-10 stations **")
  for row in rowTopTen:
    percentage = row[1] / rowPercentage[0]
    print(row[0], ":", f"{row[1]:,}", "("f"{percentage:.2%}"")")
    
################################################################## 
#
# commandFour
#
# The following command will output the least-10 ridden trains 
# in ascending order by ridership
#
def commandFour(dbConn):
  db4Cursor = dbConn.cursor()
  dbPercentage = dbConn.cursor()

  sql = """SELECT  Station_Name, SUM(Num_Riders)
           FROM Ridership
           JOIN Stations ON Ridership.Station_ID = Stations.Station_ID
           GROUP BY Station_Name
           ORDER BY SUM(Num_Riders) ASC
           LIMIT 10"""

  totalRidership = """SELECT SUM(Num_Riders)
                        FROM Ridership"""

  rowTopTen = db4Cursor.execute(sql).fetchall()
  rowPercentage = dbPercentage.execute(totalRidership).fetchone()

  print("** least-10 stations **")
  for row in rowTopTen:
    percentage = row[1] / rowPercentage[0]  # will calculate the percentage for each station and print out in next line
    print(row[0], ":", f"{row[1]:,}", "("f"{percentage:.2%}"")")  # use of fstrings to easily format output
    
################################################################## 
#
# commandFive
#
# The following command will output the stations associated when a color line is input.
# The station names will be output in ascending order.
#
def commandFive(dbConn):
  db5Cursor = dbConn.cursor()

  stationColor = input("\nEnter a line color (e.g. Red or Yellow): ")
  
  sql = """SELECT Stop_Name, Direction, ADA
           FROM Stops
           JOIN StopDetails ON Stops.Stop_ID = StopDetails.Stop_ID
           JOIN Lines ON StopDetails.Line_ID = Lines.Line_ID
           WHERE Color LIKE ?
           GROUP BY Stop_Name
           ORDER BY Stop_Name ASC"""

  rowColorLine = db5Cursor.execute(sql, [stationColor]).fetchall()  # will obtain the stop name allong with the direction/accessibility

  if not rowColorLine:  # if the query returns no results, the user will be notified
    print("**No such line...")
  else:  # otherwise the query result will output
    for row in rowColorLine:
      print(row[0], ": direction =", row[1], """(accessible? """, end = "")
      if(row[2] == 1):
        print("yes)")
      else:
        print("no)")
      
################################################################## 
#
# commandSix
#
# The following command will output the total number of riders per month in ascending order by month.
# The user will then get to chose whether or not the data will be plotted.
#
def commandSix(dbConn):
  db6Cursor = dbConn.cursor()
  x = []
  y = []

  sql = """SELECT strftime('%m', Ride_Date), SUM(Num_Riders)
           FROM Ridership
           GROUP BY strftime('%m',Ride_Date)
           ORDER BY strftime('%m',Ride_Date) ASC"""

  rowRidershipByMonth = db6Cursor.execute(sql).fetchall()

  print("** ridership by month **")
  for row in rowRidershipByMonth:  # the query will be printed in ascending order by month
      print(row[0], ":", f"{row[1]:,}")

  plotChoice = input("\nPlot? (y/n) ")  # the user will be given the choice to plot the query

  if plotChoice == "y":
    for row in rowRidershipByMonth:
      x.append(row[0])
      y.append(row[1])
  else:
    return  # if the user selects anything but "y", they will be sent back to the main command menu

  plt.xlabel("month")  # the xlabel function will put a string label for the x axis
  plt.ylabel("number of riders (x*10^8)") # similar to xlabel but instead on the y axis
  plt.title("monthly ridership") # this will set the string given as the main title of the plot
  plt.plot(x, y)
  plt.show()

################################################################## 
#
# commandSeven
#
# The following command will output the total number of riders per year in ascending order by year.
# The user will then get to chose whether or not the data will be plotted.
#
def commandSeven(dbConn):
  db7Cursor = dbConn.cursor()
  x_7 = []
  y_7 = []

  sql = """SELECT strftime('%Y', Ride_Date), SUM(Num_Riders)
           FROM Ridership
           GROUP BY strftime('%Y',Ride_Date)
           ORDER BY strftime('%Y',Ride_Date) ASC"""
  
  rowRidershipByYear = db7Cursor.execute(sql).fetchall()  # will execute the query into a tuple due to the fetchall() argument

  print("** ridership by year **")
  for row in rowRidershipByYear:
      print(row[0], ":", f"{row[1]:,}")

  plotChoice = input("\nPlot? (y/n) ")

  if plotChoice == "y":
    for row in rowRidershipByYear:
      x_7.append(row[0][2:4])  # will append the year, the [2:4] will ensure only the last two digits of the year will be appended
      y_7.append(int(row[1]))
  else:  # will return the user to the main menu if selected no
    return

  plt.xlabel("year")
  plt.ylabel("number of riders (x*10^8)")
  plt.title("yearly ridership")
  plt.plot(x_7, y_7)
  plt.show()
  
################################################################## 
#
# commandEight
#
# The following command will compare between two user selected stations
# the total number of riders per day starting with the first and 
# last five days of the year selected by the user in ascending 
# order by year. The user will then get to chose whether or not the data will be plotted.
#
def commandEight(dbConn):
  db8Cursor = dbConn.cursor()
  x_81 = []
  y_81 = []
  x_82 = []
  y_82 = []
  day = 1  # will be used to count the number of days in the year input by the user and plotted on the x axis

  userInputYear = input("\nYear to compare against? ")  # will ask the user for the year to compare
  userInputStation1 = input("\nEnter station 1 (wildcards _ and %): ")  # will obtain the name of first station
  
  sql1 = """SELECT Station_ID, Station_Name
            FROM Stations
            WHERE Station_Name LIKE ?
            ORDER BY Station_Name ASC"""

  sql2 = """SELECT strftime('%Y-%m-%d', Ride_Date), Num_Riders
            FROM Ridership
            JOIN Stations on Ridership.Station_ID = Stations.Station_ID
            WHERE Station_Name LIKE (?) AND strftime('%Y', Ride_Date) = ?
            GROUP BY strftime('%Y%m%d',Ride_Date)
            ORDER BY strftime('%Y%m%d',Ride_Date) ASC"""

  rowQuery1 = db8Cursor.execute(sql1, [userInputStation1]).fetchall()  # will get the station id and station name of first entry
  
  if not rowQuery1:  # if the station is not found, it will notify the user
    print("**No station found...")
    return
  elif len(rowQuery1) > 1:  # user wil also be notified if more than one station appears
    print("**Multiple stations found...")
    return

  rowQuery2 = db8Cursor.execute(sql2, [userInputStation1, userInputYear]).fetchall()  # will obtain the dates and number of riders for first entry

##############################

  userInputStation2 = input("\nEnter station 2 (wildcards _ and %): ")
  rowQuery3 = db8Cursor.execute(sql1, [userInputStation2]).fetchall()  # will obtain the station id and station name of second entry

  if not rowQuery3:  # similar to before, the user will be notified of any errors with the station name input
    print("**No station found...")
    return
  elif len(rowQuery3) > 1:
    print("**Multiple stations found...")
    return

  rowQuery4 = db8Cursor.execute(sql2, [userInputStation2, userInputYear]).fetchall()  # will obtain the dates and number of riders for second entry

##############################
  
  for row in rowQuery1:  # the first station input will first be output
    print("Station 1:", row[0], row[1])
    label1 = row[1]
  for i in range(5):
    print(rowQuery2[i][0], rowQuery2[i][1])
  for j in range(-5, 0):
    print(rowQuery2[j][0], rowQuery2[j][1])

  for row in rowQuery3:  # after, the second station will be output
    print("Station 2:", row[0], row[1])
    label2 = row[1]
  for i in range(5):
    print(rowQuery4[i][0], rowQuery4[i][1])
  for j in range(-5, 0):
    print(rowQuery4[j][0], rowQuery4[j][1])

  plotChoice = input("\nPlot? (y/n) ")  # the user will be asked if they want to plot the comparisons

  if plotChoice == "y":  # if they choose to do so, the number of days will be appended to the x axis and the number of riders to the y axis
    for row in rowQuery2:
      x_81.append(day)
      y_81.append(row[1])
      day = day + 1
    day = 1  # will reset the number of days for the second station
    for row in rowQuery4:
      x_82.append(day)
      y_82.append(row[1])
      day = day + 1  # counts the number of days for the year input
  else:
    return
    
  title = "riders each day of " + userInputYear
  plt.xlabel("day")
  plt.ylabel("number of riders")
  plt.title(title)
  
  plt.plot(x_81, y_81, label = label1)  # will plot the first station with a label indicating which station, same is done for the second station
  plt.plot(x_82, y_82, label = label2)
  plt.legend(loc='upper right')  # will position the legend of the labels to the upper right corner
  plt.show()

################################################################## 
#
# commandNine
#
# The following command will obtain a line color from the user
# afterwhich the program will output the station names and its latitude
# and longitude, finally the choice to plot a graph with a chicago map png
# showing the location of each stop will be provided
#
def commandNine(dbConn):
  db9Cursor = dbConn.cursor()
  x_9 = []
  y_9 = []

  userColor = input("\nEnter a line color (e.g. Red or Yellow): ")  
  userColor = userColor.lower()  # in order to prevent any errors, the color name will be set to lower case

  sql = """SELECT DISTINCT(Station_Name), Latitude, Longitude
           FROM Lines
           JOIN StopDetails ON Lines.Line_ID = StopDetails.Line_ID
           JOIN Stops ON StopDetails.Stop_ID = Stops.Stop_ID
           JOIN Stations ON Stops.Station_ID = Stations.Station_ID
           WHERE Color LIKE ?
           ORDER BY Station_Name ASC"""

  rowStationName = db9Cursor.execute(sql, [userColor]).fetchall()

  if not rowStationName:  # if there is no station found the user will be notified and sent back to the command menu
    print("**No such line...")
    return
  else:
    for row in rowStationName:
      print(f"{row[0]} : ({row[1]}, {row[2]})")

  plotChoice = input("\nPlot? (y/n) ")

##############################
  
  if plotChoice == "y":  # if the user chooses to plot
    for row in rowStationName:
      x_9.append(row[2])  # the x axis will be the longitude
      y_9.append(row[1]) # y axis will be the latitude
  else:
    return

  image = plt.imread("chicago.png")  # will output the chicago grid
  xydims = [-87.9277, -87.5569, 41.7012, 42.0868]
  plt.imshow(image, extent=xydims)
  title = userColor + " line"
  plt.title(title)  # the title will be the color input by the user
  
  if(userColor.lower() == "purple-express"):  # in this exception, the color will be purple, as there is no color purple-express
    userColor = "Purple"

  plt.plot(x_9, y_9, "o", c = userColor)
    
  for rows in rowStationName:  
    plt.annotate(rows[0], (rows[2], rows[1]))  # will output a dot of the line color on the map to the specific coordinates given in the query

  plt.xlim([-87.9277, -87.5569])
  plt.ylim([41.7012, 42.0868])
  
  plt.show()
  
##################################################################
#
# main
#
print('** Welcome to CTA L analysis app **')
print()

dbConn = sqlite3.connect('CTA2_L_daily_ridership.db')

print_stats(dbConn)

while True:  # will ask the user for a command until x is input
  userInput = input('\nPlease enter a command (1-9, x to exit): ')
  if userInput == "1":
    commandOne(dbConn)
    continue
  elif userInput == "2":
    commandTwo(dbConn)
    continue
  elif userInput == "3":
    commandThree(dbConn)
    continue
  elif userInput == "4":
    commandFour(dbConn)
    continue
  elif userInput == "5":
    commandFive(dbConn)
    continue
  elif userInput == "6":
    commandSix(dbConn)
    continue
  elif userInput == "7":
    commandSeven(dbConn)
    continue
  elif userInput == "8":
    commandEight(dbConn)
    continue
  elif userInput == "9":
    commandNine(dbConn)
    continue
  elif userInput == "x":  # this option will quit the program
    break
  else:  # if the character x or integers 1-9 is input, it will notify the user of the error
    print("**Error, unknown command, try again...")

#
# done
#
