from app.state import State, INIT, NORMAL

def test_state():
    import pytest

    with pytest.raises(TypeError):
        state = State()

    with pytest.raises(AssertionError):
        state = State("a")

    with pytest.raises(AssertionError):
        state = State([])

    state = State([INIT, NORMAL])
    assert state
    assert state.current() == INIT

    with pytest.raises(AttributeError):
        state.bad

    state.normal
    assert state.is_(NORMAL)

    state.init 
    assert state.is_(INIT)
