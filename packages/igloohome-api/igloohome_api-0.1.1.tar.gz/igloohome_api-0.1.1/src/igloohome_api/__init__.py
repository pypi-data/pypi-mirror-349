"""Library for accessing igloohome API"""
from typing import Optional

from dacite import from_dict

import aiohttp
import jwt
from dataclasses import dataclass

_OAUTH2_HOST = "https://auth.igloohome.co"
_OAUTH2_TOKEN_PATH = "/oauth2/token"
_OAUTH2_SCOPE_EVERYTHING = OAUTH2_SCOPE = ("igloohomeapi/algopin-hourly igloohomeapi/algopin-daily "
                                           "igloohomeapi/algopin-permanent igloohomeapi/algopin-onetime "
                                           "igloohomeapi/create-pin-bridge-proxied-job "
                                           "igloohomeapi/delete-pin-bridge-proxied-job "
                                           "igloohomeapi/lock-bridge-proxied-job "
                                           "igloohomeapi/unlock-bridge-proxied-job igloohomeapi/get-devices "
                                           "igloohomeapi/get-job-status igloohomeapi/get-properties")

_BASE_URL = "https://api.igloodeveloper.co"
_BASE_PATH = "igloohome"
_DEVICES_PATH_SEGMENT = "devices"


@dataclass
class LinkedDevice:
    type: str
    deviceId: str


@dataclass
class GetDeviceInfoResponse:
    id: str
    type: str
    deviceId: str
    deviceName: str
    pairedAt: str
    homeId: list[str]
    linkedDevices: list[LinkedDevice]
    batteryLevel: Optional[int]


@dataclass
class GetDevicesResponse:
    nextCursor: str
    payload: list[GetDeviceInfoResponse]


@dataclass
class CreateBridgeProxiedJobResponse:
    jobId: str


@dataclass
class GetJobStatusResponse:
    jobId: str
    expiryDate: str
    completed: bool
    jobType: str
    jobResponse: dict


BRIDGE_JOB_LOCK = 1
BRIDGE_JOB_UNLOCK = 2
BRIDGE_JOB_CREATE_CUSTOM_PIN = 4
BRIDGE_JOB_DELETE_CUSTOM_PIN = 5
BRIDGE_JOB_GET_BATTERY_LEVEL = 9
BRIDGE_JOB_GET_DEVICE_STATUS = 10
BRIDGE_JOB_GET_ACTIVITY_LOGS = 15

"""One of the possible GetDeviceInfoResponse.type values."""
DEVICE_TYPE_BRIDGE = "Bridge"
"""One of the possible GetDeviceInfoResponse.type values."""
DEVICE_TYPE_LOCK = "Lock"
"""One of the possible GetDeviceInfoResponse.type values."""
DEVICE_TYPE_KEYPAD = "Keypad"


class Auth:
    def __init__(
            self,
            session: aiohttp.ClientSession,
            client_id: str,
            client_secret: str,
            host: str = _OAUTH2_HOST,
            scope: str = _OAUTH2_SCOPE_EVERYTHING,
    ) -> None:
        self.access_token = None
        self.session = session
        self.client_id = client_id
        self.client_secret = client_secret
        self.host = host
        self.scope = scope

    async def async_get_access_token(self) -> str:
        form = aiohttp.FormData()
        form.add_field("grant_type", "client_credentials")
        form.add_field("scope", self.scope)
        response = await self.session.post(
            url=self.host + _OAUTH2_TOKEN_PATH,
            auth=aiohttp.BasicAuth(
                login=self.client_id, password=self.client_secret
            ),
            data=form,
        )
        json = await response.json()
        if response.status == 200:
            self.access_token = json["access_token"]
            return self.access_token
        else:
            raise AuthException(f'Failed to get access token. responseCode=${response.status}')

    async def async_get_valid_access_token(self) -> str:
        """Gets a valid access token."""
        if self.access_token is None:
            access_token = await self.async_get_access_token()
            return access_token
        elif is_access_token_valid(self.access_token):
            return self.access_token
        else:
            return await self.async_get_access_token()

    async def request(self, method: str, url: str, **kwargs) -> aiohttp.ClientResponse:
        """Make a request."""
        headers = kwargs.get("headers")

        if headers is None:
            headers = {}
        else:
            headers = dict(headers)

        headers["Authorization"] = f"Bearer {await self.async_get_valid_access_token()}"
        headers["Accept"] = "application/json"

        return await self.session.request(
            method, url, **kwargs, headers=headers,
        )


def is_access_token_valid(access_token: str) -> bool:
    """Check if the access token is valid."""
    try:
        # Expiry is automatically verified during decoding. Will raise ExpiredSignatureError.
        # See: https://pyjwt.readthedocs.io/en/stable/usage.html#expiration-time-claim-exp
        claims = jwt.decode(access_token, options={"require": ["exp"]})
    except Exception:
        return False


class AuthException(Exception):
    pass


class Api:
    def __init__(
            self,
            auth: Auth,
            host: str = _BASE_URL
    ):
        self.auth = auth
        self.host = host

    async def get_devices(self) -> GetDevicesResponse:
        response = await self.auth.request(
            "get",
            f'{self.host}/{_BASE_PATH}/{_DEVICES_PATH_SEGMENT}',
        )
        if response.status == 200:
            return from_dict(GetDevicesResponse, await response.json())
        else:
            raise ApiException("Response failure", response.status)

    async def get_device_info(self, deviceId: str) -> GetDeviceInfoResponse:
        response = await self.auth.request(
            "get",
            f'{self.host}/{_BASE_PATH}/{_DEVICES_PATH_SEGMENT}/{deviceId}',
        )
        if response.status == 200:
            return from_dict(GetDeviceInfoResponse, await response.json())
        else:
            raise ApiException("Response failure", response.status)

    async def create_bridge_proxied_job(
            self,
            deviceId: str,
            bridgeId: str,
            jobType: int,
            jobData: dict = None
    ) -> CreateBridgeProxiedJobResponse:
        response = await self.auth.request(
            "post",
            f'{self.host}/{_BASE_PATH}/{_DEVICES_PATH_SEGMENT}/{deviceId}/jobs/bridges/{bridgeId}',
            json={
                "jobType": jobType,
                "jobData": jobData,
            }
        )
        if response.status == 200:
            return from_dict(CreateBridgeProxiedJobResponse, await response.json())
        else:
            raise ApiException("Response failure", response.status)

    async def get_job_status(self, jobId: str) -> GetJobStatusResponse:
        response = await self.auth.request(
            "get",
            f'{self.host}/{_BASE_PATH}/jobs/{jobId}'
        )
        if response.status == 200:
            return from_dict(GetJobStatusResponse, await response.json())
        else:
            raise ApiException("Response failure", response.status)


class ApiException(Exception):
    def __init__(self, message: str, response_code: int):
        self.message = message
        self.response_code = response_code

    def __str__(self):
        return f'ApiException(message={self.message}, response_code={self.response_code})'


async def _create_exception(response: aiohttp.ClientResponse) -> ApiException:
    return ApiException(
        message=f'Unsuccessful request. code={response.status}, message={await response.text()}',
        response_code=response.status
    )
