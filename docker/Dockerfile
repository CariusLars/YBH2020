# Dockerfile forchickenservicerequest YB Hack 2020
# tag with: docker tag  <imageHash> jcarius/chickenservicerequest:202010092050
# docker tag <imageHash> chickenservicerequest.azurecr.io/chickenservicerequest:2020100922205
# push with docker push chickenservicerequest.azurecr.io/chickenservicerequest:2020100922205
# run locally with: docker run --network=host -it jcarius/chickenservicerequest:202010092050
# redeploy hook: https://$ChickenServiceRequest:rjhYwmvWbig7iftHE4PRMNv9oQrHRiQRlya9H43gfbc2k0hqmypxZrLzzLPc@chickenservicerequest.scm.azurewebsites.net/docker/hook

#==
# Intermediate stage (should not persist in final image to avoid ssh key leakage)
#==
FROM ubuntu as intermediate

RUN apt-get update && apt-get install -y git

# add credentials on build
ARG SSH_PRIVATE_KEY
RUN mkdir /root/.ssh/ \
    && echo "${SSH_PRIVATE_KEY}" > /root/.ssh/id_rsa \
    && chmod 600 /root/.ssh/id_rsa

# make sure your domain is accepted
RUN touch /root/.ssh/known_hosts \
    && ssh-keyscan bitbucket.org   >> /root/.ssh/known_hosts \
    && ssh-keyscan github.com      >> /root/.ssh/known_hosts

RUN mkdir git
RUN cd git && git clone git@github.com:CariusLars/YBH2020.git

#==
# Actual image
#==
FROM ubuntu

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip

RUN pip3 install pandas flask flask_table xlrd requests nltk google google.cloud google-cloud-language

#==
# Copy private git repos from intermediate image
#==
COPY --from=intermediate  /git/YBH2020 YBH2020

EXPOSE 5000
EXPOSE 80

WORKDIR YBH2020
CMD ["/YBH2020/deploy.sh"]
