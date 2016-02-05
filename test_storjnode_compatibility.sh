#!/usr/bin/env bash
BASE_DIR=$PWD
TMP_TEST_DIR=/tmp/storjspec_$(< /dev/urandom tr -dc _A-Z-a-z-0-9 | head -c6)
git clone https://github.com/storj/storjspec -b master $TMP_TEST_DIR
cd $TMP_TEST_DIR
make test_storjnode
rm -rf $TMP_TEST_DIR
cd $BASE_DIR
