#!/bin/bash

full_path_to_script="$(realpath "${BASH_SOURCE[0]}")"
script_parent_folder="$(dirname "$full_path_to_script")"

image_name="strast-upm/hunter"
tag="latest"

sudo docker build --no-cache -t "$image_name":"$tag" "$script_parent_folder"

image_repository="ghcr.io"
sudo docker tag "$image_name" "$image_repository/$image_name:$tag"
sudo docker push "$image_repository/$image_name:$tag"
