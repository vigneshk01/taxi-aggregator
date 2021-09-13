import random
import string

class transcation:
    txnid =""
    SALT=""
    merchantKey=""

    def __init__(self):
        self.txnid = 'abcdef123R'
        self.SALT ='yoursaltkeyvalue'
        self.merchantKey ='your merchant key'



    
    def random_string(self,letter_count, digit_count):  
        str1 = ''.join((random.choice(string.ascii_letters) for x in range(letter_count)))  
        str1 += ''.join((random.choice(string.digits) for x in range(digit_count)))  
    
        sam_list = list(str1) # it converts the string to list.  
        random.shuffle(sam_list) # It uses a random.shuffle() function to shuffle the string.  
        final_string = ''.join(sam_list)  

        self.txnid = final_string
        

    
    def getTXNid(self):
        return  self.txnid

    def getSALT(self):
        return self.SALT

    def getmerchantKey(self):
        return self.merchantKey

