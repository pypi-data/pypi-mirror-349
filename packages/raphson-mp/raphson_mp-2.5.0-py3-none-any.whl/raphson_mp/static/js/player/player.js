import { eventBus, MusicEvent } from "./event.js";
import { trackDisplayHtml } from "./track.js";
import { queue } from "./queue.js";
import { DownloadedTrack, music } from "../api.js";
import { durationToString, vars } from "../util.js";
import { windows } from "./window.js";
import { editor } from "./editor.js";
import { PlaylistCheckboxes } from "../playlistcheckboxes.js";

export const audioElement = /** @type {HTMLAudioElement} */ (document.getElementById("audio"));

class Player {
    constructor() {
        audioElement.addEventListener('ended', () => queue.next());

        // Audio element should always be playing at max volume
        // Volume is set using GainNode in audio.js
        audioElement.volume = 1;

        eventBus.subscribe(MusicEvent.TRACK_CHANGE, track => {
            this.#replaceAudioSource(track);
            this.#replaceAlbumImages(track);
            this.#replaceTrackDisplayTitle(track);
        });

        eventBus.subscribe(MusicEvent.METADATA_CHANGE, updatedTrack => {
            if (queue.currentTrack
                && queue.currentTrack.track
                && queue.currentTrack.track.path
                && queue.currentTrack.track.path == updatedTrack.path) {
                console.debug('player: updating currently playing track following METADATA_CHANGE event');
                queue.currentTrack.track = updatedTrack;
                this.#replaceTrackDisplayTitle(queue.currentTrack);
            }
        });
    }

    /**
     * @param {number} currentTime
     */
    seek(currentTime) {
        audioElement.currentTime = currentTime;
        playerControls.updateSeekBarImmediately();
    }

    /**
     * @param {number} delta number of seconds to seek forwards, negative for backwards
     * @returns {void}
     */
    seekRelative(delta) {
        const newTime = audioElement.currentTime + delta;
        if (newTime < 0) {
            this.seek(0);
        } else if (newTime > audioElement.duration) {
            this.seek(audioElement.duration);
        } else {
            this.seek(newTime);
        }
    }

    /**
     * @param {DownloadedTrack} track
     * @returns {Promise<void>}
     */
    async #replaceAudioSource(track) {
        audioElement.src = track.audioUrl;
        try {
            await audioElement.play();
        } catch (exception) {
            console.warn('player: failed to start playback: ', exception);
        }
    }

    /**
     * @param {DownloadedTrack} track
     * @returns {void}
     */
    #replaceAlbumImages(track) {
        const cssUrl = `url("${track.imageUrl}")`;

        const bgBottom = /** @type {HTMLDivElement} */ (document.getElementById('bg-image-1'));
        const bgTop = /** @type {HTMLDivElement} */ (document.getElementById('bg-image-2'));
        const fgBottom = /** @type {HTMLDivElement} */ (document.getElementById('album-cover-1'));
        const fgTop = /** @type {HTMLDivElement} */ (document.getElementById('album-cover-2'));

        // Set bottom to new image
        bgBottom.style.backgroundImage = cssUrl;
        fgBottom.style.backgroundImage = cssUrl;

        // Slowly fade out old top image
        bgTop.style.opacity = '0';
        fgTop.style.opacity = '0';

        setTimeout(() => {
            // To prepare for next replacement, move bottom image to top image
            bgTop.style.backgroundImage = cssUrl;
            fgTop.style.backgroundImage = cssUrl;
            // Make it visible
            bgTop.style.opacity = '1';
            fgTop.style.opacity = '1';
        }, 200);
    }

    /**
     * @param {DownloadedTrack} track
     * @returns {void}
     */
    #replaceTrackDisplayTitle(track) {
        const currentTrackElem = /** @type {HTMLSpanElement} */ (document.getElementById('current-track'));
        currentTrackElem.replaceChildren(trackDisplayHtml(track.track, true));
        if (track.track !== null) {
            document.title = track.track.displayText(true, true);
        } else {
            document.title = '[track info unavailable]';
        }
    }
}

export const player = new Player();

class PlayerControls {
    #seekBar = /** @type {HTMLDivElement} */ (document.getElementById('seek-bar'));
    #seekBarInner = /** @type {HTMLDivElement} */ (document.getElementById('seek-bar-inner'));
    #textPosition = /** @type {HTMLDivElement} */ (document.getElementById('seek-bar-text-position'));
    #textDuration = /** @type {HTMLDivElement} */ (document.getElementById('seek-bar-text-duration'));
    #seekBarTimer = /** @type {number | null} */ (null);

    constructor() {
        this.#initSeekBar();
        this.#initHomeButton();
        this.#initSkipButtons();
        this.#initPlayPauseButtons();
        if (!vars.offlineMode) {
            this.#initFileActionButtons();
            this.#initWebButton();
        };
    }

