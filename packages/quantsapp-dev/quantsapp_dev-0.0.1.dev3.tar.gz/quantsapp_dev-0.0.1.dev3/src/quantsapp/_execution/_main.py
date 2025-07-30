# Built-in Modules
import sys
import json
import base64
import typing
import atexit
import secrets
import threading
import functools
import contextlib
import datetime as dt
import collections.abc

from dataclasses import dataclass
from urllib.parse import urlparse, urlencode


# Third-Party Modules
from pydantic import ValidationError


# Local Modules
from quantsapp import _models as generic_models
from quantsapp._websocket._models import (
    BrokerOrderUpdateWsData_Pydantic,
)

from quantsapp._execution._models import (
    QappRawSessionData_Type,

    BrokerClient_Pydantic,
)

from quantsapp._execution._modules._broker_login_data import BrokerLoginData
from quantsapp._version import __version__ as qapp_package_version
from quantsapp._logger import qapp_logger
from quantsapp._master_data import MasterData

from quantsapp import (
    _utils as generic_utils,
    _enums as generic_enums,
    exceptions as generic_exceptions,
)

from quantsapp._websocket._options_main_ws import OptionsMainWebsocket
from quantsapp._websocket._options_broker_order_updates_ws import OptionsBrokerOrderUpdatesWebsocket
from quantsapp._execution import _enums as execution_enums


# Execution Modules
from quantsapp._execution._modules._broker_add import AddBroker
from quantsapp._execution._modules._broker_delete import DeleteBroker
from quantsapp._execution._modules._broker_list import GetBrokers, GetMappedBrokers
# from quantsapp._execution._modules._book_update import OrderBookUpdate
from quantsapp._execution._modules._order_list import GetOrders
from quantsapp._execution._modules._order_place import PlaceOrder
from quantsapp._execution._modules._order_logs import GetOrderLogs
from quantsapp._execution._modules._order_modify import ModifyOrder
from quantsapp._execution._modules._order_cancel import CancelOrders, CancelAllOrders
from quantsapp._execution._modules._position_list import GetPositions, GetPositionsCombined
from quantsapp._execution._modules._broker_ws_conn import BrokerWsConnectionStatus, BrokerWsReConnect
from quantsapp._execution._modules._broker_list_models import (
    PayloadListAvailableBrokers_Pydantic,
    ResponseListAvailableBrokers_Pydantic,

    PayloadListMappedBrokers_Pydantic,
    ResponseListMappedBrokers_Pydantic,
)
from quantsapp._execution._modules._broker_add_models import (
    PayloadBrokerLoginCredentials_Type,
    # PayloadDhanBrokerLoginCredentials_Type,
    # PayloadChoiceBrokerLoginCredentials_Type,

    PayloadDhanBrokerLoginCredentials_Pydantic,
    PayloadChoiceBrokerLoginCredentials_Pydantic,

    PayloadAddBroker_Pydantic,
    ResponseAddBroker_Pydantic,
)
from quantsapp._execution._modules._broker_delete_models import (
    PayloadDeleteBroker_Pydantic,
    ResponseDeleteBroker_Pydantic,
)
from quantsapp._execution._modules._order_list_models import (
    PayloadListOrdersFilters_Type,

    PayloadListOrders_Pydantic,
    PayloadListOrdersFilters_Pydantic,

    ResponseListOrders_Pydantic,
)
from quantsapp._execution._modules._order_place_models import (
    PayloadPlaceOrderBrokerAccounts_Type,
    PayloadPlaceOrderLeg_Type,

    PayloadPlaceOrder_Pydantic,
    PayloadPlaceOrderBrokerAccounts_Pydantic,
    PayloadPlaceOrderLeg_Pydantic,

    ResponsePlaceOrder_Pydantic,
)
from quantsapp._execution._modules._order_modify_models import (
    PayloadModifyOrder_Pydantic,
    ResponseModifyOrder_Pydantic,
)
from quantsapp._execution._modules._order_cancel_models import (
    PayloadCancelOrder_Type,
    PayloadCancelOrderIds_Pydantic,
    PayloadCancelIndividualBrokerOrder_Pydantic,
    PayloadCancelOrders_Pydantic,
    ResponseCancelOrders_Pydantic,

    PayloadCancelAllOrders_Pydantic,
    ResponseCancelAllOrders_Pydantic,
)
from quantsapp._execution._modules._position_list_models import (
    PayloadGetPositions_Type,
    PayloadGetPositions_Pydantic,
    ResponseGetPositions_Pydantic,
    ResponseGetPositionsConsolidated_Pydantic,
)
from quantsapp._execution._modules._order_logs_models import (
    PayloadGetOrderLogs_Pydantic,
    ResponseGetOrderLogs_Pydantic,
)
from quantsapp._execution._modules._broker_ws_conn_models import (
    PayloadGetBrokerWebsocketConnectionStatus_Pydantic,
    ResponseGetBrokerWebsocketConnectionStatus_Pydantic,

    PayloadBrokerWebsocketReConnect_Pydantic,
    ResponseBrokerWebsocketReConnect_Pydantic,
)

