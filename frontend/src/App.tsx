import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import React, { useState } from 'react'
import { createBoard, getBoard, solve } from './api/board'
import './App.css'
import Cell from './components/Cell'
import { useBoardContext } from './context/BoardContext'

const COLOURS = ['#c2658b', '#6082b5', '#acd995', '#a7bed9', '#47b3b0', '#67bce6', '#9178d0', '#e6a8c0', '#e2ba45', 'white'] as const

function App() {
	const [changeColour, setChangeColour] = useState<string | null>(null)
	const { rows, cols, setRows, setCols } = useBoardContext()

	const queryClient = useQueryClient()

	const { data, status, isFetching } = useQuery({
		queryKey: ['board'],
		queryFn: getBoard
	})

	const solveMutation = useMutation({
		mutationFn: solve,
		onSuccess: async () => {
			await queryClient.invalidateQueries({ queryKey: ['board'] })
			console.log('Solved!')
			setChangeColour(null)
		}
	})

	const createMutation = useMutation({
		mutationFn: ({ rows, cols }: { rows: number, cols: number }) => createBoard(rows, cols),
		onSuccess: async () => {
			await queryClient.invalidateQueries({ queryKey: ['board'] })
		}
	})

	const handleClickColourCell = (colour: string) => {
		setChangeColour(prevColour => prevColour === colour ? null : colour)
	}

	const handleSolve = () => {
		solveMutation.mutate()
	}

	if (status === 'pending') {
		return <p>Loading...</p>
	}

	if (status === 'error') {
		return <p>Error loading board</p>
	}

	return (
		<>
			<h1>Queens Master Solver</h1>
			<input
				type='number'
				value={rows}
				onChange={e => {
					createMutation.mutate({ rows: parseInt(e.target.value), cols })
					setRows(parseInt(e.target.value))
				}}
				min={1}
				max={10}
			/>
			<input
				type='number'
				value={cols}
				onChange={e => {
					createMutation.mutate({ rows, cols: parseInt(e.target.value) })
					setCols(parseInt(e.target.value))
				}}
				min={1}
				max={10}
			/>
			<div
				className='grid'
				style={{
					'--row': rows,
					'--col': cols
				} as React.CSSProperties}
			>
				{
					Array.from({ length: rows }).map((_, row) => (
						Array.from({ length: cols }).map((_, col) => (
							<Cell
								key={`${row}-${col}`}
								row={row}
								col={col}
								changeColour={changeColour}
							/>
						))
					))
				}
			</div>
			<h2>Colours</h2>
			<div className='colours-flex'>
				{COLOURS.map((colour, index) => (
					// eslint-disable-next-line jsx-a11y/click-events-have-key-events, jsx-a11y/no-static-element-interactions
					<div
						key={index}
						className={`colour-cell square ${changeColour === colour ? 'selected' : ''}`}
						style={{
							'--colour': colour
						} as React.CSSProperties}
						onClick={() => handleClickColourCell(colour)}
					/>
				))}
			</div>
			<button type='button' onClick={handleSolve}>Solve</button>

			{ isFetching && <p>Refreshing the board...</p>}
		</>
	)
}

export default App
