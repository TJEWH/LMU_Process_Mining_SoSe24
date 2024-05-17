from alpha_plus_miner import AlphaMinerplus
from sortedcontainers import SortedSet, SortedDict

# TODO: which log to test efficiently?
with open("Logs/log.csv", "r") as my_file:
    traces = SortedDict()
    logdata = my_file.read()

    events = logdata.split("\n")
    for event in events:
        case_id, activity = event.split(",")
        if case_id not in traces:
            traces[case_id] = []

        traces[case_id].append(activity)


def test_run_alphaMiner_plus():
    # Preprocessing
    alpha_miner = AlphaMinerplus(traces)
    assert alpha_miner is not None
    assert alpha_miner.traces == traces
    assert alpha_miner.transitions == SortedSet()
    assert alpha_miner.initial_transitions == SortedSet()
    assert alpha_miner.final_transitions == SortedSet()
    assert alpha_miner.relations == SortedDict()
    assert alpha_miner.pairs == []
    assert alpha_miner.maximal_pairs == []
    assert alpha_miner.places == []
    assert alpha_miner.length_one_loops is None
    assert alpha_miner.log_without_length_one_loops is None
    assert alpha_miner.F_L1L is None
    assert alpha_miner.W_minusL1L == SortedDict()
    

    alpha_miner.get_length_one_loops()
    assert alpha_miner.transitions == {'a', 'b', 'c', 'd', 'e', 'f'}
    assert alpha_miner.length_one_loops == SortedSet([])
    alpha_miner.remove_length_one_loops()
    assert alpha_miner.log_without_length_one_loops == {'a', 'b', 'c', 'd', 'e', 'f'}
    alpha_miner.get_FL1L()
    assert alpha_miner.F_L1L == SortedSet([])
    alpha_miner.generate_W_minus_L1L()
    assert alpha_miner.W_minusL1L == SortedDict({'1': ['a', 'b', 'e', 'f'], 
                                                 '2': ['a', 'b', 'c', 'e', 'd', 'b', 'f'], 
                                                 '3': ['a', 'b', 'e', 'c', 'd', 'b', 'f'], 
                                                 '4': ['a', 'b', 'c', 'd', 'e', 'b', 'f'], 
                                                 '5': ['a', 'e', 'b', 'c', 'd', 'b', 'f']})


    alpha_miner_plus = AlphaMinerplus(alpha_miner.W_minusL1L)
    assert alpha_miner_plus is not None

    alpha_miner_plus.get_initial_transitions() 
    assert alpha_miner_plus.initial_transitions == SortedSet(['a'])
    alpha_miner_plus.get_final_transitions()
    assert alpha_miner_plus.final_transitions == SortedSet(['f'])
    alpha_miner_plus.get_transitions()
    assert alpha_miner_plus.transitions == SortedSet(['a', 'b', 'c', 'd', 'e', 'f'])
    alpha_miner_plus.get_footprint()
    assert alpha_miner_plus.relations == SortedDict({'a': SortedDict({'a': '#', 'b': '->', 'c': '#', 'd': '#', 'e': '->', 'f': '#'}), 
                                                     'b': SortedDict({'a': '<-', 'b': '#', 'c': '->', 'd': '<-', 'e': '||', 'f': '->'}), 
                                                     'c': SortedDict({'a': '#', 'b': '<-', 'c': '#', 'd': '->', 'e': '||', 'f': '#'}), 
                                                     'd': SortedDict({'a': '#', 'b': '->', 'c': '<-', 'd': '#', 'e': '||', 'f': '#'}), 
                                                     'e': SortedDict({'a': '<-', 'b': '||', 'c': '||', 'd': '||', 'e': '#', 'f': '->'}), 
                                                     'f': SortedDict({'a': '#', 'b': '<-', 'c': '#', 'd': '#', 'e': '<-', 'f': '#'})}) # TODO: check if this is correct

    alpha_miner_plus.get_pairs()
    assert alpha_miner_plus.pairs == [('a', 'b'), 
                                      ('a', 'e'), 
                                      ('b', 'c'), 
                                      ('b', 'f'), 
                                      ('c', 'd'), 
                                      ('d', 'b'), 
                                      ('e', 'f'), 
                                      (('a',), ('b',)), 
                                      (('a',), ('e',)), 
                                      (('a', 'd'), ('b',)), 
                                      (('b',), ('c',)), 
                                      (('b',), ('c', 'f')), 
                                      (('b',), ('c', 'f')), 
                                      (('b',), ('f',)), 
                                      (('c',), ('d',)), 
                                      (('d', 'a'), ('b',)), 
                                      (('d',), ('b',)), 
                                      (('e',), ('f',))] # TODO: check if this is correct
    alpha_miner_plus.get_maximal_pairs()
    assert alpha_miner_plus.maximal_pairs == [('a', 'e'), 
                                              ('c', 'd'), 
                                              ('e', 'f'), 
                                              (('a', 'd'), ('b',)), 
                                              (('b',), ('c', 'f'))]

    alpha_miner_plus.add_places()
    assert alpha_miner_plus.places == [((), 'Place_0', SortedSet(['a'])), 
                                       ('a', 'Place_1', 'e'), 
                                       ('c', 'Place_2', 'd'), 
                                       ('e', 'Place_3', 'f'), 
                                       (('a', 'd'), 'Place_4', ('b',)), 
                                       (('b',), 'Place_5', ('c', 'f')), 
                                       (SortedSet(['f']), 'Place_6', ())] # TODO: check if this is correct

    alpha_miner_plus.visualize()