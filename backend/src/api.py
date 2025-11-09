from typing import Any
from ninja import NinjaAPI, Schema

from src.state.board_solver import BoardSolver
from src.state.board import Board, Cell, CellState

api = NinjaAPI()

class SolveRequest(Schema):
	rows: int
	cols: int
	grid: list[list[Cell]]

class GridState(Schema):
	grid: list[list[Cell]]
	state: CellState
	message: str

@api.post("/solve")
def solve(request, body: SolveRequest) -> list[GridState]:
	board = Board(body.rows, body.cols, body.grid)
	solution = BoardSolver(board).solve()
	return [GridState(grid=step[0], state=step[1], message=step[2]) for step in solution]
	