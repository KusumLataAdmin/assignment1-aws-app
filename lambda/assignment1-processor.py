"""
assignment1-processor
Triggered by: SQS (assignment1-queue)
Purpose: Processes S3 upload event messages delivered via SQS (S3 -> SNS -> SQS
fan-out) and logs them to CloudWatch.
IAM: Scoped to sqs:ReceiveMessage/DeleteMessage/GetQueueAttributes on
assignment1-queue only, plus CloudWatch Logs write access to its own
log group only (see assignment1-sqs-read inline policy).
"""

import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    for record in event["Records"]:
        body = json.loads(record["body"])
        logger.info(f"Processed S3 event: {json.dumps(body)}")
    return {"statusCode": 200}
