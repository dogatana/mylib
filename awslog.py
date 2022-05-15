import time
from datetime import timezone

import boto3

LIMIT_MAX = 10000

def get_records(log_group, start_dt, end_dt, limit, interval, query):
    """ログの検索"""

    if start_dt > end_dt:
        raise ValueError(f"# star {start_dt} is newer thant end {end_dt}")

    if limit < 1 or limit > LIMIT_MAX:
        raise ValueError(f"# invalid limit {limit}")

    client = boto3.client("logs")

    print("# query", query, sep="\n")

    res = client.start_query(
        logGroupName=log_group,
        startTime=aws_timestamp(start_dt),
        endTime=aws_timestamp(end_dt),
        queryString=query,
        limit=limit,
    )
    query_id = res.get("queryId")
    print("# query_id", query_id)

    while True:
        res = client.get_query_results(queryId=query_id)
        status = res["status"]
        print("# query result", status)
        if status == "Complete":
            break
        time.sleep(interval)

    records = []
    for result in res["results"]:
        records.append(
            {item["field"]: item["value"] for item in result if item["field"] != "@ptr"}
        )

    if len(records) == limit:
        print(f"# reach limit {limit}, may not include all records")
    return records


def aws_timestamp(dt):
    """datetime から AWS のタイムスタンプを取得"""
    return int(dt.astimezone(timezone.utc).timestamp()) * 1000
