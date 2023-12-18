import os
import json
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
    try:
        # 'body' 키를 사용하여 데이터를 가져오고, base64 디코딩 및 utf-8 디코딩 수행
        encoded_payload = event['body']
        decoded_payload = base64.b64decode(encoded_payload)
        logger.info("execute success")
        
    except Exception as e:
        # 오류가 발생한 경우 처리
        logger.info("execute fail")
        logger.error("Error {}".format(e))
    
    if decoded_payload and decoded_payload.get('reportType') == 'OWASP-Dependency-Check':
        logger.info("success sca test report parsing")
        severity = 50
        FINDING_TITLE = "OWASP Dependency Check Analysis"
        dep_pkgs = len(decoded_payload['report']['dependencies'])
        for i in range(dep_pkgs):
            if "packages" in decoded_payload['report']['dependencies'][i]:
                confidence = decoded_payload['report']['dependencies'][i]['packages'][0]['confidence']
                url = decoded_payload['report']['dependencies'][i]['packages'][0]['url']
                finding_id = f"{i}-{report_type.lower()}-{build_id}"
                finding_description = f"Package: {decoded_payload['report']['dependencies'][i]['packages'][0]['id']}, Confidence: {confidence}, URL: {url}"
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
