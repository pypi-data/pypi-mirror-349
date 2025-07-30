from datetime import timedelta, datetime

import requests
from django.conf import settings

from ardhi_framework.utils import refine_user

CACHE_EXP = timedelta(minutes=10)
CACHE = {'exp': datetime.now() + CACHE_EXP, 'user_ids': {}}

ACL_BASE_URL = settings.SERVICE_URLS['ACL_BASE_URL']
INVOICE_URL = settings.SERVICE_URLS['PAYMENT_SERVICE_URL']
NOTIFICATIONS_URL = settings.SERVICE_URLS['SHARED_SERVER_URL']
SHARED_SERVER_URL = settings.SERVICE_URLS['SHARED_SERVER_URL']

REGISTRATION_SERVICE = settings.SERVICE_URLS['REGISTRATION_SERVICE']


def check_authenticated(headers):
    url = ACL_BASE_URL + 'auth/' + 'status'

    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        return True
    else:
        return False


def get_user_profile(user_id, headers):
    url = ACL_BASE_URL + 'accounts/userminiprofiledetails'
    param = {
        'userid': user_id
    }
    try:
        profile_response = requests.get(url=url, headers=headers, params=param)
    except requests.exceptions.RequestException as e:
        return False
    if profile_response.status_code == 200:
        user_details = profile_response.json()
        user_details['is_refined'] = False
        return refine_user(user_details)
    else:
        return False


def get_document_details(doc_id, headers):
    url = SHARED_SERVER_URL + 'file-upload/document-detail'

    params = {
        'doc_id': doc_id
    }
    try:
        response = requests.get(url=url, params=params, headers=headers)
    except requests.exceptions.RequestException as e:
        return False

    if response.status_code == 200:
        return response.json()
    else:
        return False


def get_document_link(doc_id, headers):
    doc_details = get_document_details(
        doc_id=doc_id,
        headers=headers
    )
    if not doc_details:
        return None
    else:
        return doc_details['file']


def registration_property_details(headers, property_number):
    url = settings.SERVICE_URLS['REGISTER_SERVICE'] + 'registration-generic/property-details/get_property_details'
    response = requests.get(
        url=url,
        params={
            'property_number': property_number
        },
        headers=headers
    )
    if response.status_code == 200:
        return True, response.json()
    else:
        try:
            return False, response.json()
        except:
            return False, {
                "details": f"There was an error getting property details for this {property_number}. Please try again later"}


def survey_details(headers, parcel_number):
    url = settings.SERVICE_URLS['CADASTRE_SERVICE_URL'] + 'routing/property/status'
    response = requests.get(
        url=url,
        params={
            'property_number': parcel_number
        },
        headers=headers
    )
    if response.status_code == 200:
        return response.json()
    else:
        return False


def get_land_admin_ingestion_parcels(parcel_number, headers):
    url = settings.SERVICE_URLS['LEASE_SERVICE'] + "lease/get-parcel-status"

    try:
        response = requests.get(
            url=url,
            params={"parcel_number": parcel_number},
            headers=headers
        )
    except requests.exceptions.RequestException as e:
        return False

    if response.status_code == 200:
        return response.json()
    else:
        return False


def get_parcel_invoices_status(parcel_number, invoice_status=None, page_size=5, headers=None, multiple_status=None):
    url = INVOICE_URL + 'invoicing'
    params = {
        'parcel_number': parcel_number,
        'invoice_status': invoice_status,
        'page_size': page_size,
        'multiple_status': multiple_status
    }
    try:
        invoice_response = requests.get(url=url, params=params, headers=headers)
    except requests.exceptions.RequestException as e:
        return False
    if invoice_response.status_code == 200:
        return invoice_response.json()
    else:
        return False


