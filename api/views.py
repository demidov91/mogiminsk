from aiohttp.web import json_response


async def trips(request):
    return json_response({'trips': []})


async def providers(request):
    return json_response({'providers': []})