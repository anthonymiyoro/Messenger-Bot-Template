# coding: utf-8
import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir)

import json
from config import CONFIG
from fbmq import Attachment, Template, QuickReply, NotificationType
from fbpage import page
import requests
from pprint import pprint


USER_SEQ = {}


@page.handle_optin
def received_authentication(event):
    sender_id = event.sender_id
    recipient_id = event.recipient_id
    time_of_auth = event.timestamp

    pass_through_param = event.optin.get("ref")

    print("Received authentication for user %s and page %s with pass "
          "through param '%s' at %s" % (sender_id, recipient_id, pass_through_param, time_of_auth))

    page.send(sender_id, "Authentication successful")


@page.handle_echo
def received_echo(event):
    message = event.message
    message_id = message.get("mid")
    app_id = message.get("app_id")
    metadata = message.get("metadata")
    print("page id : %s , %s" % (page.page_id, page.page_name))
    print("Received echo for message %s and app %s with metadata %s" % (message_id, app_id, metadata))


@page.handle_message
def received_message(event):
    sender_id = event.sender_id
    recipient_id = event.recipient_id
    time_of_message = event.timestamp
    message = event.message
    # print("Received message for user %s and page %s at %s with message:"
    #       % (sender_id, recipient_id, time_of_message))
    pprint(message)

    seq = message.get("seq", 0)
    message_id = message.get("mid")
    app_id = message.get("app_id")
    metadata = message.get("metadata")

    message_text = message.get("text")
    message_attachments = message.get("attachments")
    quick_reply = message.get("quick_reply")
    # nlp = message['nlp']['entities']
    nlp = message.get("nlp")

    seq_id = sender_id + ':' + recipient_id
    if USER_SEQ.get(seq_id, -1) >= seq:
        print("Ignore duplicated request")
        return None
    else:
        USER_SEQ[seq_id] = seq

    if quick_reply:

        quick_reply_payload = quick_reply.get('payload')
        if quick_reply_payload == 'VIEW_MORE':
            view_more(sender_id)
            # print("quick reply for message %s with payload %s" % (message_id, quick_reply_payload))

        elif quick_reply_payload == 'BUY_SNEAKERS':
            show_shoes(sender_id)
            start_again(sender_id)

        elif quick_reply_payload == 'BUY_JEANS':
            show_jeans(sender_id)
            start_again(sender_id)
        else:
            print("quick reply for message %s with payload %s" % (message_id, quick_reply_payload))

# Check for user sent greetings
    elif nlp:
        nlp_payload = nlp.get('entities')
        if 'greetings' in nlp_payload:
            nlp_greet = nlp_payload.get('greetings')
            hello(sender_id)
            pprint(nlp_greet)
        # Check for different entities
        # print("Exists")

    # elif message_text:
    #     # send_message(sender_id, message_text)
    #     echo_messege(sender_id)

    elif message_attachments:
        page.send(sender_id, "Message with attachment received")

    else:
        # Create get started button
        # page.show_starting_button("START_PAYLOAD")
        user_profile = page.get_user_profile(event.sender_id)  # return dict
        print(user_profile)

        print ("Nothing")


@page.handle_delivery
def received_delivery_confirmation(event):
    delivery = event.delivery
    message_ids = delivery.get("mids")
    watermark = delivery.get("watermark")

    if message_ids:
        for message_id in message_ids:
            print("Received delivery confirmation for message ID: %s" % message_id)

    print("All message before %s were delivered." % watermark)


def send_text_callback(payload, response):
    print("SEND CALLBACK")


# Reacts to postback buttons NOT QuickReply
@page.handle_postback
def received_postback(event):
    sender_id = event.sender_id
    recipient_id = event.recipient_id
    time_of_postback = event.timestamp

    payload = event.postback_payload
    if payload == "VIEW_MORE":
        view_more(sender_id)
        # confirm

    elif payload == "START_PAYLOAD":
        send_welcome_message(sender_id, event)
        # show_branch(sender_id)

    elif payload == "START_AGAIN":
        purchase_item(sender_id)

    print("Received postback for user %s and page %s with payload '%s' at %s"
          % (sender_id, recipient_id, payload, time_of_postback))


