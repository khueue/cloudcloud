cloudcloud
----------


## Infrastructure

Provision stacks in this order:

In region **us-east-1**:

1. global

In region of your choice:

1. storage
2. main
3. dns


## Future

Add origin access protection:
- http://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-s3.html
