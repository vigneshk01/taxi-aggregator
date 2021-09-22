from user_simulator import User
import time
import json
from termcolor import colored


class UserSimulatorClient:

    def __init__(self):
        self._latest_error = ''
        self._origin=''
        self._destination=''
        self._otp = ''
        self._apiKey = ''
        self._User = User()
        self._user_id = ''
        self._book_again ='Yes'
        self. _start_ride= 1
        #self.user_simulator()
        self._booked_time=''
        self.ride_details=[]


    def Sign_Up(self):
        print('''
                    ===================
                      Sign up
                    ===================
                    ''')

        first_name = input(colored("Please enter your First Name: ", 'cyan'))
        last_name = input(colored("Please enter your Last Name: ", 'cyan'))

        response = User().passenger_signup(first_name, last_name)
        if response != 'None':
            print('Sign Up successful. Please sign in to book a taxi')
            return response
        else :
            print('Sign Up Unsuccessful. Please try again')



    def Sign_In(self):
        print(colored('''
                        ===================
                              Sign in 
                        ====================   
                        ''', 'magenta'))
        print("Enter Login Details:")

        while (self._apiKey  == ""):
            user_id = input(colored("UserName: ", 'cyan'))
            password = input(colored("Password: ", 'cyan'))
            res = User().passenger_login(user_id, password)
            #print(res)

            if res == None:
                print(colored("Invalid Login. Try again:", 'red'))
            else:
                print(colored("You have Logged in Successfully:", "green"))
                res_dict = json.loads(res)
                #print(res_dict)
                self._apiKey = res_dict['APIKey']
                self._user_id = user_id
                self.Book_Taxi()

    def Book_Taxi(self):
        print(colored('''
                      =======================
                       Initiating Taxi Booking
                      =======================   
                      ''', 'magenta'))
        if self._book_again.lower()=='yes':
            self._origin = input(colored("Enter Origin address: ", 'cyan'))
            self._destination = input(colored("Enter Destination address: ", 'cyan'))
            taxi_type_options = ["UTILITY", "DELUXE", "LUXURY", "ALL"]
            # Print out your options
            for i in range(len(taxi_type_options)):
                print(str(i + 1) + ":", taxi_type_options[i])
            result = "Noresult"
            # Take user input and get the corresponding item from the list
            while (result == "Noresult"):
                taxi_type = int(input(colored("Enter Taxi Type number: ", 'cyan')))
                if taxi_type in range(1, 5):
                    taxi_type = taxi_type_options[taxi_type - 1]
                    res = User().book_taxi(self._user_id, self._origin, self._destination, taxi_type)
                    #print(res)
                    if res == None:
                        print('Sorry. No rides available at this moment.Please try again with different taxi type')
                        retry= int(input(colored( "Sorry. No rides available at this moment.Do you want to try searching again?(yes/no):",'cyan')))
                        if retry.lower()!= "yes":
                            result = "Exit"
                            break

                    else:
                        self.ride_details = res
                        #print(self.ride_details)
                        print(colored('Please find the cost for closest available taxi', 'green'))
                        print(
                            ' '.join(["Taxi type: " + self.ride_details['vehicle_type'], "Cost: " + self.ride_details['cost']]))
                        self.Confirm_Taxi()
                        result = "Pass"
                else:
                    print(colored('Wrong Input. Please try again','red'))

    def Confirm_Taxi(self):
        confirm_booking = input(colored("Please confirm your booking with yes/no answer:", 'cyan'))
        if confirm_booking.lower() == 'yes':

            res, self._booked_time = User().book_taxi_confirm(self._user_id, self.ride_details['vehicle_num'], self._origin, self._destination, self.ride_details['vehicle_type'], self._apiKey)
            #print(res)
            if (res != None):
                print(colored('Your ride is confirmed. Please find the ride details below:', 'green'))
                res_dict = json.loads(res)

                Driver_Name = ' '.join([self.ride_details['firstname'], self.ride_details['lastname']])
                print(colored(' '.join(["Taxi Number: " + self.ride_details['vehicle_num'], "Driver Name: " + Driver_Name,
                                        "Taxi type: " + self.ride_details['vehicle_type'], "Cost: " + self.ride_details['cost']]),
                              'green'))
                self._otp = res_dict["OTP"]
                print(f'Please note:Your OTP to start the ride is  {colored(self._otp,"green")}')
                res = User().get_ride_details(self._apiKey, self._booked_time)

                wait_ride = 1
                while (wait_ride):
                    print(colored('''
                                                  ============================================
                                                             Waiting for the ride
                                                  ============================================   
                                                  ''', 'magenta'))
                    #origin_lat_lng, driver_lat_lng = User().get_taxi_curr_location(self._origin, self._otp, self.ride_details['vehicle_num'])
                    address, distance = User().get_taxi_curr_location(self._origin, self._otp,
                                                                                   self.ride_details['vehicle_num'])
                    print(
                        f'your driver is in {colored(address, "green")} and is {colored(format(distance, ".2f"), "green")} Km(s) away from your location')
                    if (distance <= 0.5):#if driver is less that half a Km away from location then start ride is enabled for the user
                        #time.sleep(10)
                        self.Start_Ride()
                        wait_ride = 0
                        break
                    else:
                        time.sleep(60)


                end_ride = 1
                while (end_ride):
                    print(colored('''
                                     ============================================
                                                Taxi Moving
                                     ============================================   
                                     ''', 'magenta'))
                   # destination_lat_lng, driver_lat_lng = User().get_taxi_curr_location(self._destination, self._otp, self.ride_details['vehicle_num'])
                    address,distance = User().get_taxi_curr_location(self._destination, self._otp, self.ride_details['vehicle_num'])
                    print(
                        f'you are in {colored(address, "green")} and are {colored(format(distance, ".2f"), "green")} Km(s) away from your Destination')
                    #trunc_destination_lat = "{: .2f}".format(destination_lat_lng['latitude'])
                    #trunc_driver_lat = "{: .2f}".format(driver_lat_lng['latitude'])
                    #print(trunc_destination_lat, trunc_driver_lat)
                    #if (trunc_destination_lat == trunc_driver_lat):
                    if (distance <= 0.5):#if passenger is less that half a Km away from destination then end ride is initiated for the user
                        print(colored("You have reached your destination. Hope you had a wonderful trip!", 'green'))
                        self.End_Ride()
                        print(colored('''
                                        ============================================
                                                   Ride has Ended
                                        ============================================   
                                        ''', 'magenta'))

                        end_ride = 0
                        break
                    else:
                        time.sleep(60)
            else:
                print(colored('Your ride is not confirmed. Please try booking the ride again:', 'red'))

        else:
            self.book_again = input(colored("Do you want to try searching for taxi again?(yes/no):", "cyan"))


    def Start_Ride(self):

            try:
                OTP = input(colored("Your ride has arrived.Please provide your OTP to start the ride: ", 'cyan'))
                if (OTP==self._otp):
                    res = User().start_ride(OTP, self.ride_details['vehicle_num'], self._origin, self._destination, self._apiKey)
                    #print(res)
                    if (res != None):
                        print(colored('''
                                      ============================================
                                                 Ride Started
                                      ============================================   
                                      ''', 'magenta'))
                        print(f'Your ride has started at"{res}". You can track your ride now. Happy Journey!!")')
                       # time.sleep(20)
                        res = User().get_ride_details(self._apiKey, self._booked_time)
                        #print(res)
                        #distance = res['total_distance']

                        #print(res)
                        #print(res['total_distance'])
                       # print(f'Your taxi is {distance} Km(s) away from you.)')
                    else:
                        print(colored("Sorry. we could not start your ride. Please try again later","red"))

                else:
                    print(colored("Invalid OTP. Try again:", 'red'))
            except Exception as err:
                self.End_Ride()


    def End_Ride(self):
        #res = User().get_ride_details(self._apiKey, self._booked_time)
        #res_json = res.json()
        #print(res)
        #print(res['total_distance'])
        #print(f'Your taxi is {res["total_distance"]} Km(s) away from you and will reach your location in short time)')
        res = User().end_ride(self._otp, self.ride_details['vehicle_num'], self._apiKey)

        feedback = input(colored("would you like to give your feedback(yes/no)? ", 'cyan'))
        if feedback == "yes":
            rating_options = ["Very happy", "Happy", "Neutral", "Unhappy", "Very Unhappy"]
            j = 5
            # Print out your options
            for i in range(len(rating_options)):
                print(str(j) + ":", rating_options[i])
                j -= 1
            rating = input(colored("On a scale of 1 to 5 ,how would you like to rate your trip ? ","cyan"))
            comments = input(colored("Please provide your comments here: ","cyan"))

            res = User().feedback(self._otp, self._apiKey, comments, rating)
            if (res != None):
                print(colored("Thank you for your feedback","green"))




def user_simulator():

    print(colored('''
           =======================
               Sign Up/ Sign In
           =======================   
           ''', 'magenta'))
    Sign_in_Options = ["Sign Up", "Sign In"]

    # Print out your options
    for i in range(len(Sign_in_Options)):
        print(str(i + 1) + ":", Sign_in_Options[i])
    result = "Noresult"
    # Take user input and get the corresponding item from the list
    while (result == "Noresult"):
        inp = int(input(colored("enter Sign Up / Sign In option number ", 'cyan')))
        if inp in range(1, 3):
            inp = Sign_in_Options[inp - 1]
            result = "Pass"
            if (inp == "Sign Up"):
                UserSimulatorClient().Sign_Up()
                UserSimulatorClient().Sign_In()
            else:
                UserSimulatorClient().Sign_In()
        else:
            print(colored("Invalid input. Try again!", 'red'))


if __name__ == "__main__":

    user_simulator()







