import requests

class Twitch_API(object):
    stream_url = 'https://api.twitch.tv/kraken/streams/'

    def check_streams(self, stream_name):
        request = requests.get(self.stream_url + stream_name)
        try:
            if request.json['stream'] is not None:
                game = request.json['stream']['game']
                viewer_count = request.json['stream']['viewers']
                return 'Stream is live playing {0} with {1} viewers.'.format(game, viewer_count)
            else:
                return 'This stream is not currently live.'
        except KeyError:
            return 'This stream could not be found.'