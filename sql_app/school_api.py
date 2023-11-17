import httpx, asyncio
from typing import Optional
from fastapi import FastAPI, Request, Header, Depends
from fastapi.responses import HTMLResponse
from database import SessionLocal, engine
from sqlalchemy.orm import Session



api_url = "https://api.nisproject.kz/users/"

# FastAPI route to fetch and return JSON data from the external API
async def fetch_data():
    async with httpx.AsyncClient() as client:
        # Make an HTTP GET request to the external API
        response = await client.get(api_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON content of the response
            json_data = response.json()
            return json_data
        else:
            # Return an error response if the request was not successful
            return {"error": f"Error: {response.status_code} - {response.text}"}
        
async def main():
    if __name__ == 'main':
        print(await fetch_data())
        return