def send_message(recipient_id, text):
    # Run function when corresponding word is typed in otherwise just echo the word
    special_keywords = {
        "button": send_button,
    }

    if text in special_keywords:
        special_keywords[text](recipient_id)
    else:
        page.send(recipient_id, text, callback=send_text_callback, notification_type=NotificationType.REGULAR)


def send_button(recipient):
    page.send(recipient, Template.Buttons("hello", [
        Template.ButtonWeb("Open Web URL", "https://www.oculus.com/en-us/rift/"),
        Template.ButtonPostBack("trigger Postback", "DEVELOPED_DEFINED_PAYLOAD"),
        Template.ButtonPhoneNumber("Call Phone Number", "+16505551234")
    ]))


@page.callback(['DEVELOPED_DEFINED_PAYLOAD'])
def callback_clicked_button(payload, event):
    print(payload, event)


def send_text_message(recipient, text):
    page.send(recipient, text, metadata="DEVELOPER_DEFINED_METADATA")


# Welcome message when get started clicked
def send_welcome_message(recipient, event):
    user_profile = page.get_user_profile(event.sender_id)  # return dict
    print(user_profile)

    text1 = "Hello " + user_profile['first_name'] + "!"
    text2 = "Welcome to your personal Shopping Example Bot. We have the following items for sale. Please choose one. 🙂"
    page.send(recipient, text1, metadata="DEVELOPER_DEFINED_METADATA")
    page.send(recipient, text2,
              quick_replies=[QuickReply(title=("Sneakers 👟"), payload="BUY_SNEAKERS"),
                             QuickReply(title=("Jeans 👖"), payload="BUY_JEANS"), ],
              metadata="DEVELOPER_DEFINED_METADATA")

# Message displayed when selecting a room
def view_more(recipient, event):
    user_profile = page.get_user_profile(event.sender_id)  # return dict
    print(user_profile)
    page.send(recipient,
              quick_replies=[QuickReply(title=("Sneakers 👟"), payload="BUY_SNEAKERS"),
                             QuickReply(title=("Jeans 👖"), payload="BUY_JEANS"),
                             ],
              metadata="DEVELOPER_DEFINED_METADATA")


# Quick reply menu after generic template
def start_again(recipient):
    page.send(recipient, "Would you like to view more items? 🙂",
              quick_replies=[QuickReply(title=("Cancel"), payload="CANCEL"),
                             QuickReply(title=("View More"), payload="VIEW_MORE")],
              metadata="DEVELOPER_DEFINED_METADATA")


def hello(recipient):
    page.send(recipient, "Hi! 😄")
    page.send(recipient, "What would you like to buy?",
              quick_replies=[QuickReply(title=("Sneakers 👟"), payload="BUY_SNEAKERS"),
                             QuickReply(title=("Jeans 👖"), payload="BUY_JEANS"),
                             ],
              metadata="DEVELOPER_DEFINED_METADATA")


def purchase_item(recipient):
    page.send(recipient, "What item would you like to purchase?",
              quick_replies=[QuickReply(title=("Sneakers 👟"), payload="BUY_SNEAKERS"),
                             QuickReply(title=("Jeans 👖"), payload="BUY_JEANS"), ],
              metadata="DEVELOPER_DEFINED_METADATA")


#Run this function to set up a persistent menu
page.show_persistent_menu([Template.ButtonPostBack('Start Again', 'START_AGAIN_PAYLOAD'),
                           Template.ButtonPostBack('Cancel', 'CANCEL_PAYLOAD')])

@page.callback(['MENU_PAYLOAD/(.+)'])
def click_persistent_menu(payload, event):
    click_menu = payload.split('/')[1]
    print("you clicked %s menu" % click_menu)

