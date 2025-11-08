from src.state.board import Board, CellState
from src.state.axis import Axis

class BoardSolver:
	board: Board
	unmarked_colour_dict: dict[str, list[tuple[int, int]]]
	colours_queen_dict: dict[str, bool]
	colours_to_rc: dict[str, tuple[dict[int, int], dict[int, int]]]

	def __init__(self, board: Board) -> None:
		"""
		Initializes the board solver with a given board.
		
		This function will iterate over all cells in the board and
		initialize all necessary data structures.
		
		After calling this function, the board solver is ready to
		solve the board.
		
		Parameters:
			board (Board): The board to solve.
		
		Returns:
			None
		"""
		self.board = board
		self.unmarked_colour_dict = {}
		self.colours_queen_dict = {}
		self.colours_to_rc = {}
		for row in range(self.board.rows):
			for col in range(self.board.cols):
				cell = self.board.grid[row][col]
				# Add all colours to colours_to_rc
				if self.colours_to_rc.get(cell.colour) is None:
					self.colours_to_rc[cell.colour] = (dict(), dict())
				# Add all colours to colours_queen_dict
				if self.unmarked_colour_dict.get(cell.colour) is None:
					self.unmarked_colour_dict[cell.colour] = []
				if self.colours_queen_dict.get(cell.colour) is None:
					self.colours_queen_dict[cell.colour] = False
				# Initialize empty rows and columns in colours_to_rc
				if self.colours_to_rc[cell.colour][0].get(row) is None:
					self.colours_to_rc[cell.colour][0][row] = 0
				if self.colours_to_rc[cell.colour][1].get(col) is None:
					self.colours_to_rc[cell.colour][1][col] = 0
				# Add all unmarked cells to unmarked_colour_dict and colours_to_rc
				if cell.state == CellState.EMPTY:
					self.unmarked_colour_dict[cell.colour]\
						.append((row, col))
					self.colours_to_rc[cell.colour][0][row] += 1
					self.colours_to_rc[cell.colour][1][col] += 1
				# Add all queens to colours_queen_dict
				if cell.state == CellState.QUEEN:
					self.colours_queen_dict[cell.colour] = True
	
	def _check_cell_empty(self, row: int, col: int):
		"""
		Checks if the cell at (row, col) is empty.
		
		Parameters:
			row (int): The row of the cell to check.
			col (int): The column of the cell to check.
		
		Returns:
			bool: True if the cell is empty, False otherwise.
		"""
		return self.board.grid[row][col].state == CellState.EMPTY
	
	def _check_cell_marked(self, row: int, col: int):
		"""
		Checks if the cell at (row, col) is marked.
		
		Parameters:
			row (int): The row of the cell to check.
			col (int): The column of the cell to check.
		
		Returns:
			bool: True if the cell is marked, False otherwise.
		"""
		return self.board.grid[row][col].state == CellState.MARKED

	def _check_cell_queen(self, row: int, col: int):
		"""
		Checks if the cell at (row, col) is a queen.
		
		Parameters:
			row (int): The row of the cell to check.
			col (int): The column of the cell to check.
		
		Returns:
			bool: True if the cell is a queen, False otherwise.
		"""
		return self.board.grid[row][col].state == CellState.QUEEN
	
	def _mark_cell_as_marked(self, row: int, col: int):
		"""
		Marks the cell at (row, col) as marked.
		
		Raises a ValueError if the cell is not empty.
		
		Removes the cell from the unmarked_colour_dict and marks it as marked in colours_queen_dict.
		
		Parameters:
			row (int): The row of the cell to mark as marked.
			col (int): The column of the cell to mark as marked.
		
		Raises:
			ValueError: If the cell is not empty.
		"""
		cell = self.board.grid[row][col]
		if cell.state != CellState.EMPTY:
			raise ValueError
		cell.state = CellState.MARKED
		try:
			if self.unmarked_colour_dict.get(cell.colour):
				self.unmarked_colour_dict[cell.colour].remove((row, col))
			self.colours_to_rc[cell.colour][0][row] -= 1
			self.colours_to_rc[cell.colour][1][col] -= 1
		except ValueError:
			pass
		
	def _mark_cell_as_queen(self, row: int, col: int):
		"""
		Marks the cell at (row, col) as a queen.
		
		Raises a ValueError if the cell is not empty and not a queen.
		
		Removes the cell from the unmarked_colour_dict and marks it as a queen in colours_queen_dict.
		
		Parameters:
			row (int): The row of the cell to mark as a queen.
			col (int): The column of the cell to mark as a queen.
		
		Raises:
			ValueError: If the cell is not empty and not a queen.
		"""
		if not self._check_cell_empty(row, col) and not self._check_cell_queen(row, col):
			raise ValueError
		cell = self.board.grid[row][col]
		cell.state = CellState.QUEEN
		try:
			if self.unmarked_colour_dict.get(cell.colour):
				self.unmarked_colour_dict[cell.colour].remove((row, col))
				self.colours_queen_dict[cell.colour] = True
		except ValueError:
			pass

	def _mark_cells_in_same_row(self, row: int, col: int):
		"""
		Marks all unmarked cells in the same row as marked.
		
		This function marks all unmarked cells that are in the same row as the given cell as marked.
		"""
		for other_col in range(self.board.cols):
			if col != other_col and self._check_cell_empty(row, other_col):
				self._mark_cell_as_marked(row, other_col)
	
	def _mark_cells_in_same_column(self, row: int, col: int):
		"""
		Marks all unmarked cells in the same column as marked.
		
		This function marks all unmarked cells that are in the same column as the given cell as marked.
		"""
		for other_row in range(self.board.rows):
			if row != other_row and self._check_cell_empty(other_row, col):
				self._mark_cell_as_marked(other_row, col)

	def _mark_cells_surrounding_cell(self, row: int, col: int):
		"""
		Marks all unmarked cells surrounding the given cell as marked.
		
		This function marks all unmarked cells that are in the same row, column, or adjacent to the given cell as marked.
		"""
		for r in range(max(0, row - 1), min(self.board.rows, row + 2)):
			for c in range(max(0, col - 1), min(self.board.cols, col + 2)):
				if self._check_cell_empty(r, c):
					self._mark_cell_as_marked(r, c)
	
	def _mark_cells_of_same_colour(self, colour: str):
		"""
		Marks all unmarked cells of the same colour as marked.
		
		This function marks all cells that are unmarked and have the same colour
		as marked. The function does not mark any cells that are not empty or
		are already marked.
		
		Parameters:
			colour (str): The colour of the cells to mark.
		
		Returns:
			None
		"""
		for (row, col) in list(self.unmarked_colour_dict[colour]):
			if self._check_cell_empty(row, col):
				self._mark_cell_as_marked(row, col)

	def _mark_cells_around_queen(self, row: int, col: int):
		"""
		Marks all cells around a queen as marked.
		
		Cells are marked in the following ways:
		- All cells in the same row are marked.
		- All cells in the same column are marked.
		- All cells directly surrounding the queen are marked.
		- All unmarked cells that have the same colour are marked.
		"""
		# Mark all cells in the same row
		self._mark_cells_in_same_row(row, col)

		# Mark all cells in the same column
		self._mark_cells_in_same_column(row, col)

		# Mark cells surrounding the queen
		self._mark_cells_surrounding_cell(row, col)

		# Mark all unmarked cells that have the same colour
		self._mark_cells_of_same_colour(self.board.grid[row][col].colour)
	
	def _check_queens(self):
		"""
		Checks all cells in the board for queens and marks all cells around
		each queen as marked.
		"""
		for row in range(self.board.rows):
			for col in range(self.board.cols):
				if self.board.grid[row][col].state == CellState.QUEEN:
					self._mark_cells_around_queen(row, col)
	
	def _check_single_colour(self):
		"""
		Checks if there is only one unmarked cell of a certain colour.
		If so, marks the cell as a queen and marks all cells around it as marked.
		"""
		for colour in self.unmarked_colour_dict:
			if len(self.unmarked_colour_dict[colour]) == 1:
				(row, col) = self.unmarked_colour_dict[colour][0]
				self._mark_cell_as_queen(row, col)
				self._mark_cells_around_queen(row, col)

	def _check_queen_would_conflict(self, row: int, col: int):
		"""
		Checks if a queen in position (row, col) would cause a conflict.
		
		A conflict occurs when a colour has no unmarked cells and has no queens.
		
		Returns early if a conflict is found to prevent unnecessary checks.
		"""
		unmarked_colours = {c: list(v) for c, v in self.unmarked_colour_dict.items()}
		unmarked_colour_cells = {cell for cells in unmarked_colours.values() for cell in cells}
		# Temporarily mark all cells in the same row
		for c in range(self.board.cols):
			if c != col and self._check_cell_empty(row, c):
				unmarked_colours[self.board.grid[row][c].colour].remove((row, c))
				unmarked_colour_cells.discard((row, c))
		# Temporarily mark all cells in the same column
		for r in range(self.board.rows):
			if r != row and self._check_cell_empty(r, col):
				unmarked_colours[self.board.grid[r][col].colour].remove((r, col))
				unmarked_colour_cells.discard((r, col))
		# Temporarily mark adjacent cells
		for r in range(row - 1, row + 2):
			for c in range(col - 1, col + 2):
				if r < 0 or r >= self.board.rows or \
					c < 0 or c >= self.board.cols:
					continue
				if (r, c) in unmarked_colour_cells and \
					self.board.grid[r][c].colour != self.board.grid[row][col].colour:
					unmarked_colours[self.board.grid[r][c].colour].remove((r, c))
					unmarked_colour_cells.discard((r, c))
		# Check if a colour has no unmarked cells and has no queens
		# If so, this is a conflict
		for colour in unmarked_colours:
			if not self.colours_queen_dict[colour] and not len(unmarked_colours[colour]):
				self._mark_cell_as_marked(row, col)
				# Check if there is a single unmarked colour before iterating again
				# This is to prevent accidentally removing the only viable cell left of a colour
				return self._check_steps()

	def _check_cells_iterative(self):
		"""
		Iterate over all empty cells and check if marking one as a queen would result in a conflict.
		If so, mark the cell as marked.
		This is to prevent accidentally removing the only viable cell left of a colour.
		"""
		for row in range(self.board.rows):
			for col in range(self.board.cols):
				if self._check_cell_empty(row, col):
					self._check_queen_would_conflict(row, col)
	
	# def _check_colour_row_helper(self, colour):
	# 	"""
	# 	Helper function to check if all unmarked cells of a colour are in the same row.
		
	# 	Args:
	# 		colour (str): The colour to check.
		
	# 	Returns:
	# 		int or None: The row number of all unmarked cells of the given colour, or None if they are not all in the same row.
	# 	"""
	# 	row = None
	# 	for (cell_row, _) in self.unmarked_colour_dict[colour]:
	# 		if row is None:
	# 			row = cell_row
	# 		elif row != cell_row:
	# 			return None
	# 	return row

	# def _check_colour_row(self):
	# 	"""
	# 	Check if all unmarked cells of a colour are in the same row.
	# 	If so, mark all cells in the same row that are not of this colour.
	# 	This is to prevent accidentally removing the only viable cell left of a colour.
	# 	"""
	# 	for colour in self.unmarked_colour_dict.keys():
	# 		row = self._check_colour_row_helper(colour)
	# 		if row is None:
	# 			continue
	# 		for col in range(self.board.cols):
	# 			if (
	# 				self._check_cell_empty(row, col) and
	# 				self.board.grid[row][col].colour != colour
	# 			):
	# 				self._mark_cell_as_marked(row, col)

	# def _check_colour_column_helper(self, colour):
	# 	"""
	# 	Check if all cells in a colour are in the same column.

	# 	Args:
	# 		colour (str): The colour to check

	# 	Returns:
	# 		int: The column that all cells in the colour are in, or None if not all cells are in the same column.
	# 	"""
	# 	col = None
	# 	for (_, cell_col) in self.unmarked_colour_dict[colour]:
	# 		if col is None:
	# 			col = cell_col
	# 		elif col != cell_col:
	# 			return None
	# 	return col

	# def _check_colour_column(self):
	# 	"""Check if all cells in a colour are in the same column and mark cells that are not the same colour as marked."""
	# 	for colour in self.unmarked_colour_dict:
	# 		column = self._check_colour_column_helper(colour)
	# 		if column is None:
	# 			continue
	# 		for row in range(self.board.rows):
	# 			if (
	# 				self._check_cell_empty(row, column) and
	# 				self.board.grid[row][column].colour != colour
	# 			):
	# 				self._mark_cell_as_marked(row, column)
	
	def _sort_by_least(self):
		"""
		Sorts the unmarked colour dictionary by the length of each colour's set.
		This is used to find the colour with the least number of unmarked cells.

		Returns:
			list: A list of colours sorted in ascending order by the length of their set.
		"""
		return sorted(self.unmarked_colour_dict, key=lambda colour: len(self.unmarked_colour_dict[colour]))
	
	def _find_group_to_compare(self, colour: str, axis: Axis):
		"""
		Finds all positions along an axis that are available for a given
		colour in a given axis.

		Args:
			colour (str): The colour to find available positions for.
			axis (Axis): The axis to find available positions in.

		Returns:
			set: A set of all positions along the given axis that are
			available for the given colour in the given axis.
		"""
		group_to_check = set()
		for (value, number) in self.colours_to_rc[colour][axis].items():
			if number:
				group_to_check.add(value)
		return group_to_check
	
	def _compare_groups(self, axis: Axis):
		"""
		If more colours share available positions than the number of positions
		available, eliminate any colour that has alternative placements elsewhere.
		This enforces mutually-exclusive column/row group constraints through
		queen placement.
		"""
		sorted_colours = self._sort_by_least()
		while sorted_colours:
			colour = sorted_colours.pop(0)
			group_to_check = self._find_group_to_compare(colour, axis)
			# Move on if there are no columns to check
			if not len(group_to_check):
				continue
			num_same = 1 # The number of sets we encounter that are equivalent
			extra_colours = set()
			for o_colour in sorted_colours:
				o_group_to_check = self._find_group_to_compare(o_colour, axis)
				if group_to_check == o_group_to_check:
					num_same += 1
				elif o_group_to_check.intersection(group_to_check):
					extra_colours.add(o_colour)
			# Move on if the number of colours with equivalent sets isn't equal
			# to the number of rows/columns to check
			if num_same != len(group_to_check):
				continue
			print(colour, self.unmarked_colour_dict[colour], extra_colours)
			# Mark the cells of the colours in the extra colours with matching columns
			for o_colour in extra_colours:
				for (row, column) in list(self.unmarked_colour_dict[o_colour]):
					if axis == 1 and column in group_to_check:
						self._mark_cell_as_marked(row, column)
					elif axis == 0 and row in group_to_check:
						self._mark_cell_as_marked(row, column)

	def _check_steps(self):
		"""
		Checks all steps in the board solver algorithm.

		This method checks for single colours, colours in rows and columns,
		iterative colour placement, and mutually-exclusive column/row group
		constraints through queen placement.

		Returns:
			None
		"""
		self._check_single_colour()
		self._compare_groups(Axis.ROW)
		self._compare_groups(Axis.COLUMN)
		self._check_cells_iterative()
	
	def _hash_state(self):
		"""
		Returns a tuple of tuples representing the state of the board.

		The outer tuple has length equal to the number of rows in the board.
		The inner tuple has length equal to the number of columns in the board.
		The state of each cell is represented by an enum value from CellState.

		This method is used to track changes in the state of the board.
		"""
		return tuple(tuple(cell.state for cell in row) for row in self.board.grid)
	
	def solve(self):
		self._check_queens()
		# self._compare_groups(Axis.COLUMN)
		prev_state = None
		while prev_state != self._hash_state():
			prev_state = self._hash_state()
			self._check_steps()