from quantsapp._api_helper._main import ApiHelper

# ----------------------------------------------------------------------------------------------------

@dataclass
class Execution:

    session_id: str
    order_updates_callback: typing.Optional[collections.abc.Callable[[BrokerOrderUpdateWsData_Pydantic], typing.Any]] = None

    # ---------------------------------------------------------------------------

    def __post_init__(self) -> None:

        self.__connect_main_ws()

        self.__connect_broker_order_updates_ws()

        self.__preprocess()

    # ---------------------------------------------------------------------------

    def __connect_main_ws(self) -> None:
        """Connect to Options Websocket to get api data"""

        # TODO change this to config
        query_params = {
            'ws_msg_type': 'api_client_login',
            'api_jwt': self.session_id,
            'portal': 'api',
            'sub_portal': 'python_sdk',
            'python_version': sys.version,
            'version': qapp_package_version,
            'country': 'in',
            # 'master_data': '1',
            'uid': generic_utils.get_mac_address(),
            'ref_id': f"{dt.datetime.now(dt.UTC):%d%m%Y}-{secrets.token_urlsafe(16)}",
        }

        url = self.__main_ws_url
        url = 'wss://server-uat.quantsapp.com'  # TODO remove this after made the code live

        url += ('&' if urlparse(url).query else '?') + urlencode(query_params)


        _ws_conn_condition = threading.Condition()
        self.ws_main = OptionsMainWebsocket(
            url=url,
            ws_conn_cond=_ws_conn_condition,
        )

        with _ws_conn_condition:
            self.ws_main.start()
            _ws_conn_condition.wait()

        # On exiting the python code, close the main ws
        # TODO change the logic of handling the ws connections
        atexit.register(self.__close_ws)

    # ---------------------------------------------------------------------------

    def __connect_broker_order_updates_ws(self) -> None:
        """Connect to Broker Order updates websocket to get Realtime order updates"""

        if not self.__should_connect_broker_order_updates_ws():
            return None

        query_params = {
            'ws_msg_type': 'etoken',
            'etoken': self.ws_main.ws_session_data['etoken'],
            'portal': 'api',
            'sub_portal': 'python_sdk',
            'python_version': sys.version,
            'version': qapp_package_version,
            'country': 'in',
            'uid': generic_utils.get_mac_address(),
            'ref_id': f"{dt.datetime.now(dt.UTC):%d%m%Y}-{secrets.token_urlsafe(16)}",
        }

        url = self.__broker_order_updates_ws_url
        url = 'wss://server-uat.quantsapp.com/order-updates'  # TODO remove this after made the code live

        url += ('&' if urlparse(url).query else '?') + urlencode(query_params)


        _ws_conn_condition = threading.Condition()
        self.ws_broker_orders = OptionsBrokerOrderUpdatesWebsocket(
            url=url,
            ws_conn_cond=_ws_conn_condition,
            order_updates_callback=self.order_updates_callback, # type: ignore
        )

        with _ws_conn_condition:
            self.ws_broker_orders.start()
            _ws_conn_condition.wait()

    # ---------------------------------------------------------------------------

    def __should_connect_broker_order_updates_ws(self) -> bool:
        """Check whether to Connect Broker Order updates websocket to get Realtime order updates"""

        if not self.order_updates_callback:
            qapp_logger.debug(f"Broker Update Callback func not passed, so don't need to connect to {OptionsBrokerOrderUpdatesWebsocket.__name__}")
            return False

        if not OptionsBrokerOrderUpdatesWebsocket.should_connect_broker_order_updates_ws():
            qapp_logger.debug(f"Trading not allowed, so don't need to connect to {OptionsBrokerOrderUpdatesWebsocket.__name__}")
            return False

        return True

    # ---------------------------------------------------------------------------

    @property
    def __main_ws_url(self) -> str:
        """Parse and get the main ws url from session id"""

        return self.__qapp_raw_session_data['ws']

    # ---------------------------------------------------------------------------

    @property
    def __broker_order_updates_ws_url(self) -> str:
        """Parse and get the Broker Order Updates ws url from session id"""

        return self.__qapp_raw_session_data['ws_order_updates']

    # ---------------------------------------------------------------------------

    @functools.cached_property
    def __qapp_raw_session_data(self) -> QappRawSessionData_Type:
        """Parse the raw session data from session_id and return it"""

        return json.loads(base64.b64decode(self.session_id.split('.')[1]))['qapp']

    # ---------------------------------------------------------------------------

    def __close_ws(self) -> None:

        _close_ws = ('ws_main', 'ws_broker_orders')

        for ws_name in _close_ws:
            with contextlib.suppress(Exception):
                if hasattr(self, ws_name):
                    getattr(self, ws_name).close_ws()

    # ---------------------------------------------------------------------------

    def __preprocess(self) -> None:
        """Do preprocess after connected to websocket"""

        self._api_helper = ApiHelper(ws=self.ws_main)

        # Master data should be processed first, 
        # as it is the based for all other preprocessing
        self.__update_master_data()

        self.__update_get_available_brokers()

        # Invoke the api helper with consolidated requests
        self._api_helper.invoke_consolidated_api()

    # ---------------------------------------------------------------------------

    def __update_master_data(self) -> None:
        """Download and update master data to memory"""

        # Get the master data and push it to memory
        MasterData().update_master_data(
            api_helper=self._api_helper,
        )

    # ---------------------------------------------------------------------------

    def __update_get_available_brokers(self) -> None:
        """Download and update the broker login data to memory"""

        BrokerLoginData().update_broker_login_data(
            api_helper=self._api_helper,
        )

    # ---------------------------------------------------------------------------

    def _error_handling(
            self,
            error: ValidationError | generic_exceptions.QuantsappException | Exception,
            response: generic_models.BaseResponse_Pydantic,
        ) -> None:
        """Handle the error and add required response error data"""

        if isinstance(error, ValidationError):
            response.error.code = generic_enums.ErrorCodes.INVALID_INPUT
            response.error.msg = str(error)
        elif isinstance(error, generic_exceptions.QuantsappException):
            response.error.code = error.error_code
            response.error.msg = str(error)
        else:
            response.error.code = generic_enums.ErrorCodes.SDK_CODE_FAILURE
            response.error.msg = 'Something went wrong!'

    # ---------------------------------------------------------------------------

    def _response_post_process(self, response: generic_models.BaseResponse_Pydantic) -> None:
        """Do the final processing on Response object"""

        # Set the error as None, if its success
        if response.success is True:
            response.error = None

    # ---------------------------------------------------------------------------

    def list_available_brokers(self, name_type: typing.Literal['str', 'enum'] = 'enum') -> ResponseListAvailableBrokers_Pydantic:
        """list the brokers based on login mode (ui only & code based)"""

        # TODO make this 
        _resp = ResponseListAvailableBrokers_Pydantic(
            success=False,
        )
        try:
            _resp.body = GetBrokers(
                ws=self.ws_main,
                payload=PayloadListAvailableBrokers_Pydantic(
                    name_type=name_type,
                ),
            ).list_available_brokers()
            _resp.success = True
        except Exception as er:
            self._error_handling(er, _resp)
        self._response_post_process(_resp)

        return _resp

    # ---------------------------------------------------------------------------

    def list_mapped_brokers(
            self,
            resync_from_broker: bool = False,
            from_cache: bool = True,
        ) -> ResponseListMappedBrokers_Pydantic:
        """list the brokers based on login mode (ui only & code based)"""

        _resp = ResponseListMappedBrokers_Pydantic(
            success=False,
        )
        try:
            _resp.body = GetMappedBrokers(
                ws=self.ws_main,
                payload=PayloadListMappedBrokers_Pydantic(
                    resync_from_broker=resync_from_broker,
                    from_cache=from_cache,
                ),
            ).list_brokers()
            _resp.success = True
        except Exception as er:
            self._error_handling(er, _resp)
        self._response_post_process(_resp)

        return _resp

    # ---------------------------------------------------------------------------

    def add_broker(
            self,
            broker: execution_enums.Broker,
            login_credentials: PayloadBrokerLoginCredentials_Type,
            delete_previous_users: bool = False,
            update_owner: bool = False,
        ) -> ResponseAddBroker_Pydantic:
        """Add Broker account to Quantsapp"""

        _resp = ResponseAddBroker_Pydantic(
            success=False,
        )
        try:
            # Parse Login Credentials
            match broker:
                case execution_enums.Broker.DHAN:
                    _login_credentials = PayloadDhanBrokerLoginCredentials_Pydantic.model_validate(login_credentials)
                case execution_enums.Broker.CHOICE:
                    _login_credentials = PayloadChoiceBrokerLoginCredentials_Pydantic.model_validate(login_credentials)
                case _:
                    raise generic_exceptions.InvalidInputError(f"Invalid Broker ({broker}) for 'access_token' login!")

            _resp.body = AddBroker(
                ws=self.ws_main,
                payload=PayloadAddBroker_Pydantic(
                    broker=broker,
                    login_credentials=_login_credentials,
                    delete_previous_users=delete_previous_users,
                    update_owner=update_owner,
                ),
            ).login()
            _resp.success = True
        except Exception as er:
            self._error_handling(er, _resp)
        self._response_post_process(_resp)

        return _resp

    # ---------------------------------------------------------------------------

    def delete_broker(
            self,
            broker: execution_enums.Broker,
            client_id: str,
        ) -> ResponseDeleteBroker_Pydantic:
        """Delete the broker account from Quantsapp, if exists"""

        _resp = ResponseDeleteBroker_Pydantic(
            success=False,
        )

        try:
            _resp.body = DeleteBroker(
                ws=self.ws_main,
                payload=PayloadDeleteBroker_Pydantic(
                    broker_client=BrokerClient_Pydantic(
                        broker=broker,
                        client_id=client_id,
                    )
                )
            ).delete()
            _resp.success = True
        except Exception as er:
            self._error_handling(er, _resp)
        self._response_post_process(_resp)

        return _resp

    # ---------------------------------------------------------------------------

    def get_orders(
            self,
            broker: execution_enums.Broker,
            client_id: str,
            resync_from_broker: bool = False,
            from_cache: bool = True,
            ascending: bool = False,
            filters: typing.Optional[PayloadListOrdersFilters_Type] = None,
        ) -> ResponseListOrders_Pydantic:
        """Retreive the orders"""

        _resp = ResponseListOrders_Pydantic(
            success=False,
        )

        try:
            # Set default filter
            _filters: PayloadListOrdersFilters_Type = filters or {}  # type: ignore

            _resp.body = GetOrders(
                ws=self.ws_main,
                payload=PayloadListOrders_Pydantic(
                    broker_client=BrokerClient_Pydantic(
                        broker=broker,
                        client_id=client_id,
                    ),
                    ascending=ascending,
                    from_cache=from_cache,
                    resync_from_broker=resync_from_broker,
                    filters=PayloadListOrdersFilters_Pydantic(
                        product=_filters.get('product'),
                        order_status=_filters.get('order_status'),
                        order_type=_filters.get('order_type'),
                        instrument=_filters.get('instrument'),
                    ),
                ),
            ).get_orders()
            _resp.success = True
        except Exception as er:
            self._error_handling(er, _resp)
        self._response_post_process(_resp)
        return _resp

    # ---------------------------------------------------------------------------

    def place_order(
            self,
            broker_accounts: list[PayloadPlaceOrderBrokerAccounts_Type],
            product: execution_enums.OrderProductType,
            order_type: execution_enums.OrderType,
            validity: execution_enums.OrderValidity,
            legs: list[PayloadPlaceOrderLeg_Type],
            exchange: generic_enums.Exchange = generic_enums.Exchange.NSE_FNO,
            marigin_benefit: bool = True,
        ) -> ResponsePlaceOrder_Pydantic:
        """Place orders"""

        _resp = ResponsePlaceOrder_Pydantic(
            success=False,
        )
        try:
            _resp.body = PlaceOrder(
                ws=self.ws_main,
                order=PayloadPlaceOrder_Pydantic(
                    broker_accounts=[
                        PayloadPlaceOrderBrokerAccounts_Pydantic(
                            broker_client=BrokerClient_Pydantic(
                                broker=broker_account['broker'],
                                client_id=broker_account['client_id'],
                            ),
                            lot_multiplier=broker_account.get('lot_multiplier', 1)
                        )
                        for broker_account in broker_accounts
                    ],
                    exchange=exchange,
                    product=product,
                    order_type=order_type,
                    validity=validity,
                    legs=[
                        PayloadPlaceOrderLeg_Pydantic(
                            qty=leg['qty'],
                            price=leg['price'],
                            instrument=generic_models.Instrument_Pydantic.from_api_str(leg['instrument']),
                            transaction_type=leg['transaction_type'],
                            stop_price=leg.get('stop_price'),
                        )
                        for leg in legs
                    ],
                    marigin_benefit=marigin_benefit,
                ),
            ).place_order()
            _resp.success = True
        except Exception as er:
            self._error_handling(er, _resp)
        self._response_post_process(_resp)
        return _resp

    # ---------------------------------------------------------------------------

    def modify_order(
            self,
            broker: execution_enums.Broker,
            client_id: str,
            b_orderid: str,
            e_orderid: str,
            qty: int,
            price: float,
        ) -> ResponseModifyOrder_Pydantic:
        """Modify existing order"""

        _resp = ResponseModifyOrder_Pydantic(
            success=False,
        )
        try:
            _resp.body = ModifyOrder(
                ws=self.ws_main,
                order=PayloadModifyOrder_Pydantic(
                    broker_client=BrokerClient_Pydantic(
                        broker=broker,
                        client_id=client_id,
                    ),
                    b_orderid=b_orderid,
                    e_orderid=e_orderid,
                    qty=qty,
                    price=price,
                ),
            ).modify_order()
            _resp.success = True
        except Exception as er:
            self._error_handling(er, _resp)
        self._response_post_process(_resp)
        return _resp

    # ---------------------------------------------------------------------------

    def cancel_orders(
            self,
            orders_to_cancel: list[PayloadCancelOrder_Type],
        ) -> ResponseCancelOrders_Pydantic:
        """Cancel specific orders from specific broker accounts"""

        _resp = ResponseCancelOrders_Pydantic(
            success=False,
        )
        try:
            _resp.body = CancelOrders(
                ws=self.ws_main,
                payload=PayloadCancelOrders_Pydantic(
                    orders=[
                        PayloadCancelIndividualBrokerOrder_Pydantic(
                            broker_client=BrokerClient_Pydantic(
                                broker=order_to_cancel['broker'],
                                client_id=order_to_cancel['client_id'],
                            ),
                            order_ids=[
                                PayloadCancelOrderIds_Pydantic(
                                    b_orderid=order_id['b_orderid'],
                                    e_orderid=order_id['e_orderid'],
                                )
                                for order_id in order_to_cancel['order_ids']
                            ],
                        )
                        for order_to_cancel in orders_to_cancel
                    ],
                ),
            ).cancel_orders()
            _resp.success = True
        except Exception as er:
            self._error_handling(er, _resp)
        self._response_post_process(_resp)
        return _resp

    # ---------------------------------------------------------------------------

    def cancel_all_orders(
            self,
            broker: execution_enums.Broker,
            client_id: str,
        ) -> ResponseCancelAllOrders_Pydantic:
        """Cancel specific orders from specific broker accounts"""

        _resp = ResponseCancelAllOrders_Pydantic(
            success=False,
        )
        try:
            _resp.body = CancelAllOrders(
                ws=self.ws_main,
                payload=PayloadCancelAllOrders_Pydantic(
                    broker_client=BrokerClient_Pydantic(
                        broker=broker,
                        client_id=client_id,
                    ),
                ),
            ).cancel_all_orders()
            _resp.success = True
        except Exception as er:
            self._error_handling(er, _resp)
        self._response_post_process(_resp)
        return _resp

    # ---------------------------------------------------------------------------

    def get_positions(
            self,
            broker_clients: list[PayloadGetPositions_Type],
            resync_from_broker: bool = False,
            from_cache: bool = True,
        ) -> ResponseGetPositions_Pydantic:
        """Get positions combinely from the specific broker accounts"""

        _resp = ResponseGetPositions_Pydantic(
            success=False,
        )
        try:
            _resp.body = GetPositions(
                ws=self.ws_main,
                payload=PayloadGetPositions_Pydantic(
                    broker_clients=[
                        BrokerClient_Pydantic(
                            broker=broker_client['broker'],
                            client_id=broker_client['client_id'],
                        )
                        for broker_client in broker_clients
                    ],
                    resync_from_broker=resync_from_broker,
                    from_cache=from_cache,
                ),
            ).get_positions()
            _resp.success = True
        except Exception as er:
            self._error_handling(er, _resp)
        self._response_post_process(_resp)
        return _resp

    # ---------------------------------------------------------------------------

    def get_positions_combined(
            self,
            broker_clients: list[PayloadGetPositions_Type],
            resync_from_broker: bool = False,
            from_cache: bool = True,
        ) -> ResponseGetPositionsConsolidated_Pydantic:
        """Get positions combinely from the specific broker accounts"""

        _resp = ResponseGetPositionsConsolidated_Pydantic(
            success=False,
        )
        try:
            _resp.body = GetPositionsCombined(
                ws=self.ws_main,
                payload=PayloadGetPositions_Pydantic(
                    broker_clients=[
                        BrokerClient_Pydantic(
                            broker=broker_client['broker'],
                            client_id=broker_client['client_id'],
                        )
                        for broker_client in broker_clients
                    ],
                    resync_from_broker=resync_from_broker,
                    from_cache=from_cache,
                ),
            ).get_positions()
            _resp.success = True
        except Exception as er:
            self._error_handling(er, _resp)
        self._response_post_process(_resp)
        return _resp

    # ---------------------------------------------------------------------------

    def get_order_api_log(
            self,
            broker: execution_enums.Broker,
            client_id: str,
            instrument: generic_models.Instrument_Pydantic,
            q_usec: dt.datetime,
        ) -> ResponseGetOrderLogs_Pydantic:
        """Get specific order logs from broker end"""

        _resp = ResponseGetOrderLogs_Pydantic(
            success=False,
        )
        try:
            _resp.body = GetOrderLogs(
                ws=self.ws_main,
                payload=PayloadGetOrderLogs_Pydantic(
                    broker_client=BrokerClient_Pydantic(
                        broker=broker,
                        client_id=client_id,
                    ),
                    instrument=instrument,
                    q_usec=q_usec,
                ),
            ).get_logs()
            _resp.success = True
        except Exception as er:
            self._error_handling(er, _resp)
        self._response_post_process(_resp)
        return _resp

    # ---------------------------------------------------------------------------

    def get_broker_websocket_conn_status(
            self,
            broker: execution_enums.Broker,
            client_id: str,
        ) -> ResponseGetBrokerWebsocketConnectionStatus_Pydantic:
        """Get Broker websocket connection status"""

        _resp = ResponseGetBrokerWebsocketConnectionStatus_Pydantic(
            success=False,
        )
        try:
            _resp.body = BrokerWsConnectionStatus(
                ws=self.ws_main,
                payload=PayloadGetBrokerWebsocketConnectionStatus_Pydantic(
                    broker_client=BrokerClient_Pydantic(
                        broker=broker,
                        client_id=client_id,
                    ),
                ),
            ).get_status()
            _resp.success = True
        except Exception as er:
            self._error_handling(er, _resp)
        self._response_post_process(_resp)
        return _resp

    # ---------------------------------------------------------------------------

    def broker_websocket_reconnect(
            self,
            broker: execution_enums.Broker,
            client_id: str,
        ) -> ResponseBrokerWebsocketReConnect_Pydantic:
        """Force reconnect to broker ws"""

        _resp = ResponseBrokerWebsocketReConnect_Pydantic(
            success=False,
        )
        try:
            _resp.body = BrokerWsReConnect(
                ws=self.ws_main,
                payload=PayloadBrokerWebsocketReConnect_Pydantic(
                    broker_client=BrokerClient_Pydantic(
                        broker=broker,
                        client_id=client_id,
                    ),
                ),
            ).reconnect()
            _resp.success = True
        except Exception as er:
            self._error_handling(er, _resp)
        self._response_post_process(_resp)
        return _resp

    # ---------------------------------------------------------------------------

    # def update_order_book(self, payload: execution_models.UpdateOrderBook) -> ...:
    #     """Resync the order book data """

    #     return OrderBookUpdate(
    #         ws=self.ws_main,
    #         payload=payload,
    #     ).update()
