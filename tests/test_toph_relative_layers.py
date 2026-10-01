from tools.toph_relative_layers import (
    BELLY,
    BENJAMIN_PATH,
    ENTRY,
    FORWARD_PATH,
    HUB,
    INGRESS,
    JUMP_MS,
    JUMPS_PER_TRAVERSAL,
    OSI_LAYER,
    TRAVERSAL_MS,
    toroid_state,
    traversal,
)


def test_geometry_and_hub():
    assert ENTRY == 0
    assert HUB == 4
    assert INGRESS == (0, 2, 4)
    assert BELLY == (4, 6, 8, 10, 4)
    assert FORWARD_PATH == (0, 2, 4, 6, 8, 10, 4)


def test_six_jumps_at_200ms_is_1200ms():
    assert JUMP_MS == 200
    assert JUMPS_PER_TRAVERSAL == 6
    assert TRAVERSAL_MS == 1200
    assert OSI_LAYER == 2
    assert toroid_state(6).elapsed_ms == 1200
    assert toroid_state(6).node == HUB
    assert toroid_state(6).traversal_complete is True


def test_forward_nodes_and_elapsed_time():
    states = traversal("forward")
    assert [s.node for s in states] == [0, 2, 4, 6, 8, 10, 4]
    assert [s.elapsed_ms for s in states] == [0, 200, 400, 600, 800, 1000, 1200]


def test_benjamin_button_is_exact_reverse():
    assert BENJAMIN_PATH == tuple(reversed(FORWARD_PATH))
    states = traversal("benjamin")
    assert [s.node for s in states] == [4, 10, 8, 6, 4, 2, 0]
    assert states[-1].node == ENTRY
    assert states[-1].elapsed_ms == 1200
