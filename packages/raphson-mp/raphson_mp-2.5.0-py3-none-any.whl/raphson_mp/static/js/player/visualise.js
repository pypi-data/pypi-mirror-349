import { audioElement } from "./player.js";
import { eventBus, MusicEvent } from "./event.js";
import { audio } from "./audio.js";

class Visualiser {
    // Settings
    #barWidth = 10;
    #minFreq = 50;
    #maxFreq = 14000;
    #xToFreqExp = 2;

    #dataArray = new Uint8Array(audio.fftSize);
    #canvas = /** @type {HTMLCanvasElement} */ (document.getElementById('visualiser'));
    /** @type {number | null} */
    #taskId = null;

    #checkbox = /** @type {HTMLInputElement} */ (document.getElementById('settings-visualiser'));

    constructor() {
        this.#checkbox.addEventListener('change', () => this.updateVisualiserState());
        audioElement.addEventListener('play', () => this.updateVisualiserState());
        audioElement.addEventListener('pause', () => this.updateVisualiserState());
        document.addEventListener('visibilitychange', () => this.updateVisualiserState());
        eventBus.subscribe(MusicEvent.SETTINGS_LOADED, () => this.updateVisualiserState());
    }

    toggleSetting() {
        this.#checkbox.checked = !this.#checkbox.checked;
        this.updateVisualiserState();
    }

    updateVisualiserState() {
        if (this.#checkbox.checked && !audioElement.paused && document.visibilityState == 'visible') {
            visualiser.#start();
        } else {
            visualiser.#stop();
        }
    }

    #stop() {
        console.debug('visualiser: stopped');
        this.#canvas.style.transform = 'translateY(100%)';
        if (this.#taskId != null) {
            clearInterval(this.#taskId);
        }
        if (this.#taskId != null) {
            cancelAnimationFrame(this.#taskId);
            this.#taskId = null;
        }
    }

    #start() {
        // Prevent double animation in case start() is accidentally called twice
        if (this.#taskId != null) {
            console.warn('visualiser: was already running');
            cancelAnimationFrame(this.#taskId);
        }

        console.debug('visualiser: started');
        this.#canvas.style.transform = '';
        this.#taskId = requestAnimationFrame(() => this.#draw());
    }

    #draw() {
        if (!audio.analyser) {
            return;
        }

        const height = this.#canvas.clientHeight;
        const width = this.#canvas.clientWidth;

        this.#canvas.height = height;
        this.#canvas.width = width;

        const draw = this.#canvas.getContext('2d');
        if (draw == null) {
            throw new Error();
        }

        draw.clearRect(0, 0, height, width);
        draw.fillStyle = "white";

        audio.analyser.getByteFrequencyData(this.#dataArray);

        const minBin = this.#minFreq / 48000 * audio.fftSize;
        const maxBin = this.#maxFreq / 48000 * audio.fftSize;
        const multiplyX = (maxBin - minBin);

        for (let x = 0; x < width; x += this.#barWidth) {
            const i = Math.floor((x / width) ** this.#xToFreqExp * multiplyX + minBin);
            const barHeight = this.#dataArray[i] * height / 256;
            draw.fillRect(x, height - barHeight, this.#barWidth, barHeight);
        }

        this.#taskId = requestAnimationFrame(() => this.#draw());
    }
}

export const visualiser = new Visualiser();
