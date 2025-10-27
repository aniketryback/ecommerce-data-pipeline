import pandas as pd
import os
from datetime import datetime
import logging
import random

# ---------- Logging Setup ----------
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    filename='logs/ingestion.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ---------- Folder Paths ----------
SOURCE_DIR = os.path.join('data', 'source')
RAW_DIR = os.path.join('data', 'raw')
os.makedirs(RAW_DIR, exist_ok=True)

def ingest_orders():
    try:
        logging.info("🚀 Starting multi-file ingestion job...")

        files = [f for f in os.listdir(SOURCE_DIR) if f.endswith('.csv')]
        if not files:
            logging.warning("No CSV files found in source directory.")
            print("⚠️ No CSV files found in source directory.")
            return

        for file in files:
            try:
                source_file_path = os.path.join(SOURCE_DIR, file)
                df = pd.read_csv(source_file_path)

                # Sample 10% of data to simulate daily ingestion
                daily_sample = df.sample(frac=0.1, random_state=random.randint(1, 100))

                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                dest_file_name = f"{os.path.splitext(file)[0]}_{timestamp}.csv"
                dest_file_path = os.path.join(RAW_DIR, dest_file_name)

                daily_sample.to_csv(dest_file_path, index=False)
                logging.info(f"Ingestion successful → {dest_file_path}")
                print(f"✅ Ingested: {file} → {dest_file_path}")

            except Exception as e:
                logging.error(f"❌ Failed to ingest {file}: {e}")
                print(f"❌ Failed to ingest {file}: {e}")

        logging.info("🎯 Multi-file ingestion job completed.")

    except Exception as e:
        logging.critical(f"💥 Ingestion job failed entirely: {e}")
        print(f"💥 Ingestion job failed entirely: {e}")

if __name__ == "__main__":
    ingest_orders()
