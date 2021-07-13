
def test_object_register():
    """Test if the ObjectRegister works.

    Basic tests.
    """
    from app.register import ObjectRegister, make_register_instance


    Thing = "Thing"
    value = " "

    Register = ObjectRegister()

    Register[Thing] = value

    assert Thing in Register

    # is the Thing like a property?
    assert Register.Thing

    # is the value of the Thing ok?
    assert Register.Thing == value

    # can I change the value?
    Register.Thing = 1
    assert Register.Thing == 1
    assert Register.Thing != value

    # is getter sending exceptions when asked for a wrong object?
    import pytest

    with pytest.raises(KeyError):
        Register.IDontExist


def test_register_instance():
    """is the register_instance working?"""
    from app.register import ObjectRegister, make_register_instance

    Register = ObjectRegister()
    register_instance = make_register_instance(Register)

    @register_instance
    class SomeObject:
        """Our test object"""

        def __init__(self):
            self.value = 1

    instance = SomeObject()

    assert Register.SomeObject
    assert Register.SomeObject == instance
    assert Register.SomeObject.value == 1

    del instance
