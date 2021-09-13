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
                         Initiating Taxi Booking
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
                    result == "Noresult"
                else :
                    result == "Pass"
                    ride_details = json.loads(res)
                    print(res_dict)
                    print('Please find the cost for closest available taxi')
                    print(' '.join(["Taxi type: "+ride_details['vehicle_type'], "Cost: "+ride_details['cost']]))

                    confirm_booking = input("Please confirm your booking with yes/no answer:")
                    if confirm_booking.lower() =='yes':
                        taxi_num = res_dict['vehicle_num']
                        res = User().book_taxi_confirm(user_id, taxi_num, Origin, Destination, taxi_type, Apikey)
                        if (res != None):
                            print(f'Your ride is confirmed. Please find the ride details below:')
                            res_dict = json.loads(res)
                            OTP = res_dict["OTP"]
                            print(f'Please note:Your OTP to start the ride is  {OTP}')
                            Driver_Name = ' '.join([ride_details['firstname'],ride_details['lastname']])
                            print(' '.join(["Taxi Number: " + ride_details['vehicle_num'], "Driver Name: " + Driver_Name, "Taxi type: " + ride_details['vehicle_type'], "Cost: " + ride_details['cost']]))
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
                                                    print('''
                                                          ============================================
                                                                     Ride Started
                                                          ============================================   
                                                          ''')
                                                    print(f"Your ride has started at {res}. You can track your ride now. Happy Journey!!")
                                                    start_ride = 0

                                                else:
                                                    print("Invalid OTP. Try again:")
                                        else:
                                            countdown = 1
                                        countdown = 1
                                        check_taxi = 1
                                        while check_taxi:
                                            while countdown:
                                                mins, secs = divmod(10, 60)
                                                timer = '{:02d}:{:02d}'.format(mins, secs)
                                                print(timer, end="\r")
                                                time.sleep(10)
                                                countdown -= 1
                                                if countdown == 0:
                                                    res, distance = User().get_taxi_curr_location(Destination, OTP, taxi_num)
                                                    print(res)
                                                    print(
                                                        f'you are in {res} and are {format(distance, ".2f")} Km(s) away from your Destination')

                                                    if (distance <= 0.5):
                                                        print('''
                                                             ============================================
                                                                        Ride Ended
                                                             ============================================   
                                                             ''')
                                                        print("You have reached your destination. Hope you had a wonderful trip!")
                                                        check_taxi = 0
                                                        feedback = input("would you like to give your feedback?(yes/no) ")
                                                        if feedback=="yes":
                                                            rating_options = ["Very happy", "Happy", "Neutral", "Unhappy","Very Unhappy"]
                                                            j=5
                                                            # Print out your options
                                                            for i in range(len(taxi_type_options)):
                                                                print(str(j) + ":", taxi_type_options[i])
                                                                j-=1
                                                            rating = input("On a scale of 1 to 5 ,how would you like to rate your trip ? ")
                                                            comments= input("Please provide your comments here: ")

                                                            res = User().feedback(OTP, taxi_num, Origin, Destination,
                                                                                Apikey)
                                                            if (res != None):
                                                                print("Thank you for your feedback")
                                                                exit()

                                                            else:
                                                                exit()
                                                        else:
                                                            exit()


                                                    else:
                                                        countdown=1
                        else:
                            print("Invalid Login. Try again:")
            else:
                print("Invalid Login. Try again:")

        else:
            print("Invalid input. Try again!")

