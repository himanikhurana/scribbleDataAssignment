from logger import LoggingInfo,LoggingError
import pandas as pd
import sys

import configparser
from Database.Database import Database
from Operations.YoutubeStats import YoutubeStats
from Outliers.Outliers import OutlierModel


def main(args):
    
    try:
        LoggingInfo("Youstats creation started")
        
        # Read configuration from config.ini
        config = configparser.ConfigParser()
        config.read("config.ini")

        areas = config["Regions"]
        db_loc = config.get('Path','DataSetPath')
        fields = config["fields"]

        db_url = config.get('Database','DBURL')

        # Create Profile
        youtube_stats = YoutubeStats(areas,fields,db_loc)
        video_entries = youtube_stats.YoutubeStats()

        LoggingInfo("Youtube stats has been created")
        # Store profiles in sqlite
        database = Database(db_url)
        database.SetupDatabase()
        status = database.StoreStats(video_entries)    
        LoggingInfo("Looking for  outliers")
        # Find Outliers based on views
        area = 'US'
        video_profiles = database.GetStats(area)
        views_outlier_obj = OutlierModel()
        outliers = views_outlier_obj.GetOutlier(video_profiles)
        outliers.to_excel('ViewsOutliers.xlsx', index=False)
        LoggingInfo("Outliers are stored into ViewsOutliers excel file")
    except Exception as E:
        LoggingError("Exiting main function with Error: " + str(E))
if __name__ == "__main__":
    main(sys.argv[1:])
