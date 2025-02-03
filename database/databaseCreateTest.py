import sqlite3

def create_connection(db_file):
    """Establish a connection to the SQLite database.
    
    This function attempts to connect to the SQLite database specified by db_file.
    If the connection fails, it logs an error message.
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database {db_file}: {e}")
    return conn

def create_table(conn, create_table_sql):
    """Create a table using the provided SQL statement.
    
    This function executes the SQL statement to create a table in the database.
    If the table creation fails, it logs an error message.
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(f"Error creating table: {e}")

def insert_data(conn, data):
    """Insert data into the image_labels table.
    
    This function inserts a new record into the image_labels table.
    It logs an error message if the insertion fails.
    """
    sql = ''' INSERT INTO image_labels(image_url, ai_label, human_1_score, human_2_score, human_3_score, human_1_comment, human_2_comment, human_3_comment, ai_accuracy)
              VALUES(?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    try:
        cur.execute(sql, data)
        conn.commit()
        return cur.lastrowid
    except sqlite3.Error as e:
        print(f"Error inserting data: {e}")
        return None

def insert_multiple_records(conn, data_list):
    """Insert multiple records into the image_labels table.
    
    This function inserts multiple records into the image_labels table.
    It logs an error message if the insertion fails.
    """
    sql = ''' INSERT INTO image_labels(image_url, ai_label, human_1_score, human_2_score, human_3_score, human_1_comment, human_2_comment, human_3_comment, ai_accuracy)
              VALUES(?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    try:
        cur.executemany(sql, data_list)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error inserting multiple records: {e}")

def validate_data(data):
    """Validate data before insertion.
    
    This function checks that all fields in the data are of valid types.
    It raises a ValueError if any field has an invalid type.
    """
    if not all(isinstance(field, (str, int, float)) for field in data):
        raise ValueError("Invalid data types in: " + str(data))
    return True

def query_records(conn, query):
    """Query records from the image_labels table.
    
    This function executes a query to fetch records from the image_labels table.
    It logs an error message if the query fails.
    """
    cur = conn.cursor()
    try:
        cur.execute(query)
        rows = cur.fetchall()
        for row in rows:
            print(row)
    except sqlite3.Error as e:
        print(f"Error querying records: {e}")

def update_record(conn, data):
    """Update a record in the image_labels table.
    
    This function updates an existing record in the image_labels table.
    It logs an error message if the update fails.
    """
    sql = ''' UPDATE image_labels
              SET image_url = ?,
                  ai_label = ?,
                  human_1_score = ?,
                  human_2_score = ?,
                  human_3_score = ?,
                  human_1_comment = ?,
                  human_2_comment = ?,
                  human_3_comment = ?,
                  ai_accuracy = ?
              WHERE image_id = ? '''
    cur = conn.cursor()
    try:
        cur.execute(sql, data)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error updating record: {e}")

def delete_record(conn, image_id):
    """Delete a record from the image_labels table.
    
    This function deletes a record from the image_labels table.
    It logs an error message if the deletion fails.
    """
    sql = 'DELETE FROM image_labels WHERE image_id=?'
    cur = conn.cursor()
    try:
        cur.execute(sql, (image_id,))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error deleting record: {e}")

def main():
    database = "astroannotate.db"

    sql_create_image_labels_table = """ CREATE TABLE IF NOT EXISTS image_labels (
                                        image_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        image_url TEXT NOT NULL,
                                        ai_label TEXT NOT NULL,
                                        human_1_score INTEGER,
                                        human_2_score INTEGER,
                                        human_3_score INTEGER,
                                        human_1_comment TEXT,
                                        human_2_comment TEXT,
                                        human_3_comment TEXT,
                                        ai_accuracy REAL
                                    ); """

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create image_labels table
        create_table(conn, sql_create_image_labels_table)

        # insert example data
        data = ('uploads/image1.jpg', 'cat', 1, 0, 1, 'Looks correct', 'I think it\'s a dog', 'Agree with AI', 85.0)
        insert_data(conn, data)

        # close connection
        conn.close()
    else:
        print("Error! cannot create the database connection.")

if __name__ == '__main__':
    main()
