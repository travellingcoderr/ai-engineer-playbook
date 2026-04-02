import boto3
import time
import json

# ☁️ Mocking the SageMaker Client
class MockSageMakerClient:
    def create_training_job(self, **kwargs):
        print(f"🚀 [SageMaker] Starting Training Job: {kwargs['TrainingJobName']}")
        time.sleep(1)
        return {"TrainingJobArn": "arn:aws:sagemaker:us-east-1:12345:training-job/fraud-detect-v1"}

    def create_model(self, **kwargs):
        print(f"📦 [SageMaker] Registering Model: {kwargs['ModelName']}")
        return {"ModelArn": "arn:aws:sagemaker:us-east-1:12345:model/fraud-detect-v1"}

    def create_endpoint_config(self, **kwargs):
        print(f"⚙️ [SageMaker] Creating Endpoint Config: {kwargs['EndpointConfigName']}")
        return {"EndpointConfigArn": "arn:aws:sagemaker:us-east-1:12345:endpoint-config/fraud-detect-v1"}

    def create_endpoint(self, **kwargs):
        print(f"🌐 [SageMaker] Deploying Endpoint: {kwargs['EndpointName']}")
        return {"EndpointArn": "arn:aws:sagemaker:us-east-1:12345:endpoint/fraud-detect-v1"}

# 🏦 Production Deployment Flow (Simulated)
def deploy_fraud_detector():
    sm = MockSageMakerClient()
    
    # 1. Start Training Job
    sm.create_training_job(
        TrainingJobName="fraud-model-train-2024",
        AlgorithmSpecification={"TrainingImage": "pytorch-training:latest"},
        InputDataConfig=[{"ChannelName": "train", "DataSource": {"S3DataSource": {"S3Uri": "s3://purple-bucket/data/"}}}]
    )

    # 2. Register for Interface
    sm.create_model(
        ModelName="fraud-detection-model",
        PrimaryContainer={"Image": "pytorch-inference:latest", "ModelDataUrl": "s3://purple-bucket/artifacts/model.tar.gz"}
    )

    # 3. Create Endpoint Config (Scaling/Instance Type)
    sm.create_endpoint_config(
        EndpointConfigName="fraud-detection-v1-config",
        ProductionVariants=[{
            "InstanceType": "ml.m5.xlarge",
            "InitialInstanceCount": 2,
            "VariantName": "AllTraffic"
        }]
    )

    # 4. Final Deployment
    sm.create_endpoint(
        EndpointName="fraud-detection-prod-endpoint",
        EndpointConfigName="fraud-detection-v1-config"
    )

    print("\n✅ Deployment Command Sent Successfully!")
    print("---")
    print("💡 Interview Tip: Mention that SageMaker 'Endpoints' are basically managed Docker containers")
    print("that handle auto-scaling, A/B testing (ProductionVariants), and monitoring out of the box.")

if __name__ == "__main__":
    deploy_fraud_detector()
