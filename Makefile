CC = gcc
CXX = g++

CFLAGS = -s -O2 -mavx2
CXXFLAGS = -s -O3 -mavx2
LDLIBS = -lm

SRCS_C = $(wildcard *.c)
SRCS_CPP = $(wildcard *.cpp)
BINS_C = $(SRCS_C:%.c=%)
BINS_CPP = $(SRCS_CPP:%.cpp=%)

.PHONY: all clean

all: $(BINS_C) $(BINS_CPP)

$(BINS_C): %: %.c
	$(CC) $(CFLAGS) $< -o $@ $(LDLIBS)
	@echo "Compiled $@."

$(BINS_CPP): %: %.cpp
	$(CXX) $(CXXFLAGS) $< -o $@ $(LDLIBS)
	@echo "Compiled $@."

clean:
	rm $(BINS_C) $(BINS_CPP)