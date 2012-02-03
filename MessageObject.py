class Message:
    source = None
    type = None
    args = None
    msg = None

    def __init__(self, source, msg_type, args, msg):
        
        self.source = source
        self.type = msg_type
        self.args = args
        self.msg = msg