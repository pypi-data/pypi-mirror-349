import base64
import json
from typing import Optional

import requests


class RateHawkSDK:
    HOTEL_URI = 'https://api.worldota.net/api/b2b/v3'
    API_ID = '12677'
    API_KEY = 'bc24f4ac-817b-4a2f-9b71-95b21e0603cd'
    HEADERS = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic %s' % base64.b64encode(bytes(f'{API_ID}:{API_KEY}', 'utf-8')).decode('utf-8')
    }
    TOKEN = None
    LANGUAGE = None
    ENDPOINTS = {
        'HOTEL_SEARCH_AUTOCOMPLETE': f'{HOTEL_URI}/search/multicomplete/',
        'HOTEL_INFORMATION': f'{HOTEL_URI}/hotel/info/',
        'HOTEL_SEARCH_BY_REGION': f'{HOTEL_URI}/search/serp/region/',
        'HOTEL_SEARCH_BY_HOTEL': f'{HOTEL_URI}/search/serp/hotels/',
        'HOTEL_ORDER': f'{HOTEL_URI}/hotel/order/booking/form/',
        'HOTEL_PREBOOK': f'{HOTEL_URI}/hotel/prebook/',
        'HOTEL_PAGE': f'{HOTEL_URI}/search/hp/',
        'HOTEL_BOOKING_FINISH': f'{HOTEL_URI}/hotel/order/booking/finish/',
        'HOTEL_BOOKING_INFO': f'{HOTEL_URI}/hotel/order/info/',
        'HOTEL_BOOKING_CANCEL': f'{HOTEL_URI}/hotel/order/cancel/',
        'HOTEL_BOOKING_STATUS': f'{HOTEL_URI}/hotel/order/booking/finish/status/',
        'HOTEL_BOOKING_VOUCHER': f'{HOTEL_URI}/hotel/order/document/voucher/download/',
        'HOTEL_FULL_STATIC_DATA': f'{HOTEL_URI}/hotel/info/dump/',
        'HOTEL_INCREMENTAL_STATIC_DATA': f'{HOTEL_URI}/hotel/info/incremental_dump/',
        'REGION_FULL_STATIC_DATA': f'{HOTEL_URI}/hotel/region/dump/',
    }
    CURRENCY = 'USD'

    def __init__(self, lang='es'):
        self.LANGUAGE = lang.lower()

    @staticmethod
    def handle_error(response):
        data = response.json()
        if response.status_code != 200 or data.get('status') == 'error':
            if data.get('status') == 'error':
                message = [f"[{data.get('error')}]"]
                debug = data.get('debug', {})
                if debug and debug.get('validation_error'):
                    message += [data.get('debug', {}).get('validation_error')]
                return {'status': 400, 'message': '. '.join(message)}
        return None

    def autocomplete_search_hotel_criteria(self, text: str):
        json_data = {
            'query': 'test',
            'language': 'es'
        }
        response = requests.post(
            'https://api.worldota.net/api/b2b/v3/search/multicomplete/', data=json.dumps(json_data), timeout=1,
            headers=self.HEADERS
        )

        error = self.handle_error(response)
        if error:
            return error

        data = response.json().get('data', {})
        return {
            'hotels': data.get('hotels', []),
            'regions': data.get('regions', []),
        }

    def hotel_information(self, hotel_id: str):
        json_data = {
            'id': hotel_id,
            'language': self.LANGUAGE
        }
        response = requests.post(
            self.ENDPOINTS.get('HOTEL_INFORMATION'), data=json.dumps(json_data), headers=self.HEADERS
        )

        error = self.handle_error(response)
        if error:
            return error

        return response.json().get('data', {})

    def availability_by_region(self, start_date: str, end_date: str, region_id: int, guests: list,
                               residency: str = None):
        json_data = {
            'checkin': start_date,
            'checkout': end_date,
            'language': self.LANGUAGE,
            'guests': guests,
            'region_id': region_id,
            'currency': self.CURRENCY,
        }
        if residency:
            json_data['residency'] = residency

        response = requests.post(
            self.ENDPOINTS.get('HOTEL_SEARCH_BY_REGION'), data=json.dumps(json_data), headers=self.HEADERS
        )

        error = self.handle_error(response)
        if error:
            return error

        return {'status': 200, 'availability': response.json().get('data', {})}

    def availability_by_hotel(self, start_date: str, end_date: str, hotel_id: str, guests: list, residency: str = None):
        json_data = {
            'checkin': start_date,
            'checkout': end_date,
            'language': self.LANGUAGE,
            'guests': guests,
            'ids': [hotel_id],
            'currency': self.CURRENCY,
        }
        if residency:
            json_data['residency'] = residency

        response = requests.post(
            self.ENDPOINTS.get('HOTEL_SEARCH_BY_HOTEL'), data=json.dumps(json_data), headers=self.HEADERS
        )

        error = self.handle_error(response)
        if error:
            return error

        return {'status': 200, 'availability': response.json().get('data', {})}

    def order(self, offer_hash: str, partner_id: str, ip: str):
        json_data = {
            'partner_order_id': partner_id,
            'book_hash': offer_hash,
            'language': self.LANGUAGE,
            'user_ip': ip
        }

        response = requests.post(
            self.ENDPOINTS.get('HOTEL_ORDER'), data=json.dumps(json_data), headers=self.HEADERS
        )
        print(json.dumps(json_data))

        error = self.handle_error(response)
        if error:
            return error

        return {'status': 200, 'order': response.json().get('data', {})}

    def pre_order(self, offer_hash: str, price_increase_percent: int):
        json_data = {
            'hash': offer_hash,
            'price_increase_percent': price_increase_percent
        }
        print(json.dumps(json_data))
        response = requests.post(
            self.ENDPOINTS.get('HOTEL_PREBOOK'), data=json.dumps(json_data), headers=self.HEADERS
        )

        error = self.handle_error(response)
        if error:
            return error

        return {'status': 200, 'order': response.json().get('data', {})}

    def hotel_page(self, start_date: str, end_date: str, hotel_id: str, guests: list, residency: str = None):
        json_data = {
            'checkin': start_date,
            'checkout': end_date,
            'language': self.LANGUAGE,
            'guests': guests,
            'id': hotel_id,
            'currency': self.CURRENCY
        }
        if residency:
            json_data['residency'] = residency
        print(json.dumps(json_data))
        response = requests.post(
            self.ENDPOINTS.get('HOTEL_PAGE'), data=json.dumps(json_data), headers=self.HEADERS
        )

        error = self.handle_error(response)
        if error:
            return error

        return {'status': 200, 'hotel': response.json().get('data', {})}

    def hotel_booking_finish(self, partner_order_id: str, user_email: str, user_phone: str,
                             contact_info_first_name: str, contact_info_last_name: str, contact_info_phone: str,
                             contact_info_email: str, payment_type: str, payment_amount: str, guests: list,
                             comment: Optional[str] = ''):
        json_data = {
            "user": {
                'email': user_email,
                'comment': comment,
                'phone': user_phone
            },
            'supplier_data': {
                'first_name_original': contact_info_first_name,
                'last_name_original': contact_info_last_name,
                'phone': contact_info_phone,
                'email': contact_info_email
            },
            'partner': {
                'partner_order_id': partner_order_id,
            },
            'language': self.LANGUAGE,
            'rooms': guests,
            'upsell_data': [],
            'payment_type': {
                'type': payment_type,
                'amount': payment_amount,
                'currency_code': self.CURRENCY
            }
        }

        response = requests.post(
            self.ENDPOINTS.get('HOTEL_BOOKING_FINISH'), data=json.dumps(json_data), headers=self.HEADERS
        )
        print(json.dumps(json_data))

        error = self.handle_error(response)
        if error:
            return error

        return {'status': 200, 'success': response.json().get('status') == 'ok'}

    def hotel_booking_info(self, partner_order_id: str):
        json_data = {
            'ordering': {
                'ordering_type': 'desc',
                'ordering_by': 'created_at'
            },
            'pagination': {
                'page_size': '10',
                'page_number': '1'
            },
            'search': {
                'partner_order_ids': [partner_order_id]
            },
            'language': self.LANGUAGE
        }

        response = requests.post(
            self.ENDPOINTS.get('HOTEL_BOOKING_INFO'), data=json.dumps(json_data), headers=self.HEADERS
        )

        error = self.handle_error(response)
        if error:
            return error

        return {'status': 200, 'hotel': response.json().get('data', {})}

    def hotel_booking_cancel(self, partner_order_id: str):
        json_data = {
            'partner_order_id': partner_order_id
        }

        response = requests.post(
            self.ENDPOINTS.get('HOTEL_BOOKING_CANCEL'), data=json.dumps(json_data), headers=self.HEADERS
        )

        error = self.handle_error(response)
        if error:
            return error

        return {'status': 200, 'hotel': response.json().get('data', {})}

    def hotel_booking_status(self, partner_order_id: str):
        json_data = {
            'partner_order_id': partner_order_id
        }

        response = requests.post(
            self.ENDPOINTS.get('HOTEL_BOOKING_STATUS'), data=json.dumps(json_data), headers=self.HEADERS
        )

        error = self.handle_error(response)
        if error:
            return error

        return {'status': 200, 'hotel': response.json().get('data', {})}

    def hotel_booking_voucher(self, partner_order_id: str):
        return {'status': 200, 'url': self.ENDPOINTS.get('HOTEL_BOOKING_VOUCHER'), 'partner_order_id': partner_order_id,
                'language': self.LANGUAGE}

    def hotel_full_dump(self):
        json_data = {
            'language': self.LANGUAGE,
            'inventory': 'all',
        }

        response = requests.post(
            self.ENDPOINTS.get('HOTEL_FULL_STATIC_DATA'), data=json.dumps(json_data), headers=self.HEADERS
        )

        error = self.handle_error(response)
        if error:
            return error

        return {'status': 200, 'data': response.json().get('data', {})}

    def hotel_incremental_dump(self):
        json_data = {
            'language': self.LANGUAGE,
            'inventory': 'all',
        }

        response = requests.post(
            self.ENDPOINTS.get('HOTEL_INCREMENTAL_STATIC_DATA'), data=json.dumps(json_data), headers=self.HEADERS
        )

        error = self.handle_error(response)
        if error:
            return error

        return {'status': 200, 'data': response.json().get('data', {})}

    def region_full_dump(self):
        json_data = {}

        response = requests.post(
            self.ENDPOINTS.get('REGION_FULL_STATIC_DATA'), data=json.dumps(json_data), headers=self.HEADERS
        )

        error = self.handle_error(response)
        if error:
            return error

        return {'status': 200, 'data': response.json().get('data', {})}
