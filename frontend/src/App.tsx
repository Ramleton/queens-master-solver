import React, { useState } from 'react'
import './App.css'
import { useBoardContext } from './BoardContext'
import Cell from './components/Cell'

const COLOURS = ['#c2658b', '#6082b5', '#acd995', '#a7bed9', '#47b3b0', '#67bce6', '#9178d0', '#e6a8c0', '#e2ba45', 'brown'] as const

function App() {
	const [changeColour, setChangeColour] = useState<string | null>(null)
	const { rows, cols, setRows, setCols } = useBoardContext()

	const handleClickColourCell = (colour: string) => {
		setChangeColour(prevColour => prevColour === colour ? null : colour)
	}

	const handleSolve = () => {

	}

	return (
		<>
			<h1>Queens Master Solver</h1>
			<input type='number' value={rows} onChange={e => setRows(parseInt(e.target.value))} min={1} max={10} />
			<input type='number' value={cols} onChange={e => setCols(parseInt(e.target.value))} min={1} max={10} />
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
						className='colour-cell square'
						style={{
							'--colour': colour
						} as React.CSSProperties}
						onClick={() => handleClickColourCell(colour)}
					/>
				))}
			</div>
			<button type='button' onClick={handleSolve}>Solve</button>
		</>
	)
}

export default App
