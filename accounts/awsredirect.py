import boto3

session = boto3.Session(
    aws_access_key_id= 'AKIAYKYQ6HVHRNSQMVWQ',
    aws_secret_access_key = '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'
)

class image():
    def UploadImage(image):
        imagedata = image
        s3 = boto3.resource('s3')
        try:
            object = s3.Object('uniqueupgradebooking', image.name)
            object.put(ACL='public-read',Body=imagedata,Key=image.name)
            return True
        except Exception as e:
            return e