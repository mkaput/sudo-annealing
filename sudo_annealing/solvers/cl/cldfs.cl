#define STACK_MAX 81

bool is_to_fill(constant const ulong *bitmask, const size_t i) {
  ulong v = bitmask[i / 64] & (convert_ulong(1) << (i % 64));
  return v != 0;
}

bool check_row(uchar *my_sudoku, uchar num, size_t i) {
  size_t start = (i / 9) * 9;
  for (size_t j = start; j < start + 9; j++) {
    if (my_sudoku[j] == num) {
      return false;
    }
  }
  return true;
}

bool check_col(uchar *my_sudoku, uchar num, size_t i) {
  size_t start = i % 9;
  for (size_t j = start; j < 81; j += 9) {
    if (my_sudoku[j] == num) {
      return false;
    }
  }
  return true;
}

bool check_box(uchar *my_sudoku, uchar num, size_t i) {
  size_t x = i % 9;
  size_t y = i / 9;
  x = (x / 3) * 3;
  y = (y / 3) * 3;
  for (size_t m = 0; m < 3; m++) {
    for (size_t n = 0; n < 3; n++) {
      size_t k = (y + m) * 9 + (x + n);
      if (my_sudoku[k] == num) {
        return false;
      }
    }
  }
  return true;
}

bool is_safe_to_put(uchar *my_sudoku, uchar num, size_t i) {
  return check_row(my_sudoku, num, i) && check_col(my_sudoku, num, i) &&
         check_box(my_sudoku, num, i);
}

bool stack_push(size_t value, private size_t *stack,
                private size_t *stack_top) {
  if (*stack_top == STACK_MAX) {
    return false;
  }
  *stack_top += 1;
  stack[*stack_top] = value;
  return true;
}

bool stack_pop(private size_t *stack_top) {
  if (*stack_top == 0) {
    return false;
  }
  *stack_top -= 1;
  return true;
}

kernel void solve(global const uchar *sudokus, constant const ulong *bitmask,
                  global uchar *solution) {
  int gid = get_global_id(0);

  global uchar *my_solution = solution + gid * 81;

  uchar my_sudoku[81];
  for (size_t i = 0; i < 81; i++) {
    my_sudoku[i] = sudokus[i + gid * 81];
  }

  size_t stack[STACK_MAX] = {0};
  size_t stack_top = 0;

rec:
  while (true) {
    // Skip unmasked cells
    while (stack[stack_top] < 81 && !is_to_fill(bitmask, stack[stack_top])) {
      stack[stack_top]++;
    }

    if (stack[stack_top] >= 81) {
      // We found solution
      for (size_t i = 0; i < 81; i++) {
        my_solution[i] = my_sudoku[i];
      }
      break;
    }

    // Try next number
    for (uchar num = my_sudoku[stack[stack_top]] + 1; num <= 9; num++) {
      if (is_safe_to_put(my_sudoku, num, stack[stack_top])) {
        my_sudoku[stack[stack_top]] = num;
        if (!stack_push(stack[stack_top] + 1, stack, &stack_top)) {
          break;
        }
        goto rec; // recursion!
      }
    }

    // We tried 1...9, so we retreat
    my_sudoku[stack[stack_top]] = 0;
    if (!stack_pop(&stack_top)) {
      // We got back to the beginning of the sudoku, so this means
      // we tried everything. Sorry, no solution!
      for (size_t i = 0; i < 81; i++) {
        my_solution[i] = 10;
      }
      break;
    }
  }
}
