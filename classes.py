from datetime import datetime
import uuid
import sys
from getpass import getpass

#This is the main show class
class Show:
    #Show class functions
    #1. Add Show
    #2. Update Show
    #3. Delete Show
    #4. View all valid shows --> For user and admin both
    #4. View Bookings --> Only for admin

    def __init__(self):
        index = 0
        self.showFile= open("showList.txt",'r')
        self.showList = []    #Contains list of all the shows that are there irrespective of whether they are valid or invalid
        for line in self.showFile:
            showDetails = line.split(",")
            self.showList.append(showDetails)
            index += 1
        self.updateList()    

    #Displays a list of all the shows that are active to the user
    def viewShows(self):
        self.updateList()
        self.List = [0]
        pos = 1
        for showDetails in self.showList: 
            if showDetails[0] == '0':
                continue
            self.List.append(showDetails[1])
            print(pos,end='')
            print(")")
            print("Name: ",end="")
            print(showDetails[2].replace('}',','))
            print("Date: ",end="")
            print(showDetails[3])
            print("Time: ",end="")
            print(showDetails[4])
            print("Available Seats: ",end="")
            print(self.availableSeats(showDetails))
            pos += 1
        if len(self.List) == 1:
            return print("\nNo shows are available right now. Kindly check in after some time.\n")     
    
    #Allows the admin to add a new show
    def addShow(self):
        print("Please enter the details of new show in order to conitnue.")
        print("Show Name: ",end='')
        showName = input()
        showName = showName.replace(',','}')
        if len(showName) == 0:
            print("\nShow name cannot be empty.\n")
            print("Please try again. Press Y to try again, else any other key to return back.")
            choice = input()
            if choice == 'Y':
                return self.addShow()
            else:  
                #Returns back
                return None  
        print("Show Date (Format: DD/MM/YYYY): ",end='')
        showDate = input()
        print("Show Time (Format: HH:MM 24Hrs Format): ",end='')
        showTime = input()
        print("Number of seats: ",end='')
        try:
            now = datetime.now()
            showSeats = int(input())
            if showSeats < 5:
                print("A show cannot be created with less than 5 seats.")
                print("Please try again. Press Y to try again, else any other key to return back.")
                choice = input()
                if choice.lower() == 'y':
                    return self.addShow()
                else:  
                    #Returns back
                    return None 
            showDater = showDate.split("/")
            showTimer = showTime.split(":")
            date = datetime(int(showDater[2]),int(showDater[1]),int(showDater[0]),int(showTimer[0]),int(showTimer[1]))
            if date < now:
                print("\n\n**New show cannot be added before current time.**\n\n")
                print("Please try again. Press Y to try again, else any other key to return back.")
                choice = input()
                if choice.lower() == 'y':
                    return self.addShow()
                else:  
                    #Returns back
                    return None  
            pos = 0
            for showDetails in self.showList: 
                pos += 1
                if showDetails[0] == 0:
                    break
                CshowDate = showDetails[3].split("/")
                CshowTime = showDetails[4].split(":")
                Cdate = datetime(int(CshowDate[2]),int(CshowDate[1]),int(CshowDate[0]),int(CshowTime[0]),int(CshowTime[1]))
                if date > Cdate:
                    break
                else:
                    continue 
        except:
            print("\nThe entered number of seats, time or date format is invalid\n")  
            print("Please try again. Press Y to try again, else any other key to return back.")
            choice = input()
            if choice == 'Y':
                return self.addShow()
            else:  
                #Returns back
                return None     
        showSUID = str(uuid.uuid4()).upper()[0:4]
        try:
            self.showList.insert(pos-1,[1,showSUID,showName,showDate,showTime,showSeats,"0\n"])
            self.showFile.close()
            self.showFile= open("showList.txt",'w')
            for showDetails in self.showList:
                count = 0
                for details in showDetails:
                    self.showFile.write(str(details))
                    if count == 6:
                        continue
                    else:
                        self.showFile.write(",")
                    count += 1
            self.showFile.close()
            self.showFile= open("showList.txt",'r')  
            return print("\n**** New show added successfully ****\n")
        except:
            print("\n****Some error occured!****\n")  
            print("Please try again. Press Y to try again, else any other key to return back.")
            choice = input()
            if choice == 'Y':
                return self.addShow()
            else:  
                #Returns back
                return None  
    
    #Updates the show list. Make the shows before the current time inavtive and also this deletes all those shows which are 30days or older
    def updateList(self):       
        now = datetime.now()
        i = 0
        for showDetails in self.showList:   
            showDate = showDetails[3].split("/")
            showTime = showDetails[4].split(":")
            date = datetime(int(showDate[2]),int(showDate[1]),int(showDate[0]),int(showTime[0]),int(showTime[1]))
            diff = int((now-date).days)
            if diff >= 0 and diff < 30:
                showDetails[0] = '0'
                for j in range(i,len(self.showList)):
                    if self.showList[j][0] == '0':
                        break 
                    else:
                        self.showList[j][0] = '0'
            elif diff > 30:
                del self.showList[i:len(self.showList)] 
                break  
            availableSeats = self.availableSeats(showDetails)
            if availableSeats <= 0:
                self.showList[i][0] = '0'   
            i += 1    

        try:
            self.showFile.close()
            self.showFile= open("showList.txt",'w')
            for showDetails in self.showList:
                count = 0
                for details in showDetails:
                    self.showFile.write(str(details))
                    if count == 6:
                        continue
                    else:
                        self.showFile.write(",")
                    count += 1
            self.showFile.close()
            self.showFile= open("showList.txt",'r')  
            return None
        except:
            print("\n****Some error occured!****\nPlease restart the application.")
            return sys.exit()
   
     #Allows the admin to remove a show from the list of all shows
    
    #This allows the user to remove/delete a show from the list of all shows
    def removeShow(self):      
        self.viewAllShows()
        if len(self.ListAll) == 1:
            return print("No shows are available right now. Kindly add some shows in order to remove them.") 
        print("Please enter the position of the show whom you want to delete: ",end="")
        try:
            removeShowPos = int(input())
            if removeShowPos > len(self.ListAll) - 1:
                print("Please enter a valid position.")
                print("Please try again. Press Y to try again, else any other key to return back.")
                choice = input()
                if choice == 'Y':
                    return self.removeShow()
                else:  
                        #Returns back
                        return None  
        except:
            print("The position must be an integer.")
            print("Please try again. Press Y to try again, else any other key to return back.")
            choice = input()
            if choice == 'Y':
                return self.removeShow()
            else:  
                #Returns back
                return None          

        try:
            print("\nAre you sure you want to delete this show? Y for yes, any other key for no")
            print("Enter your choice :",end="")
            choice = input()
            if choice.lower() != 'y':
                return print("Delete cancelled")
            del self.showList[removeShowPos -1]
            self.showFile.close()
            self.showFile= open("showList.txt",'w')
            for showDetails in self.showList:
                count = 0
                for details in showDetails:
                    self.showFile.write(str(details))
                    if count == 6:
                        continue
                    else:
                        self.showFile.write(",")
                    count += 1
            self.showFile.close()
            self.showFile= open("showList.txt",'r')  
            return print("\n**** Show deleted succesfully. ****\n")
        except:
            print("\n****Some error occured!****\n") 
            print("Please try again. Press Y to try again, else any other key to return back.")
            choice = input()
            if choice == 'Y':
                return self.removeShow()
            else:  
                #Returns back
                return None  
    
    #Prints the list of all the available shows for the admin irrespective of whether the show is valid or not
    def viewAllShows(self):    
        self.updateList()
        self.ListAll = [0]
        pos = 1
        for showDetails in self.showList: 
            self.ListAll.append(showDetails[1])
            print(pos,end='')
            print(")")
            print("Name: ",end="")
            print(showDetails[2].replace('}',','))
            print("Date: ",end="")
            print(showDetails[3])
            print("Time: ",end="")
            print(showDetails[4])
            print("Total No. of seats: ",end="")
            print(showDetails[5])
            print("Available Seats: ",end="")
            print(self.availableSeats(showDetails))
            if showDetails[0] == '0':
                print("\nThe show is currently not active.\n")
            pos += 1 
        if len(self.ListAll) == 1:
            return print("No shows are available right now. Kindly check in after some time or add new shows.")        

    #Returns the number of seats available in the show
    def availableSeats(self, showDetails):
        if showDetails[6] == '0\n' or showDetails[6] == '0':
            return int(showDetails[5])
        d = showDetails[6].split(";")
        de  = dict()
        for i in d:
            j = i.split(":")
            if j[0] in de:
                    de[j[0]] += int(j[1])
            else:    
                    de[j[0]] = int(j[1])
        count = 0
        for i in de:
            count += de[i]    
        return int(showDetails[5])-count
    
    #Allows the user to book from a list of active shows
    def bookShow(self, uid):
        print("\n")
        self.viewShows()
        if len(self.List) == 1:
            return print("\nNo shows are available right now. Kindly check in after some time.\n") 
        print("Please enter the postition of the show that you want to book: ",end="")
        try:
            bookShowPos = int(input())
            if bookShowPos > len(self.List) - 1:
                print("Please enter a valid position.")
                print("Please try again. Press Y to try again, else any other key to return back.")
                choice = input()
                if choice.upper() == 'Y':
                    return self.bookShow(uid)
                else:  
                        #Returns back
                        return None  
        except:
            print("The position must be an integer.")
            print("Please try again. Press Y to try again, else any other key to return back.")
            choice = input()
            if choice == 'Y':
                return self.bookShow(uid)
            else:  
                #Returns back
                return None          

        bookShowID = self.List[bookShowPos]
        number = 0
        for i in range(len(self.showList)):
            #print(self.showList[i][1])
            if bookShowID == self.showList[i][1]:
                showDetails = self.showList[i]
                number = i
                break
        if showDetails[6] == '0\n' or showDetails[6] == '0':
            availableSeats = int(showDetails[5])
        else:
            d = showDetails[6].split(";")
            de  = dict()
            for i in d:
                j = i.split(":")
                if j[0] in de:
                    de[j[0]] += int(j[1])
                else:    
                    de[j[0]] = int(j[1])
                if j[0] == uid:
                    print("A booking for",int(j[1]),"seat are already exists" )    
            count = 0
            for i in de:
                count += de[i]       
            availableSeats = int(showDetails[5])-count
            if uid in de: 
                print("Do you want to book more seats or exit? Enter C for booking more seats or any other key for returning back.")
                print("Please enter your choice: ",end="")
                c = input().lower()
                if c != 'c':
                    #Return back
                    return None
        print("Please enter how many seats you want to book for the given show: ",end="")
        try:
            noOfSeats = int(input())
        except:
            print("Number of seats should be integer")  
            return self.bookShow(uid)  
        if noOfSeats > availableSeats:
            print("You cannot book more seats than those that are available.")
            print("Please try again. Press Y to try again, else any other key to return back.")
            choice = input().lower()
            if choice == 'y':
                return self.bookShow(uid)
            else:  
                #Returns back
                return None
        if noOfSeats <= 0:
            print("Number of tickets cannot be negative or zero.")
            print("Please try again. Press Y to try again, else any other key to return back.")
            choice = input().lower()
            if choice == 'y':
                return self.bookShow(uid)
            else:  
                #Returns back
                return None        
        if showDetails[6] == '0\n' or showDetails[6] == '0':
            showDetails[6] = str(uid)+":"+str(noOfSeats)
        else:
            showDetails[6] = showDetails[6].replace("\n","") +";"+str(uid)+":"+str(noOfSeats)
        if number != len(self.showList)-1:
            showDetails[6] += "\n"
        self.showList[number] = showDetails
        try:
            self.showFile.close()
            self.showFile= open("showList.txt",'w')
            for showDetails in self.showList:
                count = 0
                for details in showDetails:
                    self.showFile.write(str(details))
                    if count == 6:
                        continue
                    else:
                        self.showFile.write(",")
                    count += 1
            self.showFile.close()
            self.showFile= open("showList.txt",'r')  
            return print("\n**** Show booking succesfull. The show details and tickets have been mailed to you on your registered mail id. Thank you for using BigTicket. Hope you had a great experience.  ****\n")
            #Should return back to main menu
        except:
            print("SOME ERROR OCCURED") 
            print("Please try again. Press Y to try again, else any other key to return back.")
            choice = input()
            if choice == 'Y':
                return self.bookShow(uid)
            else:  
                #Returns back
                return None
 
    #Allows the admin to update show name or make the show valid or invalid
    def updateShow(self):
        self.viewAllShows()
        if len(self.ListAll) == 1:
            return print("No shows are available right now. Kindly add some shows in order to update them.") 
        print("Please enter the postion of the show you want to update: ",end='')
        try:
            choice = int(input())
            if choice > len(self.showList) or choice == 0:
                print("\nThe position is out of range. Please try again.")
                return sel8f.updateShow()
        except:
            print("The position must be an integer.")
            print("Please try again,") 
            return self.updateShow()          
        print("\n\n")
        print("Please enter the updated details for the show")
        print("Show Name(Press **NA** if you don't want to update the name): ",end='')
        showName = input()
        if len(showName) == 0:
            print("\nShow name cannot be empty.\n")
            print("Please try again. Press Y to try again, else any other key to return back.")
            choice = input()
            if choice == 'Y':
                return self.updateShow()
            else:  
                #Returns back
                return None  
        if showName == "**NA**":
            showName = self.showList[choice-1][2].replace('}',',')
        print("Enter 1 to make the show valid or 0 to make the show invalid.")
        print("Please enter your choice: ",end="")
        try:
            checker = int(input())  
            if checker == 0 or checker == 1:
                pass
            else:
                print("Please enter a valid choice.")
                print("Please try again")
                return self.updateShow()
        except:
            print("Please enter either 1 or 2")  
            print("Please try again")
            return self.updateShow()             
        showDetails = [0,0,0,0,0,0,0]   
        showDetails[0] = checker
        showDetails[1] = self.showList[choice-1][1]
        showDetails[2] = showName
        showDetails[3] = self.showList[choice-1][3]
        showDetails[4] = self.showList[choice-1][4]
        showDetails[5] = self.showList[choice-1][5]
        showDetails[6] = self.showList[choice-1][6]
        self.showList[choice-1] = showDetails
        try:
            self.showFile.close()
            self.showFile= open("showList.txt",'w')
            for showDetails in self.showList:
                count = 0
                for details in showDetails:
                    self.showFile.write(str(details))
                    if count == 6:
                        continue
                    else:
                        self.showFile.write(",")
                    count += 1
            self.showFile.close()
            self.showFile= open("showList.txt",'r')  
            return print("\n**** Show details updated successfully. ****\n")
            #Should return back to main menu
        except:
            print("SOME ERROR OCCURED") 
            print("Please try again. Press Y to try again, else any other key to return back.")
            choice = input()
            if choice == 'Y':
                return self.updateShow()
            else:  
                #Returns back
                return None

    #Allows the user to view all of his bookings
    def viewBookings(self, uid):
        print("\nHere is a list of all the bookings done by you.\n")
        pos = 1
        for showDetails in self.showList:
            allBookings = showDetails[6].split(";")
            for i in allBookings:
                j = i.split(":")
                if j[0] == uid:
                    now = datetime.now()
                    showDater = showDetails[3].split("/")
                    showTimer = showDetails[4].split(":")
                    date = datetime(int(showDater[2]),int(showDater[1]),int(showDater[0]),int(showTimer[0]),int(showTimer[1]))
                    print(pos,end='')
                    print(")",)
                    if date < now:
                        print(" **Past booking: The time for this show has passed.**")
                    else:
                        print(" Upcoming booking")    
                    print("Show name: ",end="")
                    print(showDetails[2].replace('}',','))
                    print("Show date: ",end="")
                    print(showDetails[3])
                    print("Show time: ",end="")
                    print(showDetails[4])
                    print("No. of seats booked: ",end="")
                    print(j[1])
                    print("\n")
                    pos += 1
        if pos == 1:
            print("No bookings have been made yet.\n")         
        return None    

