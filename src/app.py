import os
from flask import Flask, jsonify, abort
import boto3
from botocore.exceptions import ClientError

def create_app():
    app = Flask(__name__)

    # Load configuration from environment
    region   = os.getenv("AWS_REGION")
    table    = os.getenv("DYNAMODB_TABLE")
    code_key = os.getenv("CODE_NAME")

    # DynamoDB setup
    dynamodb = boto3.resource("dynamodb", region_name=region)
    table = dynamodb.Table(table)

    @app.route("/secret")
    def secret():
        try:
            resp = table.get_item(Key={"code_name": code_key})
        except ClientError as e:
            app.logger.error("DynamoDB error: %s", e)
            abort(500, "Error fetching secret")
        item = resp.get("Item")
        if not item or "secret_code" not in item:
            abort(404, "Secret not found")
        return jsonify({"secret_code": item["secret_code"]})

    @app.route("/health")
    def health():
        return jsonify({
            "status": "healthy",
            "container": os.getenv("DOCKER_HUB_REPO"),
            "project": os.getenv("PROJECT_URL")
        })

    return app
