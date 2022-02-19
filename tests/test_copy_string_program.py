import pytest

from turing_machine_py import Instruction, State, TuringMachine


@pytest.mark.parametrize(("input_data"), ["", "1", "11", "111", "1111111"])
def test_copy_input_to_the_right(input_data: str) -> None:
    """Copy given input to the right.
    Alphabet: { 1 }

    Example:
        Input 1; Output: 11
        Input: 111; Output: 111111
    """
    states = [
        State(
            name="start",
            instructions=[
                Instruction(meet=["1"], write="*", move="R", set="carry-first"),
                Instruction(meet=[" "], write=" ", move=None, set="done"),
            ],
        ),
        State(
            name="carry-first",
            instructions=[
                Instruction(meet=["1"], write="1", move="R", set="carry-first"),
                Instruction(meet=[" "], write=">", move="L", set="left"),
            ],
        ),
        State(
            name="left",
            instructions=[
                Instruction(meet=["1"], write="1", move="L", set="left"),
                Instruction(meet=[">"], write=">", move="L", set="left"),
                Instruction(meet=["*"], write="1", move="R", set="copy"),
            ],
        ),
        State(
            name="copy",
            instructions=[
                Instruction(meet=["1"], write="*", move="R", set="carry"),
                Instruction(meet=[">"], write="1", move="L", set="return"),
            ],
        ),
        State(
            name="return",
            instructions=[
                Instruction(meet=["1"], write="1", move="L", set="return"),
                Instruction(meet=[" "], write=" ", move="R", set="done"),
            ],
        ),
        State(
            name="carry",
            instructions=[
                Instruction(meet=["1"], write="1", move="R", set="carry"),
                Instruction(meet=[">"], write=">", move="R", set="carry"),
                Instruction(meet=[" "], write="1", move="L", set="left"),
            ],
        ),
        State(name="done"),
    ]

    turing_machine = TuringMachine(
        input_data=input_data, start_state="start", states=states, log=True
    )
    result = turing_machine.run()

    assert result == input_data + input_data


# @pytest.mark.parametrize(("input_data"), ["", "1", "11", "111", "1111111"])
# def test_copy_input_to_the_left(input_data):
#     raise NotImplementedError
