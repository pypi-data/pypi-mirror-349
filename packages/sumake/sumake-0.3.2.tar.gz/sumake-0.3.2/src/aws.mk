get-env-aws:
	@echo ========= AWS ENV =================
	@echo AWS_ACCESS_KEY_ID=$(shell aws configure get aws_access_key_id)
	@echo AWS_SECRET_ACCESS_KEY=$(shell aws configure get aws_secret_access_key)
	@echo AWS_REGION=$(shell aws configure get region)
	@echo ===================================
