from troposphere import (
	Ref,
	Template,
)

import troposphere
import troposphere.s3

import awacs
import awacs.s3

CONFIG = {
	'app_bucket': {
		'name': 'cloudcloud-site-app',
	},
	'log_bucket': {
		'name': 'cloudcloud-site-logs',
		'object_lifetime_days': 21,
	},
}

template = Template()

log_bucket = troposphere.s3.Bucket(
	'LogBucket',
	BucketName = CONFIG['log_bucket']['name'],
	AccessControl = 'LogDeliveryWrite',
	LifecycleConfiguration = troposphere.s3.LifecycleConfiguration(
		Rules = [
			troposphere.s3.LifecycleRule(
				Id = 'DeleteOldObjects',
				Status = 'Enabled',
				ExpirationInDays = CONFIG['log_bucket']['object_lifetime_days'],
			),
		],
	),
)
template.add_resource(log_bucket)

app_bucket = troposphere.s3.Bucket(
	'AppBucket',
	BucketName = CONFIG['app_bucket']['name'],
	WebsiteConfiguration = troposphere.s3.WebsiteConfiguration(
		IndexDocument = 'index.html',
	),
	LoggingConfiguration = troposphere.s3.LoggingConfiguration(
		DestinationBucketName = Ref(log_bucket),
		LogFilePrefix = 's3/',
	),
)
template.add_resource(app_bucket)

app_bucket_policy = troposphere.s3.BucketPolicy(
	'AppBucketPolicy',
	Bucket = CONFIG['app_bucket']['name'],
	PolicyDocument = awacs.aws.Policy(
		Statement = [
			awacs.aws.Statement(
				Sid = 'AllowPublicRead',
				Effect = awacs.aws.Allow,
				Principal = awacs.aws.Principal('AWS', '*'),
				Action = [
					awacs.aws.Action('s3', 'GetObject'),
				],
				Resource = [
					awacs.s3.ARN('/'.join([
						CONFIG['app_bucket']['name'],
						'*',
					])),
				],
			),
		],
	),
)
template.add_resource(app_bucket_policy)

print template.to_json()
