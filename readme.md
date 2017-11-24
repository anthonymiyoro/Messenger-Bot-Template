Shopping Bot Template
====================

A simple Shopping Bot template running on Flask that's ready to run on Heroku.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/anthonymiyoro/shopping_bot_example)


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