#Shoes template
def show_shoes(recipient):
    page.send(recipient, Template.Generic([
        Template.GenericElement("BRADLEY MID - High-top trainers - deep navy",
                                subtitle="£99.99",
                                item_url="https://www.zalando.co.uk/clae-bradley-high-top-trainers-cl212b00r-k11.html?wmc=AFF49_IG_DE.51977_60804..",
                                image_url="https://mosaic01.ztat.net/vgs/media/pdp-gallery/CL/21/2B/00/RK/11/CL212B00R-K11@12.jpg",
                                buttons=[
                                    Template.ButtonWeb("Details & Buy 🛍️🛍", "https://www.zalando.co.uk/clae-bradley-high-top-trainers-cl212b00r-k11.html?wmc=AFF49_IG_DE.51977_60804.."),
                                    Template.ButtonShare()
                                    # Template.ButtonPhoneNumber("Call Branch", "+16505551234")
                                ]),
        Template.GenericElement("CRIMSON - Trainers - athletic navy/black/obsidian",
                                subtitle="£43.99",
                                item_url="https://www.zalando.co.uk/converse-trainers-athletic-navyblackobsidian-co412b06r-k11.html?wmc=AFF49_IG_DE.51977_60804..",
                                image_url="https://mosaic01.ztat.net/vgs/media/pdp-gallery/CO/41/2B/06/RK/11/CO412B06R-K11@12.jpg",
                                buttons=[
                                    Template.ButtonWeb("Details & Buy 🛍️🛍🛍️🛍️🛍️",
                                                       "https://www.zalando.co.uk/converse-trainers-athletic-navyblackobsidian-co412b06r-k11.html?wmc=AFF49_IG_DE.51977_60804.."),
                                    Template.ButtonShare()
                                ]),
        Template.GenericElement("JJSPIDER URBAN - Trainers - dress blues",
                                subtitle="£17.99",
                                item_url="https://www.zalando.co.uk/jack-jones-spider-trainers-ja212b025-k11.html?wmc=AFF49_IG_DE.51977_60804..",
                                image_url="https://mosaic01.ztat.net/vgs/media/pdp-gallery/JA/21/2B/02/5K/11/JA212B025-K11@115.jpg",
                                buttons=[
                                    Template.ButtonWeb("Details & Buy 🛍️🛍",
                                                       "https://www.zalando.co.uk/jack-jones-spider-trainers-ja212b025-k11.html?wmc=AFF49_IG_DE.51977_60804.."),
                                    Template.ButtonShare()
                                ]),

        Template.GenericElement("STACKS II - Trainers - blue",
                                subtitle="£32.99",
                                item_url="https://www.zalando.co.uk/supra-stacks-ii-trainers-su412b04o-k11.html?wmc=AFF49_IG_DE.51977_60804..",
                                image_url="https://mosaic01.ztat.net/vgs/media/pdp-zoom/SU/41/2B/04/OK/11/SU412B04O-K11@12.jpg",
                                buttons=[
                                    Template.ButtonWeb("Details & Buy 🛍️🛍",
                                                       "https://www.zalando.co.uk/supra-stacks-ii-trainers-su412b04o-k11.html?wmc=AFF49_IG_DE.51977_60804.."),
                                    Template.ButtonShare()
                                ]),

        Template.GenericElement("Adidas ZX 700 - Trainers - mystery blue/footwear white",
                                subtitle="£17.99",
                                item_url="https://www.zalando.co.uk/adidas-originals-trainers-mystery-bluefootwear-white-ad112b0ln-k11.html?wmc=AFF49_IG_DE.51977_60804..&zoom=true",
                                image_url="https://mosaic01.ztat.net/vgs/media/pdp-zoom/AD/11/2B/0L/NK/11/AD112B0LN-K11@12.jpg",
                                buttons=[
                                    Template.ButtonWeb("Details & Buy 🛍️🛍",
                                                       "https://www.zalando.co.uk/adidas-originals-trainers-mystery-bluefootwear-white-ad112b0ln-k11.html?wmc=AFF49_IG_DE.51977_60804.."),
                                    Template.ButtonShare()
                                ])
    ]))

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
