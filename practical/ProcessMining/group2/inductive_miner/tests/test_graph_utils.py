from practical.ProcessMining.group2.inductive_miner.src.graph_utils import *


def test_initialize_graph():
    # Test if graph is initialized correctly with and without input and empty dictionary
    graph_no_input = Graph(None)
    assert len(graph_no_input.graph) == 0
    graph_empty_dict = Graph({})
    assert len(graph_empty_dict.graph) == 0
    graph_with_input = Graph({'a': ['b'], 'b': ['c', 'd'], 'c': [], 'd': []})
    assert len(graph_with_input.graph) > 0
    assert graph_with_input.graph == {'a': ['b'], 'b': ['c', 'd'], 'c': [], 'd': []}
    graph_complex = Graph(
        {'a': ['b'], 'b': ['c'], 'c': ['a'], 'd': ['d'], 'e': ['f'], 'f': [], 'g': []}
    )
    assert len(graph_complex.graph) > 0
    assert graph_complex.graph == {
        'a': ['b'],
        'b': ['c'],
        'c': ['a'],
        'd': ['d'],
        'e': ['f'],
        'f': [],
        'g': [],
    }


def test_add_edge():
    # Test if edge is added correctly
    g = Graph({'a': ['b'], 'b': ['c', 'd'], 'c': [], 'd': []})
    g.add_edge('a', 'c')
    assert g.graph == {'a': ['b', 'c'], 'b': ['c', 'd'], 'c': [], 'd': []}
    # Test for edge which already exists
    # TODO: check if its possible to rewrite the function to check if child already exists
    # g.add_edge('a', 'b')
    # assert g.graph == {'a': ['b', 'c'], 'b': ['c', 'd'], 'c': [], 'd': []}


def test_add_node():
    # Test if node can be added to empty graph
    g0 = Graph({})
    g0.add_node('a')
    assert g0.graph == {'a': []}
    # Test if node is added correctly
    g1 = Graph({'a': ['b'], 'b': ['c', 'd'], 'c': [], 'd': []})
    g1.add_node('e')
    assert g1.graph == {'a': ['b'], 'b': ['c', 'd'], 'c': [], 'd': [], 'e': []}
    # Test for existing node
    g1.add_node('a')
    assert g1.graph == {'a': ['b'], 'b': ['c', 'd'], 'c': [], 'd': [], 'e': []}


def test_get_neighbors():
    # Test if neighbors are returned correctly
    g = Graph({'a': ['b'], 'b': ['c', 'd'], 'c': [], 'd': []})
    assert g.get_neighbors('c') == []
    assert g.get_neighbors('b') == ['c', 'd']


def test_get_all_nodes():
    # Test for empty graph
    g0 = Graph({})
    assert len(g0.get_all_nodes()) == 0
    assert g0.get_all_nodes() == []
    # Test if all nodes are returned correctly
    g1 = Graph({'a': ['b'], 'b': ['c', 'd'], 'c': [], 'd': []})
    assert len(g1.get_all_nodes()) > 0
    assert g1.get_all_nodes() == ['a', 'b', 'c', 'd']


def test_get_all_edges():
    # Test for empty graph
    g0 = Graph({})
    assert len(g0.get_all_edges()) == 0
    assert g0.get_all_edges() == []
    # Test if all edges are returned correctly
    g1 = Graph({'a': ['b'], 'b': ['c', 'd'], 'c': [], 'd': []})
    assert len(g1.get_all_edges()) > 0
    assert g1.get_all_edges() == [('a', 'b'), ('b', 'c'), ('b', 'd')]


def test____str__():
    # Test str method
    g = Graph({'a': ['b'], 'b': ['c', 'd'], 'c': [], 'd': []})
    assert str(g) == "a -> ['b']\nb -> ['c', 'd']\nc -> []\nd -> []\n"


def test_build_graph_from_edges():
    g = Graph.build_graph_from_edges({('a', 'b'), ('b', 'c'), ('b', 'd')})
    # print(g)
    assert True  # TODO recheck the output of function


def test_is_reachable():
    # Test if reachability is checked correctly
    g0 = Graph({'a': ['b'], 'b': ['c', 'd'], 'c': [], 'd': [], 'e': []})
    assert g0.is_reachable('a', 'c') == True
    assert g0.is_reachable('c', 'a') == False
    assert g0.is_reachable('a', 'e') == False
    # Test for cyclic graph
    g1 = Graph({'a': ['b'], 'b': ['c'], 'c': ['a']})
    assert g1.is_reachable('a', 'c') == True
    assert g1.is_reachable('b', 'a') == True


def test_convert_to_undirected():
    # Test with empty graph
    g0 = Graph({})
    g0 = g0.convert_to_undirected()
    assert g0.graph == {}
    # Test for complex graph
    g1 = Graph({'a': ['b'], 'b': ['c', 'd'], 'c': [], 'd': [], 'e': []})
    g1 = g1.convert_to_undirected()
    assert g1.graph == {
        'a': ['b'],
        'b': ['c', 'd', 'a'],
        'c': ['b'],
        'd': ['b'],
        'e': [],
    }


def test_find_components():
    # Test if components are found correctly
    g = Graph({'a': ['b'], 'b': ['c', 'd'], 'c': [], 'd': [], 'e': []})
    assert g.find_components() == [['a', 'b', 'c', 'd'], ['e']]
    # TODO: discuss functionality of find components


def test_find_strongly_con_components():
    # Test method strongly_connected
    g0 = Graph({'a': ['b'], 'b': ['c', 'd'], 'c': [], 'd': []})
    assert g0.find_strongly_con_components() == [['a'], ['b'], ['d'], ['c']]


def test_build_cuts_graph():
    # Test build cuts graph with semi complex graph
    g = Graph({'a': ['b'], 'b': ['c', 'd'], 'c': [], 'd': []})
    g0, map = g.build_cuts_graph([['a'], ['b'], ['d'], ['c']])

    # print(g0.graph, 'sara', map)
    assert g0.graph == {0: {1}, 1: set(), 2: set(), 3: set()}
    assert map == {'a': 0, 'b': 1, 'd': 2, 'c': 3}


def test_dfs_in_dag():
    # Test dfs implementation
    g = Graph({'a': ['b'], 'b': ['c', 'd'], 'c': [], 'd': [], 'e': []})
    assert g.dfs_in_dag('a', set()) == {'a', 'b', 'c', 'd'}
    assert g.dfs_in_dag('e', set()) == {'e'}


def test_all_pairs_reachability_dag():
    # Test reachability function for semi complex graph
    g = Graph({'a': ['b'], 'b': ['c', 'd'], 'c': [], 'd': []})
    assert g.all_pairs_reachability_dag() == {
        'a': {'a', 'c', 'b', 'd'},
        'b': {'c', 'b', 'd'},
        'c': {'c'},
        'd': {'d'},
    }


def test_find_unreachable_pairs():
    # Test unreachable pairs with edge cases
    g = Graph(
        {
            'a': ['b'],
            'b': [
                'c',
            ],
            'c': [],
            'd': ['e'],
            'e': [],
        }
    )
    assert set(g.find_unreachable_pairs()) == set(
        [
            ('c', 'e'),
            ('b', 'd'),
            ('c', 'd'),
            ('a', 'e'),
            ('a', 'd'),
            ('b', 'e'),
        ]
    )


def test_traverse_path():
    # Test traverse path from two nodes
    g = Graph({'a': ['b'], 'b': ['c', 'd'], 'c': [], 'd': []})
    assert g.traverse_path('a') == ['a', 'b', 'c']
    assert g.traverse_path('b') == ['b', 'c']
