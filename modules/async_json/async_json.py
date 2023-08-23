import aiofiles
import json

async def async_read_json(filename,default_content=[]):
    try:
        async with aiofiles.open(filename,mode="r") as file:
            data = await file.read()
            content = json.loads(data)
    except FileNotFoundError:
        async with aiofiles.open(filename,mode="w") as file:
            jdump = json.dumps(default_content)
            await file.write(jdump)
        return
    return content

async def async_write_json(filename,content):
    async with aiofiles.open(filename,mode="w") as file:
        jdump = json.dumps(content)
        await file.write(jdump)