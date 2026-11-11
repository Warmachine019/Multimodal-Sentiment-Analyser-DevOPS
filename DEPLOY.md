# Deploy on AWS Learner Lab (EC2 + Docker Compose + Prometheus + Grafana)

Files to copy INTO your project folder (overwrite): app.py, Dockerfile, docker-compose.yml, requirements-cloud.txt,
deploy/ (nginx.conf, ec2_setup.sh), monitoring/ (whole folder), templates/index.html, static/capture.js,
face/predict.py, speech/predict.py, storage.py.  Then `git add . && git commit -m "cloud + monitoring" && git push`.

## AWS console
1. Start Lab -> wait for the green dot -> click AWS. Region: us-east-1.
2. EC2 -> Launch instance: Amazon Linux 2023, t3.large, key pair vockey, 30 GB storage,
   Advanced details -> IAM instance profile = LabInstanceProfile.
3. Security group inbound rules:  SSH 22 (Anywhere)  |  HTTPS 443 (Anywhere)  |  3000 (My IP)  |  9090 (My IP)
4. Connect -> EC2 Instance Connect (browser terminal).

## On the instance
sudo dnf install -y git
git clone <your-repo-url> app && cd app
sudo bash deploy/ec2_setup.sh        # first build takes ~15-20 min

## Use it
App:        https://<public-ip>         (accept the certificate warning, allow camera + mic)
Grafana:    http://<public-ip>:3000     (admin / labdemo123) -> Dashboards -> Sentiment Analyser
Prometheus: http://<public-ip>:9090     (Status -> Targets: all should be UP)

## Update after code changes
cd ~/app && git pull && sudo docker compose up -d --build

## Save credits
Stop the instance when finished (EC2 -> Instance state -> Stop). The public IP changes on restart.
