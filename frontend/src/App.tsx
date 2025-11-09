import { useMutation } from '@tanstack/react-query'
import React, { useState } from 'react'
import { solve } from './api/board'
import './App.css'
import Cell from './components/Cell'
import { useBoardContext } from './context/BoardContext'

const COLOURS = ['#c2658b', '#6082b5', '#acd995', '#a7bed9', '#47b3b0', '#67bce6', '#9178d0', '#e6a8c0', '#e2ba45'] as const

function App() {
	const [changeColour, setChangeColour] = useState<string | null>(null)
	const { rows, cols, cells, setRows, setCols, setCells } = useBoardContext()

	const solveMutation = useMutation({
		mutationFn: async () => await solve(rows, cols, cells),
		onSuccess: response => {
			setChangeColour(null)
			const lastStep = response.pop()
			if (!lastStep) return
			setCells(lastStep.grid)
			response.push(lastStep)
		}
	})

	const handleClickColourCell = (colour: string) => {
		setChangeColour(prevColour => prevColour === colour ? null : colour)
	}

	const handleClear = () => {
		setChangeColour(null)
		setCells(Array.from({ length: rows })
			.map(() => Array.from({ length: cols })
				.map(() => ({ colour: '#a7bed9', state: 'empty' }))))
	}

	const handleEmpty = () => {
		setChangeColour(null)
		setCells(cells.map(row =>
			row.map(
				cell => ({ ...cell, state: 'empty' })
			)))
	}

	const handleSolve = () => {
		solveMutation.mutate()
	}

	return (
		<div className='app-container'>
			<h1>Queens Master Solver</h1>
			<div className='grid-size-inputs'>
				<label htmlFor='rows'>Rows</label>
				<input
					id='rows'
					type='number'
					className='grid-size-input'
					value={rows}
					onChange={e => {
						const parsedValue = parseInt(e.target.value)
						if (parsedValue)
							setRows(parsedValue)
					}}
					min={4}
					max={9}
				/>
				<label htmlFor='cols'>Columns</label>
				<input
					id='cols'
					type='number'
					className='grid-size-input'
					value={cols}
					onChange={e => {
						const parsedValue = parseInt(e.target.value)
						if (parsedValue)
							setCols(parsedValue)
					}}
					min={4}
					max={9}
				/>
				<button className='empty-button' type='button' onClick={() => handleEmpty()}>Empty</button>
				<button className='clear-button' type='button' onClick={() => handleClear()}>Clear</button>
			</div>
			<div
				className='grid-container grid'
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
			<div className='colours-container'>
				<h2>Colours</h2>
				<div className='colours-flex'>
					{COLOURS.map((colour, index) => (
						// eslint-disable-next-line jsx-a11y/click-events-have-key-events, jsx-a11y/no-static-element-interactions
						<div
							key={index}
							className={`colour-cell ${changeColour === colour ? 'selected' : ''} square`}
							style={{
								'--colour': colour
							} as React.CSSProperties}
							onClick={() => handleClickColourCell(colour)}
						/>
					))}
				</div>
			</div>
			<button className='solve-button' type='button' onClick={handleSolve}>Solve</button>
		</div>
	)
}

export default App
