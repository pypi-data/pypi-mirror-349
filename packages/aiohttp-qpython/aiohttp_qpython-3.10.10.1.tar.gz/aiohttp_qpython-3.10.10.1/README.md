This project is a branch of <a target="_blank" rel="noopener" href="https://pypi.org/project/aiohttp/">aiohttp</a> on <a href="https://www.qpython.org">QPython</a>.

Async http client/server framework (asyncio)

Project description:

- Supports both client and server side of HTTP protocol.

- Supports both client and server Web-Sockets out-of-the-box and avoids Callback Hell.

- Provides Web-server with middleware and pluggable routing.

## Getting started

### Client

To get something from the web:

```python
import aiohttp
import asyncio

async def main():

    async with aiohttp.ClientSession() as session:
        async with session.get('http://python.org') as response:

            print("Status:", response.status)
            print("Content-type:", response.headers['content-type'])

            html = await response.text()
            print("Body:", html[:15], "...")

asyncio.run(main())
```

### Server

An example using a simple server:

```python
# examples/server_simple.py
from aiohttp import web

async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)

async def wshandle(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == web.WSMsgType.text:
            await ws.send_str("Hello, {}".format(msg.data))
        elif msg.type == web.WSMsgType.binary:
            await ws.send_bytes(msg.data)
        elif msg.type == web.WSMsgType.close:
            break

    return ws


app = web.Application()
app.add_routes([web.get('/', handle),
                web.get('/echo', wshandle),
                web.get('/{name}', handle)])

if __name__ == '__main__':
    web.run_app(app)
```