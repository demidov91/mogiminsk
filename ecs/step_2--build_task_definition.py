import os
import json


prefix = 'DEV_' if os.environ.get('CIRCLE_BRANCH') != 'master' else ''
aws_account_id = os.environ['AWS_ACCOUNT_ID']


print(json.dumps({
    "requiresCompatibilities": [
        "FARGATE"
    ],
    "containerDefinitions": [
        {
            "environment": [
                {
                    "name": "POSTGRES_PASSWORD",
                    "value": os.environ['POSTGRES_PASSWORD']
                }
            ],
            "essential": True,
            "image": "postgres:9.6.10-alpine",
            "mountPoints": [
                {
                    "containerPath": "/var/lib/postgresql/data",
                    "sourceVolume": prefix + "Mogminskbot_Pgsql"
                }
            ],
            "name": "postgres",
            "portMappings": [
                {
                    "containerPort": 5432,
                    "hostPort": 5432
                }
            ]
        },
        {
            "environment": [
                {
                    "name": "POSTGRES_PASSWORD",
                    "value": os.environ['POSTGRES_PASSWORD'],
                },
                {
                    "name": "TELEGRAM_TOKEN",
                    "value": os.environ[prefix + 'TELEGRAM_TOKEN']
                },
                {
                    "name": "TELEGRAM_API_KEY",
                    "value": os.environ[prefix + 'TELEGRAM_API_KEY']
                },
                {
                    "name": "VIBER_API_KEY",
                    "value": os.environ[prefix + 'VIBER_API_KEY']
                },
                {
                    "name": "VIBER_TOKEN",
                    "value": os.environ[prefix + 'VIBER_TOKEN']
                },
                {
                    "name": "SENTRY_DSN",
                    "value": os.environ['SENTRY_DSN']
                },
                {
                    "name": "SENTRY_ENVIRONMENT",
                    "value": os.environ[prefix + 'SENTRY_ENVIRONMENT']
                },
                {
                    "name": "POSTGRESS_HOST",
                    "value": os.environ['POSTGRESS_HOST']
                },
                {
                    "name": "POSTGRESS_PORT",
                    "value": os.environ['POSTGRESS_PORT']
                }
            ],
            "essential": True,
            "image": f"{aws_account_id}.dkr.ecr.eu-central-1.amazonaws.com/mogiminsk:latest",
            "mountPoints": [],
            "name": "python",
            "portMappings": [
                {
                    "containerPort": 8090,
                    "hostPort": 8090
                }
            ],
            "logConfiguration": {
                "logDriver": "awslogs",
                "options": {
                  "awslogs-group": "/ecs/mogiminsk-python",
                  "awslogs-region": "eu-central-1",
                  "awslogs-stream-prefix": "ecs"
                }
            },
        }
    ],
    "volumes": [
        {
            "name": prefix + "Mogminskbot_Pgsql"
        }
    ],
    "networkMode": "awsvpc",
    "memory": "512",
    "cpu": "256",
    "family": "mogiminsk-madness",
    "executionRoleArn": f"arn:aws:iam::{aws_account_id}:role/ecsTaskExecutionRole",
    "placementConstraints": []
}, indent=2))
