import { useMutation, useQueryClient } from '@tanstack/react-query'
import { updateCell } from '../api/board'
import { useBoardContext, type CellContextType, type CellState } from '../context/BoardContext'

interface CellProps {
	row: number
	col: number
	changeColour: string | null
}

function Cell({ row, col, changeColour }: CellProps) {
	const queryClient = useQueryClient()
	const { setCell, cells } = useBoardContext()

	const updateMutation = useMutation({
		mutationFn: ({ row, col, newState }: { row: number, col: number, newState: Partial<CellContextType> }) => updateCell(row, col, newState),
		onSuccess: async response => {
			console.log(response)
			await queryClient.invalidateQueries({ queryKey: ['board'] })
		}
	})

	const handleClickCell = () => {
		if (changeColour) {
			// If the new colour is the same as the current, return early
			if (changeColour === cells[row][col].colour) return
			setCell(row, col, { colour: changeColour })
			updateMutation.mutate({ row, col, newState: { colour: changeColour } })
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
			updateMutation.mutate({ row, col, newState: { state: updatedState } })
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
			{cells[row][col].state === 'marked' && <img className='cell-image' src='./marked.png' alt='marked' />}
			{cells[row][col].state === 'queen' && <img className='cell-image' src='./queen.png' alt='queen' />}
		</div>
	)
}

export default Cell
