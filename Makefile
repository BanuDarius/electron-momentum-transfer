CC = gcc
DEPFLAGS = -MMD -MP
CFLAGS = -s -O2 -mavx2 $(DEPFLAGS)
LDLIBS = -lm

SRCS := $(wildcard src/*.c)

BINS := $(patsubst src/%.c, bins/%, $(SRCS))

DEPS := $(BINS:%=%.d)

.PHONY: all clean clean-output

all: bins_dir $(BINS) finish_all

bins_dir:
	@mkdir -p bins
	@mkdir -p output
	@mkdir -p output-image
	@mkdir -p output-video

$(BINS): bins/%: src/%.c | bins_dir
	@$(CC) $(CFLAGS) $< -o $@ $(LDLIBS)
	@echo "Compiled program: $@."

finish_all:
	@echo "Completed compilation."

-include $(DEPS)

clean:
	@rm -r bins
	@echo "Removed binary files."

clean-output:
	@rm -r output output-image output-video
	@echo "Removed output files."