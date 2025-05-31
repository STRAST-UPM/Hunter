#!/bin/bash

#TODO test with internet access

script_path="$(realpath "${BASH_SOURCE[0]}")"
script_parent_folder="$(dirname "$full_path_to_script")"

image_name="template_app"
tag="latest"
dockerfile_path="$script_parent_folder/Dockerfile"
sudo docker build -f "$dockerfile_path" -t "$image_name":"$tag" "$script_parent_folder" --no-cache

image_repository="ghcr.io"
docker login "$image_repository"
sudo docker push "$image_repository/$image_name:$tag"
