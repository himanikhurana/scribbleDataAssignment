from fastapi import HTTPException
from logger import LoggingError,LoggingInfo
import pandas as pd
from typing import List

from Models.VideoEntry import VideoEntry

class PreferredChannels:

    def GetPreferredChannels(self,dataset: List[VideoEntry]) -> List:
        try:
            LoggingInfo("Favoured Channels process begins here")        
            datasets = [[row.channel_title, row.views, row.likes, row.dislikes, row.comment_count] for row in dataset]
            video_info = pd.DataFrame(datasets, columns=["channel_title", "views", "likes", "dislikes", "comment_count"])
            
            # Calculate Appearance Frequency
            appearance_freq= video_info['channel_title'].value_counts()
            video_info['likes'].replace(0, 1, inplace=True)
            video_info['dislikes'].replace(0, 1, inplace=True)
            # Calculate Like to Dislike Ratio
            video_info['like_dislike_ratio'] = video_info['likes']/video_info['dislikes']
            # Calculate the mean like to dislike ratio for each channel
            like_dislike_ratio = video_info.groupby('channel_title')['like_dislike_ratio'].mean()

            # Combine Judgment Criteria
            combined_points = (appearance_freq + like_dislike_ratio) / 2

            # Create a DataFrame to store the results
            channel_points = pd.DataFrame({
                'appearance_frequency': appearance_freq,
                'like_dislike_ratio': like_dislike_ratio,
                'combined_score': combined_points
            })
            # Sort the channels by combined score in descending order
            highest_channels = channel_points.sort_values(by='combined_score', ascending=False)

            # Select the top N channels
            top_n = 10  # Change this value to select a different number of channels
            highest_channels = highest_channels.head(top_n).index.tolist()

            LoggingInfo("GetPreferredChannels: Getting Favoured Channels process ended")
            return highest_channels
        
        except Exception as e:
            LoggingError("GetPreferredChannels: Getting Favoured Channels process failed with error: " + str(e))
            raise HTTPException("Internal Server Error")
    
