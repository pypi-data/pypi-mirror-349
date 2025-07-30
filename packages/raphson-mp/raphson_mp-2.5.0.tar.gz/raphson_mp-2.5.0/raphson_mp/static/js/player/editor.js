import { windows } from "./window.js";
import { eventBus, MusicEvent } from "./event.js";
import { Track } from "../api.js";

class Editor {
    #saveButton = /** @type {HTMLButtonElement} */ (document.getElementById("editor-save"));
    #autoButton = /** @type {HTMLButtonElement} */ (document.getElementById("editor-auto"));
    #autoResultElem = /** @type {HTMLTableElement} */ (document.getElementById("editor-auto-result"));
    #autoResultBodyElem = /** @type {HTMLTableSectionElement} */ (document.getElementById("editor-auto-result-body"));
    #writingElem = /** @type {HTMLParagraphElement} */ (document.getElementById('editor-writing'));
    /** @type {Track | null} */
    #track = null;

    constructor() {
        this.#saveButton.addEventListener('click', () => this.#save());
        this.#autoButton.addEventListener('click', () => this.#auto());
    };

    /**
     * Populate input fields and show metadata editor window
     * @param {Track} track
     */
    open(track) {
        if (track == null) {
            throw new Error('Track is null');
        }
        this.#track = track;
        this.#trackToHtml();

        this.#autoResultElem.hidden = true;
        this.#autoButton.hidden = false;

        // Make editor window window visisble, and bring it to the top
        windows.open('window-editor');
    };

    /**
     * @param {string} id
     * @returns {string | null} Value of HTML input with the given id.
     */
    #getValue(id) {
        let value = /** @type {HTMLInputElement} */ (document.getElementById(id)).value;
        value = value.trim();
        return value === '' ? null : value;
    };

    /**
     * @param {string} id
     * @returns {Array<string>}
     */
    #getArrayValue(id) {
        let value = /** @type {HTMLInputElement} */ (document.getElementById(id)).value;
        const array = [];
        for (const item of value.split(';')) {
            const trimmed = item.trim();
            if (trimmed) {
                array.push(trimmed);
            }
        }
        return array;
    }

    /**
     * @param {string} id
     * @param {string | Array<string> | null} value
     */
    #setValue(id, value) {
        if (value == null) {
            value = '';
        } else if (value instanceof Array) {
            value = value.join('; ');
        }
        /** @type {HTMLInputElement} */ (document.getElementById(id)).value = value;
    }

    /**
     * Copy content from track object variables to HTML input fields
     */
    #trackToHtml() {
        if (!this.#track) {
            throw new Error();
        }
        this.#setValue('editor-path', this.#track.path);
        this.#setValue('editor-title', this.#track.title);
        this.#setValue('editor-album', this.#track.album);
        this.#setValue('editor-artists', this.#track.artists);
        this.#setValue('editor-album-artist', this.#track.albumArtist);
        this.#setValue('editor-tags', this.#track.tags);
        this.#setValue('editor-year', this.#track.year ? this.#track.year + '' : null);
        this.#setValue('editor-lyrics', this.#track.lyrics);
    }

    /**
     * Copy content from input fields to track object
     */
    #htmlToTrack() {
        if (!this.#track) {
            throw new Error();
        }
        this.#track.title = this.#getValue('editor-title');
        this.#track.album = this.#getValue('editor-album');
        this.#track.artists = this.#getArrayValue('editor-artists');
        this.#track.albumArtist = this.#getValue('editor-album-artist');
        this.#track.tags = this.#getArrayValue('editor-tags');
        const yearStr = this.#getValue('editor-year');
        this.#track.year = yearStr ? parseInt(yearStr) : null;
        this.#track.lyrics = this.#getValue('editor-lyrics');
    }

    /**
     * Save metadata and close metadata editor window
     */
    async #save() {
        if (this.#track == null) {
            throw new Error();
        }
        this.#htmlToTrack();

        // Loading text
        this.#saveButton.hidden = true;
        this.#writingElem.hidden = false;

        // Make request to update metadata
        try {
            await this.#track.saveMetadata();
        } catch (e) {
            alert('An error occurred while updating metadata.');
            return;
        } finally {
            this.#writingElem.hidden = true;
            this.#saveButton.hidden = false;
        }

        // Close window, and restore save button
        windows.close('window-editor');

        // Music player should update all track-related HTML with new metadata. This event must be
        // fired after the editor window is closed, so other windows can check whether they are open.
        eventBus.publish(MusicEvent.METADATA_CHANGE, this.#track);

        this.#track = null;
    };

    async #auto() {
        if (!this.#track) {
            throw new Error();
        }

        this.#autoButton.hidden = true;

        try {
            const array = await this.#track.acoustid();

            const rows = [];
            for (const meta of array) {
                const tdTitle = document.createElement('td');
                tdTitle.textContent = meta.title;
                const tdArtist = document.createElement('td');
                tdArtist.textContent = meta.artists.join(', ');
                const tdAlbum = document.createElement('td');
                tdAlbum.textContent = meta.album;
                const tdYear = document.createElement('td');
                tdYear.textContent = meta.year + '';
                const tdType = document.createElement('td');
                tdType.textContent = meta.releaseType;
                const tdPackaging = document.createElement('td');
                tdPackaging.textContent = meta.packaging;
                const row = document.createElement('tr');
                row.append(tdTitle, tdArtist, tdAlbum, tdYear, tdType, tdPackaging);
                rows.push(row);
            }

            this.#autoResultBodyElem.replaceChildren(...rows);
            this.#autoResultElem.hidden = false;
        } catch (ex) {
            alert('Could not fingerprint audio file, maybe it is corrupt?');
            console.warn(ex);
        }
    }

};

export const editor = new Editor();
