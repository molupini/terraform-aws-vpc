# VPC MODULE

Powered by Terraform.

  - Test locally or within docker-compose

# Features

You can:
  - Build, VPC

# Tech

Uses a number of open source projects to work properly:

* [terraform] - open-source infrastructure as code software tool.

# Installation


#### Prep

Open your favorite Terminal and run these commands.

First, if necessary:
```sh
$ mkdir ./iac
```
Second:
```sh
$ git init
```
Third:
```sh
$ git clone git@gitlab.com/bcx-sanlam-group/tfvpc.git 
```

#### Author

Making any change in your source file will update immediately if volume is attached. See todo within compose file.

Before we begin, required environment variables:
```sh
$ vi ./.env/app.development.env

# # TF
IAC_ENDPOINT_PROTOCOL=http
IAC_ENDPOINT_HOSTNAME=192.168.43.126
IAC_ENDPOINT_PORT=3001

# # AWS
AWS_ACCESS_KEY=?
AWS_SECRET_KEY=?
AWS_REGION=eu-west-1
```


### Test

Easily done in a Docker container.
Make required changes within Dockerfile + compose files if necessary. When ready, simply use docker-compose to build your environment.
This will create the *iac-terra, ...* services with necessary dependencies.
Once done, simply run the following commends:

For dev, docker compose:
```sh
$ docker-compose build
$ docker-compose up
```

Verify the deployment by docker exec. 
```sh
$ docker exec -it state_iac-terra_1 bash
```

Issue attaching the volume, copy when changes required into container
```sh
$ docker cp bin/. state_iac-terra_1:/app/.
```

Verify terraform source files
```sh
$ terraform init
$ terraform fmt
$ terraform validate
$ terraform plan -var 'id=
' -var 'aws_access_key=****' -var 'aws_secret_key=****' -var 'aws_region=eu-west-1'
$ terraform apply -var 'id=5db8b63ea67b8000241f8ea2' -var 'aws_access_key=****' -var 'aws_secret_key=****' -var 'aws_region=eu-west-1'
$ terraform destroy -var 'id=5db8b63ea67b8000241f8ea2' -var 'aws_access_key=****' -var 'aws_secret_key=****' -var 'aws_region=eu-west-1'
```


# Operating
Once [jenkins] is online and ready, you need to add credentials of your AWS Account. 
From the home page click Credentials > System on the left. Under System, click the Global credentials (unrestricted) link to access this default domain. Click Add Credentials on the left.

Kind > Secret text
```sh
Secret : "****"
ID : "AWS_ACCESS_KEY"
```

Kind > Secret text
```sh
Secret : "****"
ID : "AWS_SECRET_KEY"
```

Kind > Secret text
```sh
Secret : "****"
ID : "AWS_REGION"
```

Create a new item, example terraform_vpc_git, pipeline. Some important considerations or options.
Example below, 
*Importantly all options/parameters can be controlled by the pipeline script*

```
pipeline {
  options {
      buildDiscarder(logRotator(numToKeepStr: '7'))
  }
  ...
}
```


# Author
**Want to contribute? Great! See repo [git-repo-url] from [Maurizio Lupini][mo]    -Author, Working at [...][linkIn]**


   [mo]: <https://github.com/molupini>
   [linkIn]: <https://za.linkedin.com/in/mauriziolupini>
   [git-repo-url]: <https://gitlab.com/bcx-sanlam-group/>
   [terraform]: <https://www.terraform.io/>