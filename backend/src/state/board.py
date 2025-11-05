from enum import Enum
from typing import List
from pydantic import BaseModel

class CellState(str, Enum):
	EMPTY = "empty"
	QUEEN = "queen"
	MARKED = "marked"

class Cell(BaseModel):
	colour: str
	state: CellState

	def __str__(self):
		letter = " " if self.state == CellState.EMPTY else "X" if self.state == CellState.MARKED else "Q"
		return "[{}]".format(letter)

class Board(BaseModel):
	rows: int
	cols: int
	grid: List[List[Cell]]

	def __init__(self, rows: int, cols: int, grid: List[List[Cell]]):
		super().__init__(rows=rows, cols=cols, grid=grid)
	
	def print(self) -> None:
		for row in self.grid:
			line = ""
			for cell in row:
				line += str(cell)
			print(line)