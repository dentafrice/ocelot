from graphviz import Digraph


def pipeline_to_dot(pipeline):
    dot = Digraph(name=pipeline.name or 'Unknown')

    fittings = []
    fittings.extend(pipeline.input_fittings)

    edges = set()

    while fittings:
        fitting = fittings.pop()

        for pipe in fitting.output_pipes:
            edges.add((
                _fitting_to_node_name(pipe.input_fitting),
                _fitting_to_node_name(pipe.output_fitting),

            ))

            fittings.append(pipe.output_fitting)

    for edge in edges:
        dot.edge(*edge)

    return dot.source


def _fitting_to_node_name(fitting):
    return '{}-{}'.format(
        fitting.channel.__class__.__name__,
        fitting.identifier.split('-')[0],
    )
