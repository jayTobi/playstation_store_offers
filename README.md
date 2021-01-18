# Playstation Store Offers Web Scraper
This is a simple Python Script for scraping offers from Playstation offer websites.

It can be used for further analysis using the pandas.
## Adjustments of the offers
To get the latest offers the `URL` and `MAX_PAGE_NUMBER` constants must be changed.
These can easily be found by accessing the PS Store open the offers section, if any, and copy the URL from your browser.

## Metacritics (www.metacritic.com)
Metacritics can now be downloaded manually (webpage, e.g. PS4 Games of All Time -> save as HTML) and imported to add the ratings to the offers for filtering.

## Further development
More examples will be added later.

Known limitations:
- Only Euro is supported as currency (will be changed later)