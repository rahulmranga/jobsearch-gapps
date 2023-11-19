import requests
import pandas as pd
import json
import random
from sqlalchemy import create_engine
import psycopg2
# Replace these with your actual database credentials
database_url = "postgresql://postgres:postgres@localhost:5432/jobpostings"
engine = create_engine(database_url)


def job_search(query, latest):
    url = "https://jsearch.p.rapidapi.com/search"

    page_no = str(random.randint(3, 20))
    if latest:
        querystring = {"query": query, "date_posted": "week"}
    else:
        querystring = {"query": query, "page": page_no,
                       "num_pages": "20", 'radius': '300'}
    headers = {
        "X-RapidAPI-Key": "bbab1d2a73msh99fd58199d5a509p1e6c76jsn0dc84f490626",
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }
    print(querystring)
    response = requests.get(url, headers=headers, params=querystring)
    json_data = response.json()

#     # # with open('example.txt', 'a') as file:
#     # #     json.dump(json_data, file, indent=4)
#     # with open('example.txt', 'r') as file:
#     #     json_text = file.read()
#     # # Parse the JSON text to a Python dictionary
#     # json_data = json.loads(json_text)

    table_name = 'listings'
    data = json_data
    raw = data['data']
    df = pd.DataFrame(raw)
    print(df)
    cols = ['job_id', 'employer_name', 'job_publisher', 'job_employment_type', 'job_title', 'job_apply_link', 'job_apply_quality_score', 'job_posted_at_timestamp', 'job_posted_at_datetime_utc',
            'job_city', 'job_state', 'job_country', 'job_google_link', 'job_highlights', 'job_naics_name']
    df = df[cols]
    df['job_highlights'] = df['job_highlights'].astype(str)

    temp_table_name = "temp_" + table_name
    connection = engine.connect()
    df.to_sql(temp_table_name, engine, if_exists="replace", index=False)
    insert_query = f"""
        INSERT INTO {table_name}
        SELECT * FROM {temp_table_name}
        WHERE NOT EXISTS (
            SELECT 1 FROM {table_name}
            WHERE {table_name}.job_id = {temp_table_name}.job_id
        )
        """
    connection.execute(insert_query)
    connection.close()
    return json.dumps({"Rahul": '1'})


def database_search(query, latest):
    table_name = 'listings'
    engine = create_engine(database_url)

    # Split the query into job_title and job_city
    res = query.split(' in ')
    job_title = res[0].strip()
    job_city = res[1].split(',')[0].strip()

    if (job_city == 'United States'):
        print(str.upper(job_title))
        sql_query = f"""SELECT * FROM {table_name}
                WHERE UPPER(job_title) LIKE %s
                  AND apply_flag=%s
                order by (job_apply_quality_score,job_posted_at_datetime_utc) desc
                 limit 100;"""
        params = (f"%{job_title.upper()}%", 'N')

        df = pd.read_sql_query(sql_query, engine, params=params)

    else:
        # Use parameterized query with placeholders
        sql_query = f"""SELECT * FROM {table_name}
                        WHERE UPPER(job_title) LIKE %s AND UPPER(job_city) LIKE %s AND apply_flag='N'
                        order by (job_apply_quality_score,job_posted_at_datetime_utc) desc;"""
        params = (f"%{job_title.upper()}%", f"%{job_city.upper()}%")
        df = pd.read_sql_query(sql_query, engine, params=params)

    return df.to_json(orient='records')


def database_apply(id):
    table_name = 'listings'
    connection = create_engine(database_url)
    sql_query = f"""UPDATE {table_name} SET apply_flag='Y' where job_id='{id}';"""
    connection.execute(sql_query)
    connection.dispose()
    return f'Updated flag for {id}'


def remove_job(id):
    table_name = 'listings'
    connection = create_engine(database_url)
    sql_query = f"""UPDATE {table_name} SET apply_flag='I' where job_id='{id}';"""
    connection.execute(sql_query)
    connection.dispose()
    return f'Updated flag for {id}'
