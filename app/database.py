import oracledb
import os


WALLET_DIR = r"C:\Users\te493\Wallet_V42X863LJL1E28A7"
DB_TNS_ALIAS = "v42x863ljl1e28a7_high" 
DB_USER = "team_member_kimtaeyeon"
DB_PASSWORD = "Kimtaeyeon_password123"

try:
    oracledb.init_oracle_client(
        config_dir=WALLET_DIR, 
    )
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

