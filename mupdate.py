import requests
import mysql.connector
from datetime import datetime

# --- API Section ---
def fetch_first_50_tasks():
    url = 'https://apiweb.mile.app/api/v3/tasks'  # Initial API URL
    token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI2N2I0YTM5YzkwYzU4NGNlMTkwOTg1NTIiLCJqdGkiOiI4NmJlOTRjZDYwMDA0MjY4OWFhZjk0YTIwNjRiYjkwOTAyOTRhOWRjOTEyMjMyNDQzNzBlYTZmOGE1NGFhNDVlN2U1OGEwYzk2NmM4ZGZmNCIsImlhdCI6MTc0MDk2NTgxMC43ODU4OTcsIm5iZiI6MTc0MDk2NTgxMC43ODU5MDEsImV4cCI6MjI2NTM4MjgwMC4wMjQ2NDQsInN1YiI6IjY2ZGFhMDU4MWE3Zjk5N2VlYzA4Yjk3NiIsInNjb3BlcyI6W119.D1oj8NuAXj6INwN1QvqKKB14y6_1KS6virvxZypTZz-oPzAh4Igxe9i5cjRRSPEbuoeFWbA8RcwLhWpOpGO7qnmAvpjcVBti1CXJfMnDzM6Hbl_ncreExcxtAHA9m36CWPtnIkNbhpyNXvFrOlk5y6zQdVn9BHtykMNvUZE5T5nQUpTdGlW1-p9wBqwfOF55jO02P2hHqgIEBFiOuiu3ntTTbuoh4p7eixhw3cKZtO8wG_6FXpyUOgLjd_sZ7Ex0H-SfdrWceSsIZE9Vt3n4nTePLR0JYFPfvbZxNqZhfqYvrgOf066gs-KyU-uq9HtciXb16RzBZiy_Qr81Z2dAtKv3gnyZ3DRzX_pqc32MpLdsEB8KYpNDqQ_l7oFyfJVrlpO_yPNHG3ZRBEAp3txYPjjrU4YUX5nk5MtIs5YnJsj_aLp0k9TOn8Ikl9r4QITJ7NRVX145TTFWA9YcOuB3WckgsLMAf7LiM0AbgL195bhZ65IPy7sBK5sRMdhJjyS2ZUPgybRMubd-CB7R4ddUzY7cnPrOe8YDkOcd68Hn8miT8WP_CoyW7crK6pPjgjUowASa3p_M4nxdBfohAnL7Eha0oCphuvDBp1SJjnZ2hLwFz1fMYshfIRtHfmk_ZvJf9jeeITcEdRm8HJqLhKeZLs7pHhuyz5X14aACH0jUf-g'
    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    }

    all_tasks = []  # To store tasks from the API

    while url and len(all_tasks) < 50:
        try:
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                print(f"Error: {response.status_code} - {response.text}")
                break
            data = response.json()
            # Assuming the API returns tasks in this structure:
            # { "status": true, "tasks": { "data": [ ... ], "next_page_url": "..." } }
            if data.get('status') and data.get('tasks') and data['tasks'].get('data'):
                tasks_page = data['tasks']['data']
                remaining = 50 - len(all_tasks)
                all_tasks.extend(tasks_page[:remaining])
                if len(all_tasks) >= 50:
                    break
                url = data['tasks'].get('next_page_url')
                if not url:
                    break
            else:
                print("No more tasks or unexpected data structure.")
                break
        except Exception as e:
            print("Exception occurred:", e)
            break
    return all_tasks

# --- Database Section ---
def create_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",       # Replace with your MySQL username
        password="",       # Replace with your MySQL password
        database="bsc"     # Replace with your database name
    )

def update_measurements_with_api_data():
    # Fetch tasks from the API
    tasks = fetch_first_50_tasks()
    if not tasks:
        print("No tasks found.")
        return

    # Connect to the database
    connection = create_connection()
    cursor = connection.cursor()

    for task in tasks:
        # Get the title and kota value from the API task
        title = task.get("title", "")
        kota = task.get("kota", "")  # Ensure your API returns a 'kota' key

        # Update the measurement record where measurement_name matches the title
        update_query = "UPDATE measurement SET note = %s WHERE measurement_name = %s"
        cursor.execute(update_query, (kota, title))
        
        # Check if a row was updated
        if cursor.rowcount > 0:
            print(f"Updated measurement '{title}' with note '{kota}'.")
        else:
            print(f"No measurement found with name '{title}'.")
    
    # Commit the changes and close the connection
    connection.commit()
    cursor.close()
    connection.close()

if __name__ == "__main__":
    update_measurements_with_api_data()
import requests
# import mysql.connector

