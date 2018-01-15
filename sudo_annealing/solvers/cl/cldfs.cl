kernel void solve(
    global const uchar *in_sudoku,
    global const ulong *bitmask,
    global uchar *solution
) {
    int gid = get_global_id(0);
    printf("%x %x\n", bitmask[0], bitmask[1]);
    solution[gid] = 3;
}
