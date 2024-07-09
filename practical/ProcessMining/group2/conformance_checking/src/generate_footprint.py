from itertools import chain
import numpy as np
from enum import Enum
from natsort import natsorted


class Relations(Enum):
    BEFORE = '<-'
    SEQUENCE = '->'
    NOT_FOLLOWED = '#'
    PARALLEL = '||'


class FootPrintMatrix:

    def __init__(self, log=None, relations=None):
        """
        Initialize a FootPrintMatrix instance.

        Parameters:
        ----------
        log : dict, optional
            The input log to be converted into a list of traces for the footprint matrix.
        relations : dict, optional
            A dictionary representing the relations in the footprint matrix.
        """
        if log is not None:
            self.traces = self.convert_log_for_footprintmatrix(log)
        else:
            self.traces = []
        self.transitions = set()

        if relations is None:
            self.relations = {}
        else:
            self.relations = relations

        self.places = []

    @classmethod
    def from_relations(cls, relations):
        """
        Create a FootPrintMatrix instance from a given relations dictionary.

        This class method initializes a FootPrintMatrix object using the provided
        relations dictionary.

        Parameters:
        ----------
        relations : dict
            The relations dictionary to initialize the FootPrintMatrix.

        Returns:
        -------
        FootPrintMatrix
            A new FootPrintMatrix instance with the specified relations.
        """
        return cls(relations=relations)

    def sort_fpm_rec(self, relations):
        """
        Recursively sort the FootPrintMatrix relations dictionary.

        This method sorts the keys of the input dictionary and its nested dictionaries
        in natural order.

        Parameters:
        ----------
        relations : dict
            The relations dictionary to be sorted.

        Returns:
        -------
        dict
            A new dictionary with keys sorted in natural order.
        """
        sorted_dict = {}
        for key in natsorted(relations.keys()):
            value = relations[key]
            if isinstance(value, dict):
                sorted_dict[key] = self.sort_fpm_rec(value)
            else:
                sorted_dict[key] = value
        return sorted_dict

    def convert_log_for_footprintmatrix(self, log):
        """
        Convert an event log into a format suitable for the FootPrintMatrix.

        This method converts each trace in the log into a list of activities and
        stores them in a dictionary with trace numbers as keys.

        Parameters:
        ----------
        log : list of dict
            The event log to convert, where each trace is a list of events, and each
            event is a dictionary with at least the 'concept:name' key.

        Returns:
        -------
        dict
            A dictionary where keys are trace numbers (as strings) and values are lists
            of activity names.
        """
        traces = {}
        trace_num = 1

        for trace in log:
            activities = []
            for event in trace:
                activity_name = event['concept:name']
                activities.append(activity_name)

            traces[str(trace_num)] = activities
            trace_num += 1

        return traces

    def generate_transitions(self):
        """
        Generate and set all transitions for the current Petri net.

        This method extracts all unique transitions from the traces and stores them
        in the `transitions` attribute of the FootPrintMatrix.
        """
        self.transitions = set(chain.from_iterable(self.traces.values()))

    def generate_footprint(self) -> np.ndarray:
        """
        Generate a FootPrintMatrix by analyzing the transitions and traces.

        This method performs the following steps:
        1. Generate transitions from the traces.
        2. Remove duplicate traces.
        3. Extract relations between each pair of transitions and populate the FootPrintMatrix.
        """
        print("Generating a Footprint Matrix!")

        self.generate_transitions()

        traces_without_duplicates = set()

        for trace in self.traces.values():
            traces_without_duplicates.add("".join(trace))

        for transition_1 in self.transitions:
            self.relations[transition_1] = {}
            for transition_2 in self.transitions:
                two_element_transitions = transition_1 + transition_2
                reversed_two_element_transitions = transition_2 + transition_1

                all_relations = None
                for trace in traces_without_duplicates:
                    if (
                        two_element_transitions in trace
                        and reversed_two_element_transitions in trace
                    ):
                        all_relations = Relations.PARALLEL.value
                        break
                    if two_element_transitions in trace:
                        if all_relations == Relations.BEFORE.value:
                            all_relations = Relations.PARALLEL.value
                            break
                        else:
                            all_relations = Relations.SEQUENCE.value
                    if reversed_two_element_transitions in trace:
                        if all_relations == Relations.SEQUENCE.value:
                            all_relations = Relations.PARALLEL.value
                            break
                        else:
                            all_relations = Relations.BEFORE.value

                if all_relations is None:
                    all_relations = Relations.NOT_FOLLOWED.value
                self.relations[transition_1][transition_2] = all_relations

        self.relations = self.sort_fpm_rec(self.relations)
