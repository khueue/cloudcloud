from troposphere import (
	Template,
)

import troposphere
import troposphere.route53

CONFIG = {
	'public': {
		'hosted_zone_name': 'cloudcloud.io',
		'domain_names': [
			'cloudcloud.io',
			'www.cloudcloud.io',
		],
	},
	'cloudfront': {
		'hosted_zone_id': 'Z2FDTNDATAQYW2',
		'domain_name': 'diwuc9dghsb9d.cloudfront.net',
	},
}

template = Template()

record_sets = []

for domain in CONFIG['public']['domain_names']:
	record_set = troposphere.route53.RecordSet(
		Name = domain + '.',
		Type = 'A',
		AliasTarget = troposphere.route53.AliasTarget(
			HostedZoneId = CONFIG['cloudfront']['hosted_zone_id'],
			DNSName = CONFIG['cloudfront']['domain_name'] + '.',
		),
	)
	record_sets.append(record_set)

record_set_group = template.add_resource(troposphere.route53.RecordSetGroup(
	'RecordSetGroup',
	HostedZoneName = CONFIG['public']['hosted_zone_name'] + '.',
	RecordSets = record_sets,
))

print template.to_json()
