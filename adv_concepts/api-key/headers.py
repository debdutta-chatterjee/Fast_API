from fastapi import FastAPI, Depends, HTTPException, Header

app = FastAPI()

API_KEY = 'my-secret-key'

def get_apikey(api_key :str = Header(...)):
    if api_key!= API_KEY:
        raise HTTPException(status_code=401,detail ='Unauthorized')
    return api_key

@app.get('/data')
def app_get_data(str = Depends(get_apikey)):
    return {'message': 'Access Granted!'}
