#!/bin/bash

set -e

git push

ansible-playbook deploy.yml --extra-vars=@vars.yml --tags pull,touch
