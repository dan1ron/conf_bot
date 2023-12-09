import os

from dotenv import load_dotenv

load_dotenv()

ADMIN = int(os.environ.get("ADMIN", 523938823))
token = os.environ.get("TOKEN")
DB_CONNECTION_URL = os.environ.get("DB_CONNECTION_STRING")
DEFAULT_RATE_LIMIT = 1


# engine = create_async_engine(
#     url=make_url(DB_CONNECTION),
#     json_serializer=lambda x: json.dumps(x, ensure_ascii=False),
#     echo=True
# )
# SessionMaker = sessionmaker(
#     bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
# )
# session = SessionMaker()
# DB = Database(session)
