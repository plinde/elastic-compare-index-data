#!/bin/bash

. setenv.sh

DATA_DIR="data"

if [[ ! -d ${DATA_DIR} ]]; then mkdir -p ${DATA_DIR}; fi

CLUSTER_URI="${CLUSTER_PROTO}://${CLUSTER_USER}:${CLUSTER_PASS}@${CLUSTER_HOST}"

INDICES="index"
DATES="2016.04.10 2016.04.11"

for INDEX in $INDICES; do

	for DATE in $DATES; do

		curl -s -XPOST "${CLUSTER_URI}/${INDEX}-${DATE}/_search" -d' {"size":0,"query":{"filtered":{"query":{"query_string":{"analyze_wildcard":true,"query":"*"}}}},"aggs":{"2":{"terms":{"field":"host","size":100,"order":{"_count":"desc"}}}}}'  | jq '.aggregations' | jq '.["2"]' | jq '.buckets[].key' > ${DATA_DIR}/${INDEX}-${DATE}.json

		cat ${DATA_DIR}/${INDEX}-${DATE}.json | jo -a > ${DATA_DIR}/${INDEX}-${DATE}_hostsarray.json

	done

	### Do a comparison:
	python json-compare-engine.py $(for DATE in $DATES; do echo ${DATA_DIR}/${INDEX}-${DATE}_hostsarray.json; done | xargs)


done

