import time
from datetime import timezone

import boto3

LIMIT_MAX = 10000

def get_records(log_group, start_dt, end_dt, limit, interval, query):
    """ログの検索"""

    if limit < 1 or limit > LIMIT_MAX:
        raise ValueError("# invalid limit", limit)

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

    return records


def aws_timestamp(dt):
    """datetime から AWS のタイムスタンプを取得"""
    return int(dt.astimezone(timezone.utc).timestamp()) * 1000
