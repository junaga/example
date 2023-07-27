import { fileURLToPath } from "url"

/**
 * @param {number} max
 * @param {number} [min]
 * @returns {number}
 */
export function rand(max, min = 0) {
	return Math.floor(Math.random() * (max - min + 1) + min)
}

/** @param {number} ms */
export function sleep(ms) {
	return new Promise((resolve) => setTimeout(resolve, ms))
}

export function makeRouletteGame(accountBalance) {
	const account = {
		user: "anon",
		balance: accountBalance
	}

	function rouletteGame(bet, color) {
		if (bet > account.balance || bet <= 0) {
			const msg =
				"Game bet needs to be less than account.balance and greater than 0."
			console.error({ error: msg, accountBalance: account.balance, bet })
			throw new Error(msg)
		}

		account.balance = account.balance - bet

		const turn = {
			color: Math.random() < 0.5 ? "red" : "black"
		}

		if (turn.color === color) {
			account.balance = account.balance + bet * 2
		}

		return turn
	}

	return [rouletteGame, account]
}

function main() {
	const [game, acc] = makeRouletteGame(1_000_000)

	function offset(n) {
		const hdsq = Math.floor(n / 64) // https://www.google.com/search?q=hemidemisemiquaver
		const shifted_down = n - Math.floor(hdsq / 2)
		const randomized = shifted_down + rand(hdsq)
		return randomized
	}

	const play = { bet: null, color: null }
	const history = {
		loseStreak: 0,
		red: 0,
		black: 0
	}

	while (true) {
		// await sleep(rand(1000, 400))

		// calculate a play
		play.bet = history.loseStreak > 0 ? play.bet * 2 : 1
		play.color = history.red < history.black ? "red" : "black"

		// play the game
		const turn = game(play.bet, play.color)

		// log heavy lose streaks
		if (history.loseStreak > 10) {
			console.log(acc.balance, play, history)
		}

		// record the result
		history[turn.color] += 1
		if (play.color === turn.color) history.loseStreak = 0
		else history.loseStreak += 1
	}
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
	main()
}
