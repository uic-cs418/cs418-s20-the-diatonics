import request = require('request');
import Track from './interfaces/Track';

export default class SpotifyApi {
  static async getTrackAudioFeatures(trackId: string, token: string): Promise<Object> {
    const rawApiData = await SpotifyApi.makeAuthenticatedGetRequest(
      `https://api.spotify.com/v1/audio-features/${trackId}`,
      token
    );
    return rawApiData;
  }

  static async searchTrack(trackTitle: string, trackArtist: string, token: string): Promise<Track> {
    const results = await SpotifyApi.searchTrackHelper(
      `https://api.spotify.com/v1/search?q=${trackTitle}&type=track&market=US&offset=0&limit=50`,
      token
    );

    const result = results.find(item => (
      item.name === trackTitle &&
      item.artists.some(artist => artist.name === trackArtist)
    ));

    return {
      spotifyId: result.id,
      title: result.name,
      artist: trackArtist
    }
  }

  private static async searchTrackHelper(nextUrl: string, token: string): Promise<any[]> {
    if(nextUrl === null)
      return [];

    const rawApiData = await SpotifyApi.makeAuthenticatedGetRequest(nextUrl, token);
    const restRawApiData = await SpotifyApi.searchTrackHelper(
      rawApiData.tracks.next,
      token
    );

    return rawApiData.tracks.items.concat(restRawApiData);
  }

  /**
   * Obtains an OAuth 2.0 token from Spotify
   * Adapted from https://github.com/spotify/web-api-auth-examples/blob/master/client_credentials/app.js
   * @param clientId - Client ID provided by Spotify
   * @param clientSecret - Client secret provided by Spotify
   */
  static getOAuth2Token(clientId: string, clientSecret: string): Promise<string> {
    const authOptions = {
      url: 'https://accounts.spotify.com/api/token',
      headers: {
        'Authorization': 'Basic ' + (Buffer.from(clientId + ':' + clientSecret).toString('base64'))
      },
      form: { grant_type: 'client_credentials' },
      json: true
    };

    return new Promise((resolve, reject) => {
      request.post(authOptions, (error, response, body) => {
        if(error)
          reject(error);
        
        if(response.statusCode !== 200)
          reject(response.statusCode);

        resolve(body.access_token);
      });
    });
  }

  /**
   * 
   * @param url 
   * @param oauthToken 
   * @param body 
   */
  private static makeAuthenticatedGetRequest(url: string, oauthToken: string, body?: Object): Promise<any> {
    const options = {
      url,
      headers: { 'Authorization': `Bearer ${oauthToken}` },
      json: true
    };

    return new Promise((resolve, reject) => {
      request.get(options, (error, response, body) => {
        if(error)
          reject(error);
      
        if(response.statusCode !== 200)
          reject(response.statusCode);

        resolve(response.body);
      });
    });
  }

}