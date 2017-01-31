# -*- coding: utf-8 -*-

"""
onesignal.api
~~~~~~~~~~~

This module contains functionality for access to OneSignal API calls.
"""

import json

import requests

from .exceptions import OneSignalApiError


class OneSignal(object):
    def __init__(self, api_key, app_id=None, api_version='v1'):
        """A OneSignal API wrapper instance.

        :param api_key: Your application api key or user api key.
        :param app_id: (optional) Your application id.
        :param api_version: (optional) The API version, defaults to "v1".

        """
        self.api_key = api_key
        self.app_id = app_id

        self.api_base = 'https://onesignal.com/api/{}'
        self.api_version = api_version
        self.api_url = self.api_base.format(api_version)

        self.client = requests.Session()
        self.client.headers = {
            'Content-Type': 'application/json; charset=utf-8',
            "Authorization": "Basic {}".format(self.api_key),
        }

    def __repr__(self):
        return '<OneSignal: %s>' % (self.api_key)

    def request(self, method, url, **data):
        """Make a request to OneSignal's REST API.

        :param method: GET, POST, \D\ELETE or PUT.
        :param url: Either a full OneSignal REST API url or a portion (i.e. "players/id").
        :param \*\*data: Parameters that are accepted by OneSignal for the endpoint you're requesting.

        :rtype: dict
        """
        # if the url doesn't start with a protocol, join the "url" and self.api_url
        if not url.startswith('https://'):
            url = '%s/%s' % (self.api_url, url)

        return self._request(method, url, **data)

    def get(self, url, **data):
        """Shortcut to make a GET request to OneSignal's REST API.

        :param url: Either a full OneSignal REST API url or a portion (i.e. "players/id").
        :param \*\*data: Parameters that are accepted by OneSignal for the endpoint you're requesting.

        :rtype: dict
        """
        return self.request('GET', url, **data)

    def post(self, url, **data):
        """Shortcut to make a POST request to OneSignal's REST API.

        :param url: Either a full OneSignal REST API url or a portion (i.e. "players/id").
        :param \*\*data: Parameters that are accepted by OneSignal for the endpoint you're requesting.

        :rtype: dict
        """
        return self.request('POST', url, **data)

    def delete(self, url, **data):
        """Shortcut to make a \D\ELETE request to OneSignal's REST API.

        :param url: Either a full OneSignal REST API url or a portion (i.e. "players/id").
        :param \*\*data: Parameters that are accepted by OneSignal for the endpoint you're requesting.

        :rtype: dict
        """
        return self.request('DELETE', url, **data)

    def put(self, url, **data):
        """Shortcut to make a PUT request to OneSignal's REST API.

        :param url: Either a full OneSignal REST API url or a portion (i.e. "players/id").
        :param \*\*data: Parameters that are accepted by OneSignal for the endpoint you're requesting.

        :rtype: dict
        """
        return self.request('PUT', url, **data)

    def _request(self, method, url, **data):
        """Internal method to forge a request to OneSignal's REST API.

        :param method: GET, POST, \D\ELETE or PUT.
        :param url: Either a full OneSignal REST API url or a portion (i.e. "players/id").
        :param \*\*data: Parameters that are accepted by OneSignal for the endpoint you're requesting.

        :rtype: dict
        """

        data = data or {}

        payload = {
            'app_id': self.app_id,
        }

        payload.update(**data)

        method = method.lower()

        response_kwargs = {}

        if method != 'get':
            response_kwargs['data'] = json.dumps(payload)
        else:
            response_kwargs['params'] = payload

        print 'resposne_kwargs', response_kwargs

        func = getattr(self.client, method)

        response = func(url, **response_kwargs)

        try:
            print 'resposne.text', response.text
            content = response.json()
        except ValueError:
            raise OneSignalApiError('There was an error decoding the response, it was not JSON.')

        if response.status_code == 200:
            pass
        else:
            try:
                message = content.get('errors')
                if isinstance(message, dict):
                    message = message[message.keys()[0]]
                elif isinstance(message, list):
                    message = message[0]
            except IndexError:
                message = 'OneSignal returned an error that could not be parsed: {}'.format(response.text)

            raise OneSignalApiError(message)

        return content

    def notifications(self):
        """View the details of multiple notifications.

        Docs: https://documentation.onesignal.com/reference#view-notifications

        :rtype: dict
        """
        return self.get('notifications')

    def notifications_open(self, notification_id):
        """Track when users open a notification.

        :param notification_id: Notification to track an open for.

        Docs: https://documentation.onesignal.com/reference#track-open

        :rtype: dict
        """
        return self.put('notifications/{}'.format(notification_id))

    def notifications_create(self, **data):
        """Sends notifications to your users.

        Docs: https://documentation.onesignal.com/reference#create-notification

        :rtype: dict

        Usage::

          >>> onesignal.notifications_create(
                include_player_ids=['a8c50012-7a78-492a-8a34-6bd3aa2e5f87',],
                contents={
                  'en': 'English Message'
                }
            )
          >>> {u'id': u'732d69c7-2599-489c-89a6-55cf6b41defe', u'recipients': 1}

        """
        return self.post('notifications', **data)

    def notifications_cancel(self, notification_id):
        """Sends notifications to your users.

        Docs: https://documentation.onesignal.com/reference#create-notification

        :rtype: dict

        Usage::

          >>> onesignal.notifications_cancel('732d69c7-2599-489c-89a6-55cf6b41defe')
          >>> {u'success': true}
        """
        return self.delete('notifications/{}'.format(notification_id))

    def notifications_details(self, notification_id):
        """View the details of a single notification.

        :param notification_id: Notification to get details for.

        Docs: https://documentation.onesignal.com/reference#view-notification

        :rtype: dict

        Usage::

          >>> onesignal.notifications_details('732d69c7-2599-489c-89a6-55cf6b41defe')
          >>> {
                "id": "732d69c7-2599-489c-89a6-55cf6b41defe",
                "successful": 1,
                "failed": 0,
                "converted": 3,
                "remaining": 0,
                "queued_at": 1415914655,
                "send_after": 1415914655,
                "url": "https://yourWebsiteToOpen.com",
                "data": {
                    "foo": "bar",
                    "your": "custom metadata"
                },
                "canceled": false,
                "headings": {
                    "en": "English and default langauge heading",
                    "es": "Spanish language heading"
                },
                "contents": {
                    "en": "English language content",
                    "es": "Hola"
                }
            }
        """
        return self.get('notifications/{}'.format(notification_id))

    def apps(self):
        """View the details of all of your current OneSignal apps.

        Docs: https://documentation.onesignal.com/reference#view-apps-apps

        :rtype: dict

        Usage::

          >>> onesignal.apps()
          >>> [
                {
                    id: "92911750-242d-4260-9e00-9d9034f139ce",
                    name: "Your app 1",
                    players: 150,
                    messagable_players: 143,
                    updated_at: "2014-04-01T04:20:02.003Z",
                    created_at: "2014-04-01T04:20:02.003Z",
                    gcm_key: "a gcm push key",
                    chrome_key: "A Chrome Web Push GCM key",
                    chrome_web_origin: "Chrome Web Push Site URL",
                    chrome_web_gcm_sender_id: "Chrome Web Push GCM Sender ID",
                    chrome_web_default_notification_icon: "http://yoursite.com/chrome_notification_icon",
                    chrome_web_sub_domain:"your_site_name",
                    apns_env: "sandbox",
                    apns_certificates: "Your apns certificate",
                    safari_apns_cetificate: "Your Safari APNS certificate",
                    safari_site_origin: "The homename for your website for Safari Push, including http or https",
                    safari_push_id: "The certificate bundle ID for Safari Web Push",
                    safari_icon_16_16: "http://onesignal.com/safari_packages/92911750-242d-4260-9e00-9d9034f139ce/16x16.png",
                    safari_icon_32_32: "http://onesignal.com/safari_packages/92911750-242d-4260-9e00-9d9034f139ce/16x16@2.png",
                    safari_icon_64_64: "http://onesignal.com/safari_packages/92911750-242d-4260-9e00-9d9034f139ce/32x32@2x.png",
                    safari_icon_128_128: "http://onesignal.com/safari_packages/92911750-242d-4260-9e00-9d9034f139ce/128x128.png",
                    safari_icon_256_256: "http://onesignal.com/safari_packages/92911750-242d-4260-9e00-9d9034f139ce/128x128@2x.png",
                    site_name: "The URL to your website for Web Push",
                    basic_auth_key: "NGEwMGZmMjItY2NkNy0xMWUzLTk5ZDUtMDAwYzI5NDBlNjJj"
                }
            ]
        """
        return self.get('apps')

    def apps_details(self, app_id=None):
        """View the details of a single OneSignal app.

        :param app_id: (optional) If you're using your user API Key, you can pass one of your app ids.

        Docs: https://documentation.onesignal.com/reference#view-an-app

        :rtype: dict

        Usage::

          >>> onesignal.apps_details('92911750-242d-4260-9e00-9d9034f139ce')
          >>> {
                id: "92911750-242d-4260-9e00-9d9034f139ce",
                name: "Your app 1",
                players: 150,
                messagable_players: 143,
                updated_at: "2014-04-01T04:20:02.003Z",
                created_at: "2014-04-01T04:20:02.003Z",
                gcm_key: "a gcm push key",
                chrome_key: "A Chrome Web Push GCM key",
                chrome_web_origin: "Chrome Web Push Site URL",
                chrome_web_gcm_sender_id: "Chrome Web Push GCM Sender ID",
                chrome_web_default_notification_icon: "http://yoursite.com/chrome_notification_icon",
                chrome_web_sub_domain:"your_site_name",
                apns_env: "sandbox",
                apns_certificates: "Your apns certificate",
                safari_apns_cetificate: "Your Safari APNS certificate",
                safari_site_origin: "The homename for your website for Safari Push, including http or https",
                safari_push_id: "The certificate bundle ID for Safari Web Push",
                safari_icon_16_16: "http://onesignal.com/safari_packages/92911750-242d-4260-9e00-9d9034f139ce/16x16.png",
                safari_icon_32_32: "http://onesignal.com/safari_packages/92911750-242d-4260-9e00-9d9034f139ce/16x16@2.png",
                safari_icon_64_64: "http://onesignal.com/safari_packages/92911750-242d-4260-9e00-9d9034f139ce/32x32@2x.png",
                safari_icon_128_128: "http://onesignal.com/safari_packages/92911750-242d-4260-9e00-9d9034f139ce/128x128.png",
                safari_icon_256_256: "http://onesignal.com/safari_packages/92911750-242d-4260-9e00-9d9034f139ce/128x128@2x.png",
                site_name: "The URL to your website for Web Push",
                basic_auth_key: "NGEwMGZmMjItY2NkNy0xMWUzLTk5ZDUtMDAwYzI5NDBlNjJj"
            }
        """
        app_id = app_id or self.app_id

        return self.get('apps/{}'.format(app_id))

    def apps_create(self, name, **data):
        """Creates a new OneSignal app.

        :param name: The name of your new app, as displayed on your apps list on the dashboard. This can be renamed later.

        Docs: https://documentation.onesignal.com/reference#create-an-app

        :rtype: dict

        Usage::

          >>> onesignal.apps_create(
                'OneSignal API Test',
                apns_env='production',
                apns_p12='asdsadcvawe223cwef...',
                apns_p12_password='FooBar',
                gcm_key='a gcm push key',
            )
          >>> {
                id: "92911750-242d-4260-9e00-9d9034f139ce",
                name: "OneSignal API Test",
                players: 150,
                messagable_players: 143,
                updated_at: "2014-04-01T04:20:02.003Z",
                created_at: "2014-04-01T04:20:02.003Z",
                gcm_key: "a gcm push key",
                chrome_key: "A Chrome Web Push GCM key",
                chrome_web_origin: "Chrome Web Push Site URL",
                chrome_web_gcm_sender_id: "Chrome Web Push GCM Sender ID",
                chrome_web_default_notification_icon: "http://yoursite.com/chrome_notification_icon",
                chrome_web_sub_domain:"your_site_name",
                apns_env: "sandbox",
                apns_certificates: "Your apns certificate",
                safari_apns_cetificate: "Your Safari APNS certificate",
                safari_site_origin: "The homename for your website for Safari Push, including http or https",
                safari_push_id: "The certificate bundle ID for Safari Web Push",
                safari_icon_16_16: "http://onesignal.com/safari_packages/92911750-242d-4260-9e00-9d9034f139ce/16x16.png",
                safari_icon_32_32: "http://onesignal.com/safari_packages/92911750-242d-4260-9e00-9d9034f139ce/16x16@2.png",
                safari_icon_64_64: "http://onesignal.com/safari_packages/92911750-242d-4260-9e00-9d9034f139ce/32x32@2x.png",
                safari_icon_128_128: "http://onesignal.com/safari_packages/92911750-242d-4260-9e00-9d9034f139ce/128x128.png",
                safari_icon_256_256: "http://onesignal.com/safari_packages/92911750-242d-4260-9e00-9d9034f139ce/128x128@2x.png",
                site_name: "The URL to your website for Web Push",
                basic_auth_key: "NGEwMGZmMjItY2NkNy0xMWUzLTk5ZDUtMDAwYzI5NDBlNjJj"
            }
        """
        data.update({
            'name': name,
        })

        return self.post('apps', **data)

    def apps_update(self, app_id, **data):
        """Updates the name or configuration settings of an existing OneSignal app.

        :param app_id: The id of the app you want to update.

        Docs: https://documentation.onesignal.com/reference#update-an-app

        :rtype: dict

        Usage::

          >>> onesignal.apps_update(
                name='OneSignal API Test EDITED',
            )
          >>> {
                id: "92911750-242d-4260-9e00-9d9034f139ce",
                name: "OneSignal API Test EDITED",
                players: 150,
                messagable_players: 143,
                updated_at: "2014-04-01T04:20:02.003Z",
                created_at: "2014-04-01T04:20:02.003Z",
                gcm_key: "a gcm push key",
                chrome_key: "A Chrome Web Push GCM key",
                chrome_web_origin: "Chrome Web Push Site URL",
                chrome_web_gcm_sender_id: "Chrome Web Push GCM Sender ID",
                chrome_web_default_notification_icon: "http://yoursite.com/chrome_notification_icon",
                chrome_web_sub_domain:"your_site_name",
                apns_env: "sandbox",
                apns_certificates: "Your apns certificate",
                safari_apns_cetificate: "Your Safari APNS certificate",
                safari_site_origin: "The homename for your website for Safari Push, including http or https",
                safari_push_id: "The certificate bundle ID for Safari Web Push",
                safari_icon_16_16: "http://onesignal.com/safari_packages/92911750-242d-4260-9e00-9d9034f139ce/16x16.png",
                safari_icon_32_32: "http://onesignal.com/safari_packages/92911750-242d-4260-9e00-9d9034f139ce/16x16@2.png",
                safari_icon_64_64: "http://onesignal.com/safari_packages/92911750-242d-4260-9e00-9d9034f139ce/32x32@2x.png",
                safari_icon_128_128: "http://onesignal.com/safari_packages/92911750-242d-4260-9e00-9d9034f139ce/128x128.png",
                safari_icon_256_256: "http://onesignal.com/safari_packages/92911750-242d-4260-9e00-9d9034f139ce/128x128@2x.png",
                site_name: "The URL to your website for Web Push",
                basic_auth_key: "NGEwMGZmMjItY2NkNy0xMWUzLTk5ZDUtMDAwYzI5NDBlNjJj"
            }
        """
        return self.put('apps/{}'.format(app_id), **data)

    def devices(self, **data):
        """View the details of multiple devices in one of your OneSignal apps.

        Docs: https://documentation.onesignal.com/reference#view-devices

        :rtype: dict

        Usage::

          >>> onesignal.devices()
          >>> {
                "total_count": 3,
                "offset": 2,
                "limit": 2,
                "players": [
                    {
                        "identifier": "ce777617da7f548fe7a9ab6febb56cf39fba6d382000c0395666288d961ee566",
                        "session_count": 1,
                        "language": "en",
                        "timezone": -28800,
                        "game_version": "1.0",
                        "device_os": "7.0.4",
                        "device_type": 0,
                        "device_model": "iPhone",
                        "ad_id": null,
                        "tags": {
                            "a": "1",
                            "foo": "bar"
                        },
                        "last_active": 1395096859,
                        "amount_spent": 0.0,
                        "created_at": 1395096859,
                        "invalid_identifier": false,
                        "badge_count": 0
                    }
                ]
            }
        """
        return self.get('players', **data)

    def devices_details(self, player_id):
        """View the details of an existing device in one of your OneSignal apps.

        Docs: https://documentation.onesignal.com/reference#view-device

        :rtype: dict

        Usage::

          >>> onesignal.devices()
          >>> {
                "identifier": "ce777617da7f548fe7a9ab6febb56cf39fba6d382000c0395666288d961ee566",
                "session_count": 1,
                "language": "en",
                "timezone": -28800,
                "game_version": "1.0",
                "device_os": "7.0.4",
                "device_type": 0,
                "device_model": "iPhone",
                "ad_id": null,
                "tags": {
                    "a": "1",
                    "foo": "bar"
                },
                "last_active": 1395096859,
                "amount_spent": 0.0,
                "created_at": 1395096859,
                "invalid_identifier": false,
                "badge_count": 0
            }
        """
        return self.get('players/{}'.format(player_id))

    def devices_create(self, device_type, **data):
        """Register a new device to one of your OneSignal apps.

        :param device_type: An integer representing a device platform from the docs.

        Docs: https://documentation.onesignal.com/reference#add-a-device

        :rtype: dict

        Usage::

          >>> onesignal.devices_create(0, identifier='ce777617da7f548fe7a9ab6febb56cf39fba6d382000c0395666288d961ee566')
          >>> {
                "identifier": "ce777617da7f548fe7a9ab6febb56cf39fba6d382000c0395666288d961ee566",
                "session_count": 1,
                "language": "en",
                "timezone": -18880,
                "game_version": "1.0",
                "device_os": "",
                "device_type": 0,
                "device_model": "",
                "ad_id": null,
                "tags": {
                },
                "last_active": 1395096859,
                "amount_spent": 0.0,
                "created_at": 1395096859,
                "invalid_identifier": false,
                "badge_count": 0
            }
        """
        # TODO: maybe make this easier by mapping their ints to words
        # So a user could run: onesignal.devices_create('ios', **data)
        try:
            device_type = int(device_type)
        except ValueError:
            raise OneSignalApiError('device_type must be an integer.')

        return self.post('players', **data)

    def devices_update(self, player_id, **data):
        """Update an existing device in one of your OneSignal apps.

        :param player_id: player_id of the device you want to update.

        Docs: https://documentation.onesignal.com/reference#edit-device

        :rtype: dict

        Usage::

          >>> onesignal.devices_update('a8c50012-7a78-492a-8a34-6bd3aa2e5f87', lang='es')
          >>> {'success': true}
        """
        return self.put('players/{}'.format(player_id), **data)

    def sessions_create(self, player_id, **data):
        """Update a device's session information.

        :param player_id: player_id of the device you want to create a session for.

        Docs: https://documentation.onesignal.com/reference#new-session

        :rtype: dict

        Usage::

          >>> onesignal.sessions_create('a8c50012-7a78-492a-8a34-6bd3aa2e5f87')
          >>> {'success': true}
        """
        return self.post('players/{}/on_session'.format(player_id), **data)

    def purchases_create(self, player_id, purchases=None, **data):
        """Track a new purchase in your app.

        :param player_id: player_id of the device you want to create a purchase for.
        :param purchases: An array of purchases with the following keys: sku, amount, iso

        Docs: https://documentation.onesignal.com/reference#new-purchase

        :rtype: dict

        Usage::

          >>> onesignal.sessions_create('a8c50012-7a78-492a-8a34-6bd3aa2e5f87')
          >>> {'success': true}
        """
        purchases = purchases or []
        data = data or {}

        for purchase in purchases:
            sku = purchase.get('sku')
            amount = purchase.get('amount')
            iso = purchase.get('iso')

            if not sku or not amount or not iso:
                raise OneSignalApiError('A purchase is missing a required field: {}'.format(json.dumps(purchase)))

        data.update({
            'purchases': purchases,
        })

        return self.post('players/{}/on_purchase'.format(player_id), **data)

    def sessions_length_update(self, player_id, active_time):
        """Track a new purchase in your app.

        :param player_id: player_id of the device you want to update the session length for.

        Docs: https://documentation.onesignal.com/reference#increment-session-length

        :rtype: dict

        Usage::

          >>> onesignal.sessions_create('a8c50012-7a78-492a-8a34-6bd3aa2e5f87', active_type=3600)
          >>> {'success': true}
        """
        data = {
            'state': 'ping',
            'active_time': active_time,
        }

        return self.post('players/{}/on_focus'.format(player_id), **data)

    def csv_export(self, **data):
        """Generate a compressed CSV export of all of your current user data.

        Docs: https://documentation.onesignal.com/reference#csv-export

        :rtype: dict

        Usage::

          >>> onesignal.csv_export('a8c50012-7a78-492a-8a34-6bd3aa2e5f87', active_type=3600)
          >>> {
                "csv_file_url": "https://onesignal.com/csv_exports/b2f7f966-d8cc-11e4-bed1-df8f05be55ba/users_184948440ec0e334728e87228011ff41_2015-11-10.csv.gz"
            }
        """
        return self.post('players/csv_export', **data)
