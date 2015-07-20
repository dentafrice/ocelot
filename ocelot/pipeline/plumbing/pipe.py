class Pipe(object):
    def __init__(self, input_fitting, output_fitting):
        self.input_fitting = input_fitting
        self.output_fitting = output_fitting

    def is_input(self, fitting):
        """Returns whether or not the provided fitting is the input fitting.

        :param Fitting fitting: fitting to check.
        :returns bool: whether or not the fitting is the input fitting.
        """
        return self.input_fitting == fitting

    def is_output(self, fitting):
        """Returns whether or not the provided fitting is the output fitting.

        :param Fitting fitting: fitting to check.
        :returns bool: whether or not the fitting is the output fitting.
        """
        return self.output_fitting == fitting

    def process(self, data):
        """Writes data to the output fitting and returns the response.

        :param data: data to process.
        :returns: response from output fitting.
        """
        return self.output_fitting.process(data)
