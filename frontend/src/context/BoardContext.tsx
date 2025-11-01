import React from 'react'

type CellState = 'empty' | 'queen' | 'marked'

interface CellContextType {
	colour: string
	state: CellState
}

const initialCellState: CellContextType = {
	colour: 'white',
	state: 'empty'
}

const initialBoardState = {
	cells: Array.from({ length: 8 }).map(() => (
		Array.from({ length: 8 }).map(() => (
			initialCellState
		))
	))
}

interface BoardContext {
	cells: CellContextType[][]
	rows: number
	cols: number
	setCell: (row: number, col: number, newState: Partial<CellContextType>) => void
	setRows: (rows: number) => void
	setCols: (cols: number) => void
}

const BoardContext = React.createContext<BoardContext | null>(null)

export const useBoardContext = () => {
	const context = React.useContext(BoardContext)
	if (!context) {
		throw new Error('useBoardContext must be used within a BoardProvider')
	}
	return context
}

export const BoardProvider = ({ children }: { children: React.ReactNode }) => {
	const [cells, setCells] = React.useState<CellContextType[][]>(initialBoardState.cells)
	const rows = cells.length
	const cols = cells[0]?.length || 0

	const setRows = (rows: number) => {
		setCells(Array.from({ length: rows }).map(() => (
			Array.from({ length: cols }).map(() => (
				initialCellState
			))
		)))
	}

	const setCols = (cols: number) => {
		setCells(Array.from({ length: rows }).map(() => (
			Array.from({ length: cols }).map(() => (
				initialCellState
			))
		)))
	}

	const setCell = (row: number, col: number, newState: Partial<CellContextType>) => {
		const clonedState = structuredClone(cells)
		const oldState = clonedState[row][col]
		clonedState[row][col] = { ...oldState, ...newState }
		setCells(clonedState)
	}

	return (
		<BoardContext.Provider value={{ cells, rows, cols, setCell, setRows, setCols }}>
			{children}
		</BoardContext.Provider>
	)
}
