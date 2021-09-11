from UserSimulation import User
import time



class UserSimulatorClient:
    print('''===================
            Sign up Process
            ====================   
    ''')

    first_name = input("First Name: ")
    last_name = input("Last Name: ")

    Apikey = User().passenger_signup(first_name, last_name)

    if (Apikey != ""):
        print("Login Successful:")

    else:
        print("Invalid Login. Try again:")

    Scenario_Options = ["Regular", "Rush Hour", "Special Event"]

    # Print out your options
    for i in range(len(Scenario_Options)):
        print(str(i + 1) + ":", Scenario_Options[i])
    result = "Noresult"
    # Take user input and get the corresponding item from the list
    while (result == "Noresult"):
        inp = int(input("Enter scenario number: "))
        if inp in range(1, 4):
            inp = Scenario_Options[inp - 1]
            result = "Pass"
        else:
            print("Invalid input. Try again!")
    if (inp == "Regular"):
        print("Enter Login Details:")
        Apikey=""
        while(Apikey==""):
            user_id= input("UserName: ")
            password = input("Password: ")
            Apikey = User().passenger_login(user_id,password)

            if (Apikey !=""):
                print("Login Successful:")

            else:
                print("Invalid Login. Try again:")

        Origin = input("Enter Origin address: ")
        Destination = input("Enter Destination address: ")
        taxi_type_options = ["Utility", "Deluxe", "Luxury", "All"]

        # Print out your options
        for i in range(len(taxi_type_options)):
            print(str(i + 1) + ":", taxi_type_options[i])
        result = "Noresult"
        # Take user input and get the corresponding item from the list
        while (result == "Noresult"):
            inp = int(input("Enter Taxi Type number: "))
            if inp in range(1, 5):
                inp = taxi_type_options[inp - 1]
                res = User().book_taxi( user_id, Origin, Destination, inp)
                print(res)
                if (res != ""):
                    print("Login Successful:")

                else:
                    print("Invalid Login. Try again:")
                result = "Pass"
            else:
                print("Invalid input. Try again!")



