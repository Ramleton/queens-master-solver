import type { CellContextType } from '../context/BoardContext'
import type { SolveResponse } from '../types/boardTypes'

const apiURL = import.meta.env.VITE_API_URL as string | undefined ?? 'http://localhost:8000'

export async function solve(rows: number, cols: number, grid: CellContextType[][]): Promise<SolveResponse> {
	const response = await fetch(`${apiURL}/api/solve`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({ rows, cols, grid })
	})
	if (!response.ok) {
		const error = await response.json() as { detail?: string }
		throw new Error(error.detail ?? 'Failed to solve the board')
	}
	return response.json() as Promise<SolveResponse>
}
