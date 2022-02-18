# CowinSlotNotification

Helped family and friends to get notification of Covid Vaccination slot on Telegram for their preferred PIN code.


<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#About">About</a></li>
    <li><a href="#Tech">Tech</a></li>
    <li><a href="#Configure">Configure</a></li>
    <li><a href="#Run">Run</a></li>
    <li><a href="#Screenshots">Screenshots</a></li>
  </ol>
</details>


## About

Script connects to [Cowin Public API](https://apisetu.gov.in/public/api/cowin/cowin-public-v2), using API call gets the data for vaccination sessions by PIN for 7 days, the JSON response is filtered by slot count great than zero and for ages 18+.



## Tech

1. Python, request module, list, dictonary
2. API Request
3. Cronjob
4. Docker


## Configure

1. Create a TelegramBot [Reference](https://core.telegram.org/bots/)
2. Keep Bot token handy and secure
3. Create a telegram group along with the Bot as an added member
4. Get the chat id of the group using 
`https://api.telegram.org/bot<bot_api_token>/getUpdates`
5. Update the script/config.ini with
    1. Pincode to search as a Python list
    2. Update Bot Token and Chat ID under the resp groups.
sectionsDEV to alert incase on batch run, PROD actual valid slot alter to indented users. 


**Sample:**

> Bot Token: 1883695143:AAGjKoFU7lSBMjcwo-KAjn-rwgsJuwKgJH6s
>
> Chat ID: -529186364



## Run

1. Schedule a Cronjob

```shell
$ crontab -l
* * * * * /Users/anku/sandbox/CoWin/CoWin_Wrapper.bash
```

2. Docker Container
```shell
docker build -t cowin:latest .

docker run cowin
```



## Screenshots:

![Alert](images/CoWin-Notification.jpeg =250x250)
