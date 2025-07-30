import { browse } from "./browse.js";
import { vars } from "../util.js";
import { Track } from "../api.js";

const COLOR_MISSING_METADATA = "#ffc891"
const TRACK_INFO_UNAVAILABLE = document.createElement("span");
TRACK_INFO_UNAVAILABLE.style.color = COLOR_MISSING_METADATA;
TRACK_INFO_UNAVAILABLE.textContent = vars.tTrackInfoUnavailable;

/**
 * Get display HTML for a track
 * @param {Track|null} track
 * @param {boolean} showPlaylist
 * @returns {HTMLSpanElement}
 */
export function trackDisplayHtml(track, showPlaylist = false) {
    if (track == null) {
        return TRACK_INFO_UNAVAILABLE;
    }

    const html = document.createElement('span');
    html.classList.add('track-display-html');

    if (track.artists.length > 0 && track.title) {
        let first = true;
        for (const artist of track.artists) {
            if (first) {
                first = false;
            } else {
                html.append(', ');
            }

            const artistHtml = document.createElement('a');
            artistHtml.textContent = artist;
            artistHtml.addEventListener("click", () => browse.browseArtist(artist));
            html.append(artistHtml);
        }

        html.append(' - ' + track.title);
    } else {
        const span = document.createElement('span');
        span.style.color = COLOR_MISSING_METADATA;
        span.textContent = track.path.substring(track.path.indexOf('/') + 1);
        html.append(span);
    }

    const secondary = document.createElement('span');
    secondary.classList.add('secondary');
    secondary.append(document.createElement('br'));
    html.append(secondary);

    if (showPlaylist) {
        const playlistHtml = document.createElement('a');
        playlistHtml.addEventListener("click", () => browse.browsePlaylist(track.playlistName));
        playlistHtml.textContent = track.playlistName;
        secondary.append(playlistHtml);
    }

    const year = track.year;
    const album = track.album;
    const albumArtist = track.albumArtist;

    if (year || track.album) {
        if (showPlaylist) {
            secondary.append(', ');
        }

        if (album) {
            const albumLink = document.createElement('a');
            albumLink.addEventListener("click", () => browse.browseAlbum(album, albumArtist));
            if (albumArtist) {
                albumLink.textContent = albumArtist + ' - ' + album;
            } else {
                albumLink.textContent = album;
            }
            secondary.append(albumLink);
            if (track.year) {
                secondary.append(', ');
            }
        }

        if (year) {
            const yearLink = document.createElement('a');
            yearLink.textContent = year + '';
            yearLink.addEventListener('click', () => browse.browseYear(year));
            secondary.append(yearLink);
        }
    }

    return html;
};
