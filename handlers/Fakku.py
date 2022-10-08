from bs4 import BeautifulSoup
from aiohttp import ClientSession


class Fakku:

    def __init__(self) -> None:
        pass

    @classmethod
    async def getSoup(cls, url: str) -> BeautifulSoup:
        async with ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return BeautifulSoup((await response.read()).decode('utf-8'), 'html.parser')
                else:
                    return False

    @classmethod
    async def scrape(cls, url: str) -> dict:
        MainPage = await cls.getSoup(url)
        if MainPage:

            title = MainPage.find('h1', {
                'class': "block col-span-full text-3xl py-2 font-bold text-brand-light text-left dark:text-white dark:link:text-white"}).text

            titles = MainPage.find_all(
                "div", {"class": "inline-block w-24 text-left align-top"})
            content = MainPage.find_all(
                "div", {
                    "class": "table-cell w-full align-top text-left space-y-2 link:text-blue-700 dark:link:text-white"}
            )
            description = content[-1].text
            rawTags = MainPage.find_all(
                'a', {'class': "inline-block bg-gray-100 mb-2 leading-loose rounded py-1 px-3 mr-2 dark:bg-gray-800 text-gray-900 dark:text-gray-400 lowercase"})
            tags = [''.join(tag.text.replace('-', '').split())
                    for tag in rawTags]
            rawPreviews = MainPage.find_all('img', {'class': "w-full rounded"})
            previews = [preview.get('src') for preview in rawPreviews]
            thumb = MainPage.find('img', {
                'class': "inline-block max-w-full sm:max-w-xs sm:max-h-above-fold rounded shadow"}).get('src')

            temp = {titles[i].text: content[i].text.strip()
                    for i in range(len(titles))}
            if not 'Magazine' in temp:
                temp['Magazine'] = 'Not Mentioned'
            if not 'Favorites' in temp:
                temp['Favorites'] = 'Not Mentioned'
            if not 'Circle' in temp:
                temp['Circle'] = 'Not Mentioned'
            if not 'Parody' in temp:
                temp['Parody'] = 'Not Mentioned'
            if not 'Pages' in temp:
                temp['Pages'] = 'Not Mentioned'
            if not 'Publisher' in temp:
                temp['Publisher'] = 'Not Mentioned'

            temp["Title"] = title
            temp["Description"] = description
            temp["Tags"] = tags
            temp["Previews"] = previews
            temp["Thumbnail"] = "https:"+thumb

            return temp

        else:
            return {"error": "url invalid"}
