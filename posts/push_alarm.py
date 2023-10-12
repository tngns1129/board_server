import logging

import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging
import os
from pathlib import Path


class PushSend:
    def __init__(self):
        BASE_DIR = Path(__file__).resolve().parent.parent

    def send_new_post(title, body, token):
        registration_token = token
        message = messaging.MulticastMessage(
            notification=messaging.Notification(
                title='This is a Notification Title',
                body='This is a Notification Body',
            ),
            android=messaging.AndroidConfig(
                data={  # 앱 포그라운드 시 받을 데이터
                    "title": title,
                    "body": body,
                    "value": "0",
                },
                notification=messaging.AndroidNotification(  # 앱 백그라운드
                    title=title,
                    body=body
                )
            ),
            apns=messaging.APNSConfig(
                headers={
                    "apns-priority": "10"
                },
                payload=messaging.APNSPayload(
                    aps=messaging.Aps(
                        alert=messaging.ApsAlert(
                            title=title,
                            body=body
                        ),
                    )
                )
            ),
            tokens=registration_token,
        )
        messaging.send_multicast(message)

    def send_new_comment(title, body, token, post_id):
        registration_token = token

        message = messaging.MulticastMessage(
            notification=messaging.Notification(
                title='This is a Notification Title',
                body='This is a Notification Body',
            ),
            android=messaging.AndroidConfig(
                data={  # 앱 포그라운드 시 받을 데이터
                    "title": title,
                    "body": body,
                    "value": "1",
                    "post_id": post_id,
                },
                notification=messaging.AndroidNotification(  # 앱 백그라운드
                    title=title,
                    body=body
                )
            ),
            apns=messaging.APNSConfig(
                headers={
                    "apns-priority": "5"
                },
                payload=messaging.APNSPayload(
                    aps=messaging.Aps(
                        alert=messaging.ApsAlert(
                            title=title,
                            body=body
                        ),
                        content_available=1
                    ),
                    postId=post_id,
                )
            ),
            tokens=registration_token,
        )
        messaging.send_multicast(message)

    def send(title, body, token):

        registration_token = token

        message = messaging.MulticastMessage(
            notification=messaging.Notification(
                title='This is a Notification Title',
                body='This is a Notification Body',
            ),
            android=messaging.AndroidConfig(
                data={                                  #앱 포그라운드 시 받을 데이터
                    "title": title,
                    "body": body,
                    "value": "1",
                },
                notification=messaging.AndroidNotification( #앱 백그라운드
                    title=title,
                    body=body
                )
            ),
            apns=messaging.APNSConfig(
                headers={
                    "apns-priority": "10"
                },
                payload=messaging.APNSPayload(
                    aps=messaging.Aps(
                        alert=messaging.ApsAlert(
                            title="whaaaaat the",
                            subtitle="hh",
                            body="zzz"
                        ),
                    ),
                    postId=1,
                )
            ),
            tokens=registration_token,
        )
        messaging.send_multicast(message)