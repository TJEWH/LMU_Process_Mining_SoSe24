import csv
import os
import pm4py
from pm4py.objects.log.obj import EventLog, Trace, Event
from enum import Enum
from pm4py.objects.log.importer.xes import importer

FILE_DIR = os.path.dirname(__file__)


class AlgoPm4Py(Enum):
    ALPHA = 1
    ALPHAPLUS = 2
    INDUCTIVEMINER = 3
    HEURISTICMINER = 4


def get_log_from_file(file_path="InputLogs/L1.csv"):

    file_path = os.path.join(FILE_DIR, "..", file_path)

    if file_path.endswith(".xes"):
        log = importer.apply(file_path)
    else:
        log = EventLog()

        with open(file_path, newline='') as file:
            reader = csv.reader(file)
            current_trace = None
            trace = None
            for trace_id, activity in reader:
                if current_trace != trace_id:
                    if trace is not None:
                        log.append(trace)
                    trace = Trace()
                    trace.attributes['concept:name'] = trace_id
                    current_trace = trace_id
                event = Event()
                event["concept:name"] = activity
                trace.append(event)

            if trace is not None:
                log.append(trace)
    return log


def get_model_from_pm4py(
    log,
    algorithm: AlgoPm4Py = AlgoPm4Py.ALPHAPLUS,
):
    if algorithm == AlgoPm4Py.ALPHA:
        return pm4py.discover_petri_net_alpha(log)
    elif algorithm == AlgoPm4Py.ALPHAPLUS:
        return pm4py.discover_petri_net_alpha_plus(log)
    elif algorithm == AlgoPm4Py.INDUCTIVEMINER:
        return pm4py.discover_petri_net_inductive(log)
    elif algorithm == AlgoPm4Py.HEURISTICMINER:
        return pm4py.discover_petri_net_heuristics(log)
