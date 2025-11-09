import { useMutation } from '@tanstack/react-query'
import React, { useEffect, useMemo, useState } from 'react'
import { solve } from './api/board'
import './App.css'
import Cell from './components/Cell'
import { useBoardContext } from './context/BoardContext'
import type { GridState } from './types/boardTypes'
import { parseReplayMessage } from './utils/appUtils'

const COLOURS = ['#c2658b', '#6082b5', '#acd995', '#a7bed9', '#47b3b0', '#67bce6', '#9178d0', '#e6a8c0', '#e2ba45'] as const

function App() {
	const [changeColour, setChangeColour] = useState<string | null>(null)
	const [isReplaying, setIsReplaying] = useState<boolean>(false)
	const [currStepIndex, setCurrStepIndex] = useState<number>(-1)
	const [steps, setSteps] = useState<GridState[]>([])
	const { rows, cols, cells, setRows, setCols, setCells } = useBoardContext()

	const parsedSteps = useMemo(() => {
		return steps.map(step => parseReplayMessage(step.message))
	}, [steps])

	useEffect(() => {
		if (!isReplaying) return
		if (currStepIndex >= steps.length) {
			setIsReplaying(false)
			return
		}

		setCells(steps[currStepIndex].grid)

		const timeout = setTimeout(() => {
			setCurrStepIndex(i => i + 1)
		}, 1000)

		return () => clearTimeout(timeout)
	}, [isReplaying, currStepIndex, steps, setCells])

	const solveMutation = useMutation({
		mutationFn: async () => await solve(rows, cols, cells),
		onSuccess: response => {
			setChangeColour(null)
			const lastStep = response.pop()
			if (!lastStep) return
			setCells(lastStep.grid)
			response.push(lastStep)
			setSteps(response)
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
		setIsReplaying(false)
		setSteps([])
		setCurrStepIndex(-1)
	}

	const handleEmpty = () => {
		setChangeColour(null)
		setCells(cells.map(row => row.map(
			cell => ({ ...cell, state: 'empty' })
		)))
		setIsReplaying(false)
		setCurrStepIndex(-1)
		setSteps([])
	}

	const handleReplay = () => {
		setChangeColour(null)
		setCells(cells.map(row => row.map(
			cell => ({ ...cell, state: 'empty' })
		)))
		setCurrStepIndex(0)
		setIsReplaying(true)
	}

	const handleCancelReplay = () => {
		setIsReplaying(false)
		setCurrStepIndex(-1)
	}

	const handlePauseReplay = () => {
		setIsReplaying(!isReplaying)
	}

	const handleSolve = () => {
		solveMutation.mutate()
	}

	const replayStepMessage = () => {
		if (currStepIndex >= steps.length) return 'Done!'

		const { message, colours } = parsedSteps[currStepIndex]

		return (
			<span className='replay-message'>
				{`Step ${currStepIndex + 1}: ${message}`}
				{colours.length > 0 && (
					<span className='colour-list'>
						{colours.map(colour => (
							<span
								key={colour}
								className='colour-circle'
								style={{ backgroundColor: colour }}
							/>
						))}
					</span>
				)}
			</span>
		)
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
						if (!parsedValue) return
						setSteps([])
						setCurrStepIndex(-1)
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
						if (!parsedValue) return
						setSteps([])
						setCurrStepIndex(-1)
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
			<div className='solve-container'>
				<button
					className='solve-button'
					type='button'
					onClick={handleSolve}
					disabled={solveMutation.isPending || steps.length > 0}
				>Solve
				</button>
				{steps.length > 0 && (
					<button
						className='replay-button'
						type='button'
						onClick={handleReplay}
					>
						{(currStepIndex > 0 ? 'Restart ' : '') + 'Replay'}
					</button>
				)}
				{currStepIndex >= 0 && currStepIndex < steps.length && (
					<button
						className='pause-replay-button'
						type='button'
						onClick={handlePauseReplay}
					>
						{isReplaying ? 'Pause Replay' : 'Resume Replay'}
					</button>
				)}
				{currStepIndex >= 0 && currStepIndex < steps.length && (
					<button
						className='cancel-replay-button'
						type='button'
						onClick={handleCancelReplay}
						disabled={!isReplaying}
					>
						Cancel Replay
					</button>
				)}
			</div>
			{currStepIndex >= 0 && <p className='replay-message'>{replayStepMessage()}</p>}
		</div>
	)
}

export default App
