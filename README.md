# AWS Assignment 1 (L2) - Code Deliverable

Scalable Web Application with Monitoring & Automation

This folder contains the application code, Dockerfile, and Lambda function
source referenced in the assignment screenshots. All resources described
below were deployed manually via the AWS Management Console in account
`681604068151`, region `us-east-1`.

## Folder structure

```
assignment1-code/
├── app/
│   ├── Dockerfile        # Elastic Beanstalk Docker platform build
│   └── index.html        # Static app content served by Nginx
├── lambda/
│   ├── assignment1-processor.py         # SQS-triggered
│   ├── assignment1-sns-processor.py     # SNS-triggered
│   └── assignment1-scheduled-task.py    # EventBridge-triggered
└── README.md
```

## Architecture overview

**Web tier**
- VPC (`project-vpc`, 10.0.0.0/16) across 2 AZs, 2 public + 2 private subnets,
  Internet Gateway, NAT Gateway, S3 Gateway endpoint.
- Elastic Beanstalk environment `Assignment1-app-env` (Docker platform),
  load-balanced, Auto Scaling Min 1 / Max 2, scaling on CPUUtilization
  (>70% scale up, <30% scale down).
- App source is `app/Dockerfile` + `app/index.html`, served via Nginx on
  port 80 behind an Application Load Balancer in the public subnets.

**Data tier**
- RDS MySQL instance `assignment1-db` (db.t4g.micro) in the private
  subnets, not publicly accessible. Automated backups enabled (retention
  capped at 1 day by the AWS Learner account's free-tier limit).
- Master credentials are managed by RDS via **AWS Secrets Manager**
  (`rds!db-...`), not typed manually. The EB environment has an
  environment property `DB_SECRET_ARN` pointing at that secret's ARN; a
  production version of `app/` would call `secretsmanager:GetSecretValue`
  at startup using this ARN to obtain DB credentials rather than hardcoding
  them.
- Security group `rds-sg` only allows inbound MySQL/Aurora (3306) traffic
  from the Elastic Beanstalk EC2 security group.
- DynamoDB table `assignment1-app-logs` (on-demand billing) for
  application logs/metadata, partition key `eventId`, sort key `timestamp`.

**Event-driven pipeline**
- S3 bucket `assignment1-uploads-kusumlata` (versioning enabled, lifecycle
  rule transitioning objects to Standard-IA after 30 days, server access
  logging to `assignment1-access-logs-kusumlata`).
- On every object upload, S3 publishes to SNS topic
  `assignment1-upload-topic` (fan-out pattern, since S3 does not allow two
  direct notification configs on the same event type without a filter).
- The SNS topic fans out to:
  - `assignment1-queue` (SQS), consumed by `lambda/assignment1-processor.py`
  - `lambda/assignment1-sns-processor.py`, subscribed directly to the topic
  - An email subscription for manual verification
- A `/public/*` bucket policy allows read-only public access to static
  files under that prefix only; the rest of the bucket stays private.

**Scheduled automation**
- EventBridge rule `assignment1-scheduled-rule` (rate: 5 minutes) invokes
  `lambda/assignment1-scheduled-task.py`.

**Security**
- Each Lambda function has its own least-privilege IAM role:
  - `assignment1-processor-role`: SQS receive/delete/get-attributes scoped
    to `assignment1-queue` only, CloudWatch Logs scoped to its own log
    group only.
  - `assignment1-sns-processor-role`: CloudWatch Logs scoped to its own
    log group only (SNS invokes via a resource policy, no execution-role
    permission needed).
  - `assignment1-scheduled-task-role`: CloudWatch Logs scoped to its own
    log group only.

**Monitoring**
- CloudWatch alarms: `EBS-High-CPU-Alarm`, `EBS-High-Memory-Alarm`,
  `RDS-High-CPU-Alarm`, `RDS-Low-Memory-Alarm`, all notifying SNS topic
  `assignment1-alerts`.
- EC2 memory metrics (`mem_used_percent`) are collected via the CloudWatch
  agent, installed and configured through Systems Manager Run Command with
  a custom config pushed via Parameter Store (`AmazonCloudWatch-linux-config`),
  since EC2 does not report memory usage by default.
- CloudWatch dashboard `assignment1-dashboard` visualizes EBS (CPU +
  memory), RDS (CPU + freeable memory), S3 (bucket size/object count),
  Lambda (invocations/errors for all three functions), and DynamoDB
  (consumed read/write capacity) on one page.

## Notes

- This is a learning/assignment environment (AWS Learner Lab-style
  account), so some settings are capped below normal production defaults
  (e.g. RDS backup retention limited to 1 day). This is documented where
  relevant rather than worked around.
- The `app/` folder here is a minimal representative version of the
  deployed sample application for submission purposes; the exact bundle
  Elastic Beanstalk is running can be downloaded from **Elastic Beanstalk
  → Application versions** in the console if an identical copy is needed.
