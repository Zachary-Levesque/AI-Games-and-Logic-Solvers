from conftest import load_module


nim = load_module("nim", "Nim/nim.py")


def test_q_learning_update_uses_reward_and_future_value():
    ai = nim.NimAI(alpha=0.5, epsilon=0)
    ai.q[((1, 1), (0, 1))] = 0.2
    ai.q[((0, 1), (1, 1))] = 0.6

    ai.update([1, 1], (0, 1), [0, 1], reward=1)

    assert ai.q[((1, 1), (0, 1))] == 0.9


def test_choose_action_prefers_best_known_action_without_epsilon():
    ai = nim.NimAI(alpha=0.5, epsilon=0)
    ai.q[((1, 2), (1, 2))] = 0.9
    ai.q[((1, 2), (1, 1))] = 0.3

    assert ai.choose_action([1, 2], epsilon=False) == (1, 2)
