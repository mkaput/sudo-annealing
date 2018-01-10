from sudo_annealing.solvers.abstractcl import CLSolver


class CLDFS(CLSolver):
    @classmethod
    def full_name(cls) -> str:
        return "Backtracing, OpenCL"

    @classmethod
    def program_name(cls) -> str:
        return 'cldfs'
