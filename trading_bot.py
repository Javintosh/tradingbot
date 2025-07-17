import ccxt
from db import log_order
from time import sleep

class BingXTrader:
    def __init__(self):
        self.exchange = ccxt.bingx({
            'apiKey': BINGX_API_KEY,
            'secret': BINGX_SECRET_KEY,
            'options': {'adjustForTimeDifference': True}
        })

    def execute_order(self, symbol: str, side: str, amount: float, **kwargs):
        try:
            order = self.exchange.create_order(
                symbol=symbol,
                type='market',
                side=side,
                amount=amount
            )
            log_order(order, "MARKET", kwargs.get('sl'), kwargs.get('tp'))
            return order
        except Exception as e:
            raise Exception(f"Error en BingX: {str(e)}")

    def dca_strategy(self, symbol: str, side: str, total_amount: float, levels: int = 3):
        amount_per_level = total_amount / levels
        orders = []
        for _ in range(levels):
            orders.append(self.execute_order(symbol, side, amount_per_level))
            sleep(60)  # Espera 1 minuto entre órdenes
        return orders
