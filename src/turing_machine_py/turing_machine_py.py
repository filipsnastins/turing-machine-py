from __future__ import annotations

from typing import Dict, List

from .models import Instruction, State


class TuringMachine:
    _tape: Tape
    _head: Head
    _states: Dict[str, State]
    _start_state: State
    _log: bool

    def __init__(
        self,
        input_data: str,
        states: List[State],
        start_state: str,
        blank: str = " ",
        log: bool = False,
    ):
        self._tape = Tape(input_data, blank)
        self._head = Head(self._tape)
        self._states = self._hash_states_by_name(states)
        self._start_state = self._get_state_by_name(start_state)
        self._log = log

    # pylint: disable=no-self-use
    def _hash_states_by_name(self, states: List[State]) -> Dict[str, State]:
        return {state.name: state for state in states}

    def _get_state_by_name(self, state: str) -> State:
        try:
            return self._states[state]
        except KeyError as exc:
            raise ValueError(f"State not found: {state}") from exc

    def run(self) -> str:
        return self._run_recursion(current_state=self._start_state)

    def _run_recursion(self, current_state: State) -> str:
        self._print_state_if_log_is_enabled(state=current_state)
        current_value = self._read_current_value()
        try:
            current_instruction = self._fetch_instruction(current_state, current_value)
            self._execute_instruction(current_instruction)
            next_state = self._next_state(current_instruction)
            return self._run_recursion(current_state=next_state)
        except HaltSignal:
            return self._tape_output()

    def _print_state_if_log_is_enabled(self, state: State) -> None:
        if self._log:
            print(
                f"head: {self._head_poisition()}; state: {state.name}; tape: {self._tape_output()}"
            )

    def _head_poisition(self) -> int:
        return self._head.current_position

    def _tape_output(self) -> str:
        return self._tape.output()

    def _read_current_value(self) -> str:
        return self._head.read()

    def _fetch_instruction(self, state: State, value: str) -> Instruction:
        if not state.instructions:
            raise HaltSignal
        for instruction in state.instructions:
            if value in instruction.meet:
                return instruction
        raise ValueError(f"Instruction not found for value: {value} on state: {state.name}")

    def _execute_instruction(self, instruction: Instruction) -> None:
        self._execute_write(instruction)
        self._execute_move(instruction)

    def _execute_write(self, instruction: Instruction) -> None:
        self._head.write(instruction.write)

    def _execute_move(self, instruction: Instruction) -> None:
        move = instruction.move
        if not move:
            return
        if move == "R":
            self._head.move_right()
        elif move == "L":
            self._head.move_left()
        else:
            raise ValueError(f"Invalid move command: {move}")

    def _next_state(self, instruction: Instruction) -> State:
        if not instruction.set:
            raise HaltSignal
        return self._get_state_by_name(instruction.set)


class Tape:
    _tape: List[str]

    def __init__(self, input_data: str, blank: str):
        self._tape = list(input_data)
        self._blank = blank

    def write(self, index: int, value: str) -> None:
        try:
            self._tape[index] = value
        except IndexError:
            self._tape.insert(index, value)

    def shift_left(self) -> None:
        self._tape.insert(0, self._blank)

    def read(self, index: int) -> str:
        try:
            return self._tape[index]
        except IndexError:
            self.write(index, self._blank)
            return self.read(index)

    def output(self) -> str:
        return "".join(self._tape).strip()


class Head:
    _tape: Tape
    _index: int

    def __init__(self, tape: Tape):
        self._tape = tape
        self._index = 0

    @property
    def current_position(self) -> int:
        return self._index

    def read(self) -> str:
        return self._tape.read(self._index)

    def write(self, value: str) -> None:
        self._tape.write(self._index, value)

    def move_left(self) -> None:
        self._index -= 1
        # Compensate negative index
        if (self._index) < 0:
            self._tape.shift_left()
            self._index = 0

    def move_right(self) -> None:
        self._index += 1


class HaltSignal(Exception):
    pass
