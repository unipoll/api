import motor.motor_asyncio  # type: ignore
from unipoll_api import documents as Documents
from unipoll_api.config import get_settings

settings = get_settings()

client = motor.motor_asyncio.AsyncIOMotorClient(
    settings.mongodb_url, uuidRepresentation="standard"
)
mainDB = client.app


documentModels = [
    Documents.AccessToken,
    Documents.Resource,
    Documents.Account,
    Documents.Group,
    Documents.Workspace,
    Documents.Policy,
    Documents.Poll
]
