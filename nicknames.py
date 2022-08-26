import asyncio
from datetime import datetime as dt
from aiohttp import ClientSession 
from colorama import Fore 



async def response(session, url, headers):
    """
    добавить исключения на выдачу простого текста
    """
    async with session.get(url, headers=headers) as r:
        assert r.status == 200
        content = await r.json()

    return content 

async def parse_json(content, file):

    """
    сохрвнение в бд
    """
    for result in content["payload"]:
        for gamer_1 in result["teams"]["faction1"]["roster"]:
            file.write(gamer_1["nickname"] + '\n')

    for result in content["payload"]:
        for gamer_2 in result["teams"]["faction2"]["roster"]:
            file.write(gamer_2["nickname"] + '\n')


async def start():
    faceit_id = "42e160fc-2651-4fa5-9a9b-829199e27adb"
    links = [
        "https://api.faceit.com/match-history/v4/matches/competition?page={page}&size=100&id={faceit_id}&type=matchmaking".format(
        page=page, faceit_id=faceit_id) for page in range(1, 20)
    ]
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0",
    }

    session = ClientSession()
    # aiofiles?
    file = open("nicknames.txt", "a")

    now = dt.now()

    # asyncio.gather?
    for link in links:
        json_data = await response(session, link, headers)
        await parse_json(json_data, file)

    print(Fore.GREEN + f"{dt.now()-now} прошло с момента парсинга")

    await session.close()
    file.close()
    
if __name__ == "__main__":
    asyncio.run(start())