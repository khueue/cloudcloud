cloudcloud
----------


## Infrastructure

Make sure the contact email is visible in whois for the domain. Go here to open up contact
information for .io domains:

- <https://www.nic.io/privacy.xzx>

Then provision stacks in this order:

In the region **us-east-1**:

1. global (CloudFront requires certificates in this region)

Accept the approval emails triggered by the certificate generation, and then
in the region of your choice:

1. storage
2. main
3. dns


## Future

Add origin access protection:
- http://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-s3.html
