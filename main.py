import requests
from datetime import datetime, timedelta
from twilio.rest import Client
import smtplib

# APIs
NEWS_API_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API_KEY = "d74d788355b84532809fb82f7650c795"

STOCK_API_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_API_KEY = "6QPRDLN1E85O2DVA"

# twillio


company = "Tesla Inc"
company_symbol = "TSLA"

# smtplib
SENDER_EMAIL = "tohirjon060821@gmail.com"
RECEIVER = "itsmetohir@gmail.com"
PASSWORD = "rbaz qcsh kuab crot"

# ---------------- NEWS ---------------- #
news_params = {
    "q": company,
    "apiKey": NEWS_API_KEY,
    "searchIn": "description"
}

news_response = requests.get(url=NEWS_API_ENDPOINT, params=news_params)
news_response.raise_for_status()
news_data = news_response.json()["articles"][0]
news_message = f"{news_data["title"]}\n{news_data["description"]}\nSource >>> {news_data["url"]}"

# ---------------- STOCKS ---------------- #

stock_params = {
    "function": "TIME_SERIES_INTRADAY",
    "interval": "60min",
    "symbol": company_symbol,
    "apikey": STOCK_API_KEY,
    "outputsize": "compact"
}

yesterday = str(datetime.today() - timedelta(days=1))[:10]

stock_response = requests.get(url=STOCK_API_ENDPOINT, params=stock_params)
stock_response.raise_for_status()
# print(stock_response.json())
stock_data_open = stock_response.json()["Time Series (60min)"][f"{yesterday} 19:00:00"]["1. open"]
stock_data_close = stock_response.json()["Time Series (60min)"][f"{yesterday} 04:00:00"]["4. close"]

difference = round((float(stock_data_open) - float(stock_data_close)), 2)
dif_percent = round(abs(difference) / float(stock_data_open) * 100)

news_message = f"Subject: Stock market change!\n{company} stocks {"🔺" if difference > 0 else "🔻"} {dif_percent}%\n" + news_message
news_message = news_message.encode('ascii', 'ignore').decode('ascii')

# ---------------- EMAIL -------------- #

if dif_percent >= 5:
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=SENDER_EMAIL, password=PASSWORD)
        connection.sendmail(from_addr=SENDER_EMAIL,
                            to_addrs=RECEIVER,
                            msg=news_message)

# ---------------- SMS ---------------- #
print(dif_percent)
print(news_message)
# if dif_percent >= 5:
#     client = Client(account_sid, auth_token)
#     message = client.messages.create(
#         body=news_message,
#         from_='+12565402717',
#         to='+998334121086'
#     )
#     print(message.status)
