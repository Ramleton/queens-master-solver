import type { CellContextType } from '../context/BoardContext'

export async function getBoard(): Promise<CellContextType[][]> {
	const response = await fetch('http://localhost:8000/api/getBoard')
	return await response.json() as Promise<CellContextType[][]>
}

export async function createBoard(rows: number, cols: number): Promise<CellContextType[][]> {
	const response = await fetch('http://localhost:8000/api/createBoard', {
		method: 'POST',
		credentials: 'include',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({ rows, cols })
	})
	const res = await response.json() as Promise<CellContextType[][]>
	return res
}

export async function updateCell(row: number, col: number, newState: Partial<CellContextType>): Promise<void> {
	await fetch('http://localhost:8000/api/updateCell', {
		method: 'PUT',
		credentials: 'include',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({ row, col, ...newState })
	})
}

export async function solve(): Promise<void> {
	await fetch('http://localhost:8000/api/solve', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		}
	})
}
