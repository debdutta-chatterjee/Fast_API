import redis
import json
import hashlib
import httpx
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from pydantic import BaseModel

r = redis.Redis(host ='localhost',port='6379',db=0)
app = FastAPI()

class PostRequest(BaseModel):
    post_id:int

def make_cache_key(post_id: int):
    raw = f"external_api:post_{post_id}"
    return hashlib.sha256(raw.encode()).hexdigest()


@app.post('/get-post')
async def get_post(data:PostRequest):
    key = make_cache_key(data.post_id)

    if r.get(key):
        return JSONResponse(content = {
            'status_code' : 200,            
            'message' : 'fetched from redis'
        },
        status_code =200)
    else:
        r.set(key,data.post_id)
        return JSONResponse(content = {
            'status_code' : 200,            
            'message' : 'not fetched from redis'
        },
        status_code = 404)

@app.post('/get-post')
async def get_post(data: PostRequest):
    cache_key = make_cache_key(data.post_id)

    cached_data = r.get(cache_key)
    if cached_data:
        print('Served from Redis cache!')
        return json.loads(cached_data)
    
    print('Calling external API...')
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://jsonplaceholder.typicode.com/posts/{data.post_id}")
        if response.status_code != 200:
            return {'error': 'Post not found!'}
        
    post_data = response.json()
    r.setex(cache_key, 600, json.dumps(post_data))
    print('Fetched and stored in Cache!')
    return post_data