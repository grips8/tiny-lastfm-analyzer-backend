# This is a sample Python script.
import pylast

from api.ApiHandler import parseDates, serializeResult
from api.myLast import getUserScrobbles
from api.tracksAnalysis import analyzeData


# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def test():
    dividers = parseDates('2018', '2018', -7200, False)

    try:
        tracks = getUserScrobbles('quelthar', dividers[0], dividers[-1])
    except pylast.WSError as e:
        return {
            'result': 'FAILURE',
            'message': e.details
        }

    res = analyzeData(dividers=dividers, tracks=tracks, is_monthly_version=False)

    track_dictionary = {track.track.__str__(): track for track in tracks}
    album_dictionary = {track.album: track for track in tracks}

    ser = serializeResult(res, -7200, False, track_dictionary, album_dictionary)

    print(ser)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    test()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
