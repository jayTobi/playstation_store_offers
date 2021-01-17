#%%
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import time

# TODO use input prompt or parameters for new URLs (number of pages), i.e. new offers
URL = "https://store.playstation.com/de-de/category/c8a32583-1a65-4e09-91ab-2a07023b60eb/"
MAX_PAGE_NUMBER = 29
SHOW_ERRORS = True
local_cache_file = "offers.json"


def get_data_from_web(url: str, max_page_number: int) -> pd.DataFrame:
    games = pd.DataFrame()
    errors = []
    for i in range(1, max_page_number + 1):
        print(f"Scraping page number {i} of {MAX_PAGE_NUMBER}")
        response = urlopen(url + str(i), data=None)
        soup = BeautifulSoup(response, 'html.parser')
        SECTION_DETAILS = 'class="ems-sdk-product-tile__details"'
        all_details = soup.find_all(
            name="section", class_="ems-sdk-product-tile__details")

        for a in all_details:
            try:
                game_title = a.span.text
                reduced_percantage = a.find(
                    name="div", class_="discount-badge__container psw-l-anchor").span.text
                reduced_price = a.find(
                    name="div", class_="price__container").span.text
                details = {"title": game_title, "reduction_percentage": reduced_percantage,
                           "reduced_price": reduced_price, "page": i}
                games = games.append(details, ignore_index=True)
            except Exception as e:
                errors.append(f"error {e} on page {i} with element {a}")
        time.sleep(1)
    print(f"fetched {len(games)} successfully and found {len(errors)} errors.")
    if SHOW_ERRORS:
        print(f"Errors {errors}")
    return games

# TODO support different currencies as parameters
def convert_data_types(df: pd.DataFrame) -> pd.DataFrame:
    df["reduced_price"] = df["reduced_price"].apply(lambda x: str(x).replace(
        "€", "")).apply(lambda x: str(x).replace(",", ".")).astype(float)
    df["reduction_percentage"] = df["reduction_percentage"].apply(lambda x: str(x).replace(
        "%", "")).astype(float)
    return df

#%%
games = get_data_from_web(URL, MAX_PAGE_NUMBER)
games = convert_data_types(games)
games.to_json(local_cache_file)
#%%
games = pd.read_json(local_cache_file)
sorted = games.sort_values(by="reduced_price", ascending=False)
print(sorted.head())

# %%
sweet_range = games.loc[(games["reduced_price"] < 30) & (games["reduced_price"] > 9)]
# %%
sweet_range = sweet_range.sort_values(by="reduction_percentage", ascending=True)
# %%
