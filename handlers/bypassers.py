from bs4 import BeautifulSoup
from urllib.parse import unquote, urlparse
import base64
import cloudscraper
import json
import re
import requests
import time


def adfly_decrypt_url(code):
    a, b = "", ""
    for i in range(0, len(code)):
        if i % 2 == 0:
            a += code[i]
        else:
            b = code[i] + b

    key = list(a + b)
    i = 0

    while i < len(key):
        if key[i].isdigit():
            for j in range(i + 1, len(key)):
                if key[j].isdigit():
                    u = int(key[i]) ^ int(key[j])
                    if u < 10:
                        key[i] = str(u)
                    i = j
                    break
        i += 1

    key = "".join(key)
    decrypted = base64.b64decode(key)[16:-16]

    return decrypted.decode("utf-8")


def adfly_bypass(url):
    res = requests.get(url).text
    out = {"error": False, "src_url": url}

    try:
        ysmm = re.findall(r"ysmm\s+=\s+['|\"](.*?)['|\"]", res)[0]
    except:
        out["error"] = True
        return out

    url = adfly_decrypt_url(ysmm)

    if re.search(r"go\.php\?u\=", url):
        url = base64.b64decode(re.sub(r"(.*?)u=", "", url)).decode()
    elif "&dest=" in url:
        url = unquote(re.sub(r"(.*?)dest=", "", url))

    out["bypassed_url"] = url

    return url


def sh_st_bypass(url):
    client = requests.Session()
    client.headers.update({"referer": url})
    p = urlparse(url)

    res = client.get(url)

    sess_id = re.findall(r"""sessionId(?:\s+)?:(?:\s+)?['|"](.*?)['|"]""", res.text)[0]

    final_url = f"{p.scheme}://{p.netloc}/shortest-url/end-adsession"
    params = {"adSessionId": sess_id, "callback": "_"}
    time.sleep(5)  # !important

    res = client.get(final_url, params=params)
    dest_url = re.findall('"(.*?)"', res.text)[1].replace(r"\/", "/")

    return dest_url


def rocklinks_bypass(url):
    client = cloudscraper.create_scraper(allow_brotli=False)
    DOMAIN = "https://rocklink.in"
    url = url[:-1] if url[-1] == "/" else url

    code = url.split("/")[-1]
    final_url = f"{DOMAIN}/{code}"

    resp = client.get(final_url)

    soup = BeautifulSoup(resp.content, "html.parser")
    inputs = soup.find(id="go-link").find_all(name="input")
    data = {input.get("name"): input.get("value") for input in inputs}

    h = {"x-requested-with": "XMLHttpRequest"}

    time.sleep(5)
    r = client.post(f"{DOMAIN}/links/go", data=data, headers=h)
    return r.json()["url"]


def linkvertise_bypass(url):
    client = requests.Session()

    headers = {
        "User-Agent": "AppleTV6,2/11.1",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    client.headers.update(headers)

    url = (
        url.replace("%3D", " ")
        .replace("&o=sharing", "")
        .replace("?o=sharing", "")
        .replace("dynamic?r=", "dynamic/?r=")
    )

    id_name = re.search(r"\/\d+\/[^\/]+", url)

    if not id_name:
        return None

    paths = [
        "/captcha",
        "/countdown_impression?trafficOrigin=network",
        "/todo_impression?mobile=true&trafficOrigin=network",
    ]

    for path in paths:
        url = (
            f"https://publisher.linkvertise.com/api/v1/redirect/link{id_name[0]}{path}"
        )
        response = client.get(url).json()
        if response["success"]:
            break

    data = client.get(
        f"https://publisher.linkvertise.com/api/v1/redirect/link/static{id_name[0]}"
    ).json()

    out = {
        "timestamp": int(str(time.time_ns())[0:13]),
        "random": "6548307",
        "link_id": data["data"]["link"]["id"],
    }

    options = {"serial": base64.b64encode(json.dumps(out).encode()).decode()}

    data = client.get("https://publisher.linkvertise.com/api/v1/account").json()
    user_token = data["user_token"] if "user_token" in data.keys() else None

    url_submit = f"https://publisher.linkvertise.com/api/v1/redirect/link{id_name[0]}/target?X-Linkvertise-UT={user_token}"

    data = client.post(url_submit, json=options).json()

    return data["data"]["target"]


def sirigan_bypass(url):
    client = requests.Session()
    res = client.get(url)
    url = res.url.split("=", maxsplit=1)[-1]

    while True:
        try:
            url = base64.b64decode(url).decode("utf-8")
        except Exception:
            break

    return url.split("url=")[-1]


BYPASSERS = {
    "adfly": adfly_bypass,
    "linkvertise": linkvertise_bypass,
    "rocklinks": rocklinks_bypass,
    "shorte": sh_st_bypass,
    "sirigan": sirigan_bypass,
}
