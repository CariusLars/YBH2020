SSH_PRIVATE_KEY=`cat ~/.ssh/id_rsa`

build-image:
	docker build . --build-arg SSH_PRIVATE_KEY="${SSH_PRIVATE_KEY}"
