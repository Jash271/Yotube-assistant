from fastapi import FastAPI, Form, status
import requests
from pydantic import BaseModel
from fastapi import Body, FastAPI
from YouGlance import spy
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ['https://youglance.herokuapp.com',"http://localhost","http://localhost:8080","*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Item(BaseModel):
    query: str
    df: dict


class Ents(BaseModel):
    query: list
    video_id: str


@app.get("/get_unique_entities/{video_id}")
def get_unique_entities(video_id: str, status_code=status.HTTP_200_OK):
    obj = spy(video_id)
    k = obj.generate_df()
    unique = obj.get_unique_ents()
    print(unique)
    return {
        "unique_ents": unique,
    }


"""
@app.get("/wild_card")
def wild_card_search(item:Item,status_code=status.HTTP_200_OK):
    print(item.query)
    df=pd.DataFrame(item.df)
    print(df.head())
    return {
        'Text':'Ok'
    }
    
"""


@app.get("/wild_card/{video_id}/{query}")
def wild_card(video_id: str, query: str, status_code=status.HTTP_200_OK):
    obj = spy(video_id)
    k = obj.generate_df()
    m = obj.wildcard_search(query)
    return m


@app.post("/search_by_ents")
def search_by_ents(ents: Ents):
    obj = spy(ents.video_id)
    k = obj.generate_df()
    m = obj.search_by_ents(ents.query)
    return m


@app.get("/sentiment/{video_id}")
def get_sentiment(video_id: str):
    obj = spy(video_id)
    obj.generate_df()
    k = obj.sentiment_analysis((-0.2, 0.2))
    d = {
        "Negative": k["Negative"],
        "Positive": k["Positive"],
        "Neutral": k["Neutral"],
        "label_stats": dict(obj.show_label_stats()),
    }
    return d
