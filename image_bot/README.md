## HOW TO RUN THE BOT


## MY STEPS TAKEN

- Download folder

- install the requirements using pip and python(3)?

    navigate to folder on terminal
    
    pip install -r requirements.txt
                or
    pip3 install -r requirements.txt
    
    Create a page on Facebook
    
   create an app here https://developers.facebook.com/quickstarts/
   
   Head over to add product, select messenger
   
   Open messengers settings and select your previously selected page to generate a page token
   
   Create a verify token that can be any string eg 'my_verify_token'
   
   Place your page and verify tokens at their respective variables in main.py
   
  ` FB_PAGE_TOKEN = 'YOUR_FB_PAGE_TOKEN'
   FB_VERIFY_TOKEN = 'YOUR_FB_VERIFY_TOKEN'`
   
   You can now host your bot or test it locally using [ngrok](https://ngrok.com/)
   
   To activate your bot create a link like the one below after hosting it:
   
   ` https://<YOUR_DOMAIN>/webhook?hub.verify_token=<YOUR_FB_VERIFY_TOKEN>&init=true`
   
   This is what mine looks like:
   
   `https://2d3c7d34.ngrok.io/webhook?hub.verify_token=my_verify_token&init=true`
   
   Once your bot has been activated, scroll down to webhooks add the url below:
   
   `https://<YOUR_DOMAIN>/webhook`
   
   this is what mine looks like:
   
   `https://2d3c7d34.ngrok.io/webhook`
   
   Below that add your verify fb token
   
   `my_verify_token`
   
   Then select the messeges events.
   
   Once thats done, select your recently created page and subscribe to it.
   
   
   
   
   
   go to your created facebook page, click on add a button
   select get in touch then add the send message button.
   
   To send a message, hover on the send message button and click test button
   



## GENERIC STEPS

### Setting
```
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

### Edit config.py
```
CONFIG = {
    'FACEBOOK_TOKEN': 'YOUR_FACEBOOK_TOKEN',
    'VERIFY_TOKEN': 'YOUR_VERIFY_TOKEN',
    'SERVER_URL': 'https://YOUR_HOSTNAME'
}
```

### Run
```
python server.py

# default web server port 8080
```


<a name="facebook-app-setup"></a>
### Facebook app setup

- [Create a page](https://www.facebook.com/pages/create/) for your app, if you don't already have one
- [Create an app](https://developers.facebook.com/quickstarts/?platform=web)
- Add the Messenger product
- Select the Page to generate a page token


