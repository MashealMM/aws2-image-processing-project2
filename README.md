
 README.md — AWS 2 Image Processing Project
# AWS 2 Image Processing Project

This project demonstrates a serverless image processing workflow using AWS CDK. It is designed to resize uploaded images and store the processed versions in a dedicated folder, with accessibility in mind for visually impaired users.

##  Architecture

- **Amazon S3**: Stores uploaded and processed images.
- **AWS Lambda**: Triggered by S3 events to resize images using Pillow.
- **Lambda Layer**: Custom Linux-compatible layer containing Pillow.
- **API Gateway**: Provides a REST endpoint to generate pre-signed upload URLs.
- **IAM Roles**: Configured to allow secure access between services.

##  Workflow

1. User requests a pre-signed upload URL via API Gateway.
2. Image is uploaded to S3 using the URL.
3. S3 triggers the Lambda function.
4. Lambda downloads the image, resizes it to 256×256 pixels, and uploads it to `processed/` folder.

##  Deployment

This project uses AWS CDK (Python) for infrastructure as code.

```bash
cdk deploy


Ensure that pillow-layer.zip contains a top-level python/ folder with Pillow installed.
 Project Structure
aws2-image-processing-project/
├── lambda/
│   └── image_processor.py
├── pillow-layer.zip
├── my_cdk_project/
│   └── my_cdk_project_stack.py
├── README.md


 Status
- [x] Lambda triggers on S3 upload
- [x] Image resized and saved
- [x] Permissions configured
- [x] API Gateway tested
- [x] Logs verified in CloudWatch
Screenshots
Add screenshots of CloudWatch logs, S3 folders, or API responses here.

 Accessibility Focus
This project is optimized to support visually impaired users by enabling automated image processing and simplifying upload workflows.




