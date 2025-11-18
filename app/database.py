import os
from dotenv import load_dotenv
import oracledb

# .env 불러오기
load_dotenv()

WALLET_DIR = os.getenv("WALLET_DIR")
DB_TNS_ALIAS = os.getenv("DB_TNS_ALIAS")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

try:
    oracledb.init_oracle_client(config_dir=WALLET_DIR)
    print("✅ Oracle Thick Mode(Wallet) initialized.")
except Exception as e:
    print(f"❌ Error initializing Oracle Thick Mode: {e}")
    raise SystemExit("Thick Mode failed to start, check WALLET_DIR or Instant Client.")

pool = None

def init_db_pool():
    global pool
    try:
        pool = oracledb.create_pool(
            user=DB_USER,
            password=DB_PASSWORD,
            # DSN 대신 tnsnames.ora의 별칭(Service)을 사용
            dsn=DB_TNS_ALIAS, 
            min=2,
            max=5,
            increment=1
        )
        print("✅ DB Connection pool created successfully (Cloud Wallet).")
    except Exception as e:
        print(f"❌ Error creating DB connection pool: {e}")
        pool = None

def get_db_connection():
    if pool is None:
        raise Exception("DB pool is not initialized. Call init_db_pool() first.")
    
    connection = pool.acquire()
    return connection

def close_db_pool():
    if pool:
        pool.close()
        print("DB Connection pool closed.")

