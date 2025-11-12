from src.state.board import Board, Cell, CellState
from src.state.axis import Axis

class BoardSolver:
	board: Board
	unmarked_colour_dict: dict[str, list[tuple[int, int]]] # list(row, col)
	colours_queen_dict: dict[str, bool]
	colours_to_rc: dict[str, tuple[dict[int, int], dict[int, int]]]
	solution_steps: list[tuple[list[list[Cell]], CellState, str]] # list(row, col, state, reason)

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
		self.solution_steps = []
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
				self.solution_steps.append((
					self.board.clone().grid,
					CellState.MARKED,
					f"Cell in the same row as the Queen on ({row}, {col})"
				))
	
	def _mark_cells_in_same_column(self, row: int, col: int):
		"""
		Marks all unmarked cells in the same column as marked.
		
		This function marks all unmarked cells that are in the same column as the given cell as marked.
		"""
		for other_row in range(self.board.rows):
			if row != other_row and self._check_cell_empty(other_row, col):
				self._mark_cell_as_marked(other_row, col)
				self.solution_steps.append((
					self.board.clone().grid,
					CellState.MARKED,
					f"Cell in the same column as the Queen on ({row}, {col})"
				))

	def _mark_cells_surrounding_cell(self, row: int, col: int):
		"""
		Marks all unmarked cells surrounding the given cell as marked.
		
		This function marks all unmarked cells that are in the same row, column, or adjacent to the given cell as marked.
		"""
		for r in range(max(0, row - 1), min(self.board.rows, row + 2)):
			for c in range(max(0, col - 1), min(self.board.cols, col + 2)):
				if self._check_cell_empty(r, c):
					self._mark_cell_as_marked(r, c)
					self.solution_steps.append((
						self.board.clone().grid,
						CellState.MARKED,
						f"Cell adjacent to the queen on ({row}, {col})"
					))
	
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
				self.solution_steps.append((
					self.board.clone().grid,
					CellState.MARKED,
					f"Cell of the same colour as the queen on ({row}, {col})"
				))

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
				self.solution_steps.append((
					self.board.clone().grid,
					CellState.QUEEN, 
					f"Queen in the only unmarked {colour} cell"
				))
				self._mark_cells_around_queen(row, col)
	
	def _snapshot(self):
		"""
		Takes a snapshot of the current board state by cloning the board.

		Returns:
			Board: A cloned version of the current board state.
		"""
		return (
			self.board.clone(),
			{c: list(v) for c, v in self.unmarked_colour_dict.items()},
			dict(self.colours_queen_dict),
			{colour: (dict(r), dict(c)) for colour, (r, c) in self.colours_to_rc.items()},
			list(self.solution_steps)
		)

	def _restore(self, snapshot):
		"""
		Restores the board state from a snapshot.

		Parameters:
			snapshot (Board): The snapshot to restore the board state from.
		"""
		board_copy, unmarked, queens, rc, steps = snapshot
		self.board.restore_from(board_copy)
		self.unmarked_colour_dict = unmarked
		self.colours_queen_dict = queens
		self.colours_to_rc = rc
		self.solution_steps = steps
	
	def _check_backtrack_queen_conflicts(self, row: int, col: int) -> bool:
		"""
		Checks if marking a cell as a queen would cause a conflict through potential backtracking.
		
		If marking the cell as a queen would cause a conflict, marks the cell as marked instead.
		
		Parameters:
			row (int): The row of the cell to check.
			col (int): The column of the cell to check.
		
		Raises:
			ValueError: If marking the cell as a queen would cause a conflict.
		
		Returns:
			bool: True if marking the cell as a queen would cause a conflict, False otherwise.
		"""
		# Snapshot current state
		snapshot = self._snapshot()

		try:
			# Attempt to proceed
			self._mark_cell_as_queen(row, col)
			self.solution_steps.append((
				self.board.clone().grid,
				CellState.QUEEN, 
				f"Placing Queen on ({row}, {col}) and using backtracking to determine correct placement"
			))
			self._check_steps()
			# Check if a colour has no unmarked cells and has no queens
			# If so, this is a conflict
			for colour in self.unmarked_colour_dict.keys():
				if not self.colours_queen_dict[colour] and not len(self.unmarked_colour_dict[colour]):
					raise ValueError
		except ValueError:
			# Marking the cell as a queen would cause a conflict
			self._restore(snapshot)
			self._mark_cell_as_marked(row, col)
			self.solution_steps.append((
				self.board.grid,
				CellState.MARKED, 
				f"Marked cell on ({row}, {col}) after determining it cannot be a Queen through backtracking"
			))
			return True
		return False

	def _check_queen_would_conflict(self, row: int, col: int):
		"""
		Checks if a queen in position (row, col) would cause a conflict.
		
		A conflict occurs when a colour has no unmarked cells and has no queens.
		
		Returns early if a conflict is found to prevent unnecessary checks.
		"""
		# Skip cells already known to be non-viable
		if not self._check_cell_empty(row, col):
			return

		# Check if there are any conflicts
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
				self.solution_steps.append((
					self.board.clone().grid,
					CellState.MARKED, 
					f"Marked cell on ({row}, {col}) after determining it cannot be a Queen"
				))
				# Check if there is a single unmarked colour before iterating again
				# This is to prevent accidentally removing the only viable cell left of a colour
				return self._check_steps()
	
	def _check_cells_iterative_backtrack(self):
		"""
		Iterate over all empty cells and check if marking one as a queen would result in a conflict.
		If so, mark the cell as marked.
		This is to prevent accidentally removing the only viable cell left of a colour.
		"""
		for row in range(self.board.rows):
			for col in range(self.board.cols):
				if self._check_cell_empty(row, col):
					# Use backtracking as little as possible, as its costly
					if self._check_backtrack_queen_conflicts(row, col):
						return

	def _check_cells_iterative(self):
		"""
		Iterate over all empty cells and check if marking one as a queen would result in a conflict.
		If so, mark the cell as marked.
		This is to prevent accidentally removing the only viable cell left of a colour.
		"""
		for _, cells in dict(self.unmarked_colour_dict).items():
			for cell in cells:
				self._check_queen_would_conflict(cell[0], cell[1])
	
	def _sort_by_least(self):
		"""
		Sorts the unmarked colour dictionary by the length of each colour's set.
		This is used to find the colour with the least number of unmarked cells.

		Returns:
			list: A list of colours sorted in ascending order by the length of their set.
		"""
		return sorted(self.unmarked_colour_dict, key=lambda colour: len(self.unmarked_colour_dict[colour]))
	
	def _check_cells_of_colour_within_range(self, colour: str, axis: Axis, i: int, num_groups_checking: int):
		if not self.unmarked_colour_dict[colour]:
			return False
		for cell in self.unmarked_colour_dict[colour]:
			if i > cell[axis] or cell[axis] >= i + num_groups_checking:
				return False
		return True
	
	def _compare_groups_helper(self, sorted_colours: list, axis: Axis, i: int, num_groups_checking: int) -> tuple[list[str], list[str]]:
		in_range, not_in_range = [], []
		for colour in sorted_colours:
			if self._check_cells_of_colour_within_range(colour, axis, i, num_groups_checking):
				in_range.append(colour)
			else:
				not_in_range.append(colour)
		return in_range, not_in_range
	
	def _compare_groups_marking_helper(
		self,
		i: int,
		num_groups_checking: int,
		axis: Axis,
		in_range: list[str],
		not_in_range: list[str]
	):
		for colour in not_in_range:
			remaining_cells = list(self.unmarked_colour_dict[colour])
			for (r, c) in remaining_cells:
				if axis == 0 and r in range(i, i + num_groups_checking):
					self._mark_cell_as_marked(r, c)
					self.solution_steps.append((
						self.board.clone().grid,
						CellState.MARKED, 
						f"Marked cell on ({r}, {c}) since there are too "\
						+ f" many colours in the same row(s) as the "\
						+ f"remaining cells of colour(s) {in_range}"
					))
				elif axis == 1 and c in range(i, i + num_groups_checking):
					self._mark_cell_as_marked(r, c)
					self.solution_steps.append((
						self.board.clone().grid,
						CellState.MARKED, 
						f"Marked cell on ({r}, {c}) since there are too "\
						+ f" many colours in the same column(s) as the "\
						+ f"remaining cells of colour(s) {in_range}"
					))
	
	def _compare_groups(self, axis: Axis):
		sorted_colours = self._sort_by_least()
		axis_length = self.board.rows if axis == Axis.ROW else self.board.cols
		for num_groups_checking in range(1, axis_length):
			for i in range(axis_length + 1 - num_groups_checking):
				in_range, not_in_range = self._compare_groups_helper(sorted_colours, axis, i, num_groups_checking)
				if len(in_range) == num_groups_checking:
					self._compare_groups_marking_helper(i, num_groups_checking, axis, in_range, not_in_range)

	def _check_steps(self):
		"""
		Checks all steps in the board solver algorithm.

		This method checks for single colours, colours in rows and columns,
		iterative colour placement, and mutually-exclusive column/row group
		constraints through queen placement.

		Returns:
			None
		"""
		prev_state = None
		while prev_state != self._hash_state():
			prev_state = self._hash_state()
			self._check_queens()
			self._check_single_colour()
			if prev_state == self._hash_state():
				self._compare_groups(Axis.ROW)
			if prev_state == self._hash_state():
				self._compare_groups(Axis.COLUMN)
			if prev_state == self._hash_state():
				self._check_cells_iterative()
			if prev_state == self._hash_state():
				self._check_cells_iterative_backtrack()
	
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
		self._check_steps()
		return self.solution_steps
