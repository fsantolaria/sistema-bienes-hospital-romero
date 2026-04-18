import psycopg2
conn = psycopg2.connect('postgresql://neondb_owner:npg_QPiLZfduy3A9@ep-raspy-shadow-a4rio3ce.us-east-1.aws.neon.tech/neondb?sslmode=require')
conn.autocommit = True
cur = conn.cursor()
cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
tables = cur.fetchall()
print(f"Dropping {len(tables)} tables...")
for t in tables:
    cur.execute(f'DROP TABLE IF EXISTS "{t[0]}" CASCADE')
print("All tables dropped.")
