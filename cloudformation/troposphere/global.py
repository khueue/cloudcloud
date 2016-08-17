from troposphere import (
	Template,
)

import troposphere
import troposphere.certificatemanager

# NOTE: Must be provisioned in the us-east-1 region.

CONFIG = {
}

template = Template()

ssl_certificate = template.add_resource(troposphere.certificatemanager.Certificate(
	'SslCertificate',
	DomainName = 'cloudcloud.io',
	SubjectAlternativeNames = [
		'*.cloudcloud.io',
	],
))

print template.to_json()
