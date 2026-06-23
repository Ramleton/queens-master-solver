import { useMutation } from '@tanstack/react-query'
import React, { useMemo, useState } from 'react'
import { solve } from './api/board'
import './App.css'
import Cell from './components/Cell'
import { useBoardContext } from './context/BoardContext'
import { useReplay } from './hooks/useReplay'
import type { GridState } from './types/boardTypes'
import { parseReplayMessage } from './utils/appUtils'

const COLOURS = [
	'#c2658b',
	'#6082b5',
	'#acd995',
	'#a7bed9',
	'#47b3b0',
	'#67bce6',
	'#9178d0',
	'#e6a8c0',
	'#e2ba45'
] as const

function App() {
	const [changeColour, setChangeColour] = useState<string | null>(null)
	const [steps, setSteps] = useState<GridState[]>([])
	const [solveError, setSolveError] = useState<string | null>(null)
	const [isTransitioning, setIsTransitioning] = useState<boolean>(false)
	const { rows, cols, cells, setRows, setCols, setCells } = useBoardContext()
	const {
		isReplaying,
		currStepIndex,
		startReplay,
		pauseReplay,
		cancelReplay,
		setCurrStepIndex
	} = useReplay(steps, setCells)

	const parsedSteps = useMemo(() => {
		return steps.map(step => parseReplayMessage(step.message))
	}, [steps])

	const solveMutation = useMutation({
		mutationFn: async () => await solve(rows, cols, cells),
		onSuccess: response => {
			setChangeColour(null)
			const lastStep = response.pop()
			if (!lastStep) return
			setCells(lastStep.grid)
			response.push(lastStep)
			setSteps(response)
		},
		onError: (error: Error) => {
			setSolveError(error.message)
		}
	})

	const handleDecrement = (arrangement: 'row' | 'col') => {
		if (arrangement === 'row' && rows <= 4) return
		if (arrangement === 'col' && cols <= 4) return
		setSteps([])
		setCurrStepIndex(-1)
		if (arrangement === 'row')
			setRows(rows - 1)
		if (arrangement === 'col')
			setCols(cols - 1)
	}

	const handleIncrement = (arrangement: 'row' | 'col') => {
		if (arrangement === 'row' && rows >= 9) return
		if (arrangement === 'col' && cols >= 9) return
		setSteps([])
		setCurrStepIndex(-1)
		if (arrangement === 'row')
			setRows(rows + 1)
		if (arrangement === 'col')
			setCols(cols + 1)
	}

	const handleClickColourCell = (colour: string) => {
		setChangeColour(prevColour => (prevColour === colour ? null : colour))
	}

	const handleClear = () => {
		setChangeColour(null)
		setCells(
			Array.from({ length: rows }).map(() =>
				Array.from({ length: cols }).map(() => ({
					colour: '#a7bed9',
					state: 'empty'
				}))
			)
		)
		cancelReplay()
		setSteps([])
		setSolveError(null)
	}

	const handleEmpty = () => {
		setChangeColour(null)
		setCells(
			cells.map(row => row.map(cell => ({ ...cell, state: 'empty' })))
		)
		cancelReplay()
		setSteps([])
	}

	const handleReplay = () => {
		setIsTransitioning(true)
		setTimeout(() => {
			setChangeColour(null)
			setCells(cells.map(row => row.map(cell => ({ ...cell, state: 'empty' }))))
			startReplay()
			setIsTransitioning(false)
		}, 300)
	}

	const handleSolve = () => {
		setSolveError(null)
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
			<div className='app-header'>
				<a href='https://ishaansaini.dev' className='back-link'>
					← ishaansaini.dev
				</a>
				<h1>Queens Master Solver</h1>
				<p className='app-subtitle'>
					Enter your board, pick region colours, then hit Solve.
				</p>
			</div>
			<div className='grid-size-inputs'>
				<label htmlFor='rows'>Rows</label>
				<div id='rows' className='stepper'>
					<button type='button' onPointerDown={() => handleDecrement('row')}>−</button>
					<span className='stepper-value'>{rows}</span>
					<button type='button' onPointerDown={() => handleIncrement('row')}>+</button>
				</div>
				<label htmlFor='cols'>Columns</label>
				<div id='cols' className='stepper'>
					<button type='button' onPointerDown={() => handleDecrement('col')}>−</button>
					<span className='stepper-value'>{cols}</span>
					<button type='button' onPointerDown={() => handleIncrement('col')}>+</button>
				</div>
				<button
					className='empty-button'
					type='button'
					onClick={() => handleEmpty()}
				>
					Empty
				</button>
				<button
					className='clear-button'
					type='button'
					onClick={() => handleClear()}
				>
					Clear
				</button>
			</div>
			{solveError && <p className='error-message'>{solveError}</p>}
			<div
				className='grid-container grid'
				style={
					{
						'--row': rows,
						'--col': cols
					} as React.CSSProperties
				}
			>
				{Array.from({ length: rows }).map((_, row) =>
					Array.from({ length: cols }).map((_, col) => (
						<Cell
							key={`${row}-${col}`}
							row={row}
							col={col}
							changeColour={changeColour}
						/>
					))
				)}
			</div>
			<div className='colours-container'>
				<h2>Colours</h2>
				<div className='colours-flex'>
					{COLOURS.map((colour, index) => (
						// eslint-disable-next-line jsx-a11y/click-events-have-key-events, jsx-a11y/no-static-element-interactions
						<div
							key={index}
							className={`colour-cell ${changeColour === colour ? 'selected' : ''} square`}
							style={
								{
									'--colour': colour
								} as React.CSSProperties
							}
							onClick={() => handleClickColourCell(colour)}
						/>
					))}
				</div>
			</div>
			<div className={`solve-container ${isTransitioning} ? 'fading' : ''`}>
				<button
					className='solve-button'
					type='button'
					onClick={handleSolve}
					disabled={solveMutation.isPending || steps.length > 0}
				>
					{solveMutation.isPending ? 'Solving...' : 'Solve'}
				</button>
				{solveMutation.isPending && (
					<p className='loading-message'>
						Crunching the board — this may take a moment...
					</p>
				)}
				{steps.length > 0 && (
					<button
						className='replay-button'
						type='button'
						onClick={handleReplay}
						disabled={isTransitioning}
					>
						{(currStepIndex >= 0 ? 'Restart ' : '') + 'Replay'}
					</button>
				)}
				{currStepIndex >= 0 && currStepIndex < steps.length && (
					<button
						className='pause-replay-button'
						type='button'
						onClick={pauseReplay}
					>
						{isReplaying ? 'Pause Replay' : 'Resume Replay'}
					</button>
				)}
				{currStepIndex >= 0 && currStepIndex < steps.length && (
					<button
						className='cancel-replay-button'
						type='button'
						onClick={cancelReplay}
					>
						Cancel Replay
					</button>
				)}
			</div>
			{currStepIndex >= 0 && (
				<p className='replay-message'>{replayStepMessage()}</p>
			)}
		</div>
	)
}

export default App