#This class is created for user that is the client from which he/she can perform various functions
class User:
    def __init__(self):
        # This creates an instance of Show class from which the user can access various shows and it's functions
        self.show = Show()   
        #self.value is to know whether the user is trying to sign out or not. If user is going to sign out then self.value becomes zero 
        self.value = 1        
        return self.Menu()
   
    #def Menu is the function that prints the user menu which includes User Login, User Registration and back option
    def Menu(self):
        print("1. User Login 2. User Registration 3. Back")      
        #The try statement is to check whether the input given by the user is an integer or not. If not then it again asks the user for his input
        try:
            print("Please enter your choice: ",end="")
            choice = int(input())
        except:
            print("\nPlease enter a valid choice.")
            return self.Menu()         
        if choice == 1:
            return self.userLogin()
        elif choice == 2:
            return self.userRegistration()
        elif choice == 3:
            return 
        else:
            print("Please enter a valid choice.")
            return self.Menu()               

    #Allows the user to login
    def userLogin(self):   
        if self.value == 0:             
            return sys.exit()
        print("Kindly enter the following details in order to log in")
        print("Email ID: ",end='')
        try:
            userID = input().lower()                                                                    #userID is the mail id of the user. 
            password = getpass("Password: ").replace(",","-}-")                                           #We replace ',' by "-}-" because the value in our data file are all seperated by comma's i.e. ","
            self.userFile = open("userList.txt",'r')                                                    #Opens the user file in order to check for the existance of the user
            for line in self.userFile:                                                                  # 'line' is the variable that stores the values of each user
                userDetails = line.split(",")                                                      #line.split() command splits the various values which are seperated by comma i.e. ','
                if userID == userDetails[1] and password == userDetails[3].replace("\n",''):     #self.userDetails[1] is the email id of the user and self.userDetails[3] is the password, if they both match then log in
                    self.userDetails = userDetails
                    print("\nLogin successfull\n")
                    print("Welcome",self.userDetails[2].replace("-}-",","))
                    self.userFile.close()                                                               #This command closes the file and passes on all the user details to the after login menu.
                    return self.afterLoginMenu()
                elif userID == userDetails[1] and password != userDetails[3]:                 #If the email id exists in the list but password don't match then the user is told that password is invalid is again sent back to the previous menu.
                    print("The entered password is invalid. Kindly try logging in again.\n") 
                    self.userFile.close()   
                    return self.Menu()
            print("No user exists with this mail id.")
            print("Kindly create an account first in order to log in.\n")                               #else if the entered mail id does not match any of the mail id in the list then the user in asked to register and then log in
            return self.Menu()
        except:
            if self.value == 0:
                return sys.exit()
            print("\nSome error occured. Please try again from the starting. Sorry for the inconvenience.")   
            print("Quiting the software")
            return sys.exit() 

    #This is the menu that user sees after log in
    def afterLoginMenu(self):    
        if self.value == 0:
            return sys.exit()
        self.userID = self.userDetails[0].replace(",","-}-")    
        self.UserName = self.userDetails[2].replace(",","-}-")
        self.userMail = self.userDetails[1].replace(",","-}-")
        print("1. View available shows 2. Book a new show 3. View bookings 4. View Profile 5. Update Profile 6. Sign Out")     
        try:
            choicee = int(input("Please enter your choice to continue: "))     
            if choicee == 1:
                self.show.viewShows()
                return self.afterLoginMenu()              #This guides the user to first the function that shows user all the lists and then back to the afterLoginMenu
            elif choicee == 2:
                self.show.bookShow(self.userID)
                print("The tickets have been mailed to",self.userMail)
                return self.afterLoginMenu()              #This guides the user to first the function that allows the user to book show and then back to the afterLoginMenu
            elif choicee == 3:
                self.show.viewBookings(self.userID)    
                return self.afterLoginMenu()              #This allows user to view all the bookings done by him and then back to the afterLoginMenu
            elif choicee == 4:
                self.viewProfile()                        #This allows user to view all his profile details and then back to the afterLoginMenu
                return self.afterLoginMenu()
            elif choicee == 5:
                self.updateProfile()                      #This is a feature that is not currently active 
                return self.afterLoginMenu()
            elif choicee == 6:
                self.value = 0                            #When user tries to sign out then self.value changes to 0 and takes the user backs to main menu
                return None
            else:
                print('\nPlease enter a valid choice')    #If the input enetered by user cannot be converted to an integer type then it prompts an error that the input is invalid and guides the user back to the afterloginMenu
                return self.afterLoginMenu() 
        except:
            if self.value == 0:
                return sys.exit()
            print('\nPlease enter a valid choice')
            return self.afterLoginMenu()             

    #Allows the user to register
    def userRegistration(self):
        if self.value == 0:
            return sys.exit()
        print("Kindly enter the following details in order to create a new account")
        print("Full name: ",end="")
        userName = input().replace(",","-}-")
        print("Age: ",end='')
        try:
            userAge = int(input())
            if userAge < 18:
                print("The user must be 18 or older in order to create an account.")
                print("Please try again.")
                return self.userRegistration()
        except:
            print("The age must be an integer.")
            print("Please try again.")  
            return self.userRegistration()
        print("Email ID: ",end="")
        userMail = input().lower()
        if '@' not in userMail or '.' not in userMail:
            print("The entered email is not valid.")
            print("Please try again.")  
            return self.userRegistration()
        val = self.checkExistance(userMail)       #checkExistance function return's 0 if a user exits with the given mail id and 1 if he doesn't
        if val == 0:
            print("An user already exists with this user id. Kindly try logging back in.")
            print("Returning back to previous menu.\n")
            return self.Menu()
        userUID = str(uuid.uuid4()).upper()[0:4]   
        password = getpass("Please enter your password: ")
        repassword = getpass("Please re-enter your password: ")
        if repassword != password:
            print("The enter password is incorrect.\nPlease try again")
            return self.userRegistration()
        try:
            self.userFile = open("userList.txt",'a')
            self.userFile.write(userUID)
            self.userFile.write(",")
            self.userFile.write(userMail.replace(",","-}-"))
            self.userFile.write(",")
            self.userFile.write(userName)
            self.userFile.write(",")
            self.userFile.write(password.replace(",","-}-"))
            self.userFile.write("\n")
            print("\nUser registration successfull. Kindly log in again to sign in.")
            print("Returning back to previous menu.")
            self.userFile.close()
            return self.Menu()
        except:
            if self.value == 0:
                return sys.exit()
            print("\nSome error occured. Please try again from the starting. Sorry for the inconvenience.")   
            print("Quiting the software")
            return sys.exit()
    
    #checks whether an user already exists for not
    def checkExistance(self, ID):
        self.userFile = open("userList.txt",'r')
        for line in self.userFile:
            userDetails = line.split(",")
            if ID == userDetails[1]:
                self.userFile.close()
                return 0
        self.userFile.close()
        return 1

    #Allows the user to view his profile and update information
    def viewProfile(self):
        print("Name :",self.UserName)
        print("Email :",self.userMail)
        print("\n")
        return self.afterLoginMenu()
    
    #Allows the user to update his profile
    def updateProfile(self):
        print("This feature would be made avaiable in the future.")     #feature would be made available in the future
        return self.afterLoginMenu()
    
