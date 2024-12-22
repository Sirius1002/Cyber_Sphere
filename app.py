# Cloud Security Config Checker - Backend (Python)
# Using Flask for backend and AWS SDK (Boto3) for interacting with AWS services.

from flask import Flask, request, jsonify
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

app = Flask(__name__)

# AWS Configuration
AWS_REGION = "us-east-1"
s3_client = boto3.client('s3', region_name=AWS_REGION)

# Helper function to check S3 bucket configurations
def check_s3_bucket_security():
    try:
        buckets = s3_client.list_buckets()
        findings = []

        for bucket in buckets['Buckets']:
            bucket_name = bucket['Name']
            bucket_acl = s3_client.get_bucket_acl(Bucket=bucket_name)

            # Check for public access
            for grant in bucket_acl['Grants']:
                if grant['Grantee'].get('URI') == "http://acs.amazonaws.com/groups/global/AllUsers":
                    findings.append({
                        "bucket": bucket_name,
                        "issue": "Public access detected",
                        "severity": "High"
                    })

        return findings

    except NoCredentialsError:
        return {"error": "AWS credentials not found."}
    except PartialCredentialsError:
        return {"error": "Incomplete AWS credentials."}
    except Exception as e:
        return {"error": str(e)}

# API Endpoints
@app.route("/scan/s3", methods=["GET"])
def scan_s3():
    findings = check_s3_bucket_security()
    return jsonify(findings)

@app.route("/scan", methods=["POST"])
def scan_all():
    # Example to include multiple scans in future
    s3_findings = check_s3_bucket_security()
    return jsonify({
        "s3_findings": s3_findings
    })

if __name__ == "__main__":
    app.run(debug=True)
