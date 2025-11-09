import type { ParsedReplayMessage } from '../types/appTypes'

export function parseReplayMessage(raw: string): ParsedReplayMessage {
	if (raw.includes('[')) {
		const [text, colourPart] = raw.split('[')
		const colours = colourPart
			.replace(']', '')
			.replaceAll('\'', '')
			.split(',')
			.map(s => s.trim())
		const singular = text.replaceAll('(s)', '')
		const plural = text.replaceAll('(s)', 's')
		const message = colours.length === 1 ? singular : plural

		return { message, colours }
	}

	const match = raw.match(/#([0-9a-f]{6})/i)
	if (match) {
		const colour = `#${match[1]}`
		const message = raw.replace(colour, '').trim()
		return { message, colours: [colour] }
	}

	return {
		message: raw,
		colours: []
	}
}
