"""
assignment1-scheduled-task
Triggered by: EventBridge rule (assignment1-scheduled-rule), fixed rate of
5 minutes.
Purpose: Placeholder periodic job (e.g. a health check or cleanup task in a
real application) that logs its own execution timestamp to CloudWatch,
proving the schedule is firing correctly.
IAM: CloudWatch Logs write access scoped to its own log group only.
EventBridge invokes this function via a resource-based policy attached
to the function itself, created automatically when the rule's target
was configured.
"""

import json
import logging
import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    now = datetime.datetime.utcnow().isoformat()
    logger.info(f"Scheduled task executed at {now}")
    return {"statusCode": 200, "body": f"Ran at {now}"}
