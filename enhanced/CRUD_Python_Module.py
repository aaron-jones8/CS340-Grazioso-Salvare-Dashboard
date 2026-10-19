import os
from urllib.parse import quote_plus

from pymongo import ASCENDING, MongoClient
from pymongo.errors import PyMongoError


class AnimalShelter(object):
    """CRUD operations for the Animal collection in MongoDB."""

    def __init__(
        self,
        username: str = None,
        password: str = None,
        host: str = "localhost",
        port: int = 27017,
        auth_db: str = "admin",
        db_name: str = "aac",
        collection_name: str = "animals",
    ):
        """
        Initialize the MongoClient and set database/collection handles.

        Enhancement: credentials are no longer hardcoded. If not passed in
        directly, they are read from the AAC_MONGO_USERNAME and
        AAC_MONGO_PASSWORD environment variables. If neither source
        provides them, construction fails loudly (ValueError) instead of
        silently falling back to a default account baked into the source
        file.
        """
        username = username if username is not None else os.environ.get("AAC_MONGO_USERNAME")
        password = password if password is not None else os.environ.get("AAC_MONGO_PASSWORD")

        if not username or not password:
            raise ValueError(
                "MongoDB credentials not provided. Pass username/password directly to "
                "AnimalShelter(), or set the AAC_MONGO_USERNAME and AAC_MONGO_PASSWORD "
                "environment variables before creating an instance."
            )

        self.client = None
        self.database = None
        self.collection = None

        try:
            # Enhancement: username and password are URL-escaped before being
            # placed in the connection URI, so credentials containing
            # characters like '@', ':', or '/' don't break the URI or get
            # silently misinterpreted as part of the host/path.
            safe_username = quote_plus(username)
            safe_password = quote_plus(password)
            uri = f"mongodb://{safe_username}:{safe_password}@{host}:{port}/?authSource={auth_db}"
            client = MongoClient(uri, serverSelectionTimeoutMS=5000)

            # Bug fix: MongoClient() connects lazily and does not raise on
            # bad credentials by itself -- the original code's try/except
            # around just this line never actually caught an authentication
            # failure, because no network round trip happens until the
            # first real operation runs. Forcing a ping here, inside the
            # try/except, verifies the connection and credentials
            # immediately instead of reporting false success at startup.
            client.admin.command("ping")

            self.client = client
            self.database = self.client[db_name]
            self.collection = self.database[collection_name]

            # Enhancement: build the indexes this dashboard's queries
            # actually rely on, once, at startup.
            self._ensure_indexes()
        except PyMongoError as e:
            print(f"ERROR: Could not connect to MongoDB: {e}")
            self.client = None
            self.database = None
            self.collection = None

    def _ensure_indexes(self):
        """
        Create the compound index the dashboard's filter queries rely on.

        Every rescue-type filter in the dashboard queries animal_type,
        breed, and sex_upon_outcome for equality together with a range on
        age_upon_outcome_in_weeks, in a single query. Without an index,
        MongoDB has to scan every document in the collection on every
        filter click. This index follows the standard Equality-Sort-Range
        ordering recommended for compound indexes: the equality fields
        come first, with the range field (age) last, so MongoDB can use
        the index for the whole query instead of just part of it.
        create_index() is idempotent -- calling it again with the same
        spec is a cheap no-op -- so this is safe to run on every startup
        rather than requiring a separate one-time setup step.
        """
        if self.collection is None:
            return
        try:
            self.collection.create_index(
                [
                    ("animal_type", ASCENDING),
                    ("breed", ASCENDING),
                    ("sex_upon_outcome", ASCENDING),
                    ("age_upon_outcome_in_weeks", ASCENDING),
                ],
                name="animal_type_breed_sex_age_idx",
            )
        except PyMongoError as e:
            print(f"WARNING: Could not create index: {e}")

    # ---------- C: CREATE ----------

    def create(self, data: dict) -> bool:
        """
        Insert a single document into the collection.

        """
        if self.collection is None:
            return False

        if not isinstance(data, dict) or not data:
            # Data must be a non-empty dictionary
            return False

        try:
            result = self.collection.insert_one(data)
            return result.acknowledged
        except PyMongoError as e:
            print(f"ERROR in create(): {e}")
            return False

    # ---------- R: READ ----------

    def read(self, query: dict) -> list:
        """
        Query for documents in the collection.

        """
        if self.collection is None:
            return []

        if query is None:
            query = {}

        if not isinstance(query, dict):
            return []

        try:
            cursor = self.collection.find(query)
            return list(cursor)
        except PyMongoError as e:
            print(f"ERROR in read(): {e}")
            return []

    # ---------- U: UPDATE ----------

    def update(self, query: dict, new_values: dict) -> int:
        """
        Update every document matching `query`, setting the fields given
        in `new_values`.

        Returns the number of documents modified, or 0 on any failure.

        Enhancement: `query` is required to be a non-empty dict. An empty
        query would match every document in the collection, and silently
        applying `new_values` to the entire collection from a dashboard
        click is almost never what's intended -- this guards against an
        accidental mass update, the same safeguard a real production data
        layer should have.
        """
        if self.collection is None:
            return 0

        if not isinstance(query, dict) or not query:
            print("ERROR in update(): query must be a non-empty dict")
            return 0

        if not isinstance(new_values, dict) or not new_values:
            print("ERROR in update(): new_values must be a non-empty dict")
            return 0

        try:
            result = self.collection.update_many(query, {"$set": new_values})
            return result.modified_count
        except PyMongoError as e:
            print(f"ERROR in update(): {e}")
            return 0

    # ---------- D: DELETE ----------

    def delete(self, query: dict) -> int:
        """
        Delete every document matching `query`.

        Returns the number of documents deleted, or 0 on any failure.

        Enhancement: same safeguard as update() -- an empty query is
        rejected rather than silently deleting the entire collection.
        """
        if self.collection is None:
            return 0

        if not isinstance(query, dict) or not query:
            print("ERROR in delete(): query must be a non-empty dict")
            return 0

        try:
            result = self.collection.delete_many(query)
            return result.deleted_count
        except PyMongoError as e:
            print(f"ERROR in delete(): {e}")
            return 0
