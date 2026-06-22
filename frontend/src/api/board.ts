import type { CellContextType } from '../context/BoardContext'
import type { SolveResponse } from '../types/boardTypes'

const API_URL = import.meta.env.VITE_API_URL as string | undefined ?? 'http://localhost:8000'

export async function solve(rows: number, cols: number, grid: CellContextType[][]): Promise<SolveResponse> {
	const response = await fetch(`${API_URL}/api/solve`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({ rows, cols, grid })
	})
	return response.json() as Promise<SolveResponse>
}
