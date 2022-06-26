""""
AWS CloudWatchLogs の取得ヘルパ

参考： https://docs.aws.amazon.com/ja_jp/AmazonCloudWatch/latest/logs/CWL_QuerySyntax.html
"""
import time
from datetime import datetime, timezone
from typing import List

import boto3

# API では最大 10,000 件まで取得可能
LIMIT_MAX = 10_000


def get_records(
    log_group: str,
    start_dt: datetime,
    end_dt: datetime,
    limit: int,
    interval: int,
    query: str,
) -> List:
    """ログの検索"""

    if start_dt >= end_dt:
        raise ValueError(f"# star:{start_dt} >= end:{end_dt}")

    if limit < 1 or limit > LIMIT_MAX:
        raise ValueError(f"# invalid limit {limit}")

    client = boto3.client("logs")

    print("# query string", query, sep="\n")

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
        print(f"# reach limit {limit}, the result may not include all records")
    return records


def aws_timestamp(dt: datetime) -> int:
    """local datetime から AWS のタイムスタンプを取得"""
    return int(dt.astimezone(timezone.utc).timestamp())
