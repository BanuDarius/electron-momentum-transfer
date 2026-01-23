CC = gcc
CXX = g++
DEPFLAGS = -MMD -MP
CFLAGS = -s -O2 -mavx2 $(DEPFLAGS)
CXXFLAGS = -s -O3 -mavx2 $(DEPFLAGS)
LDLIBS = -lm

SRCS_C := $(wildcard src/*.c)
SRCS_CPP := $(wildcard src/*.cpp)

BINS_C := $(patsubst src/%.c, bins/%, $(SRCS_C))
BINS_CPP := $(patsubst src/%.cpp, bins/%, $(SRCS_CPP))


DEPS := $(BINS_C:%=%.d) $(BINS_CPP:%=%.d)

.PHONY: all clean clean_outputs

all: bins_dir $(BINS_C) $(BINS_CPP) finish_all

bins_dir:
	@mkdir -p bins
	@mkdir -p output
	@mkdir -p output-image
	@mkdir -p output-video

$(BINS_C): bins/%: src/%.c | bins_dir
	@$(CC) $(CFLAGS) $< -o $@ $(LDLIBS)
	@echo "Compiled C program: $@."

$(BINS_CPP): bins/%: src/%.cpp | bins_dir
	@$(CXX) $(CXXFLAGS) $< -o $@ $(LDLIBS)
	@echo "Compiled C++ program: $@."

finish_all:
	@echo "Completed compilation."

-include $(DEPS)

clean:
	rm -r bins

clean-output:
	rm -r output output-image output-video