import type { CellContextType } from '../context/BoardContext'
import type { SolveResponse } from '../types/boardTypes'

export async function solve(rows: number, cols: number, grid: CellContextType[][]): Promise<SolveResponse> {
	const response = await fetch('http://localhost:8000/api/solve', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({ rows, cols, grid })
	})
	return response.json() as Promise<SolveResponse>
}
