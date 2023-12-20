user_agents = [
    "Googlebot/2.1 (+http://www.google.com/bot.html)",
    "Mozilla/5.0 (compatible; bingbot/2.0;  http://www.bing.com/bingbot.htm)",
    "Mozilla/5.0 (compatible; adidxbot/2.0;  http://www.bing.com/bingbot.htm)",
    "Mozilla/5.0 (seoanalyzer; compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)",
    "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm) SitemapProbe",
    "Mozilla/5.0 (Windows Phone 8.1; ARM; Trident/7.0; Touch; rv:11.0; IEMobile/11.0; NOKIA; Lumia 530) like Gecko (compatible; adidxbot/2.0; +http://www.bing.com/bingbot.htm)",
    "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 7_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53 (compatible; adidxbot/2.0;  http://www.bing.com/bingbot.htm)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 7_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53 (compatible; adidxbot/2.0; +http://www.bing.com/bingbot.htm)",
]

header = {
    "x-ig-app-id": "936619743392459",
    "x-instagram-ajax": "2f6bf8b37c04",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://www.instagram.com/accounts/login/",
    "content-type": "application/x-www-form-urlencoded",
}


header2 = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://www.instagram.com/accounts/login/",
    "x-csrftoken": ''
}

username_field = "username"
password_field = "enc_password"
home_url = "https://www.instagram.com/"
login_url = "https://www.instagram.com/accounts/login/ajax/"

browser_data = {
    "header": header,
    "home_url": home_url,
    "login_url": login_url,
    "username_field": username_field,
    "password_field": password_field,
}

response_codes = {"succeed": 1, "failed": 0, "locked": -1}

db_path = 'database.db'