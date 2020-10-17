from requests_html import HTMLSession, HTML

from lxml.etree import ParserError

session = HTMLSession()


class Profile:
    """
        Parse twitter profile and split informations into class as attribute.

        Attributes:
            - name
            - username
            - birthday
            - location
            - biography
            - website
            - profile_photo
            - banner_photo
            - likes_count
            - tweets_count
            - followers_count
            - following_count
            - is_verified
            - is_private
            - user_id
    """

    def __init__(self, username):
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Referer": f"https://twitter.com/{username}",
            "User-Agent": "Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36",
            "X-Twitter-Active-User": "yes",
            "X-Requested-With": "XMLHttpRequest",
            "Accept-Language": "en-US",
        }

        page = session.get(f"https://twitter.com/{username}", headers=headers)
        self.username = username
        self.__parse_profile(page)



    def __parse_profile(self, page):
        try:
            html = HTML(html=page.text, url="bunk", default_encoding="utf-8")
        except KeyError:
            raise ValueError(
                f'Oops! Either "{self.username}" does not exist or is private.'
            )
        except ParserError:
            pass

        try:
            self.is_private = html.find(".ProfileHeaderCard-badges .Icon--protected")[0]
            self.is_private = True
        except Exception as e:
            self.is_private = False

        self.is_verified = True
        try:
            q = html.find("a.badge")[0]
            if not q:
                self.is_verified = False
        except Exception as e:
            self.is_verified = False

        try:
            self.location = html.find("div.location")[0].text
            if not self.location:
                self.location = None
        except Exception as e:
            self.location = None

        try:
            self.birthday = html.find(".ProfileHeaderCard-birthdateText")[0].text
            if self.birthday:
                self.birthday = self.birthday.replace("Born ", "")
            else:
                self.birthday = None
        except Exception as e:
            self.birthday = None

        try:
            self.profile_photo = html.find("td.avatar img")[0].attrs["src"]
        except Exception as e:
            self.profile_photo = None

        try:
            self.banner_photo = html.find(".ProfileCanopy-headerBg img")[0].attrs["src"]
        except Exception as e:
            self.banner_photo = None

        try:
            page_title = html.find("title")[0].text
            self.name = page_title[: page_title.find("(")].strip()
        except Exception as e:
            self.name = None

        try:
            self.user_id = html.find(".ProfileNav")[0].attrs["data-user-id"]
        except Exception as e:
            self.user_id = None

        try:
            self.biography = html.find("div.bio div.dir-ltr")[0].text
            if not self.biography:
                self.biography = None
        except Exception as e:
            self.biography = None

        try:
            self.website = html.find("div.url div.dir-ltr")[0].text
            if not self.website:
                self.website = None
        except Exception as e:
            self.website = None

        try:
            profile_stat_table = html.find('table.profile-stats')[0]
            stats = profile_stat_table.find('td div.statnum')
        except:
            self.stats = None

        # get total tweets count if available
        try:
            self.tweets_count = int(stats[0].text.replace(',',''))
        except Exception as e:
            self.tweets_count = None

        # get total following count if available
        try:
            self.following_count = int(stats[1].text.replace(',',''))
        except Exception as e:
            self.following_count = None

        # get total follower count if available
        try:
            self.followers_count = int(stats[2].text.replace(',',''))
        except Exception as e:
            self.followers_count = None

        # get total like count if available
        try:
            q = html.find('li[class*="--favorites"] span[data-count]')[0].attrs["data-count"]
            self.likes_count = int(q)
        except Exception as e:
            self.likes_count = None
            self.likes_count = "Unavailable"

    def to_dict(self):

        #Commented out are the data that aren't available in the mobile version
        return dict(
            name=self.name,
            username=self.username,
            #birthday=self.birthday,
            biography=self.biography,
            location=self.location,
            website=self.website,
            profile_photo=self.profile_photo,
            #banner_photo=self.banner_photo,
            #likes_count=self.likes_count,
            tweets_count=self.tweets_count,
            followers_count=self.followers_count,
            following_count=self.following_count,
            is_verified=self.is_verified,
            #is_private=self.is_private,
            #user_id=self.user_id
        )
    def get_tweets(self):
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Referer": f"https://twitter.com/{username}",
            "User-Agent": "Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36",
            "X-Twitter-Active-User": "yes",
            "X-Requested-With": "XMLHttpRequest",
            "Accept-Language": "en-US",
        }

        page = session.get(f"https://twitter.com/{username}", headers=headers)
        self.__parse_profile(page)

    def __dir__(self):
        return [
            "name",
            "username",
            "birthday",
            "location",
            "biography",
            "website",
            "profile_photo",
            'banner_photo'
            "likes_count",
            "tweets_count",
            "followers_count",
            "following_count",
            "is_verified",
            "is_private",
            "user_id"
        ]

    def __repr__(self):
        return f"<profile {self.username}@twitter>"

print(Profile("shroud").to_dict())