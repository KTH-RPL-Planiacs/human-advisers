from py4j.java_gateway import JavaGateway
from py4j.protocol import Py4JNetworkError


def pythonify(gateway_obj):
    """
    Makes a copy of the Py4J iterable (java object wrapped for python) to separate result from Py4J.
    Elements of the iterable are assumed to have copy semantics.
    :param gateway_obj: A wrapped java array
    :return: A pure python list with all copied elements
    """
    res_copy = []
    for res in gateway_obj:
        res_copy.append(res)
    return res_copy


class PrismBridge:
    """
    The PrismBridge accesses the PrismEntryPoint running in java.
    """

    def __init__(self):
        """
        If the construction of the PrismBridge fails, you have most likely forgotten to start the Java entry point.
        """
        self.gateway = JavaGateway()
        self.prism_handler = self.gateway.entry_point.getPrismHandler()

    def load_model_file(self, model_file):
        """
        Loads a PRISM model into the model checker.
        :param model_file: the path to the model file
        """
        self.prism_handler.loadModelFile(model_file)

    def check_property(self, property_string):
        """
        Quantiatively modelchecks a given PRISM property on the previously loaded model.
        :param property_string: property to check
        :return: A list of floats, indicating the probability of the property holding in that state.
        The index corresponds to the state id.
        """
        result = self.prism_handler.checkProperty(property_string)
        return pythonify(result)

    def synthesize_strategy(self, property_string, test=False):
        strat = self.prism_handler.synthesizeStrategy(property_string)
        # TODO: ugly, but works. fix later
        # TODO: find out how to get move labels from move indices in strat.getNextMove(state)
        if test:
            strat_path = "../prism_bridge/adv.tra"
        else:
            strat_path = "prism_bridge/adv.tra"
        strategy = {}
        # assumes memoryless deterministic
        with open(strat_path, 'r') as f:
            for line in f:
                split_line = line.split()
                if len(split_line) == 2:
                    strategy[split_line[0]] = split_line[1]
            f.close()
        return strategy


if __name__ == "__main__":
    try:
        prism_bridge = PrismBridge()
        print("Successfully connected to PRISM java gateway!")
    except Py4JNetworkError as err:
        print("Py4JNetworkError:", err)
        print("It is most likely that you forgot to start the PRISM java gateway. "
              "Compile and launch PrismEntryPoint.java!")
