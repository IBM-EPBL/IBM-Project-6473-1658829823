from flask import Flask, redirect, url_for, render_template, request
import ibm_boto3
from ibm_botocore.client import Config, ClientError

COS_ENDPOINT = "https://s3.jp-tok.cloud-object-storage.appdomain.cloud"
COS_API_KEY_ID = "meCOCF7JI7wdXw8hFeMm8eHjFrBqSSM7BI7VwiaRQ5uM"
COS_INSTANCE_CRN = "crn:v1:bluemix:public:cloud-object-storage:global:a/dd8aafd0309c4c368a44bf452a6e4ade:2401d891-01cb-4aac-accd-8513a1a328c3::"

cos = ibm_boto3.resource("s3",
                         ibm_api_key_id=COS_API_KEY_ID,
                         ibm_service_instance_id=COS_INSTANCE_CRN,
                         config=Config(signature_version="oauth"),
                         endpoint_url=COS_ENDPOINT
                         )

app = Flask(__name__)


def get_bucket_contents(bucket_name):
    print("Retrieving bucket contents from: {0}".format(bucket_name))
    try:
        files = cos.Bucket(bucket_name).objects.all()
        files_names = []
        for file in files:
            files_names.append(file.key)
            print("Item: {0} ({1} bytes).".format(file.key, file.size))
        return files_names
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to retrieve bucket contents: {0}".format(e))



@app.route('/')
def index():
    file1 = get_bucket_contents('image-bucket-kmnr')
    return render_template('index.html', files=file1)




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8089, debug=True)
