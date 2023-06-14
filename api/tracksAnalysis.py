import pandas as pd


def monthlyImpl(groups):
    res = {'artist': [], 'album': [], 'song': []}

    for bucket, group in groups:
        artists = group['artist'].value_counts()
        artists_d = artists.nlargest(3).to_dict()
        artists_d['timestamp'] = bucket
        albums = group['album'].value_counts()
        albums_d = albums.nlargest(3).to_dict()
        albums_d['timestamp'] = bucket
        songs = group['repr'].value_counts()
        songs_d = songs.nlargest(3).to_dict()
        songs_d['timestamp'] = bucket
        res['artist'].append(artists_d)
        res['album'].append(albums_d)
        res['song'].append(songs_d)

    return res


def yearlyImpl(groups):
    res = {'artist': [], 'album': [], 'song': []}

    for bucket, group in groups:
        artists = group['artist'].value_counts()
        artists_d = artists.nlargest(5).to_dict()
        albums = group['album'].value_counts()
        albums_d = albums.nlargest(5).to_dict()
        songs = group['repr'].value_counts()
        songs_d = songs.nlargest(5).to_dict()

        for key, val in artists_d.items():
            artist_scrobbles = group.loc[group['artist'] == key]
            top_song = artist_scrobbles['repr'].value_counts()
            top_song_d = top_song.nlargest(1).to_dict()
            top_album = artist_scrobbles['album'].value_counts()
            top_album_d = top_album.nlargest(1).to_dict()
            temp = {key: val} | top_song_d | top_album_d
            temp['timestamp'] = bucket
            res['artist'].append(temp)

        for key, val in albums_d.items():
            album_scrobbles = group.loc[group['album'] == key]
            top_song = album_scrobbles['repr'].value_counts()
            top_song_d = top_song.nlargest(2).to_dict()
            temp = {key: val} | top_song_d
            temp['timestamp'] = bucket
            res['album'].append(temp)

        for key, val in songs_d.items():
            temp = {key: val, " ": "", "  ": "", 'timestamp': bucket}
            res['song'].append(temp)

        return res


def analyzeData(dividers, tracks, is_monthly_version):
    df = pd.DataFrame(([track.track.__str__(),
                        track.track.artist.__str__(),
                        track.album.__str__(),
                        int(track.timestamp)]
                       for track in tracks),
                      columns=["repr", "artist", "album", "timestamp"],
                      copy=True)

    df["bucket"] = pd.cut(df["timestamp"], bins=dividers, right=False, labels=dividers[:-1], include_lowest=True)

    groups = df.groupby('bucket')

    return monthlyImpl(groups) if is_monthly_version else yearlyImpl(groups)
