import psycopg2

try:
    connection = psycopg2.connect(
        host="localhost",          # change if needed
        database="Hackathon",   # <-- Excel wale db name se replace karo
        user="postgres",           # ya jo bhi user hai
        password="qwer1234",  # apna password
        port="5432"
    )

    cursor = connection.cursor()

    # Simple test query
    cursor.execute("SELECT version();")
    db_version = cursor.fetchone()

    print("✅ Connected Successfully!")
    print("PostgreSQL Version:", db_version)

    cursor.close()
    connection.close()

except Exception as e:
    print("❌ Connection Failed")
    print("Error:", e)