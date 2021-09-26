###########################################################################################################
#This function captures Client actions for Passenger Simulation
###########################################################################################################
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
        self._booked_time=''
        self.ride_details=[]


    def Sign_Up(self):
        print(colored('''
                                        ===================
                                              Sign up
                                        ===================
                    ''','magenta',attrs=['bold']))

        first_name = input(colored("Please enter your First Name: ", 'cyan'))
        last_name = input(colored("Please enter your Last Name: ", 'cyan'))

        response = User().passenger_signup(first_name, last_name)
        if response != 'None':
            print(colored(f'''\nSign Up successful. Please find your login details below
Username: {response['UserName']}, Password:{response['Password']}\n
''',"green"))
            return response
        else :
            print(colored('\nSign Up Unsuccessful. Please try again','red'))



    def Sign_In(self):
        try:
            print(colored('''
                                        ===================
                                              Sign in 
                                        ===================  
                            ''', 'magenta',attrs=['bold']))
            print(colored("Enter Login Details:\n","green"))
            count=3

            while (self._apiKey  == "" and count>0):

                user_id = input(colored("UserName: ", 'cyan',attrs=['bold']))
                password = input(colored("Password: ", 'cyan',attrs=['bold']))
                res = User().passenger_login(user_id, password)
                #print(res)

                if res == None:
                    print(colored("\nInvalid Login. Try again:", 'red'))
                    count-=1
                else:
                    print(colored("\nYou have Logged in Successfully:", "green"))
                    res_dict = json.loads(res)
                    #print(res_dict)
                    self._apiKey = res_dict['APIKey']
                    self._user_id = user_id
                    self.Book_Taxi()
        except Exception as err:
            print(colored("\nInvalid Input. Try again later:", 'red'))

    def Book_Taxi(self):
        print(colored('''
                                        ============================
                                          Initiating Taxi Booking
                                        ============================   
                      ''', 'magenta',attrs=['bold']))
        while(self._book_again.lower() =='yes'):
            print(colored('\nNote: Address and lat,long formats accepted in Origin and Destination','magenta',attrs=['bold']))
            self._origin = input(colored("Origin: ", 'cyan'))
            self._destination = input(colored("Destination: ", 'cyan'))
            taxi_type_options = ["UTILITY", "DELUXE", "LUXURY", "ALL"]
            # Print out your options
            for i in range(len(taxi_type_options)):
                print(str(i + 1) + ":", taxi_type_options[i])
            result = "Noresult"
            # Take user input and get the corresponding item from the list
            book_taxi_retry = 3# if no rides available user can retry two more times for different taxi type
            while (result == "Noresult" and book_taxi_retry>0):
                taxi_type = int(input(colored("Enter Taxi Type number: ", 'cyan')))
                if taxi_type in range(1, 5):
                    taxi_type = taxi_type_options[taxi_type - 1]
                    res = User().book_taxi(self._user_id, self._origin, self._destination, taxi_type)

                    if res == None:
                        print('\nSorry. No rides available at this moment.Please try again with different taxi type')
                        book_taxi_retry -=1

                    else:
                        self._book_again ='no'
                        book_taxi_retry = 0
                        self.ride_details = res
                        #print(res)
                        print(colored('\nPlease find the cost for closest available taxi', 'green'))
                        print(
                            ' '.join(["Taxi type: " + self.ride_details['vehicle_type'], "Cost: " + self.ride_details['cost']]))
                        self.Confirm_Taxi()
                        result = "Pass"
                else:
                    print(colored('\nWrong Input. Please try again','red'))
            if result != "Pass":
                self._book_again = input(
                    colored("\nSorry. No rides available at this moment.Do you want to try searching again?(yes/no):", 'cyan'))



    def Confirm_Taxi(self):
        try:

            confirm_booking = input(colored("\nWould you like to confirm this booking?(yes/no) :", 'cyan'))
            if confirm_booking.lower() == 'yes':

                res, self._booked_time = User().book_taxi_confirm(self._user_id, self.ride_details['vehicle_num'], self._origin, self._destination, self.ride_details['vehicle_type'], self._apiKey)
                #print(res)
                if (res != None):
                    print(colored('\nYour ride is confirmed. Please find the ride details below:', 'green'))
                    res_dict = json.loads(res)

                    Driver_Name = ' '.join([self.ride_details['firstname'], self.ride_details['lastname']])
                    print(colored(' '.join(["Taxi Number: " + self.ride_details['vehicle_num'], "Driver Name: " + Driver_Name,
                                            "Taxi type: " + self.ride_details['vehicle_type'], "Cost: " + self.ride_details['cost']]),
                                  'green'))
                    self._otp = res_dict["OTP"]
                    print(f'\nPlease note:Your OTP to start the ride is  {colored(self._otp,"green")}')
                    res = User().get_ride_details(self._apiKey, self._booked_time)

                    wait_ride = 1
                    while (wait_ride):
                        print(colored('''
                                ============================================
                                         Waiting for the ride
                                ============================================   
                                                      ''', 'magenta',attrs=['bold']))

                        address, distance = User().get_taxi_curr_location(self._origin, self._otp,
                                                                                       self.ride_details['vehicle_num'])
                        print(
                            f'your driver is in {colored(address, "green",attrs=["bold"])} and is {colored(format(distance, ".2f"), "green",attrs=["bold"])} Km(s) away from your location')
                        if (distance < 0.1):#if driver is less than 100 meters away from location then start ride is enabled for the user
                            #time.sleep(10)
                            self.Start_Ride()
                            wait_ride = 0
                            break
                        else:
                            time.sleep(60)#wait for a min before checking for current location of the taxi again


                    end_ride = 1
                    while (end_ride):
                        print(colored('''
                                ============================================
                                        Taxi Moving
                                ============================================   
                                         ''', 'magenta',attrs=['bold']))

                        address,distance = User().get_taxi_curr_location(self._destination, self._otp, self.ride_details['vehicle_num'])
                        print(
                            f'you are in {colored(address, "magenta",attrs=["bold"])} and are {colored(format(distance, ".2f"), "magenta",attrs=["bold"])} Km(s) away from your Destination')

                        if (distance < 0.10):#if passenger is less than 100 meters away from destination then end ride is initiated for the user
                            print(colored("\nYou have reached your destination. Hope you had a wonderful trip!", 'green'))
                            error = "no" # confirming ride was successful without error
                            self.End_Ride(error)
                            print(colored('''
                                ============================================
                                           Ride has Ended
                                ============================================   
                                            ''', 'magenta',attrs=['bold']))

                            end_ride = 0
                            break
                        else:
                            time.sleep(60)#wait for a min before checking for current location of the taxi again
                else:
                    print(colored('\nYour ride is not confirmed. Please try booking the ride again:', 'red'))

            else:
                self._book_again = input(colored("\nDo you want to try searching for taxi again?(yes/no):", "cyan"))


        except Exception as err:
            error ="yes"
            self.End_Ride(error)
            print(colored('''
                                            ============================================
                                                       Ride not confirmed
                                            ============================================   
                                                        ''', 'magenta',attrs=['bold']))

    def Start_Ride(self):

            try:
                count = 3 # to retry OTP entry 3 times in case of wrong entry
                while (count > 0):
                    OTP = input(colored("\nYour ride has arrived.Please provide your OTP to start the ride: ", 'cyan'))


                    if (OTP==self._otp):
                        res = User().start_ride(OTP, self.ride_details['vehicle_num'], self._origin, self._destination, self._apiKey)
                        #print(res)
                        if (res != None):
                            print(colored('''
                                ============================================
                                                Ride Started
                                ============================================   
                                          ''', 'magenta',attrs=['bold']))
                            print(colored(f'\nYour ride has started at{res}. You can track your ride now. Happy Journey!!','green'))

                            res = User().get_ride_details(self._apiKey, self._booked_time)
                            count=0

                        else:
                            print(colored("\nSorry. we could not start your ride. Please try again later","red"))
                            count =0
                            break
                    else:
                        count -= 1
                        print(colored(f"\nInvalid OTP. {count} more attempts left. Try again:", 'red'))


            except Exception as err:
                error = "yes"
                self.End_Ride(error)
                print("Ride ended due to an error. Sorry for the inconvenience")

    def End_Ride(self, err):
        res = User().end_ride(self._otp, self.ride_details['vehicle_num'], self._apiKey)
        if err =="no":
            feedback = input(colored("\nwould you like to give your feedback(yes/no)? ", 'cyan'))
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
                    print(colored("\nThank you for your feedback","green",attrs=['bold']))




def user_simulator():
    try:
        print(colored('''
                                        =======================
                                           Sign Up/ Sign In
                                        =======================   
               ''', 'magenta',attrs=['bold']))
        Sign_in_Options = ["Sign Up", "Sign In"]

        # Print out your options
        for i in range(len(Sign_in_Options)):
            print(str(i + 1) + ":", Sign_in_Options[i])
        result = "Noresult"
        # Take user input and get the corresponding item from the list
        while (result == "Noresult"):
            inp = int(input(colored("Enter Sign Up/Sign In option number ", 'cyan')))

            if int(inp) in range(1, 3):
                inp = Sign_in_Options[inp - 1]
                result = "Pass"
                if (inp == "Sign Up"):
                    UserSimulatorClient().Sign_Up()
                    book_taxi = input(colored("Would you like to book a taxi (yes/no)?", 'cyan'))
                    if book_taxi.lower() =="yes":
                        UserSimulatorClient().Sign_In()
                else:
                    UserSimulatorClient().Sign_In()
            else:
                print(colored("\nInvalid input. Try again!", 'red'))

    except Exception as err:
        print(colored("\nInvalid input. Try again later!", 'red'))
if __name__ == "__main__":

    user_simulator()







