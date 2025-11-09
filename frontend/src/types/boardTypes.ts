import type { CellContextType } from '../context/BoardContext'

export type CellState = 'empty' | 'queen' | 'marked'

export type SolveResponse = {
	steps: [CellContextType[][], CellState, string][]
}
