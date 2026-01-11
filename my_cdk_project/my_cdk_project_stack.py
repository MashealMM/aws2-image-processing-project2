from aws_cdk import (
    Stack,
    RemovalPolicy,
    Duration,
    aws_s3 as s3,
    aws_lambda as _lambda,
    aws_s3_notifications as s3n,
    aws_apigateway as apigw
)
from constructs import Construct

class MyCdkProjectStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # -----------------------------
        # 1) S3 bucket for image uploads
        # -----------------------------
        self.bucket = s3.Bucket(
            self,
            "ImageUploadBucket",
            versioned=False,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True
        )

        # -----------------------------
        # 2) Pillow Layer (Python 3.9)
        # -----------------------------
        pillow_layer = _lambda.LayerVersion(
            self,
            "PillowLayer",
            code=_lambda.Code.from_asset("pillow-layer.zip"),
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_9],
            description="Custom Pillow Layer built on Linux"
        )

        # -----------------------------
        # 3) Lambda function for image processing (Python 3.9)
        # -----------------------------
        self.image_processor = _lambda.Function(
            self,
            "ImageProcessorFunction",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="image_processor.handler",
            code=_lambda.Code.from_asset("lambda"),
            layers=[pillow_layer],
            timeout=Duration.seconds(10)
        )
        self.bucket.grant_put(self.image_processor)

        # Allow Lambda to read from S3
        self.bucket.grant_read(self.image_processor)

        # Trigger Lambda when a new file is uploaded
        self.bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED,
            s3n.LambdaDestination(self.image_processor)
        )

        # -----------------------------
        # 4) Lambda to generate presigned upload URLs (Python 3.9)
        # -----------------------------
        self.generate_url = _lambda.Function(
            self,
            "GenerateUploadURLFunction",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="generate_url.handler",
            code=_lambda.Code.from_asset("lambda"),
            environment={
                "BUCKET_NAME": self.bucket.bucket_name
            }
        )

        # Allow Lambda to generate presigned URLs (PUT)
        self.bucket.grant_put(self.generate_url)

        # -----------------------------
        # 5) API Gateway endpoint
        # -----------------------------
        api = apigw.LambdaRestApi(
            self,
            "GenerateUploadURLApi",
            handler=self.generate_url,
            proxy=False
        )

        upload = api.root.add_resource("upload")
        upload.add_method(
            "GET",
            apigw.LambdaIntegration(self.generate_url)
        )