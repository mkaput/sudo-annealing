kernel void solve(global const uchar *in_sudoku, global uchar *solution) {
    int gid = get_global_id(0);
    solution[gid] = 3;
}
