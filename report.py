import subprocess
import time

target_sites = [
    "http://127.0.0.1:8080/WebGoat/"
]


for site_url in target_sites:
    
    # rm report file if exists
    rm_file_command = [
            "rm", "-f", f"/home/ec2-user/zap-scan-report.json",
    ]
    subprocess.run(rm_file_command)

    zap_command = [
        "/home/ec2-user/ZAP_2.14.0/zap.sh", "-cmd",
        "-quickurl", site_url,
        "-quickout", f"/home/ec2-user/zap-scan-report.json",
        "-port", "8090",
    ]
    subprocess.run(zap_command)
    
    # Upload report file to S3
    s3_upload_command = [
            "aws", "s3", "cp",
            f"/home/ec2-user/zap-scan-report.json",
            f"s3://zap-tbucket/Report/zap-scan-report.json",
    ]
    subprocess.run(s3_upload_command)
    time.sleep(30)
