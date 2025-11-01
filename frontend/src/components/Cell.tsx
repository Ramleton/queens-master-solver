import { useBoardContext } from '../BoardContext'

interface CellProps {
	row: number
	col: number
	changeColour: string | null
}

function Cell({ row, col, changeColour }: CellProps) {
	const { setCell, cells } = useBoardContext()

	const handleClickCell = () => {
		console.log('Cell clicked at:', row, col)

		if (changeColour) {
			setCell(row, col, { colour: changeColour })
		} else {
			switch (cells[row][col].state) {
				case 'empty':
					setCell(row, col, { state: 'marked' })
					break
				case 'marked':
					setCell(row, col, { state: 'queen' })
					break
				case 'queen':
					setCell(row, col, { state: 'empty' })
					break
				default:
					break
			}
		}
	}

	return (
		// eslint-disable-next-line jsx-a11y/click-events-have-key-events, jsx-a11y/no-static-element-interactions
		<div
			onClick={() => handleClickCell()}
			className='grid-cell square'
			style={{
				'--colour': cells[row][col].colour
			} as React.CSSProperties}
		>
			{cells[row][col].state === 'marked' && <img className='cell-image' src='./marked.png' alt='marked' />}
			{cells[row][col].state === 'queen' && <img className='cell-image' src='./queen.png' alt='queen' />}
		</div>
	)
}

export default Cell
