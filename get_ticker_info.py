import re
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests


def get_ticker_info(tickers):
    with ThreadPoolExecutor() as executor:
        futures = {}

        for ticker in tickers:
            url = f"https://www.marketwatch.com/investing/stock/{ticker}"
            futures[executor.submit(requests.get, url)] = ticker

    tickers = []

    for future in as_completed(futures):
        response = future.result().text

        try:
            price = float(re.search(r'"price" content="\$(.*?)"', response).group(1))
        except Exception:
            continue

        name = re.search(r'"name" content="(.*?)"', response).group(1)
        changes = float(re.search(r'"priceChange" content="(.*?)"', response).group(1))

        tickers.append(
            {
                "name": name,
                "changes": changes,
                "symbol": futures[future],
                "price": price,
            }
        )

    tickers.sort(key=lambda ticker: ticker["symbol"])

    return tickers[:9]
