import requests
from bs4 import BeautifulSoup
anime_info = dict()


def extract_from_spaceit_pad(tag):
    try:
        key = tag.find("span", class_="dark_text").text.split(":")[0]
    except:
        return
    if key == "Score":
        try:
            score = tag.find("span", itemprop="ratingValue").text
            users = tag.find("span", itemprop="ratingCount").text
        except:
            pass
        value = {"Rating": score, "Rated_by_users": users}
        anime_info[key] = value
        return

    extras = tag.find_all("span", itemprop="genre")

    try:
        tag.find("sup").extract()
        tag.find("div", class_="statistics-info").extract()
    except:
        pass

    for s in tag.select('div.spaceit_pad span.dark_text'):
        s.extract()

    if extras:
        for s in extras:
            s.extract()

    value = tag.text.strip().replace("#", "")
    if "Aired" == key:
        dates = value.split("to")
        first_aired = dates[0].strip()
        if dates[1]:
            last_aired = dates[1].strip()
        else:
            last_aired = "N/A"
        value = {"First_aired": first_aired, "Last_aired": last_aired}
        anime_info[key] = value
        return

    if "," in value and key != "Members" and key != "Favorites":
        value = [_.strip() for _ in value.split(",")]

    anime_info[key] = value
    return


def extract_from_table(tag):
    related_anime = dict()
    keys = tag.select("td.ar.fw-n.borderClass")
    for s in keys:
        s.extract()
    values = tag.select("td.borderClass")
    for i in range(len(values)):
        td = values[i].find_all("a")
        value = []
        for name in td:
            value.append({"Name": name.text, "Link": name.get('href')})

        key = keys[i].text.split(":")[0]
        related_anime[key] = value
    return related_anime


def extract_songs(tag):
    try:
        tag.find("script").extract()
        tag.find("div", id="js-oped-popup").extract()
    except:
        pass

    songs = tag.find("table").find_all("td", width="84%")
    song_list = []
    for song in songs:
        index = song.find(
            "span", class_="theme-song-index").text.split(":")[0].strip()
        artist = song.find("span", class_="theme-song-artist").text.strip()
        episodes = song.find("span", class_="theme-song-episode").text.strip()
        try:
            theme_song = song.find(
                "span", class_="theme-song-title").text.strip().strip('\"')
        except:
            song.find(
            "span", class_="theme-song-index").extract()
            song.find("span", class_="theme-song-artist").extract()
            song.find("span", class_="theme-song-episode").extract()
            theme_song = song.text.strip().strip('\"')

        song_list.append({
            "Index": index,
            "Song": theme_song,
            "Artist": artist,
            "Episodes": episodes
        })
    return song_list


def MAL(anime_id):
    response = requests.get(
        f"https://myanimelist.net/anime/{anime_id}")

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        try:
            rom_title = soup.find("h1", class_="title-name").text
            anime_info['Main Title'] = rom_title
        except:
            pass
        try:
            eng_title = soup.find("p", class_="title-english").text
            anime_info['Secondary Title'] = eng_title
        except:
            pass
        try:
            poster = soup.select_one("img.ac").get("data-src")
            anime_info['Poster'] = poster
        except:
            pass
        try:
            description = soup.find("p", itemprop="description").text
            anime_info['Description'] = description
        except:
            pass
        try:
            info = soup.find_all("div", class_="spaceit_pad")
            for tag in info:
                extract_from_spaceit_pad(tag)
        except:
            pass
        try:
            related = soup.select_one("table.anime_detail_related_anime")
            anime_info['Related'] = extract_from_table(related)
        except:
            pass
        try:
            opening_theme = soup.select_one(
                "div.theme-songs.js-theme-songs.opnening")
            anime_info['Opening Themes'] = extract_songs(opening_theme)
        except:
            pass
        try:
            ending_theme = soup.select_one(
                "div.theme-songs.js-theme-songs.ending")
            anime_info['Ending Themes'] = extract_songs(ending_theme)
        except:
            pass
        return anime_info

    else:
        return {'error': 'not found'}
