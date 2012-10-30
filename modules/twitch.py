import requests

class Twitch_API(object):
    stream_url = 'https://api.twitch.tv/kraken/streams/'

    def check_streams(self, stream_name):
        request = requests.get(self.stream_url + stream_name)
        try:
            if request.json['stream'] is not None:
                game = request.json['stream']['game']
                viewer_count = request.json['stream']['viewers']
                return '8.: 11{0} is: 7live 8.:. 4 Playing: 7{1} 8.:. 9Viewercount: 7 {2}  8:.'.format(stream_name, game, viewer_count)
            else:
                return 'This stream is not currently live.'
        except KeyError:
            return 'This stream could not be found.'