from troposphere import (
	Template,
)

import troposphere
import troposphere.cloudfront

CONFIG = {
	'public': {
		'domain_names': [
			'cloudcloud.io',
			'*.cloudcloud.io',
		],
	},
	'origin': {
		'domain_name': 'cloudcloud-site-app.s3.amazonaws.com',
	},
	'log_bucket': {
		'name': 'cloudcloud-site-logs',
		'prefix': 'cloudfront/',
	},
	'ssl_certificate_arn': 'arn:aws:acm:us-east-1:682695698822:certificate/92d6717c-52a3-4c6e-9928-79f1ae68d8e1',
}

template = Template()

cloudfront_distribution = template.add_resource(troposphere.cloudfront.Distribution(
	'CloudFrontDistribution',
	DistributionConfig = troposphere.cloudfront.DistributionConfig(
		Enabled = True,
		PriceClass = 'PriceClass_100',
		Aliases = CONFIG['public']['domain_names'],
		Origins = [
			troposphere.cloudfront.Origin(
				Id = 'app-s3-origin',
				DomainName = CONFIG['origin']['domain_name'],
				S3OriginConfig = troposphere.cloudfront.S3Origin(
				),
			),
		],
		ViewerCertificate = troposphere.cloudfront.ViewerCertificate(
			AcmCertificateArn = CONFIG['ssl_certificate_arn'],
			SslSupportMethod = 'sni-only',
		),
		DefaultRootObject = 'index.html',
		DefaultCacheBehavior = troposphere.cloudfront.DefaultCacheBehavior(
			ViewerProtocolPolicy = 'redirect-to-https',
			AllowedMethods = [
				'GET',
				'HEAD',
			],
			CachedMethods = [
				'GET',
				'HEAD',
			],
			Compress = True,
			DefaultTTL = 10, # @todo XXX Update this.
			MinTTL = 10, # @todo XXX Update this.
			MaxTTL = 10, # @todo XXX Update this.
			TargetOriginId = 'app-s3-origin',
			ForwardedValues = troposphere.cloudfront.ForwardedValues(
				QueryString = False,
				Headers = [],
				Cookies = troposphere.cloudfront.Cookies(
					Forward = 'none',
				),
			),
		),
		Logging = troposphere.cloudfront.Logging(
			Bucket = CONFIG['log_bucket']['name'] + '.s3.amazonaws.com',
			Prefix = CONFIG['log_bucket']['prefix'],
			IncludeCookies = True,
		),
	),
))

print template.to_json()
