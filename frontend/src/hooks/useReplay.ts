import { useCallback, useEffect, useState } from 'react'
import type { GridState } from '../types/boardTypes'

export function useReplay(steps: GridState[], setCells: (grid: GridState['grid']) => void) {
	const [isReplaying, setIsReplaying] = useState<boolean>(false)
	const [currStepIndex, setCurrStepIndex] = useState<number>(-1)

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

	const startReplay = useCallback(() => {
		setCurrStepIndex(0)
		setIsReplaying(true)
	}, [])

	const pauseReplay = useCallback(() => {
		setIsReplaying(prev => !prev)
	}, [])

	const cancelReplay = useCallback(() => {
		setIsReplaying(false)
		setCurrStepIndex(-1)
	}, [])

	return {
		isReplaying,
		currStepIndex,
		startReplay,
		pauseReplay,
		cancelReplay,
		setCurrStepIndex
	}
}
