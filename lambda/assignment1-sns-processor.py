"""
assignment1-sns-processor
Triggered by: SNS (assignment1-upload-topic)
Purpose: Subscribes directly to the SNS topic that S3 publishes to on every
object upload, and logs the notification content to CloudWatch.
IAM: CloudWatch Logs write access scoped to its own log group only.
No explicit SNS permission needed in the execution role -- SNS invokes
this function via a resource-based policy attached to the function
itself, created automatically when the trigger was added.
"""

import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    for record in event["Records"]:
        sns_message = record["Sns"]["Message"]
        logger.info(f"Received SNS notification: {sns_message}")
    return {"statusCode": 200}
