from typing import Optional
from ninja import NinjaAPI, Schema

from src.state.board import Board, Cell, CellState

api = NinjaAPI()

current_board: Board | None = None

class CreateBoardRequest(Schema):
	rows: int
	cols: int

class UpdateCellRequest(Schema):
	row: int
	col: int
	colour: Optional[str] = None
	state: Optional[CellState] = None

@api.get("/getBoard")
def get_board(request):
	global current_board
	if current_board is None:
		grid = [[Cell(colour='white', state=CellState.EMPTY) for _ in range(8)] for _ in range(8)]
		current_board = Board(rows=8, cols=8, grid=grid)
	return current_board.model_dump().get('grid')

@api.post("/createBoard")
def create_board(request, body: CreateBoardRequest):
	if body.rows <= 0 or body.rows > 10 or body.cols <= 0 or body.cols > 10:
		return 400
	global current_board
	grid = [[Cell(colour='white', state=CellState.EMPTY) for _ in range(body.cols)] for _ in range(body.rows)]
	current_board = Board(rows=body.rows, cols=body.cols, grid=grid)
	return current_board.model_dump().get('grid')

@api.post("/solve")
def solve(request):
	if current_board is None:
		return 404
	# current_board.solve() # TODO
	return 204

@api.put("/updateCell")
def update_cell(request, body: UpdateCellRequest):
	if current_board is None:
		return 404
	if body.colour:
		current_board.grid[body.row][body.col].colour = body.colour
	if body.state:
		current_board.grid[body.row][body.col].state = body.state
	return 204