
import requests
import pandas as pd

start_page = 1

payload = {
        # "country_code": "at",
        # "country_codes[]":"it",
        "country_codes[]":["at","au"],
        # "country_codes[]":"fr",
        # "currency_code":"EUR",
        # "grape_filter":"varietal",
        "min_rating":"3.8",
        "order_by":"ratings_average",
        # "order":"asc",
        # "page": 1,
        # "price_range_max":"30",
        # "price_range_min":"10",
        # "wine_type_ids[]":"1",
        "language": "en"
    }


r = requests.get(
    "https://www.vivino.com/api/explore/explore",
    params = payload,
    headers= {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0"
    }
)

results_all = []

n_matches = r.json()['explore_vintage']['records_matched']

for i in range(start_page, max(1, int(n_matches / 25)) + 1):
    payload['page'] = i

    # print(f'Scraping data from page: {payload["page"]}')

    r = requests.get(
    "https://www.vivino.com/api/explore/explore",
    params = payload,
    headers= {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0"
    }
    )

    results = [
            (
                t["vintage"]["wine"]["winery"]["name"], 
                f'{t["vintage"]["wine"]["name"]} {t["vintage"]["year"]}',
                t["vintage"]["statistics"]["ratings_average"],
                t["vintage"]["statistics"]["ratings_count"],
                t["price"]["amount"],
                t["vintage"]["wine"]["region"]["country"]["seo_name"],
            )
            for t in r.json()["explore_vintage"]["matches"]
            ]
        
    results_all = results_all + results
    # print(type(results_all[0]))
# print(results_all)

dataframe = pd.DataFrame(results_all,columns=['Winery','Wine','Rating','num_review','Price', 'Country'])

# df_at = dataframe.query("Country != 'italy'")
dataframe.query("num_review > 50", True)


# print(dataframe.sort_values(by=['Country']))

# print(df_at)
print(len(dataframe.index))
dataframe.to_pickle('at_au.pkl')
