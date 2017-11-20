Shopping Bot Template
====================

A simple Shopping Bot template running on Flask that's ready to run on Heroku.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/anthonymiyoro/shopping_bot_example)

## INSTRUCTION TEXT FOR WEBSITE


### FACEBOOK SETUP

1. Set up a facebook [page](https://www.facebook.com/pages/create/).

2. Go to the Facebook Developer’s Quickstart Page and click “Skip and Create App ID” at the top right. Then create a new Facebook App for your bot and give your app a name, category and contact email.
    
	![create-fb-app](https://blog.hartleybrody.com/wp-content/uploads/2016/06/create-fb-app-1024x604.png "")
    
    You’ll see your new App ID at the top right on the next page. Scroll down and click “Get Started” next to Messenger.
    
    ![setup-fb-messenger-app](https://blog.hartleybrody.com/wp-content/uploads/2016/06/setup-fb-messenger-app-1024x613.png "")


3. Now you’re in the Messenger settings for your Facebook App. There are a few things in here you’ll need to fill out in order to get your chatbot wired up to the Heroku endpoint we setup earlier.

	![setup-fb-messenger-app](https://blog.hartleybrody.com/wp-content/uploads/2016/06/page-access-token-generation-1024x346.png "")
    
    Using the Page you created earlier (or an existing Page), click through the auth flow and you’ll receive a Page Access Token for your app.
        
	Click on the Page Access Token to copy it to your clipboard. 
   
4. Paste the page access token into its field in the config.py file.

5. Head over to Messenger under products in you projects facebook developer page and click on settings. Navigate to the webhooks section, click on edit events and select messages and messaging_postbacks as shown below.
	
	![fb-events](https://github.com/anthonymiyoro/Bot-Builder-Site/blob/master/images/events.png "")



### NGROK SETUP

1. Download your desired bot template from the website

2. Dowload ngrok from their [page](https://ngrok.com/download).

3. On Linux or OSX you can unzip ngrok from a terminal with the following command. 

	```
	unzip /path/to/ngrok.zip

	```
	On Windows, just double click ngrok.zip.

4. Navigate to the folder containing the unzipped contents of ngrock and run it with the command ./ngrok . You should see something similar to the image below on your terminal.

5. Copy and replace the facebook token and server url in the config.py file and replace FACEBOOK_TOKEN_HERE with the facebook page token selected as in the instructions above and SERVER_URL_HERE with the url displayed after running ngrok:

	```
	CONFIG = {
     'FACEBOOK_TOKEN': 'FACEBOOK_TOKEN_HERE',
     'VERIFY_TOKEN': 'my_verify_token',
     'SERVER_URL': 'SERVER_URL_HERE'
 	}

	```

6. Run your bot by running python server.py after saving your changes to the server.py file. 

7. Head over to your apps page on the Facebook for Developers site and under products, select webhooks.

	![URL subscription](https://github.com/anthonymiyoro/Bot-Builder-Site/blob/master/images/subscription.png "")

	Once selected click on edit subscription and copy your https url (as shown below) from ngrock in your terminal to the Callback URL section followed by /webhook. 
	
	![ngrok](https://cdn-images-1.medium.com/max/1600/1*LtnvanCk2-ZVJY1kA0cMfQ.png "")
	
	According to the image above, our callback url will be 

	```
	https://bd2cb171.ngrok.io/webhook

	```
	Under the Verify Token field of the page subscription, add 
	```
	my_verify_token

	```
	as seen in the config.py file. 
	
	![Webhook](https://github.com/anthonymiyoro/Bot-Builder-Site/blob/master/images/webhook.png "")
	
	You can then click on the verify and save button to save the webhook.


### HEROKU INSTRUCTIONS

After clicking the click to deploy buttons below, your selected template will be hosted and deployed ontu Heroku automatically. The only issue is that the config.py file does not contain your specific Facebook page keys and server url.

To fix this, follow the following steps;

1. Dowload the heroku CLI from [here](https://devcenter.heroku.com/articles/heroku-cli). 

2. Once heroku has been installed, open the heroku [dashboard](https://dashboard.heroku.com/apps).
Select your newly created app and navigate to the deploy section as shown in the images below.

![Overview](https://github.com/anthonymiyoro/Bot-Builder-Site/blob/master/images/overview.png "").


![Deploy](https://github.com/anthonymiyoro/Bot-Builder-Site/blob/master/images/deploy.png "")

3. Run the code indicated in the image below to get a copy of your bot template and navigate to its folder in your terminal.

![Run](https://github.com/anthonymiyoro/Bot-Builder-Site/blob/master/images/install-amended.png "")


4. Open your config.py file and fill in the required variables replacing FACEBOOK_TOKEN_HERE with you facebook app pages' token and SERVER_URL_HERE with the url of your newly created heroku server.

The config.py file should look like the snippet below:

	```
	CONFIG = {
     'FACEBOOK_TOKEN': 'FACEBOOK_TOKEN_HERE',
     'VERIFY_TOKEN': 'my_verify_token',
     'SERVER_URL': 'SERVER_URL_HERE'
 	}

	```

When filled, it should look like the snippet below:

	```
	CONFIG = {
     'FACEBOOK_TOKEN': 'EAAHUC2GIMSoZAioyW4orexO9tCCHvdCCnC2GIMSoZAioyW4orexO9tCCHvdCC2GIMSoZAioyW4orexO9tCCHvdCLF1mFlnqC2GIMSoZAioyW4orexO9tCCHvdCxdLF1mFlnqC2GIMSoZAioyW4orexO9tCCHvdC',
     'VERIFY_TOKEN': 'my_verify_token',
     'SERVER_URL': 'https://site-example-name.herokuapp.com/'
 	}
 	
	```

5. Once filled, save your config.py file and head over to the heroku [dashboard](https://dashboard.heroku.com/apps) and select your previously created app. 

6. Once selected you should se something similar to the image below: 

![Overview](https://github.com/anthonymiyoro/Bot-Builder-Site/blob/master/images/overview.png "").

Navigate to the deploy section and then select the heroku-git option as shown in the image below:

![Deploy](https://github.com/anthonymiyoro/Bot-Builder-Site/blob/master/images/deploy.png "")

Ensure you have navigated to the folder containing your bot and type in the given commands to your terminal as indicated in the image below:

![Install](https://github.com/anthonymiyoro/Bot-Builder-Site/blob/master/images/install.png "")


## HOW TO EDIT YOUR BOTS TEMPLATE

The logic of all the bots here are held in the messenger.py file of the template. Below are the following elements you'll want to add followed by the code needed to implement them.

### QUICK REPLIES

A quick reply consists of small buttons which are good for presenting multiple choices to a user. A quick reply is defined in own function as shown below:

```
def hello(recipient):
    page.send(recipient, "Hi! 😄")
    page.send(recipient, "What would you like to buy?",
              quick_replies=[QuickReply(title=("Sneakers 👟"), payload="BUY_SNEAKERS"),
                             QuickReply(title=("Jeans 👖"), payload="BUY_JEANS"),
                             ],
              metadata="DEVELOPER_DEFINED_METADATA")
	      
```

![quick reply](https://github.com/anthonymiyoro/Bot-Builder-Site/blob/master/images/quick_reply.png "")


The response for the button is ran when the payload is recieved. The Jeans 👖 button above should allow the user to view all the jeans and make a purchase. The template is called when the payload BUY_JEANS from button above, is recieved as shown below.

```
elif quick_reply_payload == 'BUY_JEANS':
            show_jeans(sender_id)
            start_again(sender_id)
   
```

This snippet is found within the recieved message function which collects the different messages and deals with them respectively.

```
@page.handle_message
def received_message(event):
    sender_id = event.sender_id
    recipient_id = event.recipient_id
    time_of_message = event.timestamp
    message = event.message
    
```

Running both functions produces the result shown below:

![quick_resuts](https://github.com/anthonymiyoro/Bot-Builder-Site/blob/master/images/quick_reply_results.png "")


### CREATING TEMPLATES

There are 2 types of templates used in the bots found on this site. They include: 

### GENETIC TEMPLATES

These can hold a maximum of 3 buttons per item together with image and text. Its implementation is as below:

```

#Jeans template
def show_jeans(recipient):
    page.send(recipient, Template.Generic([
        Template.GenericElement("ONSWARP CAMP - Jeans Skinny Fit - dark ",
                                subtitle="by Only & Sons for £99.99",
                                item_url="https://www.zalando.co.uk/only-and-sons-onswarp-camp-jeans-skinny-fit-os322g04j-k11.html?wmc=AFF49_IG_DE.51977_60804..",
                                image_url="https://mosaic01.ztat.net/vgs/media/pdp-gallery/OS/32/2G/03/9K/21/OS322G039-K21@10.jpg",
                                buttons=[
                                    Template.ButtonWeb("Details & Buy 🛍️🛍", "https://www.zalando.co.uk/only-and-sons-onswarp-camp-jeans-skinny-fit-os322g04j-k11.html?wmc=AFF49_IG_DE.51977_60804.."),
                                    Template.ButtonShare()
                                    # Template.ButtonPhoneNumber("Call Branch", "+16505551234")
                                ]),
        Template.GenericElement("MICK - Jeans Skinny Fit - seismology",
                                subtitle="by J Brand for £259.99",
                                item_url="https://www.zalando.co.uk/converse-trainers-athletic-navyblackobsidian-co412b06r-k11.html?wmc=AFF49_IG_DE.51977_60804..",
                                image_url="https://mosaic01.ztat.net/vgs/media/pdp-zoom/JB/22/2G/00/OK/11/JB222G00O-K11@10.jpg",
                                buttons=[
                                    Template.ButtonWeb("Details & Buy 🛍️🛍",
                                                       "https://www.zalando.co.uk/j-brand-jeans-skinny-fit-seismology-jb222g00o-k11.html?wmc=AFF49_IG_DE.51977_60804.."),
                                    Template.ButtonShare()
                                ]),
        Template.GenericElement("ONSWARP RAW EDGE - Jeans Skinny Fit - light blue denim",
                                subtitle="by Only & Sons for £25.99",
                                item_url="https://www.zalando.co.uk/only-and-sons-onswarp-raw-edge-jeans-skinny-fit-light-blue-denim-os322g04o-k11.html?wmc=AFF49_IG_DE.51977_60804..",
                                image_url="https://mosaic01.ztat.net/vgs/media/pdp-zoom/OS/32/2G/04/OK/11/OS322G04O-K11@10.jpg",
                                buttons=[
                                    Template.ButtonWeb("Details & Buy 🛍️🛍",
                                                       "https://www.zalando.co.uk/only-and-sons-onswarp-raw-edge-jeans-skinny-fit-light-blue-denim-os322g04o-k11.html?wmc=AFF49_IG_DE.51977_60804.."),
                                    Template.ButtonShare()
                                ])
    ]))
    
```

With the outcome as in the photo below:

![generic_template](https://github.com/anthonymiyoro/Bot-Builder-Site/blob/master/images/generic_template.png "")

Each `Template.GenericElement` represents one square in the template. They support different buttons and the example below contains call and postback buttons.

```
page.send(recipient_id, Template.Generic([
  Template.GenericElement("rift",
                          subtitle="Next-generation virtual reality",
                          item_url="https://www.oculus.com/en-us/rift/",
                          image_url=CONFIG['SERVER_URL'] + "/assets/rift.png",
                          buttons=[
                              Template.ButtonWeb("Open Web URL", "https://www.oculus.com/en-us/rift/"),
                              Template.ButtonPostBack("tigger Postback", "DEVELOPED_DEFINED_PAYLOAD"),
                              Template.ButtonPhoneNumber("Call Phone Number", "+16505551234")
                          ]),
  Template.GenericElement("touch",
                          subtitle="Your Hands, Now in VR",
                          item_url="https://www.oculus.com/en-us/touch/",
                          image_url=CONFIG['SERVER_URL'] + "/assets/touch.png",
                          buttons=[
                              Template.ButtonWeb("Open Web URL", "https://www.oculus.com/en-us/rift/"),
                              Template.ButtonPostBack("tigger Postback", "DEVELOPED_DEFINED_PAYLOAD"),
                              Template.ButtonPhoneNumber("Call Phone Number", "+16505551234")
                          ])
]))

```

### RECIEPT TEMPLATES

Unlike generic templates, recipiept templates only have 1 item. Their code follows a similar structure to below:

```
    receipt_id = "order1357"
    element = Template.ReceiptElement(title="Hotel Room",
                                      subtitle="Includes: Bed, Breakfast and Board",
                                      quantity=1,
                                      price=75.00,
                                      currency="USD",
                                      image_url="http://www.vhotel.sg/Bencoolen/scripts/images/accomodations/rooms/b_twin_display.jpg"
                                      )

    summary = Template.ReceiptSummary(subtotal=78.99,
                                      total_tax=2.99,
                                      total_cost=78.99)

    adjustment = Template.ReceiptAdjustment(name="New Customer Discount", amount=-50)
    page.send(recipient, text, metadata="DEVELOPER_DEFINED_METADATA")
    page.send(recipient, Template.Receipt(recipient_name='Peter Chang',
                                          order_number=receipt_id,
                                          currency='USD',
                                          payment_method='Visa 1234',
                                          timestamp="1428444852",
                                          elements=[element],
                                          # address=address,
                                          summary=summary,
                                          adjustments=[adjustment]))
```
The above code will generate a reciept looking like the image below:

![reciept_template](https://github.com/anthonymiyoro/Bot-Builder-Site/blob/master/images/receipt.png "")


## WORKING WITH BUTTONS

We have 2 types of buttons in our templates, postback buttons and quick replies.

### POSTBACK BUTTONS

Postback buttons are handled within the `received_postback` function which responds to a given payload.

```
@page.handle_postback
def received_postback(event):
    sender_id = event.sender_id
    recipient_id = event.recipient_id
    time_of_postback = event.timestamp

    payload = event.postback_payload

    if payload == "SELECT_BRANCH":
        select_room_message(sender_id,event)
        show_hotel_room(sender_id)

    elif payload == "SELECT_ROOM":
        book_another(sender_id)
        # confirm

```

### QUICK REPLY BUTTONS

Quick reply buttons are handled in the `recieved message` function along with the rest of the incoming messages from the user.

```
@page.handle_message
def received_message(event):
    sender_id = event.sender_id
    recipient_id = event.recipient_id
    time_of_message = event.timestamp
    message = event.message
    
     if quick_reply:

        quick_reply_payload = quick_reply.get('payload')
        if quick_reply_payload == 'CONFIRM':
            book_another(sender_id)

        elif quick_reply_payload == 'BOOK_ANOTHER_ROOM':
            show_hotel_room(sender_id)

        elif quick_reply_payload == 'RESERVATION':
            send_receipt(sender_id)
    
    
```


## ADDING NLP FUNCTIONALITY

After following the instructions [here](https://developers.facebook.com/docs/messenger-platform/built-in-nlp/), head over to the `recieved message` function and assign the nlp payload that you want as shown in the example below.

```
elif nlp:
	nlp_payload = nlp.get('entities')
        if 'greetings' in nlp_payload:
            nlp_greet = nlp_payload.get('greetings')
            hello(sender_id)
            pprint(nlp_greet)

```

The above snippet runs the hello function whenever a greeting is sent to the bot.

