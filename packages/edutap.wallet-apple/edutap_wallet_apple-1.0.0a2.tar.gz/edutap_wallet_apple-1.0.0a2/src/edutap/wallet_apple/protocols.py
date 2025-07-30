# pylint: disable=too-few-public-methods
from .models import handlers
from typing import Protocol
from typing import runtime_checkable


@runtime_checkable
class PassRegistration(Protocol):
    """
    Protocol definition for an injectable PassRegistration handler.
    It will be used by the webservice to handle pass registration.
    """

    async def register_pass(
        self,
        device_libray_id: str,
        pass_type_id: str,
        serial_number: str,
        push_token: handlers.PushToken | None,
    ) -> None:
        """
        see https://developer.apple.com/documentation/walletpasses/register-a-pass-for-update-notifications
        """

    async def unregister_pass(
        self, device_library_id: str, pass_type_id: str, serial_number: str
    ) -> None:
        """
        see https://developer.apple.com/documentation/walletpasses/unregister-a-pass-for-update-notifications
        """


@runtime_checkable
class PassDataAcquisition(Protocol):
    """
    Protocol definition for an injectable PassDataAcquisition handler
    """

    async def get_pass_data(
        self, *, pass_type_id: str | None, serial_number: str, update: bool = False
    ) -> handlers.PassData:
        """
        Fetches pass creation data from the database
        is called by the Edutap Apple Provider upon creation of a new pass

        :param pass_type_id: the pass type identifier
        :param serial_number: the serial number of the pass
        :param update: if True the pass data is updated, this is normally true
            when this function is invoked by the apple phone

        """

    async def get_push_tokens(
        self, device_library_id: str | None, pass_type_id: str, serial_number: str
    ) -> list[handlers.PushToken]:
        """
        called during pass update,
        returns a push token
        see https://developer.apple.com/documentation/walletpasses/pushtoken
        and https://developer.apple.com/documentation/usernotifications/sending-notification-requests-to-apns
        XXX: device_library_id appears to always be None, double check and
            remove from plugin contract if so
        """

    async def get_update_serial_numbers(
        self, device_library_id: str, pass_type_id: str, last_updated: str | None = None
    ) -> handlers.SerialNumbers:
        """
        Fetches the serial numbers of the passes that have been updated since the last update
        see https://developer.apple.com/documentation/walletpasses/get-the-list-of-updatable-passes
        """

    async def check_authentication_token(
        self, pass_type_id: str | None, serial_number: str | None, token: str
    ) -> bool:
        """
        checks if a given authentication token is valid
        """


@runtime_checkable
class Logging(Protocol):
    """
    Protocol definition for a logging handler
    """

    async def log(self, entries: handlers.LogEntries) -> None:
        """
        see https://developer.apple.com/documentation/walletpasses/log-a-message
        """
