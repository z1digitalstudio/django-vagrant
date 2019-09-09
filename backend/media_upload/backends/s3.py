import boto3
from botocore.exceptions import ClientError

from django.conf import settings
from media_upload.backends.base import BaseMediaUploadBackend


class S3MediaUploadBackend(BaseMediaUploadBackend):
    def get_presigned_url(self):
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )

        filename = self._get_filename()
        mimetype = self._get_content_type()
        try:
            response = s3_client.generate_presigned_url(
                "put_object",
                Params={
                    "Bucket": settings.AWS_BUCKET_NAME,
                    "Key": filename,
                    "ContentType": mimetype,
                },
                ExpiresIn=int(settings.UPLOAD_TOKEN_EXPIRE_TIME),
                HttpMethod="PUT",
            )
        except ClientError:
            return
        return {
            "uploadUrl": response,
            "contentType": mimetype,
            "retrieveUrl": response.split("?")[0],
        }
