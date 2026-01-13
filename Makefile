CC = gcc
CXX = g++

DEPFLAGS = -MMD -MP

CFLAGS = -s -O2 -mavx2 $(DEPFLAGS)
CXXFLAGS = -s -O3 -mavx2 $(DEPFLAGS)
LDLIBS = -lm

SRCS_C = $(wildcard *.c)
SRCS_CPP = $(wildcard *.cpp)

BINS_C = $(SRCS_C:%.c=%)
BINS_CPP = $(SRCS_CPP:%.cpp=%)

DEPS = $(SRCS_C:%.c=%.d) $(SRCS_CPP:%.cpp=%.d)

.PHONY: all clean

all: $(BINS_C) $(BINS_CPP)

$(BINS_C): %: %.c
	$(CC) $(CFLAGS) $< -o $@ $(LDLIBS)
	@echo "Compiled $@."

$(BINS_CPP): %: %.cpp
	$(CXX) $(CXXFLAGS) $< -o $@ $(LDLIBS)
	@echo "Compiled $@."

-include $(DEPS)

clean:
	rm $(BINS_C) $(BINS_CPP) $(DEPS)