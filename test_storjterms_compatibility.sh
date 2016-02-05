#!/usr/bin/env bash
export STORJTERMS_RPC_URL="http://127.0.0.1:7000"
BASE_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
TMP_TEST_DIR=/tmp/storjspec_$(< /dev/urandom tr -dc _A-Z-a-z-0-9 | head -c6)
git clone https://github.com/storj/storjspec -b master $TMP_TEST_DIR
cd $TMP_TEST_DIR
make test_storjterms
rm -rf $TMP_TEST_DIR
