import time
import datetime
import json
import aiohttp
import asyncio
import os
import sys
import signal

RPS = 100
CHUNK_SIZE = 1000
headers = {
	'accept': 'application/json',
}

base_url = 'api_endpoint'
result = {}

data = list(range(10000))

async def fetch_response(url, datapoint):
	async with limit:
		json_data = {'data_for_post': datapoint}
		try:
			async with aiohttp.ClientSession() as session:
				 async with session.request("POST", url, headers=headers, json=json_data, verify_ssl=False, timeout=30) as resp:
				 	resp_data = await resp.read()
				 	resp_data = json.loads(resp_data)
				 	if limit.locked():
				 		await asyncio.sleep(1)
				 	return resp_data
		except Exception as e: #naked exceptions are bad
			print(e)
			return None



async def process_chunk(chunk):
	tasks = []
	for i, row in enumerate(chunk):
		tasks.append(fetch_response(base_url, row))
	return await asyncio.gather(*tasks)


for i in range(0, len(data), CHUNK_SIZE):
	print(f'Processing chunk {i}')
	try:
		limit = asyncio.Semaphore(RPS)
		loop = asyncio.get_event_loop()
		tmp = loop.run_until_complete(process_chunk(data[i: i+CHUNK_SIZE]))
		res = postprocess(tmp)
	except Exception as e: #naked exception is bad
		print(e)
		print(f'failure on iteration {i}')