bool is_to_fill(constant const ulong *bitmask, const size_t i) {
    ulong v = bitmask[i / 64] & (convert_ulong(1) << (i % 64));
    return v != 0;
}

kernel void solve(
    global const uchar *in_sudoku,
    constant const ulong *bitmask,
    global uchar *solution
) {
    int gid = get_global_id(0);

    global const uchar *my_sudoku = in_sudoku + gid * 81;
    global uchar *my_solution = solution + gid * 81;

    for (size_t i = 0; i < 81; i++) {
        if (is_to_fill(bitmask, i)) {
            my_solution[i] = 100;
        } else {
            my_solution[i] = my_sudoku[i];
        }
    }
}
