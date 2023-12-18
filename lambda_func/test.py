import os
import json
import boto3
import base64
import logging
from datetime import datetime, timezone
import securityhub

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

FINDING_TITLE = "CodeAnalysis"
FINDING_DESCRIPTION_TEMPLATE = "Summarized report of code scan with {0}"
FINDING_TYPE_TEMPLATE = "{0} code scan"
BEST_PRACTICES_OWASP = "https://owasp.org/www-project-top-ten/"
report_url = "https://aws.amazon.com"

def process_message(event):
    if event['messageType'] == 'CodeScanReport':
        account_id = boto3.client('sts').get_caller_identity().get('Account')
        region = os.environ['AWS_REGION']
        created_at = event['createdAt']
        source_repository = event['source_repository']
        source_branch = event['source_branch']
        source_commitid = event['source_commitid']
        build_id = event['build_id']
        report_type = event['reportType']
        finding_type = FINDING_TYPE_TEMPLATE.format(report_type)
        generator_id = f"{report_type.lower()}-{source_repository}-{source_branch}"
    
    if event and event.get('reportType') == 'OWASP-Dependency-Check':
        logger.info("success sca test report parsing")
        severity = 50
        FINDING_TITLE = "OWASP Dependency Check Analysis"
        dep_pkgs = len(event['report']['dependencies'])
        for i in range(dep_pkgs):
            if "packages" in event['report']['dependencies'][i]:
                confidence = event['report']['dependencies'][i]['packages'][0]['confidence']
                url = event['report']['dependencies'][i]['packages'][0]['url']
                finding_id = f"{i}-{report_type.lower()}-{build_id}"
                finding_description = f"Package: {event['report']['dependencies'][i]['packages'][0]['id']}, Confidence: {confidence}, URL: {url}"
                created_at = datetime.now(timezone.utc).isoformat()

                if confidence == "HIGHEST":
                    normalized_severity = 80
                else:
                    normalized_severity = 50

                securityhub.import_finding_to_sh(i, account_id, region, created_at, source_repository, source_branch, source_commitid, build_id, report_url, finding_id, generator_id, normalized_severity, severity, finding_type, FINDING_TITLE, finding_description, BEST_PRACTICES_OWASP)

def lambda_handler(event, context):
    """ Lambda entrypoint """
    try:
        logger.info("Starting function")
        process_message(event)
    except Exception as error:
        logger.error("Error {}".format(error))
        raise
