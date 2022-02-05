import pytest

from turing_machine_py import Instruction, State, TuringMachine


def test_unknown_start_state_raises_value_error():
    with pytest.raises(ValueError):
        states = [State(name="first")]

        turing_machine = TuringMachine(
            input_data="1", start_state="unknown", states=states, log=True
        )

        turing_machine.run()


def test_empty_state_gives_the_same_output():
    input_data = "110"
    states = [State(name="start")]

    turing_machine = TuringMachine(
        input_data=input_data, start_state="start", states=states, log=True
    )
    result = turing_machine.run()

    assert result == input_data


def test_invalid_move_direction_raises_value_error():
    states = [
        State(
            name="start",
            instructions=[Instruction(meet=["1"], write="1", move="U")],
        )
    ]

    with pytest.raises(ValueError):
        turing_machine = TuringMachine(input_data="1", start_state="start", states=states)
        turing_machine.run()


def test_instruction_encountered_unknown_value_raises_value_error():
    states = [
        State(
            name="start",
            instructions=[Instruction(meet=["1"], write="1", move="R")],
        )
    ]

    with pytest.raises(ValueError):
        turing_machine = TuringMachine(input_data="ZZZZZZZ", start_state="start", states=states)
        turing_machine.run()


def test_print_the_same_1_to_the_right():
    """Input: 1; Output: 11
    Alphabet: { 1 }

    """
    states = [
        State(
            name="right",
            instructions=[Instruction(meet=["1"], write="1", move="R", set="write")],
        ),
        State(
            name="write",
            instructions=[Instruction(meet=[" "], write="1", move="L", set="done")],
        ),
        State(name="done"),
    ]

    turing_machine = TuringMachine(input_data="1", start_state="right", states=states, log=True)
    result = turing_machine.run()

    assert result == "11"


def test_print_the_same_1_to_the_left():
    """Input: 1; Output: 11
    Alphabet: { 1 }

    """
    states = [
        State(
            name="left",
            instructions=[Instruction(meet=["1"], write="1", move="L", set="write")],
        ),
        State(
            name="write",
            instructions=[Instruction(meet=[" "], write="1", move="R", set="done")],
        ),
        State(name="done"),
    ]

    turing_machine = TuringMachine(input_data="1", start_state="left", states=states, log=True)
    result = turing_machine.run()

    assert result == "11"
