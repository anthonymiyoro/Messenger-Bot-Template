# coding: utf-8
import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir)

import json
from config import CONFIG
from fbmq import Attachment, Template, QuickReply, NotificationType
from fbpage import page
import requests


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
    print("Received message for user %s and page %s at %s with message:"
          % (sender_id, recipient_id, time_of_message))
    print(message)

    seq = message.get("seq", 0)
    message_id = message.get("mid")
    app_id = message.get("app_id")
    metadata = message.get("metadata")

    message_text = message.get("text")
    message_attachments = message.get("attachments")
    quick_reply = message.get("quick_reply")

    seq_id = sender_id + ':' + recipient_id
    if USER_SEQ.get(seq_id, -1) >= seq:
        print("Ignore duplicated request")
        return None
    else:
        USER_SEQ[seq_id] = seq

    if quick_reply:

        quick_reply_payload = quick_reply.get('payload')
        if quick_reply_payload == 'CONFIRM':
            book_another(sender_id)
            print("quick reply for message %s with payload %s" % (message_id, quick_reply_payload))

        elif quick_reply_payload == 'BOOK_ANOTHER_ROOM':
            show_hotel_room(sender_id)

        elif quick_reply_payload == 'RESERVATION':
            send_receipt(sender_id)

        elif quick_reply_payload == 'CANCEL':
            show_hotel_room(sender_id)
        else:
            print("quick reply for message %s with payload %s" % (message_id, quick_reply_payload))

    if message_text:
        send_message(sender_id, message_text)
    elif message_attachments:
        page.send(sender_id, "Message with attachment received")


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
# Add postback button payloads in if statements
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

    elif payload == "START_PAYLOAD":
        send_welcome_messege(sender_id, event)
        show_branch(sender_id)

    elif payload == "BOOK_ROOM":
        show_hotel_room(sender_id)

    elif payload == "RESERVATION":
        send_receipt(sender_id)
        last_messege(sender_id)

    elif payload == "START_AGAIN":
        show_hotel_room(sender_id)

    print("Received postback for user %s and page %s with payload '%s' at %s"
          % (sender_id, recipient_id, payload, time_of_postback))


def send_message(recipient_id, text):
    # Run function when corresponding word is typed in otherwise just echo the word
    special_keywords = {
        "button": send_button,
        "receipt": send_receipt,
        "branch": show_branch,
        "hotel": show_hotel_room,

    }

    if text in special_keywords:
        special_keywords[text](recipient_id)
    else:
        page.send(recipient_id, text, callback=send_text_callback, notification_type=NotificationType.REGULAR)


def send_button(recipient):
    """
    Shortcuts are supported
    page.send(recipient, Template.Buttons("hello", [
        {'type': 'web_url', 'title': 'Open Web URL', 'value': 'https://www.oculus.com/en-us/rift/'},
        {'type': 'postback', 'title': 'tigger Postback', 'value': 'DEVELOPED_DEFINED_PAYLOAD'},
        {'type': 'phone_number', 'title': 'Call Phone Number', 'value': '+16505551234'},
    ]))
    """
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
def send_welcome_messege(recipient, event):
    user_profile = page.get_user_profile(event.sender_id)  # return dict
    print(user_profile)

    text = "Hello " + user_profile['first_name'] + "! Welcome to the Hotel Test Bot. \n Please choose a preferred hotel branch. 🙂"
    page.send(recipient, text, metadata="DEVELOPER_DEFINED_METADATA")


# Message displayed when selecting a room
def select_room_message(recipient, event):
    user_profile = page.get_user_profile(event.sender_id)  # return dict
    print(user_profile)

    text = "Good Choice " + user_profile['first_name'] + "! \n Please select your preferred room."
    page.send(recipient, text, metadata="DEVELOPER_DEFINED_METADATA")


