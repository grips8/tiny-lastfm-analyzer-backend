import time

import pylast
from flask_restful import Resource, request
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta

from api.myLast import getUserScrobbles, getArtistImage
from api.tracksAnalysis import analyzeData


def parseDates(_from_date, _to_date, timezone_offset, is_monthly_version):
    dividers = []
    if is_monthly_version:
        delta = relativedelta(months=1)
        from_date = datetime.strptime(_from_date + ' +0000', "%Y-%m %z")
        to_date = datetime.strptime(_to_date + ' +0000', "%Y-%m %z")
    else:
        delta = relativedelta(years=1)
        from_date = datetime.strptime(_from_date + ' +0000', "%Y %z")
        to_date = datetime.strptime(_to_date + ' +0000', "%Y %z")
    to_date += delta
    tmp = from_date
    while tmp != to_date:
        dividers.append(int(tmp.timestamp() + timezone_offset))
        tmp += delta
    dividers.append(int(to_date.timestamp() + timezone_offset))
    return dividers


def serializeResult(data, timezone_offset, is_monthly_version, track_dictionary, album_dictionary):
    res = {'artist': [], 'album': [], 'song': []}
    years = {}
    labels = ['name', 'scrobbles', 'second', 'secondScrobbles', 'third', 'thirdScrobbles']
    yearly_labels = ['1st', '2nd', '3rd', '4th', '5th']

    yearly_index = 0

    for bucket in data['artist']:
        date = datetime.fromtimestamp(bucket['timestamp'] - timezone_offset, tz=timezone.utc)
        bucket.pop('timestamp')
        if date.year not in years.keys():
            years[date.year] = True
            res['artist'].append({'year': date.year.__str__(), 'months': []})
        month = {'month': date.strftime('%B') if is_monthly_version else yearly_labels[yearly_index]}
        yearly_index += 1

        ind = 0
        for key, val in bucket.items():
            month[labels[ind]] = key
            ind += 1
            month[labels[ind]] = val
            ind += 1
        try:
            month['img'] = getArtistImage(month['name'])
        except AttributeError:
            month['img'] = "https://fakeimg.pl/400x400"
            print(f"Error getting track cover image for >>>> {month['name']}")

        if not is_monthly_version:
            month['secondLabel'] = 'most listened song:'
            month['thirdLabel'] = 'most listened album:'

        res['artist'][-1]['months'].append(month)

    years.clear()
    yearly_index = 0

    for bucket in data['album']:
        date = datetime.fromtimestamp(bucket['timestamp'] - timezone_offset, tz=timezone.utc)
        bucket.pop('timestamp')
        if date.year not in years.keys():
            years[date.year] = True
            res['album'].append({'year': date.year.__str__(), 'months': []})
        month = {'month': date.strftime('%B') if is_monthly_version else yearly_labels[yearly_index]}
        yearly_index += 1

        ind = 0
        for key, val in bucket.items():
            month[labels[ind]] = key
            ind += 1
            month[labels[ind]] = val
            ind += 1

        track_album = album_dictionary[month['name']].track.get_album()
        try:
            month['img'] = track_album.get_cover_image(size=3) if track_album is not None \
                else album_dictionary[month['name']].track.get_cover_image(size=3)
        except IndexError:
            month['img'] = "https://fakeimg.pl/400x400"
            print(f"Error getting track cover image for >>>> {month['name']}")

        if not is_monthly_version:
            month['secondLabel'] = 'most listened song:'
            month['thirdLabel'] = '2nd most listened song:'

        res['album'][-1]['months'].append(month)

    years.clear()
    yearly_index = 0

    for bucket in data['song']:
        date = datetime.fromtimestamp(bucket['timestamp'] - timezone_offset, tz=timezone.utc)
        bucket.pop('timestamp')
        if date.year not in years.keys():
            years[date.year] = True
            res['song'].append({'year': date.year.__str__(), 'months': []})
        month = {'month': date.strftime('%B') if is_monthly_version else yearly_labels[yearly_index]}
        yearly_index = 0

        ind = 0
        for key, val in bucket.items():
            month[labels[ind]] = key
            ind += 1
            month[labels[ind]] = val
            ind += 1

        track_album = track_dictionary[month['name']].track.get_album()
        try:
            month['img'] = track_album.get_cover_image(size=3) if track_album is not None \
                else track_dictionary[month['name']].track.get_cover_image(size=3)
        except IndexError:
            month['img'] = "https://fakeimg.pl/400x400"
            print(f"Error getting track cover image for >>>> {month['name']}")

        if not is_monthly_version:
            month['secondLabel'] = ''
            month['thirdLabel'] = ''

        res['song'][-1]['months'].append(month)

    return res


class ApiHandler(Resource):
    def get(self):
        args = {'username': request.args.get('username', type=str),
                'fromDate': request.args.get('fromDate', type=str),
                'toDate': request.args.get('toDate', type=str),
                'timezoneOffset': request.args.get('timezoneOffset', type=int),
                'isMonthlyVersion': request.args.get('isMonthlyVersion', type=str)}

        args['isMonthlyVersion'] = True if args['isMonthlyVersion'] == 'true' else False
        args['timezoneOffset'] *= 60

        if any(x is None for x in args.values()):
            return {
                'result': 'FAILURE',
                'message': 'Query parameters are not valid!'
            }

        start = time.time()
        dividers = parseDates(args['fromDate'], args['toDate'], args['timezoneOffset'], args['isMonthlyVersion'])

        try:
            tracks = getUserScrobbles(args['username'], dividers[0], dividers[-1])
        except pylast.WSError as e:
            return {
                'result': 'FAILURE',
                'message': e.details
            }

        print(f"Tracks fetched in: {time.time() - start}")
        start = time.time()

        track_dictionary = {track.track.__str__(): track for track in tracks}
        album_dictionary = {track.album: track for track in tracks}

        analyzedData = analyzeData(dividers, tracks, args['isMonthlyVersion'])
        # analyzedData = {'artist': [], 'album': [], 'song': []}

        print(f"Analyzed data in: {time.time() - start}")
        start = time.time()

        serializedData = serializeResult(analyzedData, args['timezoneOffset'], args['isMonthlyVersion'],
                                         track_dictionary, album_dictionary)

        print(f"Serialized data in: {time.time() - start}")

        return serializedData
