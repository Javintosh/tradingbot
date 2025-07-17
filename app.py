from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from trading_bot import BingXTrader
from config import WEBHOOK_API_KEY, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID
import requests
import logging

app = FastAPI()
bot = BingXTrader()
logging.basicConfig(filename='trades.log', level=logging.INFO)

def send_telegram(message: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload)

@app.post("/webhook")
async def handle_webhook(request: Request):
    try:
        data = await request.json()
        
        # Validar API Key
        if data.get("api_key") != WEBHOOK_API_KEY:
            raise HTTPException(status_code=403, detail="API Key inválida")

        # Ejecutar orden
        order = bot.execute_order(
            symbol=data["symbol"],
            side=data["side"],
            amount=float(data["amount"]),
            sl=data.get("sl"),
            tp=data.get("tp")
        )

        # Notificar a Telegram
        message = f"""
        � **Orden Ejecutada** ({data.get('strategy', 'MARKET')})
        - Par: {data['symbol']}
        - Tipo: {data['side'].upper()}
        - Cantidad: {data['amount']}
        """
        send_telegram(message)

        return JSONResponse({"status": "success", "order": order})

    except Exception as e:
        logging.error(f"Error: {e}")
        send_telegram(f"❌ **Error**: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