# Show different hotel branches
def show_branch(recipient):
    page.send(recipient, Template.Generic([
        Template.GenericElement("Seven Suns Hotel Template",
                                subtitle="Nairobi Branch",
                                item_url="https://sevensuns.com",
                                image_url="https://taj.tajhotels.com/content/dam/luxury/hotels/Taj_Mahal_Delhi/images/4x3/HotelFacade4x3.jpg",
                                buttons=[
                                    # Template.ButtonWeb("Open Web URL", "https://www.oculus.com/en-us/rift/"),
                                    Template.ButtonPostBack("Select Branch", "SELECT_BRANCH"),
                                    Template.ButtonPhoneNumber("Call Branch", "+16505551234")
                                ]),
        Template.GenericElement("Seven Suns Hotel Template",
                                subtitle="Mombasa Branch",
                                item_url="https://sevensuns.com",
                                image_url="https://www.safarihotelsnamibia.com/wp-content/uploads/2014/11/Safari-Court-Hotel-Pool.jpg",
                                buttons=[
                                    # {'type': 'web_url', 'title': 'Open Web URL',
                                    #  'value': 'https://www.oculus.com/en-us/rift/'},
                                    {'type': 'postback', 'title': 'Select Branch',
                                     'value': 'SELECT_BRANCH'},
                                    {'type': 'phone_number', 'title': 'Call Branch', 'value': '+16505551234'},
                                ])
    ]))


#Show hotel room template
def show_hotel_room(recipient):
    page.send(recipient, Template.Generic([
        Template.GenericElement("Seven Suns Hotel Template",
                                subtitle="Basic Suite",
                                item_url="https://sevensuns.com",
                                image_url="http://www.vhotel.sg/Bencoolen/scripts/images/accomodations/rooms/b_twin_display.jpg",
                                buttons=[
                                    # Template.ButtonWeb("Open Web URL", "https://www.oculus.com/en-us/rift/"),
                                    Template.ButtonPostBack("Select Room", "SELECT_ROOM")
                                    # Template.ButtonPhoneNumber("Call Branch", "+16505551234")
                                ]),
        Template.GenericElement("Seven Suns Hotel Template",
                                subtitle="Deluxe Suite",
                                item_url="https://sevensuns.com",
                                image_url="http://www.vhotel.sg/Bencoolen/scripts/images/accomodations/rooms/b_premier_display.jpg",
                                buttons=[
                                    # {'type': 'web_url', 'title': 'Open Web URL',
                                    #  'value': 'https://www.oculus.com/en-us/rift/'},
                                    {'type': 'postback', 'title': 'Select Room',
                                     'value': 'SELECT_ROOM'},
                                    # {'type': 'phone_number', 'title': 'Call Branch', 'value': '+16505551234'},
                                ]),
        Template.GenericElement("Seven Suns Hotel Template",
                                subtitle="Premium Suite",
                                item_url="https://sevensuns.com",
                                image_url="http://www.vhotel.sg/Bencoolen/scripts/images/accomodations/rooms/b_patio_display.jpg",
                                buttons=[
                                    # {'type': 'web_url', 'title': 'Open Web URL',
                                    #  'value': 'https://www.oculus.com/en-us/rift/'},
                                    {'type': 'postback', 'title': 'Select Room',
                                     'value': 'SELECT_ROOM'},
                                    # {'type': 'phone_number', 'title': 'Call Branch', 'value': '+16505551234'},
                                ])
    ]))


# Reciept to show that items have been purchased
def send_receipt(recipient):
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

    page.send(recipient, Template.Receipt(recipient_name='Peter Chang',
                                          order_number=receipt_id,
                                          currency='USD',
                                          payment_method='Visa 1234',
                                          timestamp="1428444852",
                                          elements=[element],
                                          # address=address,
                                          summary=summary,
                                          adjustments=[adjustment]))


# Quick reply menu to book another room
def book_another(recipient):
    page.send(recipient, "Would you like to book another room? 🙂",
              quick_replies=[QuickReply(title=("Book another room"), payload="BOOK_ANOTHER_ROOM"),
                             QuickReply(title=("Cancel"), payload="CANCEL"),
                             QuickReply(title=("Continue with booking"), payload="RESERVATION")],
              metadata="DEVELOPER_DEFINED_METADATA")


#Last messege after reciept has been shown
def last_messege(recipient):
    page.send(recipient, "Would you like to continue?",
              quick_replies=[QuickReply(title=("Book another room"), payload="BOOK_ANOTHER_ROOM"),
                             QuickReply(title=("Cancel"), payload="CANCEL"),
                             QuickReply(title=("Start Again"), payload="START_AGAIN")],
              metadata="DEVELOPER_DEFINED_METADATA")


#Run this function to set up a persistent menu
page.show_persistent_menu([Template.ButtonPostBack('Start Again', 'START_AGAIN_PAYLOAD'),
                           Template.ButtonPostBack('Cancel', 'CANCEL_PAYLOAD')])

@page.callback(['MENU_PAYLOAD/(.+)'])
def click_persistent_menu(payload, event):
  click_menu = payload.split('/')[1]
  print("you clicked %s menu" % click_menu)





