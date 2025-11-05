from typing import Optional
from ninja import NinjaAPI, Schema

from src.state.board_solver import BoardSolver
from src.state.board import Board, Cell, CellState

api = NinjaAPI()

class SolveRequest(Schema):
	rows: int
	cols: int
	grid: list[list[Cell]]

@api.post("/solve")
def solve(request, body: SolveRequest):
	board = Board(body.rows, body.cols, body.grid)
	BoardSolver(board).solve()
	return board.model_dump().get('grid')