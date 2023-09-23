from fastapi import HTTPException
from logger import LoggingError,LoggingInfo
from typing import List
import pandas as pd

from Models.VideoEntry import VideoEntry

class TopVideos:
    
    def FetchTopVideosData(self,dataset: List[VideoEntry]):
        try:
            LoggingInfo("Getting Most Trending Videos")
            datasets = [[row.video_id, row.title, row.trending_date, row.views, row.likes, row.dislikes, row.comment_count] for row in dataset]
            df = pd.DataFrame(datasets, columns=["video_id", "title","trending_date", "views", "likes", "dislikes", "comment_count"])
            
            top_videos = df.groupby('video_id')['trending_date'].nunique()

            sorted_top_videos = top_videos.sort_values(ascending=False)

            top_videos = sorted_top_videos.head(10).index.to_list()
            

            top_video_titles_df = df[df['video_id'].isin(top_videos)][['title']]
            top_video_titles = top_video_titles_df.drop_duplicates()['title'].to_list()
            
            LoggingInfo("Got most trending videos")
            return top_video_titles
        
        except Exception as e:
            LoggingError("Error occuured while getting most trending videos: " + str(e))
            raise HTTPException("Internal Server Error")
        
