# Built-in Modules
from dataclasses import dataclass


# Local Modules
from quantsapp import (
    exceptions as generic_exceptions,
    _utils as generic_utils,
)
from quantsapp._websocket import (
    OptionsMainWebsocket,
    _config as websocket_config,
)
from quantsapp._execution import (
    _models as execution_models,
    _types as execution_types,
    _enums as execution_enums,
    _cache as execution_cache,
)
from quantsapp._execution._modules._order_list import GetOrders


# ----------------------------------------------------------------------------------------------------


@dataclass
class CancelOrders:

    ws: OptionsMainWebsocket
    payload: execution_models.CancelOrders

    # ---------------------------------------------------------------------------

    def cancel_orders(self) -> execution_types.CancelOrdersResponse:
        """Cancel pending orders"""

        self._validate_data()
        
        cancel_orders_resp: execution_types.CancelOrdersApiResponse = self.ws.invoke_api(
            # TODO try to make this more generic and take it from some config
            payload={
                'action': websocket_config.WsActionKeys.BROKER_ORDERS,
                'mode': 'cancel_orders',
                'order': {
                    order.broker_client._api_str: [  # type: ignore - private variable
                        {
                            'b_orderid': order_id.b_orderid,
                            'e_orderid': order_id.e_orderid,
                        }
                        for order_id in order.order_ids
                    ]
                    for order in self.payload.orders
                }
            },
        ) # type: ignore

        if cancel_orders_resp['status'] != '1':
            raise generic_exceptions.BrokerOrdersCancelFailed(cancel_orders_resp['msg'])
    
        return {
            'success': not cancel_orders_resp['has_failed'],
            'ref_id': cancel_orders_resp['q_ref_id_c'],
        }

    # ---------------------------------------------------------------------------
    
    def _validate_data(self) -> None:
        """validate the data which can't be done from the pydantic level(may be due to circular import Error)"""

        if not generic_utils.MarketTimings.is_market_open():
            raise generic_exceptions.InvalidInputError('Market Closed')

        for order in self.payload.orders:
            for order_id in order.order_ids:
                exist_order = self._get_existing_order(
                    broker_client=order.broker_client,
                    order_id=order_id,
                )
                self._validate_order_status(exist_order)

    # ---------------------------------------------------------------------------

    def _validate_order_status(self, exist_order: execution_types.OrderListingData):

        if exist_order['order_status'] in (
            execution_enums.OrderStatus.CANCELLED,
            execution_enums.OrderStatus.COMPLETED,
            execution_enums.OrderStatus.FAILED,
            execution_enums.OrderStatus.REJECTED,
        ):
            raise generic_exceptions.InvalidInputError(f"Order already {exist_order['order_status']}")

    # ---------------------------------------------------------------------------

    def _get_existing_order(self, broker_client: execution_models.BrokerClient, order_id: execution_models.CancelOrderIds) -> execution_types.OrderListingData:
        """Get the existing order from cache, if not found then try fetching from api again"""

        # TODO move this to generic area where it can be used by other modules
        
        _tmp_order_id_ref = f"{order_id.b_orderid}|{order_id.e_orderid}"

        _exist_order_data = execution_cache.orders.get(broker_client, {}).get(_tmp_order_id_ref)

        # Try fetch exist order from api one time to check if the user having the order or not
        # TODO don't get orders again for same broker client
        if not _exist_order_data:
            GetOrders(
                ws=self.ws,
                payload=execution_models.ListOrders(
                    broker_client=broker_client,
                    from_cache=False,
                )
            ).update_orders()

        _exist_order_data = execution_cache.orders.get(broker_client, {}).get(_tmp_order_id_ref)

        if not _exist_order_data:
            raise generic_exceptions.InvalidInputError('Broker Order Not found')

        return _exist_order_data

# ----------------------------------------------------------------------------------------------------


@dataclass
class CancelAllOrders:

    ws: OptionsMainWebsocket
    payload: execution_models.CancelAllOrders

    # ---------------------------------------------------------------------------

    def cancel_all_orders(self) -> execution_types.CancelOrdersResponse:
        """Cancel all pending orders belongs to specific broker account"""
        
        cancel_all_orders_resp: execution_types.CancelOrdersApiResponse = self.ws.invoke_api(
            # TODO try to make this more generic and take it from some config
            payload={
                'action': websocket_config.WsActionKeys.BROKER_ORDERS,
                'mode': 'cancel_orders',
                'cancel_all': True,
                'broker_client': self.payload.broker_client._api_str,  # type: ignore - private variable
            },
        ) # type: ignore

        if cancel_all_orders_resp['status'] != '1':
            raise generic_exceptions.BrokerOrdersCancelFailed(cancel_all_orders_resp['msg'])
    
        return {
            'success': cancel_all_orders_resp['has_failed'],
            'ref_id': cancel_all_orders_resp['q_ref_id_c'],
        }

    # ---------------------------------------------------------------------------

  