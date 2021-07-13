
def test_state():
    from app.state import State, INIT, NORMAL

    import pytest

    # that is not how it works
    with pytest.raises(TypeError):
        state = State()

    with pytest.raises(AssertionError):
        state = State("a")

    with pytest.raises(AssertionError):
        state = State([])

    # this is how it works
    state = State([INIT, NORMAL])
    assert state
    assert state.current() == INIT

    # there is no state "bad" so wont work
    with pytest.raises(AttributeError):
        state.bad

    # set state normal
    state.normal
    assert state.is_(NORMAL)

    # set state init
    state.init 
    assert state.is_(INIT)
