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
		'domain_name': 'cloudcloud-site-app.s3-website-eu-west-1.amazonaws.com',
	},
	'log_bucket': {
		'name': 'cloudcloud-site-logs',
		'prefix': 'cloudfront/',
	},
	'ssl_certificate_arn': 'arn:aws:acm:us-east-1:682695698822:certificate/ac4effec-29f1-4419-a0a7-fc3a79e00b73',
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
				Id = 'origin',
				DomainName = CONFIG['origin']['domain_name'],
				CustomOriginConfig = troposphere.cloudfront.CustomOrigin(
					OriginProtocolPolicy = 'http-only', # No SSL for S3 websites.
				),
			),
		],
		# ViewerCertificate = troposphere.cloudfront.ViewerCertificate(
		# 	IamCertificateId = CONFIG['ssl_certificate_arn'],
		# 	# MinimumProtocolVersion = 'TLSv1',
		# 	SslSupportMethod = 'sni-only',
		# ),
		DefaultCacheBehavior = troposphere.cloudfront.DefaultCacheBehavior(
			ViewerProtocolPolicy = 'allow-all', # @todo XXX redirect-to-https when SSL is in place.
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
			TargetOriginId = 'origin',
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
