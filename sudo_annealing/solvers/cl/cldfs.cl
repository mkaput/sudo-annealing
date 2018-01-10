__kernel void solve(__global const int8 *in_sudoku, __global int8 *solution) {
    int gid = get_global_id(0);
    solution[gid] = in_sudoku[gid];
}
