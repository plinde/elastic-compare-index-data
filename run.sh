#!/bin/bash

. setenv.sh


if [[ ! -d ${DATA_DIR} ]]; then mkdir -p ${DATA_DIR}; fi

for INDEX in $INDICES; do

	for DATE in $DATES; do

		curl -s -XPOST "${CLUSTER_URI}/${INDEX}-${DATE}/_search" -d' {"size":0,"query":{"filtered":{"query":{"query_string":{"analyze_wildcard":true,"query":"*"}}}},"aggs":{"2":{"terms":{"field":"host","size":100,"order":{"_count":"desc"}}}}}'  | jq '.aggregations' | jq '.["2"]' | jq '.buckets[].key' > ${DATA_DIR}/${INDEX}-${DATE}.json

		cat ${DATA_DIR}/${INDEX}-${DATE}.json | sort | jo -a > ${DATA_DIR}/${INDEX}-${DATE}_hostsarray.json

	done

	### Do a comparison; args like CLUSTER_HOST, CLUSTER_PORT, then 2-pair'd fields for the two input files
	python json-compare-engine.py $CLUSTER_HOST $CLUSTER_PORT $(for DATE in $DATES; do echo ${DATA_DIR}/${INDEX}-${DATE}_hostsarray.json; done | xargs)


done

