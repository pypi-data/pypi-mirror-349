import logging
import urllib.parse

import requests
from requests import Response

from coin_sdk.common.securityservice import SecurityService
from coin_sdk.common.sendrequest import ErrorHandler
from coin_sdk.number_portability.domain import ConfirmationStatus, MessageType
from coin_sdk.number_portability.messages.common import ErrorMessages

logger = logging.getLogger(__name__)


class NumberPortabilityErrorHandler(ErrorHandler):

    def error_message_to_object(self, error_message):
        ErrorMessages(error_message.transactionId, error_message.errors)

    def on_connection_error(self, status: int, description: str, response: Response):
        raise requests.ConnectionError(f'HTTP Status: {status}, {description}', response=response)

    def on_not_found(self, error_object, response: Response):
        pass

    def on_other_error(self, status: int, description: str, response: Response):
        raise requests.HTTPError(f'HTTP Status: {status}, {description}', response=response)


def get_stream(url: str, offset: int, confirmation_status: ConfirmationStatus, message_types: [MessageType], security_service: SecurityService):
    params = {
        'offset': offset,
        'messageTypes': message_types and ','.join([message_type.value for message_type in message_types]),
        'confirmationStatus': confirmation_status and confirmation_status.value
    }
    params = {k: v for k, v in params.items() if v is not None}
    full_url = f'{url}?{urllib.parse.urlencode(params)}'

    headers = security_service.generate_headers(full_url)
    cookie = security_service.generate_jwt()
    return requests.get(full_url, stream=True, headers=headers, cookies=cookie, timeout=(15,25))
