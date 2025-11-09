from typing import Any
from ninja import NinjaAPI, Schema

from src.state.board_solver import BoardSolver
from src.state.board import Board, Cell, CellState

api = NinjaAPI()

class SolveRequest(Schema):
	rows: int
	cols: int
	grid: list[list[Cell]]

class SolveResponse(Schema):
	steps: list[tuple[list[list[Cell]], CellState, str]]

@api.post("/solve")
def solve(request, body: SolveRequest):
	board = Board(body.rows, body.cols, body.grid)
	solution_steps = BoardSolver(board).solve()
	return SolveResponse(steps=solution_steps)