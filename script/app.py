# Module List
import requests
import sys
import json
import hashlib
from datetime import datetime
from configparser import ConfigParser

"""
References:
Co-WIN Public APIs
https://apisetu.gov.in/public/marketplace/api/cowin/cowin-public-v2


Exit Codes:-
1 - Error for Request to receive OTP
2 - Error for Request to authneticate with recived OTP
3 - Error for Request to get slots for the next 5 days
4 - Error for Request to Telegram to pass notification
"""


# Functions

def authentication():
    """
    Connect's to CoWin User Authentication APIs to Authenticate a beneficiary by Mobile/OTP and Confirm mobile OTP for authentication
    This function requires the OTP as an interative input by the user.

    Request 1: Passes RMN to generate OTP
    Request 2: Passes OTP as SHA256 Hash along with txnId from Request 1
    """


    url = "https://cdn-api.co-vin.in/api/v2/auth/public/generateOTP"
    payload = {"mobile": ""}
    payload.update(mobile = rmn )
    headers = {"Content-Type": "application/json"}
    response = requests.request("POST", url, json=payload, headers=headers) # Request 1
    if response.status_code == 200: 
        json_data = json.loads(response.text)
        txnId = json_data['txnId']
    else:
        print ("Request Failed")
        sys.exit(1)

    OTPfromuser = input("Enter OTP: ")
    OTPhash = hashlib.sha256(OTPfromuser.encode()).hexdigest()

    url = "https://cdn-api.co-vin.in/api/v2/auth/public/confirmOTP"
    payload = {
        "otp": "",
        "txnId": ""
    }
    payload.update(otp = OTPhash , txnId = txnId)
    headers = {"Content-Type": "application/json"}
    response = requests.request("POST", url, json=payload, headers=headers) # Request 2
    if response.status_code == 200:
        print (response.text)
    else:
        print ("Request Failed")
        sys.exit(2)
    # authentication Ends



def calendarByPin(pin):
    """
    Connect's to CoWin Appointment Availability APIs to Get vaccination sessions by PIN for 7 days

    Request 3: Passes pincode and todays date in DD-MM-YYYY
    """


    url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin"
    todayDate = datetime.today().strftime('%d-%m-%Y')
    querystring = {"pincode":"","date":""}
    querystring.update(pincode = pin , date = todayDate)
    payload = ""
    headers = {"Accept-Language": "hi_IN", "user-agent": "insomnia/2021.2.2"}
    response = requests.request("GET", url, data=payload, headers=headers, params=querystring) # Request 3
    if response.status_code == 200:
        global rawDataResponse
        rawDataResponse = json.loads(response.text)
    else:
        print ("Request Failed")
        sys.exit(3)
    # calendarByPin Ends


def analysis():
    """
    Filters out the JSON response from Request 3 based on
    slotsMinAge > 18
    slotsAvailableCapacity > 0
    """
    
    centerList = rawDataResponse['centers']
    for centers in centerList:
        #centerName = centers['name']
        centerSessions = centers['sessions']
        for slots in centerSessions:
            slotsAvailableCapacity = slots['available_capacity_dose1']
            slotsMinAge = slots['min_age_limit']
            slotsDate = slots['date']
            districtName=centers['district_name']
            pinCode=centers['pincode']
            blockName=centers['block_name']
            vaccine=slots['vaccine']
            if slotsMinAge == 18 and slotsAvailableCapacity != 0:
            #if slotsMinAge == 18 and slotsAvailableCapacity == 0:
                #msgtemplate=" Vaccination Slot Alert ...\n\nDate           : *{0}*\nDistrict      : *{1}*\nPincode    : *{2}*\nName         : *{3}*\nVaccine     : *{4}*\nSlotCount: *{5}*\n[Click here to Register](https://selfregistration.cowin.gov.in/)\n\nStay Safe Good Luck".format(slotsDate, districtName, pinCode, blockName, vaccine, slotsAvailableCapacity)
                ifFoundSlot=True
                msgtemplate="""
Vaccination Slot Alert ...
Date           : *{0}*
District      : *{1}*
Pincode    : *{2}*
Name         : *{3}*
Vaccine     : *{4}*
SlotCount: *{5}*\n
[Click here to Register](https://selfregistration.cowin.gov.in/)\n
Stay Safe Good Luck""".format(slotsDate, districtName, pinCode, blockName, vaccine, slotsAvailableCapacity)
                telegramMsg(msgtemplate)
        #End
    # analysis Ends


def telegramMsg(MessageToPost):
    """
    Post notification to end user via telegram group as a Bot.

    Request 4: Passes metadata of valid slots from analysis along with Telegram Bot token and Group chatID  
    """
    token=parser.get('PROD', 'token')
    chatId=parser.get('PROD', 'chatId')
    baseurl = 'https://api.telegram.org/bot{0}/sendMessage?chat_id={1}&text={2}&parse_mode=Markdown'.format(token, chatId, MessageToPost)
    response = requests.get(baseurl) # Request 4
    if response.status_code != 200:
        print ("Request Failed")
        sys.exit(4)
    # telegramMsg Ends


def telegramMsgAck():
    """
    Post notification to developer about PROD run.

    Request 5: Passes metadata of run along with Telegram Bot token and Group chatID  
    """
    token=parser.get('DEV', 'token')
    chatId=parser.get('DEV', 'chatId')
    MessageToPost="""
PROD Batch run at: {0}
Slots Found: {1}
""".format(datetime.today().strftime('%d-%m-%Y:%H:%M:%S'), ifFoundSlot)
    #MessageToPost='PROD Batch run at {0}'.format(datetime.today().strftime('%d-%m-%Y:%H:%M:%S'))
    baseurl = 'https://api.telegram.org/bot{0}/sendMessage?chat_id={1}&text={2}&parse_mode=Markdown&disable_notification=True'.format(token, chatId, MessageToPost)
    response = requests.get(baseurl) # Request 5
    if response.status_code != 200:
        print ("Request Failed")
        sys.exit(5)
    # telegramMsgAck Ends


# Main Function

def main():
    # sys.exit(0)
    #authentication() # User requires authentication for Co-WIN Protected APIs; For public API this is not required.

    # Read Configuration file
    global rmn, parser, ifFoundSlot
    parser = ConfigParser()
    parser.read('config.ini')
    ifFoundSlot=False

    # Define global variables 
    #global rmn, token, chatId
    

    rmn = parser.get('DEFAULT', 'mobileNumber')
    # Configure Telegram notification group between DEV / PROD 
    # if parser.get('DEFAULT', 'testing'):  
    #     token=parser.get('DEV', 'token')
    #     chatId=parser.get('DEV', 'chatId')
    # else:
    #     token=parser.get('PROD', 'token')
    #     chatId=parser.get('PROD', 'chatId')

    #telegramMsgAck()
    
    pincodeList=json.loads(parser.get('DEFAULT', 'pincodeList'))
    for pincode in pincodeList:
        print("Searching for Pincode : ", pincode)
        calendarByPin(pincode)
        analysis()
    
    telegramMsgAck()
# Main Ends

    

# Main Script

if __name__ == "__main__":
    main()

