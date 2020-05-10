#Software Name: BigTicket
#The default admin is Admin Mail: admin@bigticket.com; Admin Name: Admin; Admin Password: password

import sys
from classes import User
from classes import Admin

#This is the main menu. It shows up when the software is opened. 
def MainMenu():
    print("Welcome to BigTicket! \nThe fastest and the biggest movie ticking system in Noida\n")
    print("Please chose on of the options from below to continueee")
    print("1. Admin User 2. Client User 3. Exit")
    try:
        print("Please enter your choice: ",end="")
        choicer = int(input())
    except:
        print("\nPlease enter a valid choice.")
        return MainMenu()    
    if choicer == 1:      #Allows the user to use the software as an admin
        admin = Admin()
        return admin.Menu()
    elif choicer == 2:    #Allows the user to use the software as an client user
        user = User()
        return MainMenu()
    elif choicer == 3:    #Allows the user to exit the software
        print("\nThank you for using our service. Have a nice day.")
        return sys.exit()
    else:
        print("\nPlease enter a valid choice.")  
        return MainMenu()   

if __name__ == '__main__':
    MainMenu()        #This calls the main function

