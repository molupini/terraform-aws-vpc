FROM hashicorp/terraform:full as base

ENV TERRAFORM_INST_VERSION=0.12.16
# ARG ACCESS_KEY
# ARG SECRET_KEY
# ARG AWS_REGION

# ENV AWS_ACCESS_KEY=${ACCESS_KEY}
# ENV AWS_SECRET_KEY=${SECRET_KEY}
# ENV AWS_REGION=${AWS_REGION}

RUN apk add python3

RUN pip3 install requests

RUN pip3 install fire

RUN pip3 install awscli

RUN apk add --no-cache tini

WORKDIR /go/bin

RUN wget -q https://releases.hashicorp.com/terraform/${TERRAFORM_INST_VERSION}/terraform_${TERRAFORM_INST_VERSION}_linux_amd64.zip

RUN unzip terraform_${TERRAFORM_INST_VERSION}_linux_amd64.zip -o

WORKDIR /app

ENTRYPOINT ["/sbin/tini", "--"]


# Development 
FROM base as dev

COPY ./bin/. app

CMD [ "/bin/bash" ]


# Prodution, comment out below for testing with compose file.
FROM base as prod

COPY ./bin/. app

CMD [ "/bin/bash" ]
