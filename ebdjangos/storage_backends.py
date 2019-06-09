from storages.backends.s3boto3 import S3Boto3Storage

class MediaSeatStorage(S3Boto3Storage):
    location = 'media/seat_images'
    file_overwrite = False

