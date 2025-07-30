from abc import ABC, abstractmethod
from agentutil.utils.models import News
from typing import List
from agentutil.utils.models import NewsORM
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os



class AgentAssistant(ABC):
    SUCCESS_FINAL_STATE = "موفق✅"
    FAILURE_FINAL_STATE = "ناموفق❌"
    @abstractmethod
    def publish_article(self, news_id: str, news: News):
        pass

    @abstractmethod
    def update_news_status(
        news_id: str,
        new_status: str,
        title: str = None,
        cms_news_id: int = None,
        cost: int = None,
        duration=None
            ):
        pass
    
    @abstractmethod
    def get_blacklisted_urls() -> List[str]:
        pass


class TestAgentAssistant(AgentAssistant):
    def __init__(self):
        super().__init__()

    def publish_article(self, news_id: str, news: News):
        print(f"Publishing article: {news.title} for user: {news_id}")
        return True, 1111

    def update_news_status(
        self,
        news_id: str,
        new_status: str,
        title: str = None,
        cms_news_id: int = None,
        cost: int = None,
        duration=None
            ):
        
        # update news
        db_name = os.environ.get("DB_NAME")
        db_user = os.environ.get("DB_USER")
        db_password = os.environ.get("DB_PASSWORD")
        db_host = os.environ.get("DB_HOST")
        db_port = os.environ.get("DB_PORT")
        try:
            db_url = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
            engine = create_engine(db_url)
            SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
            with SessionLocal() as session:
                news_obj = session.query(NewsORM).filter(NewsORM.id == news_id).first()
                if news_obj:
                    if new_status:
                        news_obj.status = new_status
                    if title:
                        news_obj.title = title
                    if cms_news_id:
                        news_obj.news_id = cms_news_id
                    if cost:
                        news_obj.cost = cost
                    if duration:
                        news_obj.duration = duration
                session.commit()
        except Exception as e:
            pass
        print(f"Updating news status: {news_id} to {new_status}")
        if title:
            print(f"Title: {title}")
        if cms_news_id: 
            print(f"CMS News ID: {cms_news_id}")
        if cost:
            print(f"Cost: {cost}")
        if duration:
            print(f"Duration: {duration}")
        # Simulate a database update
        # In a real implementation, this would update the database
        # For this test, we'll just print the values
        print("News status updated successfully.")
        # Simulate a successful update by returning True
        return True
    
    def get_blacklisted_urls(self) -> List[str]:
        # Simulate fetching blacklisted URLs
        # In a real implementation, this would fetch from a database or API
        return ["https://instagram.com", "https://facebook.com"]
    
    def save_create_config(self, *args, **kwargs):
        pass
