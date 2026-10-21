import mysql.connector

def connection():
    return mysql.connector.connect(
        host="mysql-3b673509-aucegypt-3dd3.e.aivencloud.com",
        port=20077,
        user="avnadmin",
        password="YOUR_AIVEN_PASSWORD",
        database="defaultdb",
        ssl_ca="ca.pem",
        connection_timeout=60
    )
  
def show_dataset():
    conn = connection()
    curr = conn.cursor()
    curr.execute("SELECT COUNT(*) FROM DATASET")
    counter = curr.fetchone()[0]
    print(f"Total datasets: {counter}")
    curr.close()
    conn.close()

def register_user():
    email = input("Email: ")
    username = input("Username: ")
    gender = input("Gender: ")
    age = input("Age: ")
    birth_date = input("Birth date (YYYY-MM-DD): ")
    country = input("Country: ")

    conn = connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM USERS WHERE Email = %s OR Username = %s", (email, username))
    existing_user = cur.fetchone()

    if existing_user:
        print("Email or username already exists. User not inserted.")
    else:
        query = """
        INSERT INTO USERS (Email, Username, Gender, Age, Birth_date, Country)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (email, username, gender, age, birth_date, country)

        cur.execute(query, values)
        conn.commit()
        print("User registered successfully.")

    cur.close()
    conn.close()

def register_usage():
    project_name = input("Project name: ")
    project_category = input("Project category: ")
    email = input("Email: ")
    dataset_id = input("Dataset ID: ")

    conn = connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM USERS WHERE Email = %s", (email,))
    user_exists = cur.fetchone()

    cur.execute("SELECT * FROM DATASET WHERE Dataset_ID = %s", (dataset_id,))
    dataset_exists = cur.fetchone()

    if not user_exists:
        print("User email does not exist.")
    elif not dataset_exists:
        print("Dataset ID does not exist.")
    else:
        query = """
        INSERT INTO USAGE_INFO (Project_Name, Project_Category, User_Email, Dataset_ID)
        VALUES (%s, %s, %s, %s)
        """
        values = (project_name, project_category, email, dataset_id)
        cur.execute(query, values)
        conn.commit()
        print("Usage added successfully.")

    cur.close()
    conn.close()

def view_usage():
    email = input("Email: ")
    conn = connection()
    cur = conn.cursor()
    
    cur.execute("""SELECT Usage_ID, Project_Name, Project_Category, Dataset_ID 
                FROM USAGE_INFO
                WHERE User_Email = %s""", (email,))

    rows = cur.fetchall()
    
    if(len(rows) == 0):
        print("No usage info found for this email.")
    else:
        for row in rows:
            print(row)
    cur.close()
    conn.close()

def org_dataset():
    org_type = input("Organization type: ")
    conn = connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT D.Dataset_ID, D.Title, O.Name, O.Organization_Type
        FROM DATASET D
        JOIN ORGANIZATION O
        ON D.Organization_ID = O.Organization_ID
        WHERE O.Organization_Type = %s
    """, (org_type,))

    rows = cur.fetchall()
    if len(rows) == 0:
        print("No datasets found.")
    else:
        for row in rows:
            print(row)

    print(len(rows), "datasets found.")

    cur.close()
    conn.close()

def top_organizations():
    conn = connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT O.Name, COUNT(*) AS total_datasets
        FROM ORGANIZATION O
        JOIN DATASET D
        ON O.Organization_ID = D.Organization_ID
        GROUP BY O.Organization_ID, O.Name
        ORDER BY total_datasets DESC
        LIMIT 5
    """)

    rows = cur.fetchall()
    for row in rows:
        print(row)

    cur.close()
    conn.close()

def dataset_format():
    file_format = input("Format: ")
    conn = connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT DISTINCT D.Dataset_ID, D.Title, R.Format
        FROM DATASET D
        JOIN RESOURCES R
        ON D.Dataset_ID = R.Dataset_ID
        WHERE R.Format = %s
    """, (file_format,))

    rows = cur.fetchall()
    if len(rows) == 0:
        print("No datasets found.")
    else:
        for row in rows:
            print(row)

    cur.close()
    conn.close()

def datasets_tag():
    tag = input("Tag: ")
    conn = connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT D.Dataset_ID, D.Title, DT.Tag_Name
        FROM DATASET D
        JOIN DATASETTAG DT
        ON D.Dataset_ID = DT.Dataset_ID
        WHERE DT.Tag_Name = %s
    """, (tag,))

    rows = cur.fetchall()
    if len(rows) == 0:
        print("No datasets found.")
    else:
        for row in rows:
            print(row)

    cur.close()
    conn.close()

def total_datasets_org():
    conn = connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT O.Name, COUNT(D.Dataset_ID)
        FROM ORGANIZATION O
        JOIN DATASET D
        ON O.Organization_ID = D.Organization_ID
        GROUP BY O.Organization_ID, O.Name
        ORDER BY COUNT(D.Dataset_ID) DESC
    """)

    rows = cur.fetchall()
    if len(rows) == 0:
        print("No data found.")
    else:
        for row in rows:
            print(row)

    cur.close()
    conn.close()

