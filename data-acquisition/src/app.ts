require("dotenv").config();

import BillboardScraper = require('billboard-top-100');
import Track from './interfaces/Track';
import SpotifyApi from './SpotifyApi';

const BILLBOARD_OUTPUT_FILENAME = (startDate:string, endDate:string) => `billboard-${startDate}-${endDate}.csv`;
const SPOTIFY_SONG_DATA_FILENAME = `spotify.csv`;

testToken();

async function testToken() {
    const token = await SpotifyApi.getOAuth2Token(
        process.env.SPOTIFY_CLIENT_ID, process.env.SPOTIFY_CLIENT_SECRET
    );

    console.log(token);
    // console.log();

    // const trackInfo: Track = await SpotifyApi.searchTrack('Time Is Running Out', 'Muse', token);
    // const trackFeatures = await SpotifyApi.getTrackAudioFeatures(trackInfo.spotifyId, token);
    // console.log(trackInfo);
    // console.log(trackFeatures);

    BillboardScraper.getChart('hot-100', '2016-01-01', (err, chart) => {
        if(err) {
            console.error(err);
            return;
        }

        chart.songs.forEach(async song => {
            console.log(`${song.title} :: ${song.artist}`);
            const trackInfo: Track = await SpotifyApi.searchTrack(song.title, song.artist, token);
            const trackFeatures = await SpotifyApi.getTrackAudioFeatures(trackInfo.spotifyId, token);
            console.log(trackInfo);
            console.log(trackFeatures);
            console.log();
        });
    });

}

/* BillboardScraper.getChart('hot-100', '2016-08-27', (err, chart) => {
    const tracks: Track[] = [];

    if(err)
        console.error(err);

    chart.songs.forEach(song => {
        tracks.push({
            song: song.title,
            artist: song.artist
        });
    });

    console.log(tracks);
});*/