import string
import warnings
import pandas as pd
# import browser_cookie3 as bc3
import facebook_scraper as fbscrap

warnings.filterwarnings("ignore")

# fb_cookies = utils.dict_from_cookiejar(fb_cookies)
# fbscrap.set_cookies("fb_cookies/0bac2758-f9a0-4a79-9d7e-2f8c2d4db96c.txt")
# print(fbscrap.get_profile("zuck").keys())
# print(type(fb_cookies))

def get_group_id(link):
    arg:str = str(link.split("groups/")[1])
    if arg.isdecimal():
        return int(arg)

    ginfo = fbscrap.get_group_info(arg)
    return int(ginfo["id"])



def main():
    fbscrap.set_cookies("fb_cookies/0bac2758-f9a0-4a79-9d7e-2f8c2d4db96c.txt")
    posts = []
    group_link = "https://www.facebook.com/groups/397222924626707/"
    # fbscrap.get_group_info()
    group_id = get_group_id(group_link)
    # posts = group_posts(group_id)

    # for post in posts:
    #     print(post)
    #     break
    genders = []
    texts = []
    rel_status = []
    usernames = []
    location = []
    

    for post in fbscrap.get_posts(group=group_id, page_limit = 1):
        usernames.append(post["username"])
        texts.append(post["post_text"])

    for user in usernames:
        try:
            profile = fbscrap.get_profile(user)
            print(profile.keys())
            break
            genders.append(profile["Basic info"])
            rel_status.append(profile["Relationship"])
            # location.append(profile)
        except Exception as e:
            rel_status.append("Null")
            genders.append("Null")

    data = pd.DataFrame()
    data["User"] = usernames
    data["Text"] = texts
    data["Gender"] = genders
    data["Relationship"] = rel_status

    pd.DataFrame.to_csv(data, "flagged/FB_Scraped.csv")


def testing():
    fbscrap.set_cookies("fb_cookies/0bac2758-f9a0-4a79-9d7e-2f8c2d4db96c.txt")
    p = fbscrap.get_profile('venkata.goparaju.12')
    print(p["Basic info"])


# testing()
main()