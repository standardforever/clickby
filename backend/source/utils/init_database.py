from common.libs import db_connection
from common.models.user_models import User
from utils.auth_utils import get_password_hash, get_user


from app.config import app_config

USERS_DATABASE_NAME = app_config.database_name
USERS_COLLECTION_NAME = "users"
async def init_indices_users():
	await db_connection.create_index(USERS_DATABASE_NAME, USERS_COLLECTION_NAME, "id", unique=True)
	await db_connection.create_index(USERS_DATABASE_NAME, USERS_COLLECTION_NAME, "username", unique=True)
	await db_connection.create_index(USERS_DATABASE_NAME, USERS_COLLECTION_NAME, "email", unique=True)
	print(f"[INFO] {USERS_DATABASE_NAME}.{USERS_COLLECTION_NAME} initialized.")
	


async def load_data_users():

	user = User(
		username=app_config.username,
		password=get_password_hash(app_config.password),
		email=app_config.email,
		scopes=["*"]
	)

	user.is_verified = True
	user.disabled = False
	if await get_user(app_config.email):
		return
	await init_indices_users()
	await db_connection.create(USERS_DATABASE_NAME, USERS_COLLECTION_NAME, user.model_dump(mode="json"))
	print(f"[INFO] Created first User in {USERS_DATABASE_NAME}.{USERS_COLLECTION_NAME}")
