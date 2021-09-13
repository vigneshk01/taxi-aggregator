from UserSimulation import User
import time
import json



class UserSimulatorClient:




    print('''
        =======================
            Confirm Scenario
        =======================   
        ''')
    Scenario_Options = ["Regular", "Rush Hour", "Special Event"]

    # Print out your options
    for i in range(len(Scenario_Options)):
        print(str(i + 1) + ":", Scenario_Options[i])
    result = "Noresult"
    # Take user input and get the corresponding item from the list
    while (result == "Noresult"):
        inp = int(input("Enter scenario option number: "))
        if inp in range(1, 4):
            inp = Scenario_Options[inp - 1]
            result = "Pass"
        else:
            print("Invalid input. Try again!")
    if (inp == "Regular"):
        print('''
                ===================
                      Sign in 
                ====================   
                ''')
        print("Enter Login Details:")
        Apikey=""
        while(Apikey==""):
            user_id = input("UserName: ")
            password = input("Password: ")
            res = User().passenger_login(user_id,password)
            print(res)

            if res ==None:
                print("Invalid Login. Try again:")
            else:
                print("Login Successful:")
                res_dict = json.loads(res)
                Apikey = res_dict['APIKey']


        print('''
                        =======================
                         Initiate Taxi Booking
                        =======================   
                        ''')
        Origin = input("Enter Origin address: ")
        Destination = input("Enter Destination address: ")
        taxi_type_options = ["UTILITY", "DELUXE", "LUXURY", "ALL"]

        # Print out your options
        for i in range(len(taxi_type_options)):
            print(str(i + 1) + ":", taxi_type_options[i])
        result = "Noresult"
        # Take user input and get the corresponding item from the list
        while (result == "Noresult"):
            taxi_type = int(input("Enter Taxi Type number: "))
            if taxi_type in range(1, 5):
                taxi_type = taxi_type_options[taxi_type - 1]
                res = User().book_taxi( user_id, Origin, Destination, taxi_type)

                print(res_dict)
                if res == None:
                    print('Sorry. No rides available at this moment.Please try again later')
                    exit()
                else :
                    res_dict = json.loads(res)
                    print(res_dict)
                    print('Please find the cost for closest available taxi')
                    print(' '.join(["Taxi type: "+res_dict['vehicle_type'], "Cost: "+res_dict['cost']]))

                #confirm_booking= input("Please confirm your booking with yes/no:")

                    taxi_num = res_dict['vehicle_num']
                    res = User().book_taxi_confirm(user_id, taxi_num, Origin, Destination, taxi_type, Apikey)
                    if (res != None):
                        print(res)
                        res_dict = json.loads(res)
                        OTP = res_dict["OTP"]
                        result == "Pass"
                        print(f'Please note:Your OTP to start the ride is  {OTP}')
                        print('''
                                                   ============================================
                                                              Checking taxi location
                                                   ============================================   
                                                   ''')

                        countdown =1
                        check_taxi =1
                        while check_taxi:
                            while countdown:
                                mins, secs = divmod(10, 60)
                                timer = '{:02d}:{:02d}'.format(mins, secs)
                                print(timer, end="\r")
                                time.sleep(10)
                                countdown -= 1
                                if countdown == 0:
                                    res,distance = User().get_taxi_curr_location(Origin, OTP, taxi_num)
                                    print(res)
                                    print(f'your driver is in {res} and is {format(distance, ".2f")} Km(s) away from your location')

                                    if (distance <= 0.5):
                                        start_ride = 1
                                        check_taxi = 0
                                        while(start_ride):
                                            OTP = input("Your ride has arrived.Please provide your OTP: ")
                                            res = User().start_ride(OTP, taxi_num, Origin, Destination, Apikey)
                                            print(res)
                                            if (res != None):
                                                print("Your ride has started. You can track your ride now")
                                                start_ride = 0

                                            else:
                                                print("Invalid OTP. Try again:")
                                    else:
                                        countdown = 1
                    else:
                        print("Invalid Login. Try again:")

            else:
                print("Invalid input. Try again!")

