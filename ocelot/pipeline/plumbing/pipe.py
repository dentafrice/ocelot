class Pipe(object):
    def __init__(self, input_fitting, output_fitting):
        self.input_fitting = input_fitting
        self.output_fitting = output_fitting

    def is_input(self, fitting):
        return self.input_fitting == fitting

    def is_output(self, fitting):
        return self.output_fitting == fitting

    def process(self, data):
        return self.output_fitting.process(data)
