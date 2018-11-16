import dpkt

class PCAPReader(object):
    def __init__(self, f):
        """
        Specify which PCAP will be iterated over
        """
        self.file = f

    def __iter__(self):
        """
        Allows one to row that boat gently down the stream.

        Iterable interface reads in a PCAP and lazily yields each row so that it can be processed.
        """
        with open(self.file, 'rb') as f:
            pcap = dpkt.pcap.Reader(f)
            for timestamp, buffer in pcap:
                yield (timestamp, buffer)