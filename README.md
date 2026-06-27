---
title: My Mlflow Tracker
emoji: 👁
colorFrom: gray
colorTo: green
sdk: docker
pinned: false
short_description: 'MLFlow tracker for jedha '
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference

# jedha-mlworkflow

## build et lancement du mlflow ui 
```
docker build . -t jedha-mlworkflow:0.1.0
docker run --rm -p  5000:5000 -e PORT=5000 jedha-mlworkflow:0.1.0
```
## avec base postgres extrnalisé
```
docker build . -t jedha-mlworkflow:0.2.0
docker run --rm -p 5000:5000 -e PORT=5000 -e BACKEND_STORE_URI="postgresql://neondb_owner:xxxxxx.eu-west-2.aws.neon.tech/neondb?sslmode=require" jedha-mlworkflow:0.2.0
```
## lancement de train.py en local
```
export APP_URI=http://localhost:5000
python train.py
```

# depuis HuggingFace
## lancement de train.py en local avec mlflow tracker sur HuggingFace et ARTIFACT_STORE_URI sur un bucket S3
```
export APP_URI=https://franckidda-my-mlflow-tracker.hf.space
export AWS_SECRET_ACCESS_KEY=xxxxxxxx
export AWS_ACCESS_KEY_ID=xxxxxxxxxxxx
pip install boto3
python train.py
```


## Get container logs (SSE)
```
    curl -N \
     -H "Authorization: Bearer $HF_TOKEN" \
     "https://huggingface.co/api/spaces/franckidda/my-mlflow-tracker/logs/run"
```
## Get build logs (SSE)
```
     curl -N \
     -H "Authorization: Bearer $HF_TOKEN" \
     "https://huggingface.co/api/spaces/franckidda/my-mlflow-tracker/logs/build"
```

## mlflow CLI - necessite la variable MLFLOW_TRACKING_URI
```
pip install mlflow
export MLFLOW_TRACKING_URI=https://franckidda-my-mlflow-tracker.hf.space
(RLenv) fidda@BIBIFRANCK-2:~/jedha_architecte_ia/aifs-ft-01/M8-MLEngineering/D5/exercises/my-mlflow-tracker$ mlflow experiments search
Experiment Id    Name                        Artifact Location  
---------------  --------------------------  -------------------
0                Default                     mlflow-artifacts:/0
1                my-first-mlflow-experiment  mlflow-artifacts:/1
(RLenv) fidda@BIBIFRANCK-2:~/jedha_architecte_ia/aifs-ft-01/M8-MLEngineering/D5/exercises/my-mlflow-tracker$ mlflow experiments get --experiment-id 1
Experiment ID      : 1
Name               : my-first-mlflow-experiment
Artifact Location  : mlflow-artifacts:/1
Lifecycle Stage    : active
Creation Time      : 1782547888126
Last Update Time   : 1782547888126
Tags               : 

(RLenv) fidda@BIBIFRANCK-2:~/jedha_architecte_ia/aifs-ft-01/M8-MLEngineering/D5/exercises/my-mlflow-tracker$ mlflow experiments get --experiment-id 2
Experiment ID      : 2
Name               : my-second-mlflow-experiment
Artifact Location  : s3://my-jedha-bucket-for-mlflow/2
Lifecycle Stage    : active
Creation Time      : 1782565502537
Last Update Time   : 1782565502537
Tags               : 
```

## pip install boto3 + credential AWS dans la session active ou sera lancé le srcipt train.py
```
2026/06/27 15:13:18 WARNING mlflow.sklearn: Saving scikit-learn models in the pickle or cloudpickle format requires exercising caution because these formats rely on Python's object serialization mechanism, which can execute arbitrary code during deserialization. The recommended safe alternative is the 'skops' format. For more information, see: https://scikit-learn.org/stable/model_persistence.html
2026/06/27 15:13:26 WARNING mlflow.utils.autologging_utils: Encountered unexpected error during sklearn autologging: Unable to locate credentials
LogisticRegression model
Accuracy: 1.0
🏃 View run persistent-mouse-123 at: https://franckidda-my-mlflow-tracker.hf.space/#/experiments/2/runs/d3e6f98283c94a5ab3884139c46b8fa9
🧪 View experiment at: https://franckidda-my-mlflow-tracker.hf.space/#/experiments/2
```

## Controle du contenu du S3 associé au service ml-flow tracker
```
install de awscli
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
    unzip awscliv2.zip
    sudo ./aws/install
    aws --version

export AWS_SECRET_ACCESS_KEY=xxxxxxxx
export AWS_ACCESS_KEY_ID=xxxxxxxxxxxx

fidda@BIBIFRANCK-2:~$ aws s3 ls s3://my-jedha-bucket-for-mlflow/2/models/m-f74925c4bbce4621b1e1b00c63042ae0/artifacts/
2026-06-27 15:17:20        960 MLmodel
2026-06-27 15:17:20        247 conda.yaml
2026-06-27 15:17:21        824 model.pkl
2026-06-27 15:17:21        123 python_env.yaml
2026-06-27 15:17:20        121 requirements.txt

fidda@BIBIFRANCK-2:~$ aws s3 ls s3://my-jedha-bucket-for-mlflow/2/acf74fbc9ea047098a0efc72124539b4/artifacts/
2026-06-27 15:17:24      49274 estimator.html
2026-06-27 15:17:29        102 metric_info.json
2026-06-27 15:17:24      29847 training_confusion_matrix.png
```