import json
import boto3
import os
from PIL import Image

def handler(event, context):
    print("🖼️ Event received:", json.dumps(event))

    # استخراج معلومات الملف من الحدث
    try:
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        print(f"📦 Bucket: {bucket}, 🗂️ Key: {key}")
    except Exception as e:
        print("❌ Failed to parse event:", str(e))
        return

    # إعداد المسارات المؤقتة
    s3 = boto3.client('s3')
    download_path = f"/tmp/{os.path.basename(key)}"
    upload_key = f"processed/{os.path.basename(key)}"
    upload_path = f"/tmp/processed-{os.path.basename(key)}"

    try:
        # تحميل الصورة من S3
        s3.download_file(bucket, key, download_path)
        print("✅ File downloaded to:", download_path)

        # فتح الصورة وتغيير حجمها
        with Image.open(download_path) as img:
            resized = img.resize((256, 256))

            # تحويل إلى RGB إذا كانت RGBA لتجنب خطأ JPEG
            if resized.mode == "RGBA":
                resized = resized.convert("RGB")

            # حفظ الصورة بصيغة JPEG
            resized.save(upload_path, format="JPEG")
            print("✅ Image resized and saved to:", upload_path)

        # رفع الصورة المعالجة إلى S3
        s3.upload_file(upload_path, bucket, upload_key)
        print("✅ Image uploaded to:", upload_key)

    except Exception as e:
        print("❌ Error during processing:", str(e))