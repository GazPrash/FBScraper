import facebook_crawler
import pandas as pd
import numpy as np
import requests
import bs4
import time

groupurl = 'https://www.facebook.com/groups/bookclubfavorites'
df = facebook_crawler.Crawl_GroupPosts(groupurl, until_date='2022-7-7')

groupid = "865107857005917"
# df = pd.read_csv("flagged/FbGroupScrpaed.csv")
df["GROUPID"] = df["GROUPID"].apply(lambda x : x if str(x) == groupid else np.nan)
df.dropna(subset=["GROUPID"], inplace= True, axis=0)


pd.DataFrame.to_csv(df, "flagged/FB_Scraped5.csv")
# df = pd.read_csv("flagged/FB_Scraped5.csv")

main_data = pd.DataFrame()
main_data["Username"] = df["NAME"]
main_data["Content"] = df["CONTENT"]
main_data["Comments"] = df["COMMENTCOUNT"]
main_data["Likes"] = df["LIKECOUNT"]

cookies = {
    'datr': 'aH65YyzZJ288kDWq1Kz_vsFA',
    'sb': 'en_BY9r-UFe27Lift9mRq8TN',
    'dpr': '1.25',
    'locale': 'en_GB',
    'wd': '1536x718',
    'c_user': '100035482513585',
    'xs': '7%3AYF9BAkfnF8RZwA%3A2%3A1674411648%3A-1%3A13224',
    'fr': '0hAIVZZUhersgBUtU.AWV2Z9g-GoFw4QaRgCgkEj56PSQ.BjwX96.Oj.AAA.0.0.BjzX5_.AWVYx_ibPEQ',
    'm_page_voice': '100035482513585',
}

headers = {
    'authority': 'mbasic.facebook.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    # 'cookie': 'datr=aH65YyzZJ288kDWq1Kz_vsFA; sb=en_BY9r-UFe27Lift9mRq8TN; dpr=1.25; locale=en_GB; wd=1536x718; c_user=100035482513585; xs=7%3AYF9BAkfnF8RZwA%3A2%3A1674411648%3A-1%3A13224; fr=0hAIVZZUhersgBUtU.AWV2Z9g-GoFw4QaRgCgkEj56PSQ.BjwX96.Oj.AAA.0.0.BjzX5_.AWVYx_ibPEQ; m_page_voice=100035482513585',
    'referer': 'https://mbasic.facebook.com/home.php?ref_component=mbasic_home_header&ref_page=%2Fwap%2Fprofile_timeline.php%3Ainfo&paipv=0&eav=AfYEnEyVweN-f9G14vGTFUt43ixCi6drfiH66Xgr2JYg_gshE9hh5Vy62M3OzUARn5U&tbua=1',
    'sec-ch-ua': '"Not_A Brand";v="99", "Brave";v="109", "Chromium";v="109"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'sec-gpc': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36',
}

params = {
    'ref_component': 'mbasic_home_header',
    'ref_page': '/wap/home.php',
    'refid': '7',
    'paipv': '0',
    'eav': 'AfZ7DNC18mrDe55PW_XrABiEWI3enMzneHEG_i-pdSNqH1_n0aPqiTRsQJ-3jhK8JRQ',
    'tbua': '1',
}



def get_gender(binfo_html):
    soup = bs4.BeautifulSoup(str(binfo_html), "lxml")
    for div in soup.find_all("div"):
        try: 
            content = str(div.contents[0])
        except Exception:
            continue

        if content == "Male":
            return "Male"
        elif content == "Female":
            return "Female"
        
    return "Null"



genders = []
for ind, user in enumerate(df["ACTORID"]):
    user_link = f"https://mbasic.facebook.com/{''.join(str(user).split(' '))}"
    try:
        response = requests.get(user_link, params=params, cookies=cookies, headers=headers)
    except Exception:
        # In case FB temporarily suspends the account, this exception cause will be triggered and script wont break
        genders.extend(["Null" for _ in range(len(list(df["ACTORID"])) - (ind+1))])

    soup = bs4.BeautifulSoup(response.text, "lxml")
    basic_info = soup.find("div", id = "basic-info")
    user_gender = get_gender(basic_info)

    genders.append(user_gender)

    print(f"{ind} Profile(s) Done")

    # waiting 2 sec before accessing a new profile to avoid detection in facebook
    time.sleep(3)


main_data["Gender"] = genders
pd.DataFrame.to_csv(main_data, "flagged/FB_ScrapedFinal2.csv")

# import pandas as pd


# d = pd.read_csv("flagged/FB_ScrapedFinal.csv")

# percent = d["Gender"].value_counts(normalize=True)
# print(percent)