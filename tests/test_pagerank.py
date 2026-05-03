from conftest import load_module


pagerank = load_module("pagerank", "PageRank Simulation/pagerank.py")


def test_transition_model_for_sink_page_distributes_evenly():
    corpus = {
        "1.html": set(),
        "2.html": {"1.html"},
    }

    probabilities = pagerank.transition_model(corpus, "1.html", 0.85)

    assert probabilities["1.html"] == 0.5
    assert probabilities["2.html"] == 0.5
    assert sum(probabilities.values()) == 1


def test_iterative_pagerank_normalizes_output():
    corpus = {
        "1.html": {"2.html"},
        "2.html": {"1.html"},
    }

    ranks = pagerank.iterate_pagerank(corpus, 0.85)

    assert abs(sum(ranks.values()) - 1) < 1e-9
