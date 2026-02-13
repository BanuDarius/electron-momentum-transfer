CC = gcc
CFLAGS = -s -O3 -march=native -Iinclude -fopenmp -MMD -MP
LDLIBS = -lm -fopenmp

SRC_DIR = src
INC_DIR = include
OBJ_DIR = build
BIN_DIR = bin

MODULE_SRCS = $(SRC_DIR)/extra.c $(SRC_DIR)/init.c $(SRC_DIR)/ponderomotive.c
MODULE_OBJS = $(patsubst $(SRC_DIR)/%.c, $(OBJ_DIR)/%.o, $(MODULE_SRCS))

MAIN_SRCS = $(SRC_DIR)/laser_electron.c $(SRC_DIR)/error_calculator.c $(SRC_DIR)/find_enter_exit_time.c $(SRC_DIR)/find_final_p.c $(SRC_DIR)/find_max_p.c

MAIN_BIN = $(patsubst $(SRC_DIR)/%.c, $(BIN_DIR)/%, $(MAIN_SRCS))

all: directories $(MAIN_BIN)
	@echo "Compilation complete."

$(BIN_DIR)/laser_electron: $(OBJ_DIR)/laser_electron.o $(MODULE_OBJS)
	@$(CC) $(CFLAGS) $^ -o $@ $(LDLIBS)
	@echo "Linked $@."

$(BIN_DIR)/oscillator: $(OBJ_DIR)/oscillator.o
	@$(CC) $(CFLAGS) $^ -o $@ $(LDLIBS)
	@echo "Linked $@."

$(BIN_DIR)/%: $(OBJ_DIR)/%.o
	@$(CC) $(CFLAGS) $< -o $@ $(LDLIBS)
	@echo "Linked $@."

$(OBJ_DIR)/%.o: $(SRC_DIR)/%.c
	@$(CC) $(CFLAGS) -c $< -o $@
	@echo "Compiled $@."

directories:
	@mkdir -p $(OBJ_DIR) $(BIN_DIR) output output-image output-video input

clean:
	@rm -rf $(OBJ_DIR) $(BIN_DIR)
	@echo "Removed binary files."

clean-output:
	@rm -rf output output-image output-video input
	@echo "Removed output directories."

clean-all:
	@rm -rf $(OBJ_DIR) $(BIN_DIR) output output-image output-video input
	@echo "Removed all output files."

-include $(OBJ_DIR)/*.d

.SECONDARY: