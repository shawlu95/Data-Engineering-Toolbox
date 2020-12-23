### Cluster automation using CLI commands
#### Overview
Create a cluster using CLI commands and learn about the Dataproc-GCP workflow and workflow automation.

#### Objective
Create a customized Dataproc cluster using Cloud Shell.

#### Workflow
* Create a VM.
* Create a storage bucket at the **same region**.
* Create the environment variables VM:

```bash
BUCKET=<bucket-name>
MYREGION=<region>
MYZONE=<zone>
PROJECT_ID=<project ID>
BROWSER_IP=<your-browser-ip>
```

* Study the initialization script:

```bash
#!/bin/bash
# install Google Python client on all nodes
apt-get update
apt-get install -y python-pip
pip install --upgrade google-api-python-client

# Use metadata to differentiate master/worker nodes.
ROLE=$(/usr/share/google/get_metadata_value attributes/dataproc-role)
if [[ "${ROLE}" == 'Master' ]]; then
   git clone https://github.com/GoogleCloudPlatform/training-data-analyst
fi
```

* Copy script to bucket: `gsutil cp init-script.sh gs://$BUCKET`

* Create cluster from CLI. Datalab script also included:
    - tags: Applies a network tag so you can automate the creation of firewall rules.
    - scopes: Applies Cloud IAM restrictions and permissions to the cluster.
    - num-preemptible-workers: Controls the number of low cost worker nodes present.
    - initialization-actions: Customizes the software on the cluster.

```bash
gcloud dataproc clusters create cluster-custom \
--bucket $BUCKET \
--subnet default \
--zone $MYZONE \
--region $MYREGION \
--master-machine-type n1-standard-2 \
--master-boot-disk-size 100 \
--num-workers 2 \
--worker-machine-type n1-standard-1 \
--worker-boot-disk-size 50 \
--num-preemptible-workers 2 \
--image-version 1.2 \
--scopes 'https://www.googleapis.com/auth/cloud-platform' \
--tags customaccess \
--project $PROJECT_ID \
--initialization-actions 'gs://'$BUCKET'/init-script.sh','gs://dataproc-initialization-actions/datalab/datalab.sh'
```

* Create Firewall rule.

```bash
gcloud compute \
--project=$PROJECT_ID \
firewall-rules create allow-custom \
--direction=INGRESS \
--priority=1000 \
--network=default \
--action=ALLOW \
--rules=tcp:9870,tcp:8088,tcp:8080 \
--source-ranges=$BROWSER_IP/32 \
--target-tags=customaccess
```

#### Productions
* Turn the create commands into a script so that you can start up a cluster on demand.
* Add an option to the command to terminate the cluster after a quiet period.
* Turn the firewall rule into a script so that you can enable/disable external (browser) access only when it is required for administration activities.
* Develop and test your application in Datalab notebooks.
* Host the production application in a Cloud Storage bucket.
* Host and access your data in either Cloud Storage, BigQuery, or Bigtable.
* For capacity, Edit the number of preemptible worker nodes using Console, and the running cluster will adapt.
* Shut down the cluster when not in use, or schedule auto termination.
