import os
import pylast
import lastfmcache


API_KEY = os.environ["LASTFM_API_KEY"]
API_SECRET = os.environ["LASTFM_API_SECRET"]

lastfm_network = pylast.LastFMNetwork(
    api_key=API_KEY,
    api_secret=API_SECRET
)

lastfm_cache = lastfmcache.LastfmCache(
    api_key=API_KEY,
    shared_secret=API_SECRET
)


def getUserScrobbles(user, start_stamp, end_stamp):
    tracks = lastfm_network.get_user(user).get_recent_tracks(limit=None, time_from=start_stamp, time_to=end_stamp)
    return tracks


def getArtistImage(artist_name):
    return lastfm_cache.get_artist(artist_name=artist_name).cover_image
