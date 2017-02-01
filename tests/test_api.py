import responses
import unittest

import uuid

from onesignal import OneSignal

class OneSignalApiTestCase(unittest.TestCase):
    def setUp(self):
        self.onesignal = OneSignal('', '')
        self.app_id = str(uuid.uuid4())
        self.notification_id = str(uuid.uuid4())
        self.player_id = str(uuid.uuid4())

    @responses.activate
    def test_notifications(self):
        _json = {
            'total_count': 1,
            'limit': 50,
            'notifications': [{
                'isSafari': False,
                'big_picture': None,
                'filters': None,
                'chrome_icon': None,
                'ios_badgeType': None,
                'app_id': self.app_id,
                'amazon_background_data': None,
                'canceled': False,
                'android_led_color': None,
                'headings': {},
                'ios_category': None,
                'ttl': None,
                'web_buttons': None,
                'id': self.notification_id,
                'contents': {
                    'en': 'English Message'
                },
                'buttons': None,
                'isFirefox': False,
                'isAdm': False,
                'ios_badgeCount': None,
                'android_sound': None,
                'failed': 0,
                'send_after': 1485885004,
                'delayed_option': None,
                'adm_big_picture': None,
                'wp_wns_sound': None,
                'firefox_icon': None,
                'android_accent_color': None,
                'chrome_big_picture': None,
                'adm_group': None,
                'ios_sound': None,
                'adm_group_message': None,
                'android_group': None,
                'adm_sound': None,
                'tags': None,
                'successful': 1,
                'android_group_message': None,
                'wp_sound': None,
                'include_player_ids': [self.player_id],
                'isWP_WNS': False,
                'small_icon': None,
                'adm_large_icon': None,
                'data': None,
                'errored': 0,
                'android_visibility': None,
                'isIos': True,
                'large_icon': None,
                'delivery_time_of_day': None,
                'url': None,
                'queued_at': 1485885004,
                'isAndroid': False,
                'excluded_segments': [],
                'isChrome': False,
                'remaining': 0,
                'adm_small_icon': None,
                'converted': 0,
                'chrome_web_icon': None,
                'content_available': None,
                'isChromeWeb': False,
                'isWP': False,
                'included_segments': [],
                'template_id': None,
                'priority': None
            }]
        }

        responses.add(
            responses.GET,
            self.onesignal.construct_api_url('notifications'),
            json=_json,
            status=200,
            content_type='application/json',
        )

        response = self.onesignal.notifications()
        self.assertEqual(response['total_count'], 1)
        self.assertEqual(response['notifications'][0]['id'], self.notification_id)


    @responses.activate
    def test_apps(self):
        _json = [
            {
                'id': self.app_id,
                'name': 'Your app 1',
                'players': 150,
                'messagable_players': 143,
                'updated_at': '2014-04-01T04:20:02.003Z',
                'created_at': '2014-04-01T04:20:02.003Z',
                'gcm_key': 'a gcm push key',
                'chrome_key': 'A Chrome Web Push GCM key',
                'chrome_web_origin': 'Chrome Web Push Site URL',
                'chrome_web_gcm_sender_id': 'Chrome Web Push GCM Sender ID',
                'chrome_web_default_notification_icon': 'http://yoursite.com/chrome_notification_icon',
                'chrome_web_sub_domain': 'your_site_name',
                'apns_env': 'sandbox',
                'apns_certificates': 'Your apns certificate',
                'safari_apns_cetificate': 'Your Safari APNS certificate',
                'safari_site_origin': 'The homename for your website for Safari Push, including http or https',
                'safari_push_id': 'The certificate bundle ID for Safari Web Push',
                'safari_icon_16_16': 'http://onesignal.com/safari_packages/92911750-242d-4260-9e00-9d9034f139ce/16x16.png',
                'safari_icon_32_32': 'http://onesignal.com/safari_packages/92911750-242d-4260-9e00-9d9034f139ce/16x16@2.png',
                'safari_icon_64_64': 'http://onesignal.com/safari_packages/92911750-242d-4260-9e00-9d9034f139ce/32x32@2x.png',
                'safari_icon_128_128': 'http://onesignal.com/safari_packages/92911750-242d-4260-9e00-9d9034f139ce/128x128.png',
                'safari_icon_256_256': 'http://onesignal.com/safari_packages/92911750-242d-4260-9e00-9d9034f139ce/128x128@2x.png',
                'site_name': 'The URL to your website for Web Push',
                'basic_auth_key': 'NGEwMGZmMjItY2NkNy0xMWUzLTk5ZDUtMDAwYzI5NDBlNjJj'
            }
        ]

        responses.add(
            responses.GET,
            self.onesignal.construct_api_url('apps'),
            json=_json,
            status=200,
            content_type='application/json',
        )

        response = self.onesignal.apps()

        self.assertEqual(len(response), 1)
        self.assertEqual(response[0]['id'], self.app_id)
