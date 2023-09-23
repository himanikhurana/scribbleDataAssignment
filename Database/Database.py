from logger import LoggingError,LoggingInfo
from typing import List
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from Models.VideoEntry import VideoEntryDB,VideoEntry

class Database:

    def __init__(self, db_url):
        self.DBURL = db_url
        self.engine = create_engine(self.DBURL)

    def SetupDatabase(self):
        # Drop the table if it exists
        drop_table_query = text("DROP TABLE IF EXISTS video_entries")
        with self.engine.connect() as connection:
            connection.execute(drop_table_query)

        VideoEntryDB.__table__.create(bind=self.engine)

    def StoreStats(self,video_entries: List[VideoEntry]):
        LoggingInfo("Database creation started")
        Session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        session = Session()

        try:
            for entry in video_entries:
                db_entry = VideoEntryDB(**entry.dict())
                session.add(db_entry)
            session.commit()
            LoggingInfo("Saved to the Database")
        except Exception as e:
            session.rollback()
            LoggingError("Error occurred while saving into database : " + str(e))
        finally:
            session.close()


    def GetStats(self,area: str) -> List[VideoEntry]:
        try:
            LoggingInfo("Database: Getting data from database started")
            Session = sessionmaker(bind=self.engine)
            session = Session()
            query = session.query(VideoEntryDB).filter_by(area=area)
            output = query.all()
            session.close()
            LoggingInfo("DFecthed data from database")
            return output
        except Exception as e:
            session.close()
            LoggingError("Error occuured while fetching from database: " + str(e))
                
