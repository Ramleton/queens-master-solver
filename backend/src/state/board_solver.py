from src.state.board import Board, Cell, CellState
import copy

class BoardSolver:
	board: Board
	unmarked_colour_dict: dict[str, list[tuple[int, int]]]
	colours_queen_dict: dict[str, bool]
	colours_to_rc: dict[str, tuple[dict[int, int], dict[int, int]]]

	def __init__(self, board: Board) -> None:
		self.board = board
		self.unmarked_colour_dict = {}
		self.colours_queen_dict = {}
		self.colours_to_rc = {}
		for row in range(self.board.rows):
			for col in range(self.board.cols):
				# Add all colours to colours_to_rc
				if self.colours_to_rc.get(self.board.grid[row][col].colour) is None:
					self.colours_to_rc[self.board.grid[row][col].colour] = (dict(), dict())
				# Add all colours to colours_queen_dict
				if self.unmarked_colour_dict.get(self.board.grid[row][col].colour) is None:
					self.unmarked_colour_dict[self.board.grid[row][col].colour] = []
				if self.colours_queen_dict.get(self.board.grid[row][col].colour) is None:
					self.colours_queen_dict[self.board.grid[row][col].colour] = False
				# Initialize empty rows and columns in colours_to_rc
				if self.colours_to_rc[self.board.grid[row][col].colour][0].get(row) is None:
					self.colours_to_rc[self.board.grid[row][col].colour][0][row] = 0
				if self.colours_to_rc[self.board.grid[row][col].colour][1].get(col) is None:
					self.colours_to_rc[self.board.grid[row][col].colour][1][col] = 0
				# Add all unmarked cells to unmarked_colour_dict and colours_to_rc
				if self.board.grid[row][col].state == CellState.EMPTY:
					self.unmarked_colour_dict[self.board.grid[row][col].colour]\
						.append((row, col))
					self.colours_to_rc[self.board.grid[row][col].colour][0][row] += 1
					self.colours_to_rc[self.board.grid[row][col].colour][1][col] += 1
				# Add all queens to colours_queen_dict
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
			self.colours_to_rc[self.board.grid[row][col].colour][0][row] -= 1
			self.colours_to_rc[self.board.grid[row][col].colour][1][col] -= 1
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
		# self.board.print()
		# Temporarily mark all cells in the same row
		for other_col in range(self.board.cols):
			if other_col != col and self._check_cell_empty(row, other_col):
				unmarked_colours[self.board.grid[row][other_col].colour].remove((row, other_col))
				unmarked_colour_cells.remove((row, other_col))
		# Temporarily mark all cells in the same column
		for other_row in range(self.board.rows):
			if other_row != row and self._check_cell_empty(other_row, col):
				unmarked_colours[self.board.grid[other_row][col].colour].remove((other_row, col))
				unmarked_colour_cells.remove((other_row, col))
		# Temporarily mark adjacent cells
		for other_row in range(row - 1, row + 2):
			for other_col in range(col - 1, col + 2):
				if other_row < 0 or other_row >= self.board.rows or \
					other_col < 0 or other_col >= self.board.cols:
					continue
				if (other_row, other_col) in unmarked_colour_cells and \
					self.board.grid[other_row][other_col].colour != self.board.grid[row][col].colour:
					unmarked_colours[self.board.grid[other_row][other_col].colour].remove((other_row, other_col))
					unmarked_colour_cells.remove((other_row, other_col))
		# Check if a colour has no unmarked cells and has no queens
		# If so, this is a conflict
		for colour in unmarked_colours:
			if not self.colours_queen_dict[colour] and not len(unmarked_colours[colour]):
				self._mark_cell_as_marked(row, col)
				# Check if there is a single unmarked colour before iterating again
				# This is to prevent accidentally removing the only viable cell left of a colour
				return self._check_steps()

	def _check_cells_iterative(self):
		for row in range(self.board.rows):
			for col in range(self.board.cols):
				if self._check_cell_empty(row, col):
					self._check_queen_would_conflict(row, col)
	
	def _check_colour_row_helper(self, colour):
		row = None
		for (cell_row, _) in self.unmarked_colour_dict[colour]:
				if row == None:
					row = cell_row
				elif row != cell_row:
					return None
		return row

	def _check_colour_row(self):
		for colour in self.unmarked_colour_dict.keys():
			row = self._check_colour_row_helper(colour)
			for col in range(self.board.cols):
				if row is not None and \
					self._check_cell_empty(row, col) and \
					self.board.grid[row][col].colour != colour:
					self._mark_cell_as_marked(row, col)

	def _check_colour_column_helper(self, colour):
		col = None
		for (_, cell_col) in self.unmarked_colour_dict[colour]:
				if col == None:
					col = cell_col
				elif col != cell_col:
					return None
		return col

	def _check_colour_column(self):
		for colour in self.unmarked_colour_dict:
			column = self._check_colour_column_helper(colour)
			# Getting this far means all cells of the same colour are in the same column
			# Mark all cells of other colours in the same column
			for row in range(self.board.rows):
				if column is not None and \
					self._check_cell_empty(row, column) and \
					self.board.grid[row][column].colour != colour:
					self._mark_cell_as_marked(row, column)
	
	def _sort_by_least(self):
		return sorted(self.unmarked_colour_dict, key=lambda colour: len(self.unmarked_colour_dict[colour]))
	
	def _find_columns_to_compare(self, colour):
		columns_to_check = set()
		for (column, number) in self.colours_to_rc[colour][1].items():
			if number:
				columns_to_check.add(column)
		return columns_to_check

	def _find_rows_to_compare(self, colour):
		rows_to_check = set()
		for (row, number) in self.colours_to_rc[colour][0].items():
			if number:
				rows_to_check.add(row)
		return rows_to_check
	
	def _compare_columns(self):
		sorted_colours = self._sort_by_least()
		while sorted_colours:
			colour = sorted_colours.pop(0)
			columns_to_check = self._find_columns_to_compare(colour)
			# Move on if there are no columns to check
			if not len(columns_to_check):
				continue
			num_supersets = 1 # The colour itself is a superset
			strict_supersets = set()
			for o_colour in sorted_colours:
				o_columns_to_check = self._find_columns_to_compare(o_colour)
				if columns_to_check.issubset(o_columns_to_check):
					num_supersets += 1
					if len(o_columns_to_check) > len(columns_to_check):
						strict_supersets.add(o_colour)
			if len(strict_supersets) and num_supersets > len(columns_to_check):
				# There is a strict superset of columns that are not a subset
				# So, we mark the cells of the colours in the strict supersets with matching columns
				for o_colour in strict_supersets:
					for (row, column) in copy.deepcopy(self.unmarked_colour_dict[o_colour]):
						if column in columns_to_check:
							self._mark_cell_as_marked(row, column)
	
	def _compare_rows(self):
		sorted_colours = self._sort_by_least()
		while sorted_colours:
			colour = sorted_colours.pop(0)
			rows_to_check = self._find_rows_to_compare(colour)
			# Move on if there are no rows to check
			if not len(rows_to_check):
				continue
			num_supersets = 1 # The colour itself is a superset
			strict_supersets = set()
			for o_colour in sorted_colours:
				o_rows_to_check = self._find_rows_to_compare(o_colour)
				if rows_to_check.issubset(o_rows_to_check):
					num_supersets += 1
					if len(o_rows_to_check) > len(rows_to_check):
						strict_supersets.add(o_colour)
			if len(strict_supersets) and num_supersets > len(rows_to_check):
				# There is a strict superset of rows that are not a subset
				# So, we mark the cells of the colours in the strict supersets with matching rows
				for o_colour in strict_supersets:
					for (row, column) in copy.deepcopy(self.unmarked_colour_dict[o_colour]):
						if row in rows_to_check:
							self._mark_cell_as_marked(row, column)

	def _check_steps(self):
		self._check_single_colour()
		self._check_colour_row()
		self._check_colour_column()
		self._check_cells_iterative()
		self._compare_columns()
		self._compare_rows()
	
	def solve(self):
		self._check_queens()
		for _ in range(10):
			self._check_steps()