# # --- API Section: Fetch All Tasks ---
# def fetch_all_tasks():
#     url = 'https://apiweb.mile.app/api/v3/tasks'  # Initial API URL
#     token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI2N2I0YTM5YzkwYzU4NGNlMTkwOTg1NTIiLCJqdGkiOiI4NmJlOTRjZDYwMDA0MjY4OWFhZjk0YTIwNjRiYjkwOTAyOTRhOWRjOTEyMjMyNDQzNzBlYTZmOGE1NGFhNDVlN2U1OGEwYzk2NmM4ZGZmNCIsImlhdCI6MTc0MDk2NTgxMC43ODU4OTcsIm5iZiI6MTc0MDk2NTgxMC43ODU5MDEsImV4cCI6MjI2NTM4MjgwMC4wMjQ2NDQsInN1YiI6IjY2ZGFhMDU4MWE3Zjk5N2VlYzA4Yjk3NiIsInNjb3BlcyI6W119.D1oj8NuAXj6INwN1QvqKKB14y6_1KS6virvxZypTZz-oPzAh4Igxe9i5cjRRSPEbuoeFWbA8RcwLhWpOpGO7qnmAvpjcVBti1CXJfMnDzM6Hbl_ncreExcxtAHA9m36CWPtnIkNbhpyNXvFrOlk5y6zQdVn9BHtykMNvUZE5T5nQUpTdGlW1-p9wBqwfOF55jO02P2hHqgIEBFiOuiu3ntTTbuoh4p7eixhw3cKZtO8wG_6FXpyUOgLjd_sZ7Ex0H-SfdrWceSsIZE9Vt3n4nTePLR0JYFPfvbZxNqZhfqYvrgOf066gs-KyU-uq9HtciXb16RzBZiy_Qr81Z2dAtKv3gnyZ3DRzX_pqc32MpLdsEB8KYpNDqQ_l7oFyfJVrlpO_yPNHG3ZRBEAp3txYPjjrU4YUX5nk5MtIs5YnJsj_aLp0k9TOn8Ikl9r4QITJ7NRVX145TTFWA9YcOuB3WckgsLMAf7LiM0AbgL195bhZ65IPy7sBK5sRMdhJjyS2ZUPgybRMubd-CB7R4ddUzY7cnPrOe8YDkOcd68Hn8miT8WP_CoyW7crK6pPjgjUowASa3p_M4nxdBfohAnL7Eha0oCphuvDBp1SJjnZ2hLwFz1fMYshfIRtHfmk_ZvJf9jeeITcEdRm8HJqLhKeZLs7pHhuyz5X14aACH0jUf-g'
#     headers = {
#         'Authorization': 'Bearer ' + token,
#         'Content-Type': 'application/json'
#     }
    
#     all_tasks = []  # To store tasks from all pages
    
#     while url:
#         try:
#             response = requests.get(url, headers=headers)
#             if response.status_code != 200:
#                 print(f"Error: {response.status_code} - {response.text}")
#                 break
#             data = response.json()
#             # Check for the expected structure: { "status": true, "tasks": { "data": [...], "next_page_url": "..." } }
#             if data.get('status') and data.get('tasks') and data['tasks'].get('data'):
#                 tasks_page = data['tasks']['data']
#                 all_tasks.extend(tasks_page)
#                 url = data['tasks'].get('next_page_url')
#                 if not url:
#                     break
#             else:
#                 print("No more tasks or unexpected data structure.")
#                 break
#         except Exception as e:
#             print("Exception occurred:", e)
#             break
#     return all_tasks

# # --- Database Connection ---
# def create_connection():
#     return mysql.connector.connect(
#         host="127.0.0.1",
#         user="root",       # Replace with your MySQL username
#         password="",       # Replace with your MySQL password
#         database="bsc"     # Replace with your database name
#     )

# # --- Matching and Updating Records ---
# def update_measurements_with_api_data():
#     tasks = fetch_all_tasks()
#     if not tasks:
#         print("No tasks found from API.")
#         return

#     connection = create_connection()
#     cursor = connection.cursor()

#     for task in tasks:
#         # Retrieve values from API data
#         title = task.get("title", "")
#         kota = task.get("kota", "")  # Ensure your API returns a 'kota' key

#         if not title:
#             continue  # Skip tasks with no title

#         # Update measurement record where measurement_name matches the API title
#         update_query = "UPDATE measurement SET note = %s WHERE measurement_name = %s"
#         cursor.execute(update_query, (kota, title))

#         if cursor.rowcount > 0:
#             print(f"Updated measurement '{title}' with note '{kota}'.")
#         else:
#             print(f"No measurement found with name '{title}'.")
    
#     connection.commit()
#     cursor.close()
#     connection.close()

# if __name__ == "__main__":
#     update_measurements_with_api_data()
