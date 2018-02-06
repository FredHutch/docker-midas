#!/bin/bash

set -e

test_image(){
	
	img_tag=$1

	[[ "${#img_tag}" == "0" ]] && echo "Please specify image" && return

	[[ "$(docker run $img_tag echo True)" != "True" ]] && echo "Tag not found ($img_tag)" && return

	docker run \
		-v $PWD/temp:/share \
		--rm \
		$img_tag \
			run.py \
				--input /share/SRR1297187_1.100k.fastq.gz \
				--ref-db /share/midas_db_v1.2/ \
				--output-folder /share/ \
				--temp-folder /share
}

test_image $1

