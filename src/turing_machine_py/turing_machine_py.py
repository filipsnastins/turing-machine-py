from __future__ import annotations

import logging
from typing import Dict, List

from .models import Instruction, State

logger = logging.getLogger()


class TuringMachine:
    _tape: Tape
    _head: Head
    _states: Dict[str, State]

    _current_state: State
    _current_instruction: Instruction
    _current_value: str

    def __init__(
        self,
        input_data: str,
        start_state: str,
        states: List[State],
        blank: str = " ",
        log: bool = False,
    ):
        self._log = log
        self._tape = Tape(input_data, blank)
        self._head = Head(self._tape)
        self._hash_states(states)
        self._set_start_state(start_state)

    def run(self) -> str:
        if self._log:
            logger.info(
                "head: %s; state: %s; tape: %s",
                self._head.current_position,
                self._current_state.name,
                self._tape.print(),
            )
        try:
            self._read_current_value()
            self._fetch_instruction()
            self._execute_instruction()
            self._next_state()
        except StopIteration:
            return self._tape.print()
        return self.run()

    def _hash_states(self, states: List[State]):
        self._states = {state.name: state for state in states}

    def _set_start_state(self, start_state):
        try:
            self._current_state = self._states[start_state]
        except KeyError as exc:
            raise ValueError(f"Start state not found: '{start_state}'") from exc

    def _read_current_value(self):
        self._current_value = self._head.read()

    def _fetch_instruction(self):
        if not self._current_state.instructions:
            self._halt()
        for instruction in self._current_state.instructions:
            if self._current_value in instruction.meet:
                self._current_instruction = instruction
                return
        raise ValueError(
            (
                f"Instruction not found for value: '{self._current_value}'"
                f"on state: '{self._current_state.name}'"
            )
        )

    def _execute_instruction(self):
        self._execute_write()
        self._execute_move()

    def _execute_write(self):
        self._head.write(self._current_instruction.write)

    def _execute_move(self):
        move = self._current_instruction.move
        if not move:
            return
        if move == "R":
            self._head.move_right()
        elif move == "L":
            self._head.move_left()
        else:
            raise ValueError(f"Invalid move command: '{move}'")

    def _next_state(self):
        if not self._current_state.instructions:
            self._halt()
        # mypy is complaining about self._current_instruction.set being None without this if check
        if self._current_instruction.set:
            self._current_state = self._states[self._current_instruction.set]

    def _halt(self):
        raise StopIteration("Halt!")


class Tape:
    _tape: List[str]

    def __init__(self, input_data: str, blank):
        self._tape = list(input_data)
        self._blank = blank

    def write(self, index: int, value: str):
        try:
            self._tape[index] = value
        except IndexError:
            self._tape.insert(index, value)

    def read(self, index: int) -> str:
        try:
            return self._tape[index]
        except IndexError:
            self.write(index, self._blank)
            return self.read(index)

    def print(self) -> str:
        return "".join(self._tape).strip()

    def compensate_negative_index(self):
        self._tape.insert(0, self._blank)


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

    def write(self, value: str):
        self._tape.write(self._index, value)

    def move_left(self):
        self._index -= 1
        if (self._index) < 0:
            self._tape.compensate_negative_index()
            self._index = 0

    def move_right(self):
        self._index += 1