    #updateSeekBarSlowly() {
        if (audioElement.paused) return;
        // animation raises total CPU usage of the music player by 7x, not worth it
        // this.#seekBarInner.style.transition = 'width 1s linear'; // slow transition, matching throttle time
        this.#updateSeekBar();
    }

    updateSeekBarImmediately() {
        // this.#seekBarInner.style.transition = 'width .05s linear'; // very fast transition
        this.#updateSeekBar();
    }

    #updateSeekBar() {
        // Save resources updating seek bar if it's not visible
        if (document.visibilityState != 'visible') {
            return;
        }

        let barCurrent;
        let barDuration;
        let barWidth;

        if (isFinite(audioElement.currentTime) && isFinite(audioElement.duration)) {
            barCurrent = durationToString(Math.round(audioElement.currentTime));
            barDuration = durationToString(Math.round(audioElement.duration));
            barWidth = ((audioElement.currentTime / audioElement.duration) * 100) + '%';
        } else {
            barCurrent = '--:--';
            barDuration = '--:--';
            barWidth = 0 + '';
        }

        this.#textPosition.textContent = barCurrent;
        this.#textDuration.textContent = barDuration;
        this.#seekBarInner.style.width = barWidth;
    }

    #initSeekBar() {
        const onMove = event => {
            const newTime = ((event.clientX - this.#seekBar.offsetLeft) / this.#seekBar.offsetWidth) * audioElement.duration;
            player.seek(newTime);
            event.preventDefault(); // Prevent accidental text selection
        };

        const onUp = () => {
            document.removeEventListener('mousemove', onMove);
            document.removeEventListener('mouseup', onUp);
        };

        this.#seekBar.addEventListener('mousedown', event => {
            const newTime = ((event.clientX - this.#seekBar.offsetLeft) / this.#seekBar.offsetWidth) * audioElement.duration;
            player.seek(newTime);

            // Keep updating while mouse is moving
            document.addEventListener('mousemove', onMove);

            // Unregister events on mouseup event
            document.addEventListener('mouseup', onUp);

            event.preventDefault(); // Prevent accidental text selection
        });

        // Scroll to seek
        this.#seekBar.addEventListener('wheel', event => {
            player.seekRelative(event.deltaY < 0 ? 3 : -3);
        }, { passive: true });

        audioElement.addEventListener('durationchange', () => this.updateSeekBarImmediately());

        // Seek bar is not updated when page is not visible. Immediately update it when the page does become visibile.
        document.addEventListener('visibilitychange', () => {
            this.updateSeekBarImmediately();
            if (document.visibilityState == 'visible' && !this.#seekBarTimer) {
                console.debug('player: start seek bar timer');
                this.#seekBarTimer = setInterval(() => this.#updateSeekBarSlowly(), 1000);
            } else if (document.visibilityState == 'hidden' && this.#seekBarTimer) {
                console.debug('player: cancel seek bar timer');
                clearInterval(this.#seekBarTimer);
                this.#seekBarTimer = null;
            }
        });

        // Updating the width of an element is quite expensive
        // Only update seek bar every second, with an animation so it seems smooth
        this.#seekBarTimer = setInterval(() => this.#updateSeekBarSlowly(), 1000);
    }

    #initHomeButton() {
        const homeButton = /** @type {HTMLButtonElement} */ (document.getElementById('button-home'));
        homeButton.addEventListener('click', () => window.open('/', '_blank'));
    }

    #initSkipButtons() {
        const prevButton = /** @type {HTMLButtonElement} */ (document.getElementById('button-prev'));
        const nextButton = /** @type {HTMLButtonElement} */ (document.getElementById('button-next'));
        prevButton.addEventListener('click', () => queue.previous());
        nextButton.addEventListener('click', () => queue.next());
    }

    #initPlayPauseButtons() {
        const pauseButton = /** @type {HTMLButtonElement} */ (document.getElementById('button-pause'));
        const playButton = /** @type {HTMLButtonElement} */ (document.getElementById('button-play'));

        // Play pause click actions
        pauseButton.addEventListener('click', () => audioElement.pause());
        playButton.addEventListener('click', () => audioElement.play());

        const updateButtons = () => {
            pauseButton.hidden = audioElement.paused;
            playButton.hidden = !audioElement.paused;
        };

        audioElement.addEventListener('pause', updateButtons);
        audioElement.addEventListener('play', updateButtons);

        // Hide pause button on initial page load, otherwise both play and pause will show
        pauseButton.hidden = true;
    }

    /**
     * Handle presence of buttons that perform file actions: dislike, copy, share, edit, delete
     */
    #initFileActionButtons() {
        const dislikeButton = /** @type {HTMLButtonElement} */ (document.getElementById('button-dislike'));
        const copyButton = /** @type {HTMLButtonElement} */ (document.getElementById('button-copy'));
        const shareButton = /** @type {HTMLButtonElement} */ (document.getElementById('button-share'));
        const editButton = /** @type {HTMLButtonElement} */ (document.getElementById('button-edit'));
        const deleteButton = /** @type {HTMLButtonElement} */ (document.getElementById('button-delete'));

        const requiresRealTrack = [dislikeButton, copyButton, shareButton];
        const requiresWriteAccess = [editButton, deleteButton];

        async function updateButtons() {
            const isRealTrack = queue.currentTrack && queue.currentTrack.track;
            for (const button of requiresRealTrack) {
                button.hidden = !isRealTrack;
            }

            const hasWriteAccess = isRealTrack && (await music.playlist(/** @type {string} */(queue?.currentTrack?.track?.playlistName))).write;
            for (const button of requiresWriteAccess) {
                button.hidden = !hasWriteAccess;
            }
        }

        updateButtons();
        eventBus.subscribe(MusicEvent.TRACK_CHANGE, updateButtons);

        // Dislike button
        dislikeButton.addEventListener('click', async () => {
            if (queue.currentTrack && queue.currentTrack.track) {
                await queue.currentTrack.track.dislike();
                queue.next();
            } else {
                throw new Error();
            }
        });

        // Copy button
        const copyTrack = /** @type {HTMLButtonElement} */ (document.getElementById('copy-track'));
        const copyPlaylist = /** @type {HTMLSelectElement} */ (document.getElementById('copy-playlist'));
        const copyDoButton = /** @type {HTMLButtonElement} */ (document.getElementById('copy-do-button'));
        copyButton.addEventListener('click', () => {
            if (!queue.currentTrack || !queue.currentTrack.track) {
                throw new Error();
            }
            copyTrack.value = queue.currentTrack.track.path;
            windows.open('window-copy');
        });
        copyDoButton.addEventListener('click', async () => {
            if (!queue.currentTrack || !queue.currentTrack.track) {
                throw new Error();
            }
            copyDoButton.disabled = true;
            try {
                await queue.currentTrack.track.copyTo(copyPlaylist.value);
            } catch (err) {
                console.error(err);
                alert('Error: ' + err);
            }
            windows.close('window-copy');
            copyDoButton.disabled = false;
        });

        // Share button is handled by share.js

        // Edit button
        editButton.addEventListener('click', () => {
            if (queue.currentTrack && queue.currentTrack.track) {
                editor.open(queue.currentTrack.track);
            }
        });

        // Delete button
        const deleteSpinner = /** @type {HTMLDivElement} */ (document.getElementById('delete-spinner'));
        deleteButton.addEventListener('click', async () => {
            if (!queue.currentTrack || !queue.currentTrack.track) {
                return;
            }
            deleteSpinner.hidden = false;
            await queue.currentTrack.track.delete();
            queue.next();
            deleteSpinner.hidden = true;
        });
    }

    #initWebButton() {
        const addButton = /** @type {HTMLButtonElement} */ (document.getElementById('online-add'));
        const urlInput = /** @type {HTMLInputElement} */ (document.getElementById('online-url'));

        addButton.addEventListener('click', async () => {
            windows.close('window-online');
            const track = await music.downloadTrackFromWeb(urlInput.value);
            queue.add(track, true);
        });
    }
}

