import moment = require('moment');

export default interface LeaderboardInstance {
    spotifyId: string
    weekOf: moment.Moment
    position: number
    changeSinceLastWeek: number
    weeksOnChart: number
}