import type { CellContextType } from '../context/BoardContext'

export type CellState = 'empty' | 'queen' | 'marked'

export type GridState = {
	grid: CellContextType[][]
	state: CellState
	message: string
}

export type SolveResponse = GridState[]