#This class is created for the admin from which he/she can perform various functions 
class Admin:

    def __init__(self):
        self.value = 1
        return self.Menu()

    #This is the first menu that prints. 
    def Menu(self):       
        #A new admin cannot be created directly. It can be only created by a already existent admin. The default admin is Admin Mail: admin@bigticket.com; Admin Name: Admin; Admin Password: password
        print("1. Admin Login 2. Back")
        try:
            print("Please enter your choice: ",end="")
            choicet = int(input())        
        except:
            print("\nPlease enter a valid choice.")
            return self.Menu()
        if choicet == 1:
            return self.adminLogin()
        elif choicet == 2:
            return None
        else:
            print("Please enter a valid choice.")
            return self.Menu()
            
    #Allows the admin to login
    def adminLogin(self):
        if self.value == 0:
            return sys.exit()
        print("Kindly enter the following details in order to log in")     #The admin login is completely similar to the userLofgin function.
        print("Email ID: ",end='')
        try:
            adminID = input().lower()
            password = getpass("Password: ").replace(",","-}-")
            self.adminFile = open("adminList.txt",'r')
            for line in self.adminFile:
                self.adminDetails = line.split(",")
                if adminID == self.adminDetails[1] and password == self.adminDetails[3].replace("\n",''):
                    print("\nLogin successfull\n")
                    print("Welcome",self.adminDetails[2].replace("-}-",","))
                    self.adminFile.close()
                    return self.afterLoginMenu()
                elif adminID == self.adminDetails[1] and password != self.adminDetails[3]:
                    print("The entered password is invalid. Kindly try logging in again.\n") 
                    return self.adminLogin()
            print("No admin exists with this mail id. Kindly create an account first in order to log in.\n")
            return self.Menu()
        except:
            if self.value == 0:
                return sys.exit()
            print("\nSome error occured. Please try again from the starting. Sorry for the inconvenience.")   
            print("Quiting the software")
            return sys.exit()    

    #This is the menu that admin sees after log in
    def afterLoginMenu(self):
        if self.value == 0:
            return sys.exit()
        self.show = Show()  
        self.adminID = self.adminDetails[0]
        self.adminMail = self.adminDetails[1].replace("-}-",",")
        self.adminName = self.adminDetails[2].replace("-}-",",")
        print("1. View All shows 2. Add Show 3. Remove Show 4. Update Show 5. Add new admin 6. Sign Out")
        try:
            choicee = int(input("Please enter your choice to continue: "))
            if choicee == 1:
                self.show.viewAllShows()
                return self.afterLoginMenu()
            elif choicee == 2:
                self.show.addShow()
                return self.afterLoginMenu()
            elif choicee == 3:
                self.show.removeShow()
                return self.afterLoginMenu()
            elif choicee == 4:
                self.show.updateShow()
                return self.afterLoginMenu()
            elif choicee == 5:
                self.adminRegistration()
                return self.afterLoginMenu()
            elif choicee == 6:
                self.value = 0
                return None
            else:
                print('\nPlease enter a valid choice')
                return self.afterLoginMenu() 
        except:
            if self.value == 0:
                return sys.exit()
            print('\nPlease enter a valid choice')
            return self.afterLoginMenu()      

    #Allows the admin to register after an admin as already logged in 
    def adminRegistration(self):
        print("Kindly enter the following details in order to create a new account")
        print("Full name: ",end="")
        adminName = input().replace(",","-}-")
        print("Age: ",end='')
        try:
            adminAge = int(input())
            if adminAge < 18:
                print("The admin must be 18 or older in order to create an account.")
                print("Please try again.")
                return self.adminRegistration()
        except:
            print("The age must be an integer.")
            print("Please try again.")  
            return self.adminRegistration()
        print("Email ID: ",end="")
        adminMail = input().lower()
        if '@' not in adminMail or '.' not in adminMail:
            print("The entered email is not valid.")
            print("Please try again.")  
            return self.adminRegistration()
        val = self.checkExistance(adminMail)    
        if val == 0:
            print("An admin already exists with this admin id.")
            print("Returning back to previous menu.\n")
            return self.afterLoginMenu()
        adminUID = str(uuid.uuid4()).upper()[0:4]   
        password = getpass("Please enter your password: ")
        repassword = getpass("Please re-enter your password: ")
        if repassword != password:
            print("The enter password is incorrect.\nPlease try again")
            return self.adminRegistration()
        try:
            self.adminFile = open("adminList.txt",'a')
            self.adminFile.write(adminUID)
            self.adminFile.write(",")
            self.adminFile.write(adminMail.replace(",","-}-"))
            self.adminFile.write(",")
            self.adminFile.write(adminName)
            self.adminFile.write(",")
            self.adminFile.write(password.replace(",","-}-"))
            self.adminFile.write("\n")
            print("\nNew admin created successfully")
            print("Returning back to previous menu.")
            self.adminFile.close()
            return self.afterLoginMenu()
        except:
            print("\nSome error occured. Please try again from the starting. Sorry for the inconvenience.")   
            print("Quiting the software")
            return sys.exit()
    
    #Checks whether an admin already exists for not, if yes then this functions return 0 else it returns 1
    def checkExistance(self, ID): 
        self.adminFile = open("adminList.txt",'r')
        for line in self.adminFile:
            adminDetails = line.split(",")
            if ID == adminDetails[1]:
                self.adminFile.close()
                return 0
        self.adminFile.close()
        return 1


#This message gets printed when the user to open this file directly
if __name__ == '__main__':
    print("This file is not meant to be opened by the client. Please run main.py")
    
    
