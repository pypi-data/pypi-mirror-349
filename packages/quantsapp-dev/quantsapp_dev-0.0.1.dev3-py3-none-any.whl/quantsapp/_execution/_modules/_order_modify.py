# Built-in Modules
import time
from dataclasses import dataclass


# Local Modules
from quantsapp._master_data import MasterData
from quantsapp import (
    exceptions as generic_exceptions,
    _utils as generic_utils,
)
from quantsapp._websocket._options_main_ws import OptionsMainWebsocket
from quantsapp._websocket import (
    _config as websocket_config,
)
from quantsapp._execution import (
    _cache as execution_cache,
    _enums as execution_enums,
)


from quantsapp._execution._modules._order_list_models import ResponseOrderListingData_Type
from quantsapp._execution._modules._order_modify_models import (
    ApiResponseModifyOrder_Type,

    PayloadModifyOrder_Pydantic,
)


# ----------------------------------------------------------------------------------------------------


@dataclass
class ModifyOrder:

    ws: OptionsMainWebsocket
    order: PayloadModifyOrder_Pydantic

    # ---------------------------------------------------------------------------

    def modify_order(self) -> str:
        """Modify the existing order"""

        self._validate_data()

        modify_order_resp: ApiResponseModifyOrder_Type = self.ws.invoke_api(
            # TODO try to make this more generic and take it from some config
            payload={
                'action': websocket_config.WsActionKeys.BROKER_ORDERS,
                'mode': 'modify_order',
                'broker_client': self.order.broker_client._api_str,  # type: ignore - private variable
                'b_orderid': self.order.b_orderid,
                'e_orderid': self.order.e_orderid,
                'order': {
                    'qty': self.order.qty,
                    'price': self.order.price
                }
            },
        ) # type: ignore

        if modify_order_resp['status'] != '1':
            raise generic_exceptions.BrokerOrdersPlacingFailed(modify_order_resp['msg'])

        # Wait for sometime, so that the order update will be recevied and update the modification on cache data
        # TODO check whether order update websocket is connected or not
        time.sleep(1)

        return 'Order Modified'

    # ---------------------------------------------------------------------------

    def _validate_data(self) -> None:
        """validate the data which can't be done from the pydantic level(may be due to circular import Error)"""

        if not generic_utils.MarketTimings.is_market_open():
            raise generic_exceptions.InvalidInputError('Market Closed')

        exist_order = self._get_existing_order()    

        self._validate_order_status(exist_order)
        self._validate_qty(exist_order)

    # ---------------------------------------------------------------------------

    def _validate_order_status(self, exist_order: ResponseOrderListingData_Type):

        if exist_order['order_status'] in (
            execution_enums.OrderStatus.CANCELLED,
            execution_enums.OrderStatus.COMPLETED,
            execution_enums.OrderStatus.FAILED,
            execution_enums.OrderStatus.REJECTED,
        ):
            raise generic_exceptions.InvalidInputError(f"Order already {exist_order['order_status']}")

    # ---------------------------------------------------------------------------

    def _validate_qty(self, exist_order: ResponseOrderListingData_Type):

        _lot_size: int = MasterData.master_data['symbol_data'][exist_order['instrument'].symbol]['lot_size'][exist_order['instrument'].expiry]

        if self.order.qty % _lot_size != 0:
            raise generic_exceptions.InvalidInputError(f"Invalid Qty, should be multiple of {_lot_size} for {exist_order['instrument'].symbol!r}")

    # ---------------------------------------------------------------------------

    def _get_existing_order(self) -> ResponseOrderListingData_Type:
        """Get the existing order from cache, if not found then try fetching from api again"""

        # TODO move this to generic area where it can be used by other modules

        _tmp_order_id_ref = f"{self.order.b_orderid}|{self.order.e_orderid}"

        if not (_exist_order_data := execution_cache.orders.get(self.order.broker_client, {}).get(_tmp_order_id_ref)):
            raise generic_exceptions.InvalidInputError('Broker Order Not found')

        return _exist_order_data