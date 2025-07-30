deploy_path := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))


ifneq ("$(wildcard .env.make)","")
include .env.make
$(info Including .env.make file)
#	export
else ifneq ("$(wildcard .env)","")
include .env
$(info Including .env file)
#	export
endif

test2 = $(TEST2)

sumake_help:
	@echo deploy_path: $(deploy_path)
	sumake -h

include $(deploy_path)/ssh.mk
include $(deploy_path)/docker.mk
include $(deploy_path)/aws.mk

UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Linux)
# pass
else ifeq ($(UNAME_S),Darwin)
# pass
endif


#sumake_version:
#	@echo 2023.5.9

# $(call check_conda, my_env)
#define check_conda
#$(eval conda_env := $(1)) \
#if [ $(USE_CONDA) != false ]; then \
#$(eval CONDA_RUN := conda run -n $(conda_env) --no-capture-output); \
#fi
#endef
# 这一行放到里面就不起作用了，我也不知道为什么
export conda_run = conda run -n $(CONDA_ENV) --no-capture-output
ifeq ($(USE_CONDA),false)
	export conda_run=
endif
#if $(filter $(conda) $(USE_CONDA),false),, $(eval CONDA_RUN := conda run -n $(conda_env) --no-capture-output))

# define upload
# 	rsync -av  \
# 		--rsh="ssh -o StrictHostKeyChecking=no -p $(DEPLOY_PORT)" \
# 		$(1) \
# 		${DEPLOY_HOST}:$(patsubst %,%, $(if $(2),$(2),~/$(patsubst %,%,$(1))))
# endef

# define command
# 	ssh -p $(DEPLOY_PORT) $(DEPLOY_HOST) $(1)
# endef
