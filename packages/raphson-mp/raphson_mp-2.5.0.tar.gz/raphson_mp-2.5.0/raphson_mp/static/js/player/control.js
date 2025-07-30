import { controlChannel, ControlCommand } from "../api.js";
import { audioElement } from "./player.js";
import { queue } from "./queue.js";
import { audio } from "./audio.js";

controlChannel.registerMessageHandler(ControlCommand.SERVER_PLAY, () => {
    audioElement.play();
});

controlChannel.registerMessageHandler(ControlCommand.SERVER_PAUSE, () => {
    audioElement.pause();
});

controlChannel.registerMessageHandler(ControlCommand.SERVER_PREVIOUS, () => {
    queue.previous();
});

controlChannel.registerMessageHandler(ControlCommand.SERVER_NEXT, () => {
    queue.next();
});

async function updateNowPlaying() {
    const track = queue.currentTrack && queue.currentTrack.track ? queue.currentTrack.track : null;
    const duration = audioElem.duration ? audioElem.duration : (track ? track.duration : null);
    if (duration) {
        const data = {
            track: track ? track.path : null,
            paused: audioElem.paused,
            position: audioElem.currentTime,
            duration: duration,
            control: true,
            volume: audio.getVolume(),
        };

        controlChannel.sendMessage(ControlCommand.CLIENT_PLAYING, data);
    }
}

setInterval(updateNowPlaying, 30_000);

controlChannel.registerConnectHandler(() => {
    updateNowPlaying();
});

const audioElem = audioElement;
audioElem.addEventListener("play", updateNowPlaying);
audioElem.addEventListener("pause", updateNowPlaying);
audioElem.addEventListener("seeked", updateNowPlaying);
