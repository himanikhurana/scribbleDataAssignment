import configparser
from fastapi import FastAPI
import uvicorn

from Database.Database import Database
from Models.VideoEntry import Areas
from Workflows.GroupPopularity import GroupPopularity
from Workflows.TopVideos import TopVideos
from Workflows.PreferredChannels import PreferredChannels


app = FastAPI()

# Read configuration from config.ini
config = configparser.ConfigParser()
config.read("config.ini")

areas = config["areas"]
db_loc = config.get('Path', 'db_loc')
fields = config["fields"]

db_url = config.get('Database', 'DBURL')

# Initialize Database object
database = Database(db_url)

@app.get("/")
def read_root():
    return {"Hello": "World"}


''' Define a task workflow for customers
find the category that have relatively higher business potential on basis of views and area
http://localhost:8000/category-popularity?area=US
'''
@app.get("/category-popularity")
def get_group_popularity(area: areas):
    video_stats = database.GetStats(area)
    popularity_obj = GroupPopularity()
    popularity_data = popularity_obj.GetGroupWiseData(video_stats)
    return popularity_data

'''
Define a task workflow for customers
title of videos with maximum trending days
http://localhost:8000/trending-videos?area=US
'''
@app.get("/trending-videos")
def get_trending_videos(area: areas):
    video_stats = database.GetStats(area)
    trending_videos_obj = TopVideos()
    trending_videos_data = trending_videos_obj.FetchTopVideosData(video_stats)
    return trending_videos_data

'''
Define a task workflow for customers
most favoured channel
http://localhost:8000/favoured-channels?area=US
'''
@app.get("/favoured-channels")
def get_favoured_channels(area: areas):
    video_stats = database.GetProfiles(area)
    favoured_channels_obj = PreferredChannels()
    favoured_channels = favoured_channels_obj.GetPreferredChannels(video_stats)
    return favoured_channels

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
 