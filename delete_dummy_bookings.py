import psycopg2, os
from psycopg2.extras import RealDictCursor

conn = psycopg2.connect(os.environ['RENDER_DATABASE_URL'], cursor_factory=RealDictCursor)
conn.autocommit = True
with conn.cursor() as cur:
    cur.execute("DELETE FROM bookings WHERE professional_name IN ('Arjun Mehta', 'Studio Lumina', 'Priya Sharma');")
    print(f'Deleted {cur.rowcount} dummy bookings.')
