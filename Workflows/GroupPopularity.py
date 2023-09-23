from fastapi import HTTPException
from logger import LoggingInfo,LoggingError
import pandas as pd
from typing import List

from Models.VideoEntry import VideoEntry

class GroupPopularity:
    
    def GetGroupWiseData(self,dataset: List[VideoEntry]):
        try:
            LoggingInfo("Group Wise Data  collection  started")        
            dataset = [[row.Group_title, row.views, row.likes, row.dislikes, row.comment_count] for row in dataset]
            df = pd.DataFrame(dataset, columns=["Group_title", "views", "likes", "dislikes", "comment_count"])
            
            # Group the data by Group_title and calculate sum of views, likes, and comments
            Group_popularity = df.groupby('Group_title')[['views', 'likes', 'comment_count']].sum()

            # Sort the categories by total views in descending order
            sorted_groups = Group_popularity.sort_values(by='views', ascending=False)

            # Display the top 10 popular categories
            top_popular_groups= sorted_groups.head(10).index.to_list()
            
            LoggingInfo("Fecthed data group wise")
            
            return top_popular_groups
        
        except Exception as e:
            LoggingError("Some error occurred while processing group wise data: " + str(e))
            raise HTTPException("Internal Server Error")
 
        
