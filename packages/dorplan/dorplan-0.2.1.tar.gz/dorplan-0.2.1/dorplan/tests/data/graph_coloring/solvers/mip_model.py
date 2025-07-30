import pulp as pl
from cornflow_client.constants import (
    PULP_STATUS_MAPPING,
    SOLUTION_STATUS_FEASIBLE,
    SOLUTION_STATUS_INFEASIBLE,
)
import pytups as pt
from ..core import Solution, Experiment


class PulpMip(Experiment):
    def solve(self, options: dict):
        model = pl.LpProblem()
        input_data = pt.SuperDict.from_dict(self.instance.data)
        nodes = self.instance.get_nodes()
        pairs = input_data["pairs"]
        max_colors = len(nodes) - 1
        all_colors = range(max_colors)

        # binary if node n has color c
        node_color = pt.SuperDict(
            {
                (node, color): pl.LpVariable(
                    f"node_color_{node}_{color}", 0, 1, pl.LpBinary
                )
                for node in nodes
                for color in range(max_colors)
            }
        )
        # TODO: identify maximum cliques and apply constraint on the cliques instead of on pairs
        # colors should be different if part of pair
        for pair in pairs:
            for color in all_colors:
                model += (
                    node_color[pair["n1"], color] + node_color[pair["n2"], color] <= 1
                )

        # max one color per node
        for node in nodes:
            model += pl.lpSum(node_color[node, color] for color in all_colors) == 1
        # objective function
        model += pl.lpSum(
            node_color[node, color] * color for node in nodes for color in all_colors
        )
        solver = pl.HiGHS(msg=True, timeLimit=options.get("timeLimit", 10))
        termination_condition = model.solve(solver)
        if termination_condition not in [pl.LpStatusOptimal]:
            return dict(
                status=PULP_STATUS_MAPPING.get(termination_condition),
                status_sol=SOLUTION_STATUS_INFEASIBLE,
            )
        # get the solution
        assign_list = (
            node_color.vfilter(pl.value)
            .keys_tl()
            .vapply(lambda v: dict(node=v[0], color=v[1]))
        )
        self.solution = Solution(dict(assignment=assign_list))

        return dict(
            status=PULP_STATUS_MAPPING.get(termination_condition),
            status_sol=SOLUTION_STATUS_FEASIBLE,
        )
