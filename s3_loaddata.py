import s3util

S3BUCKET=""
S3PREFIX=""
S3_DELTA_LAKE_TABLE = f's3://{S3BUCKET}/{S3PREFIX}'
s3util.syncfrom("loans.delta", S3_DELTA_LAKE_TABLE)