export const playerControls = new PlayerControls();

/**
 * @returns {Promise<void>}
 */
async function updatePlaylistDropdowns() {
    console.debug('playlist: updating dropdowns');

    const playlists = await music.playlists();

    const selects = /** @type {HTMLCollectionOf<HTMLSelectElement>} */ (document.getElementsByClassName('playlist-select'));
    for (const select of selects) {
        const previouslySelectedValue = select.value;

        // Remove all children except the ones that should be kept
        const keptChildren = [];
        for (const child of select.children) {
            if (child instanceof HTMLElement && child.dataset.keep === 'true') {
                keptChildren.push(child);
                continue;
            }
        }
        select.replaceChildren(...keptChildren);

        const primaryPlaylist = /** @type {HTMLDivElement} */ (document.getElementById('primary-playlist')).textContent;
        const onlyWritable = select.classList.contains('playlist-select-writable');

        for (const playlist of playlists) {
            const option = document.createElement('option');
            option.value = playlist.name;
            option.textContent = playlist.name;
            option.disabled = onlyWritable && !playlist.write;
            select.appendChild(option);
        }

        // After all options have been replaced, the previously selected option should be restored
        if (previouslySelectedValue) {
            select.value = previouslySelectedValue;
        } else if (primaryPlaylist) {
            select.value = primaryPlaylist;
        }
    }
}

updatePlaylistDropdowns();

const checkboxesParent = /** @type {HTMLDivElement} */ (document.getElementById('playlist-checkboxes'));
const onPlaylistChange = () => eventBus.publish(MusicEvent.PLAYLIST_CHANGE);
new PlaylistCheckboxes(checkboxesParent, onPlaylistChange).createPlaylistCheckboxes();
