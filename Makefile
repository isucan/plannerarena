PROBLEMS_DIR=problems/
RESULTS_DIR=results/
RESULTS_DB=db/benchmark.db

BENCHMARK_APP=../omplapp/build/bin/benchmark
DB_SCRIPT=../omplapp/ompl/scripts/benchmark_statistics.py

CFG_FILES=$(shell find $(PROBLEMS_DIR) -name *.cfg)
LOG_FILES=$(addprefix $(RESULTS_DIR),$(notdir $(CFG_FILES:.cfg=.log)))
TARGETS=$(basename $(notdir $(CFG_FILES)))

all:	benchmark

benchmark:	$(TARGETS)
	if test -e $(RESULTS_DB); then \
	mv $(RESULTS_DB) $(RESULTS_DB).backup; \
	fi
	$(DB_SCRIPT) $(LOG_FILES) --database=$(RESULTS_DB)

define RUN_BENCHMARK_template
$(basename $(notdir $(1))): $(1)
	$(BENCHMARK_APP) $(1)
endef

$(foreach cfg,$(CFG_FILES),$(eval $(call RUN_BENCHMARK_template,$(cfg))))

clean:
	rm -f *.console
