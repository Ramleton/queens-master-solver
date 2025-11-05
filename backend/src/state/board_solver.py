from src.state.board import Board, Cell, CellState
import sys
import copy

class BoardSolver:
	board: Board
	unmarked_colour_dict: dict[str, list[tuple[int, int]]]
	colours_queen_dict: dict[str, bool]

	def __init__(self, board: Board) -> None:
		self.board = board
		self.unmarked_colour_dict = {}
		self.colours_queen_dict = {}
		for row in range(self.board.rows):
			for col in range(self.board.cols):
				# Add all colours to colours_queen_dict
				if self.unmarked_colour_dict.get(self.board.grid[row][col].colour) is None:
					self.unmarked_colour_dict[self.board.grid[row][col].colour] = []
				if self.colours_queen_dict.get(self.board.grid[row][col].colour) is None:
					self.colours_queen_dict[self.board.grid[row][col].colour] = False
				# Add all unmarked cells to unmarked_colour_dict
				if self.board.grid[row][col].state == CellState.EMPTY:
					self.unmarked_colour_dict[self.board.grid[row][col].colour]\
						.append((row, col))
				if self.board.grid[row][col].state == CellState.QUEEN:
					self.colours_queen_dict[self.board.grid[row][col].colour] = True
	
	def _check_cell_empty(self, row: int, col: int):
		return self.board.grid[row][col].state == CellState.EMPTY
	
	def _check_cell_marked(self, row: int, col: int):
		return self.board.grid[row][col].state == CellState.MARKED

	def _check_cell_queen(self, row: int, col: int):
		return self.board.grid[row][col].state == CellState.QUEEN
	
	def _mark_cell_as_marked(self, row: int, col: int):
		if self.board.grid[row][col].state != CellState.EMPTY:
			raise ValueError
		self.board.grid[row][col].state = CellState.MARKED
		try:
			if self.unmarked_colour_dict.get(self.board.grid[row][col].colour):
				self.unmarked_colour_dict[self.board.grid[row][col].colour].remove((row, col))
		except ValueError:
			pass
		
	def _mark_cell_as_queen(self, row: int, col: int):
		if not self._check_cell_empty(row, col) and not self._check_cell_queen(row, col):
			raise ValueError
		self.board.grid[row][col].state = CellState.QUEEN
		try:
			if self.unmarked_colour_dict.get(self.board.grid[row][col].colour):
				self.unmarked_colour_dict[self.board.grid[row][col].colour].remove((row, col))
				self.colours_queen_dict[self.board.grid[row][col].colour] = True
		except ValueError:
			pass

	def _mark_cells_in_same_row(self, row: int, col: int):
		for other_col in range(self.board.cols):
			if col != other_col and self._check_cell_empty(row, other_col):
				self._mark_cell_as_marked(row, other_col)
	
	def _mark_cells_in_same_column(self, row: int, col: int):
		for other_row in range(self.board.rows):
			if row != other_row and self._check_cell_empty(other_row, col):
				self._mark_cell_as_marked(other_row, col)

	def _mark_cells_surrounding_cell(self, row: int, col: int):
		for other_row in range(row - 1, row + 2):
			for other_col in range(col - 1, col + 2):
				if other_row < 0 or other_row >= self.board.rows or \
					other_col < 0 or other_col >= self.board.cols or \
					not self._check_cell_empty(other_row, other_col):
					continue
				self._mark_cell_as_marked(other_row, other_col)
	
	def _mark_cells_of_same_colour(self, colour: str):
		for (row, col) in copy.deepcopy(self.unmarked_colour_dict[colour]):
			if self._check_cell_empty(row, col):
				self._mark_cell_as_marked(row, col)

	def _mark_cells_around_queen(self, row: int, col: int):
		# Mark all cells in the same row
		self._mark_cells_in_same_row(row, col)

		# Mark all cells in the same column
		self._mark_cells_in_same_column(row, col)

		# Mark cells surrounding the queen
		self._mark_cells_surrounding_cell(row, col)

		# Mark all unmarked cells that have the same colour
		self._mark_cells_of_same_colour(self.board.grid[row][col].colour)

		self._check_steps()
	
	def _check_queens(self):
		for row in range(self.board.rows):
			for col in range(self.board.cols):
				if self.board.grid[row][col].state == CellState.QUEEN:
					self._mark_cells_around_queen(row, col)
	
	def _check_single_colour(self):
		for colour in self.unmarked_colour_dict:
			if len(self.unmarked_colour_dict[colour]) == 1:
				(row, col) = self.unmarked_colour_dict[colour][0]
				self._mark_cell_as_queen(row, col)
				self._mark_cells_around_queen(row, col)
	
	def _flatten[T](self, arr: list[list[T]]) -> list[T]:
		flattened = []
		for items in arr:
			for item in items:
				flattened.append(item)
		return flattened

	def _check_queen_would_conflict(self, row: int, col: int):
		unmarked_colours = copy.deepcopy(self.unmarked_colour_dict)
		unmarked_colour_cells = self._flatten(list(unmarked_colours.values()))
		for other_row in range(row - 1, row + 2):
			for other_col in range(col - 1, col + 2):
				if other_row < 0 or other_row >= self.board.rows or \
					other_col < 0 or other_col >= self.board.cols:
					continue
				if (other_row, other_col) in unmarked_colour_cells and \
					self.board.grid[other_row][other_col].colour != self.board.grid[row][col].colour:
					unmarked_colours[self.board.grid[other_row][other_col].colour].remove((other_row, other_col))
		for colour in unmarked_colours:
			if not self.colours_queen_dict[colour] and not len(unmarked_colours[colour]):
				self._mark_cell_as_marked(row, col)
				# Check if there is a single unmarked colour before iterating again
				# This is to prevent accidentally removing the only viable cell left of a colour
				return self._check_steps()

	def _check_cells_iterative(self):
		for (row, col) in self._flatten(list(self.unmarked_colour_dict.values())):
			self._check_queen_would_conflict(row, col)


	def _check_colour_row(self):
		for colour in self.unmarked_colour_dict:
			row = None
			for cell in self.unmarked_colour_dict[colour]:
				if row == None:
					row = cell[0]
				elif row != cell[0]:
					return
			# Getting this far means all cells of the same colour are in the same row
			# Mark all cells of other colours in the same row
			for col in range(self.board.cols):
				if row is not None and \
					self._check_cell_empty(row, col) and \
					self.board.grid[row][col].colour != colour:
					self._mark_cell_as_marked(row, col)

	def _check_colour_column(self):
		for colour in self.unmarked_colour_dict:
			column = None
			for cell in self.unmarked_colour_dict[colour]:
				if column == None:
					column = cell[1]
				elif column != cell[1]:
					return
			# Getting this far means all cells of the same colour are in the same column
			# Mark all cells of other colours in the same column
			for row in range(self.board.rows):
				if column is not None and \
					self._check_cell_empty(row, column) and \
					self.board.grid[row][column].colour != colour:
					self._mark_cell_as_marked(row, column)

	def _check_steps(self):
		self._check_single_colour()
		self._check_colour_row()
		self._check_colour_column()
		self._check_cells_iterative()
	
	def solve(self):
		# sys.setrecursionlimit(44)
		self._check_queens()
		self._check_steps()