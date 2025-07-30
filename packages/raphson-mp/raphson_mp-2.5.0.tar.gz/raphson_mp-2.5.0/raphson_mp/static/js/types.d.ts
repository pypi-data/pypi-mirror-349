export type Vars = {
    csrfToken: string,
    offlineMode: string,
    loadTimestamp: number,
    tBrowseArtist: string,
    tBrowseAlbum: string,
    tBrowseTag: string,
    tBrowsePlaylist: string,
    tBrowseYear: string,
    tBrowseRecentlyAdded: string,
    tBrowseRecentlyReleased: string,
    tBrowseRandom: string,
    tBrowseMissingMetadata: string,
    tBrowseNothing: string,
    tActivityFileAdded: string,
    tActivityFileModified: string,
    tActivityFileDeleted: string,
    tActivityFileMoved: string,
    tTrackInfoUnavailable: string,
    tNoData: string,
};

export type TrackJson = {
    playlist: string
    path: string
    mtime: number
    ctime: number
    duration: number
    title: string | null
    album: string | null
    album_arist: string | null
    year: number | null
    artists: Array<string>
    tags: Array<string>
    video: string | null
    display: string
    lyrics: string | null
};

export type ControlServerPlaying = {
    player_id: string
    username: string
    update_time: number,
    paused: boolean,
    position: number,
    duration: number,
    control: boolean,
    volume: number,
    track: TrackJson,
};

export type ControlServerPlayed = {
    played_time: number,
    username: string,
    track: TrackJson,
};

export type ControlServerFileChange = {
    change_time: number,
    action: string,
    track: string,
    username: string | null,
}
