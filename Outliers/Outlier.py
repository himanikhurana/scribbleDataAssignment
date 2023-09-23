from logger  import LoggingError, LoggingInfo
import pandas as pd
from typing import List

from Models.VideoEntry import VideoEntry

class OutlierModel:
    
    # Interquartile Range (IQR)
    def GetOutlier(self,dataset: List[VideoEntry]):
        try:
            LoggingInfo("Looking for Outlier")    
            datasets = [[row.video_id, row.views] for row in dataset]
            df = pd.DataFrame(datasets, columns=["video_id", "views"])
            
            # Calculate the IQR for views
            Q1 = df['views'].quantile(0.25)
            Q3 = df['views'].quantile(0.75)
            IQR = Q3 - Q1
            
            # Define the threshold for outliers
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            # Find outliers and return video_ids
            outliers_res = df[(df['views'] < lower_bound) | (df['views'] > upper_bound)]
            LoggingInfo("Found the outlier")
            return outliers_res

        except Exception as e:
            LoggingError("Error occuured while finding outliers: " + str(e))
            