def total_datasets_format():
    conn = connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT Format, COUNT(DISTINCT Dataset_ID)
        FROM RESOURCES
        GROUP BY Format
        ORDER BY COUNT(DISTINCT Dataset_ID) DESC
    """)

    rows = cur.fetchall()
    if len(rows) == 0:
        print("No data found.")
    else:
        for row in rows:
            print(row)

    cur.close()
    conn.close()

def total_datasets_org_type():
    conn = connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT O.Organization_Type, COUNT(D.Dataset_ID)
        FROM ORGANIZATION O
        JOIN DATASET D
        ON O.Organization_ID = D.Organization_ID
        GROUP BY O.Organization_Type
        ORDER BY COUNT(D.Dataset_ID) DESC
    """)

    rows = cur.fetchall()
    if len(rows) == 0:
        print("No data found.")
    else:
        for row in rows:
            print(row)

    cur.close()
    conn.close()

def total_datasets_topic():
    conn = connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT Category, COUNT(*)
        FROM DATASET
        GROUP BY Category
        ORDER BY COUNT(*) DESC
    """)

    rows = cur.fetchall()
    if len(rows) == 0:
        print("No data found.")
    else:
        for row in rows:
            print(row)

    cur.close()
    conn.close()

def top_datasets_users():
    conn = connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT D.Dataset_ID, D.Title, COUNT(U.User_Email) AS total_users
        FROM DATASET D
        JOIN USAGE_INFO U
        ON D.Dataset_ID = U.Dataset_ID
        GROUP BY D.Dataset_ID, D.Title
        ORDER BY total_users DESC
        LIMIT 5
    """)

    rows = cur.fetchall()
    if len(rows) == 0:
        print("No data found.")
    else:
        for row in rows:
            print(row)

    cur.close()
    conn.close()

def usage_project_type():
    conn = connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT Project_Category, COUNT(*)
        FROM USAGE_INFO
        GROUP BY Project_Category
        ORDER BY COUNT(*) DESC
    """)

    rows = cur.fetchall()
    if len(rows) == 0:
        print("No data found.")
    else:
        for row in rows:
            print(row)

    cur.close()
    conn.close()


def top_tags_by_project_type():
    conn = connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT U.Project_Category, DT.Tag_Name, COUNT(*) AS total
        FROM USAGE_INFO U
        JOIN DATASETTAG DT
        ON U.Dataset_ID = DT.Dataset_ID
        GROUP BY U.Project_Category, DT.Tag_Name
        ORDER BY U.Project_Category, total DESC
    """)

    rows = cur.fetchall()
    if len(rows) == 0:
        print("No data found.")
    else:
        current_category = None
        count = 0

        for row in rows:
            category, tag, total = row

            if category != current_category:
                current_category = category
                count = 0
                print("\nProject Category:", category)

            if count < 10:
                print((tag, total))
                count += 1

    cur.close()
    conn.close()


def main():
    while True:
        print("\nPlease choose an option:")
        print("1. Show total datasets")
        print("2. Register user")
        print("3. Add usage info")
        print("4. View my usage info")
        print("5. View datasets by organization type")
        print ("6. View top 5 organizations by number of datasets")
        print("7. View datasets by format")
        print("8. View datasets by tag")
        print("9. View total datasets by organization")
        print("10. View total datasets by format")
        print("11. View total datasets by organization type")
        print("12. View total datasets by topic")
        print("13. View top 5 datasets by number of users")
        print("14. View usage distribution by category")
        print("15. View top 10 tags by category")
        print("16. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            show_dataset()
        elif choice == "2":
            register_user()
        elif choice == "3":
            register_usage()
        elif choice == "4":
            view_usage()
        elif choice == "5":
            org_dataset()
        elif choice == "6":
            top_organizations()
        elif choice == "7":
            dataset_format()
        elif choice == "8":
            datasets_tag()
        elif choice == "9":
            total_datasets_org()
        elif choice == "10":
            total_datasets_format()
        elif choice == "11":
            total_datasets_org_type()
        elif choice == "12":
            total_datasets_topic()
        elif choice == "13":
            top_datasets_users()
        elif choice == "14":
            usage_project_type()
        elif choice == "15":
            top_tags_by_project_type()
        elif choice == "16":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()