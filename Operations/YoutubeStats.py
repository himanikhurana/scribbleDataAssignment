from datetime import date
import json
from logger import LoggingInfo,LoggingError
import os
import pandas as pd

from Models.VideoEntry import VideoEntry


class YoutubeStats:
    
    def __init__(self,areas,fields,db_loc):
        self.areas = areas
        self.fields = fields
        self.db_loc = db_loc
        self.group = {}

    def YoutubeStats(self):
        
        video_entries = []
        try:
            for _,areas in self.areas.items():
                
                LoggingInfo(f"Triggered population of youtube stats for {areas}")
                
                vid_set = set()
                # Reads from CSV File
                csv_file_name = areas + "video_representation.csv"
                csv_file_loc= os.path.join(self.db_loc, csv_file_name)
                if areas in ('RU','MX', 'JP','KR'):
                    df = pd.read_csv(csv_file_loc, encoding='ISO-8859-1')
                else:
                    df = pd.read_csv(csv_file_loc)
                df = df.drop_duplicates()
                
                aggregators = {
                'title': 'first',  # Keep the first value
                'channel_title': 'first',
                'category_id': 'first',
                'publish_time': 'first',
                'tags': 'first',
                'views': 'max',  # Max of views
                'likes': 'max',  
                'dislikes': 'max',
                'comment_count': 'max',
                'thumbnail_link': 'first',
                'comments_disabled': 'first',
                'ratings_disabled': 'first',
                'video_error_or_removed': 'first',
                'description': 'first'
                }
                df = df.groupby(['video_id', 'trending_date']).agg(aggregators).reset_index()
                df['description'] = df['description'].astype(str)
                #Read Category JSON File
                json_file = areas + "_category_id.json"
                json_file_path = os.path.join(self.db_loc, json_file)

                with open(json_file_path, "r") as group_data:
                    groups_data = json.load(group_data)

                self.groups = {}
                self.refineGroups(groups_data)
                
                for _, row in df.iterrows():
                    
                    if row['video_id'] == '#NAME?':
                        continue
                    
                    vid_set.add(row['video_id'])
                    year, day, month = map(int, row["trending_date"].split('.'))
                    converted_date = date(year + 2000, month, day)
                    profile = {
                        "video_id": row["video_id"],
                        "channel_title": row["channel_title"],
                        "category_id": row["group_id"],
                        "tags": row["tags"],
                        "description": row["description"],
                        "trending_date": converted_date,
                        "title": row["title"],
                        "region": areas,            
                    }

                    # relate gruop ID to group title
                    group_id = str(row["category_id"])
                    if group_id in self.group:
                        profile["category_title"] = self.group[group_id]
                    else:
                        profile["category_title"] = "Unknown Category"

                    for _,attr in self.fields.items():
                        profile[attr] = row[attr]

                    obj = VideoEntry(**profile)

                    video_entries.append(obj)
                LoggingInfo(f"Youtube stat for - {areas} is populated")
        except Exception as E:
            LoggingError("Some error occurred " + str(E)) 
        
        return video_entries
        
    def refineGroups(self,group_data):

        for group in group_data['items']:
            self.group[group['id']] = group['snippet']['title']


