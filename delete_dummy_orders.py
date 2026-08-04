import psycopg2, os
from psycopg2.extras import RealDictCursor

conn = psycopg2.connect(os.environ['RENDER_DATABASE_URL'], cursor_factory=RealDictCursor)
conn.autocommit = True
with conn.cursor() as cur:
    cur.execute("""
        DELETE FROM orders 
        WHERE items_json LIKE '%Canon EOS R5 Body%' 
           OR items_json LIKE '%DJI Ronin-S Gimbal%' 
           OR items_json LIKE '%LED Studio Light Kit%';
    """)
    print(f'Deleted {cur.rowcount} dummy orders.')
