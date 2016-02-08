PY_VERSION := 2.7
WHEEL_DIR := /tmp/wheelhouse
PIP := env/bin/pip
PY := env/bin/python
USE_WHEELS := 0
ifeq ($(USE_WHEELS), 0)
  WHEEL_INSTALL_ARGS := # void
else
  WHEEL_INSTALL_ARGS := --use-wheel --no-index --find-links=$(WHEEL_DIR)
endif


help:
	@echo ""
	@echo "COMMANDS:"
	@echo "  test               Run all tests."
	@echo "  test_storjnet      Run storjnet tests."
	@echo "  test_storjlib      Run storjlib tests."
	@echo "  graphs             Compile graphviz graphs for documentation."
	@echo "  clean              Remove all generated files."
	@echo "  setup              Setup development environment."
	@echo "  wheels             Build dependency wheels & save in $(WHEEL_DIR)."
	@echo ""
	@echo "VARIABLES:"
	@echo "  PY_VERSION         Version of python to use. 2 or 3"
	@echo "  WHEEL_DIR          Where you save your wheels. Default: $(WHEEL_DIR)."
	@echo "  USE_WHEELS         Install packages from wheel dir, off by default."
	@echo ""


clean:
	rm -rf env
	find | grep -i ".*\.pyc$$" | xargs -r -L1 rm


virtualenv: clean
	virtualenv -p /usr/bin/python$(PY_VERSION) env
	$(PIP) install wheel


wheels: virtualenv
	$(PIP) wheel --find-links=$(WHEEL_DIR) --wheel-dir=$(WHEEL_DIR) -r requirements.txt



setup: virtualenv
	$(PIP) install $(WHEEL_INSTALL_ARGS) -r requirements.txt


test_storjnet: setup
	# TODO test_storjnet


test_storjlib_store: setup
	# TODO test_storjlib_store


test_storjlib_contract: setup
	$(PY) storjlib/contract/test.py --verbose


test_storjlib_audit: setup
	$(PY) storjlib/audit/test.py --verbose


test_storjlib: test_storjlib_contract test_storjlib_audit test_storjlib_store
test: test_storjnet test_storjlib


graphs:
	dot -Tpng status.dot -o status.png
	dot -Tpng storjlib/audit/scheme.dot -o storjlib/audit/scheme.png
