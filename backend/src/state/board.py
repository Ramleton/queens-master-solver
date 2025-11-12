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

	def __init__(self,  colour: str, state: CellState):
		super().__init__(colour=colour, state=state)
	
	def clone(self) -> "Cell":
		return Cell(colour=self.colour, state=self.state)

	def __str__(self):
		letter = " " if self.state == CellState.EMPTY else "X" if self.state == CellState.MARKED else "Q"
		return "[{}]".format(letter)

class Board(BaseModel):
	rows: int
	cols: int
	grid: List[List[Cell]]

	def __init__(self, rows: int, cols: int, grid: List[List[Cell]]):
		super().__init__(rows=rows, cols=cols, grid=grid)
	
	def clone(self) -> "Board":
		new_grid = [[cell.clone() for cell in row] for row in self.grid]
		return Board(rows=self.rows, cols=self.cols, grid=new_grid)

	def restore_from(self, other: "Board"):
		self.grid = [[cell.clone() for cell in row] for row in other.grid]
	
	def print(self) -> None:
		for row in self.grid:
			line = ""
			for cell in row:
				line += str(cell)
			print(line)