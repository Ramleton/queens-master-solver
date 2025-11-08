import { useBoardContext, type CellState } from '../context/BoardContext'
import marked from '/marked.png'
import queen from '/queen_2.png'

interface CellProps {
	row: number
	col: number
	changeColour: string | null
}

function Cell({ row, col, changeColour }: CellProps) {
	const { setCell, cells } = useBoardContext()

	const handleClickCell = () => {
		if (changeColour) {
			// If the new colour is the same as the current, return early
			if (changeColour === cells[row][col].colour) return
			setCell(row, col, { colour: changeColour })
		} else {
			let updatedState: CellState = 'empty'
			switch (cells[row][col].state) {
				case 'empty':
					updatedState = 'marked'
					break
				case 'marked':
					updatedState = 'queen'
					break
				default:
					break
			}
			setCell(row, col, { ...cells[row][col], state: updatedState })
		}
	}

	return (
		// eslint-disable-next-line jsx-a11y/click-events-have-key-events, jsx-a11y/no-static-element-interactions
		<div
			onClick={() => handleClickCell()}
			className='square'
			style={{
				'--colour': cells[row][col].colour
			} as React.CSSProperties}
		>
			{cells[row][col].state === 'marked' && <img className='cell-image marked' src={marked} alt='marked' />}
			{cells[row][col].state === 'queen' && <img className='cell-image queen' src={queen} alt='queen' />}
		</div>
	)
}

export default Cell
