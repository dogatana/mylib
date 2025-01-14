""""
AWS CloudWatchLogs の取得ヘルパ

参考： https://docs.aws.amazon.com/ja_jp/AmazonCloudWatch/latest/logs/CWL_QuerySyntax.html
"""
import logging
import time
import traceback
from datetime import datetime, timezone
from typing import List

import boto3

# API では最大 10,000 件まで取得可能
LIMIT_MAX = 10_000

client = boto3.client("logs")


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
        raise ValueError(f"# start:{start_dt} >= end:{end_dt}")

    if limit < 1 or limit > LIMIT_MAX:
        raise ValueError(f"# invalid limit {limit}")

    res = client.start_query(
        logGroupName=log_group,
        startTime=aws_timestamp(start_dt),
        endTime=aws_timestamp(end_dt),
        queryString=query,
        limit=limit,
    )
    query_id = res.get("queryId")
    logging.info(f"query_id: {query_id}")

    break_status = set(["Complete", "Failed", "Cancelled", "Timeout", "Unknown"])
    res = {}
    try:
        while True:
            res = client.get_query_results(queryId=query_id)
            status = res["status"]
            if status in break_status:
                print("")
                logging.info(f"query result: {status}")
                break
            if status == "Running":
                print(".", end="", flush=True)
            else:
                logging.info(f"query result: {status}")
            time.sleep(interval)
    except KeyboardInterrupt:
        logging.warning("*** KeyBoardInterrupt ***")
        return []
    except Exception as e:
        logging.error("*** Exception ***\n" "".join(traceback.format_exception(e)))
        return []

    records = []

    if "results" not in res:
        return records

    for result in res["results"]:
        records.append(
            {item["field"]: item["value"] for item in result if item["field"] != "@ptr"}
        )

    if len(records) == limit:
        logging.warning(f"reach limit {limit}, the result may not include all records")
    return records


def aws_timestamp(dt: datetime) -> int:
    """local datetime から AWS のタイムスタンプを取得"""
    return int(dt.astimezone(timezone.utc).timestamp())


def query_loop(query_id, interval):
    break_status = set(["Complete", "Failed", "Cancelled", "Timeout", "Unknown"])
    while True:
        res = client.get_query_results(queryId=query_id)
        status = res["status"]
        logging.info(f"query result: {status}")
        if status in break_status:
            break
        time.sleep(interval)
