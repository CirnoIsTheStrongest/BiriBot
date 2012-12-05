import requests

class Twitch_API(object):
    def __init__(self):
        self.twitch_stream_url = 'https://api.twitch.tv/kraken/streams/'
        self.twitch_vods_url = 'https://api.twitch.tv/kraken/channels/'

    def check_stream(self, stream_name):
        ''' checks which service the stream is on '''
        pass
    def check_streams(self, stream_name):
        ''' checks twitch for stream info '''
        stream_info = requests.get(self.twitch_stream_url + stream_name)
        vods_list = requests.get(self.twitch_vods_url + stream_name + '/videos')
        try:
            if stream_info.json['stream'] is not None:
                game = stream_info.json['stream']['game']
                viewer_count = stream_info.json['stream']['viewers']
                url = stream_info.json['stream']['channel']['url']
                return '8.: 11{0} is: 7live 8.:. 4 Playing: 7{1} 8.:. 9Viewercount: 7 {2}  8:: Link - {3} :.'.format(
                    stream_name, 
                    game, 
                    viewer_count,
                    url
                    )
            else:
                vods = vods_list.json['videos'][1]['url']
                return 'This stream is not currently live. Latest vod here: {}'.format(vods)
        except KeyError:
                return 'This stream could not be found.'

    def check_own3d(self, stream_name):
        ''' checks own3d.tv for stream info '''
        pass