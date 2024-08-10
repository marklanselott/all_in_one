from . import Providers
import asyncio

priority_list_all = [
    "spotifydown",
    "SpotifyMate",
    "spotisongdownloader"
]

Provider_list = [
    {
        "name": "spotifydown",
        "path": Providers.spotifydown
    },
    {
        "name": "SpotifyMate",
        "path": Providers.SpotifyMate
    },
    {
        "name": "spotisongdownloader",
        "path": Providers.spotisongdownloader
    }
]

async def worker(provider, url):
    result = await provider["path"](url)
    return result

async def first_response(url: str, priority_list: list=priority_list_all) -> Providers.response:
    tasks = [asyncio.create_task(worker(provider, url), name=provider['name']) for provider in Provider_list]
    pending_tasks = set(tasks)
    successful_result = None

    while pending_tasks:
        done, pending = await asyncio.wait(pending_tasks, return_when=asyncio.FIRST_COMPLETED)

        for task in done:
            result = task.result()
            provider_name = task.get_name()
            if result.status:
                if provider_name in priority_list:
                    # Если результат от приоритетного провайдера, отменяем остальные задачи
                    for pending_task in pending:
                        pending_task.cancel()
                    await asyncio.gather(*pending, return_exceptions=True)
                    return Providers.response(result.status, result.service_name, result.data)
                elif not successful_result:
                    # Если это первый успешный результат, но не приоритетный
                    successful_result = result

            pending_tasks.remove(task)

    if successful_result:
        return Providers.response(successful_result.status, successful_result.service_name, successful_result.data)
    
    return None
