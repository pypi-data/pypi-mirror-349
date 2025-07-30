# DEPLOY_HOST
# DEPLOY_PORT
# DEPLOY_USERNAME
# DEPLOY_PASSWORD

USERNAME ?= $(shell whoami)
DEPLOY_USERNAME ?= $(USERNAME)

DEPLOY_PORT ?= 22
DEPLOY_HOST ?= $(DEPLOY_USERNAME)@$(DEPLOY_ADDRESS)

ENVIRONMENT =  @export DEPLOY_PORT=$(DEPLOY_PORT); \
                export DEPLOY_HOST=$(DEPLOY_HOST); \
                export DEPLOY_USERNAME=$(USERNAME); \
                export DEPLOY_PASSWORD=$(DEPLOY_PASSWORD); \

deploy_path := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
python = $(ENVIRONMENT) python
call_utils = $(python) $(deploy_path)/utils.py


.PHONY: wget_if_not_exist

define wget_if_not_exist
@if [ ! -f $(1) ]; then \
	mkdir -p $(dir $(1)); \
	wget -O $(1) $(2); \
else \
	echo "File already exists: $(1) "; \
fi
endef

define upload
	$(call_utils) upload $(1) $(2)
endef

define upload_root
	$(call_utils) upload --root $(1) $(2)
endef

define download
	$(call_utils) download $(1) $(2)
endef



define command
	$(call_utils) ssh '$(1)'
endef
define ssh
	$(call_utils) ssh '$(1)'
endef
define ssh_root
	$(call_utils) ssh --root '$(1)'
endef

# special a script to run on remote server
define ssh_file
	echo '$(2)'
	$(call_utils) ssh --file $(1) '$(2)'
endef
define ssh_root_file
	$(call_utils) ssh --root --file $(1) '$(2)'
endef
