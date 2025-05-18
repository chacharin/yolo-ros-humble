
import os, ctypes

def mute_c_stderr():
    """
    Redirect the C-level STDERR (fd-2) to /dev/null so native libraries
    like PyTorch/Caffe2 can't print one-time warnings such as the NNPACK
    message.  Must be called before those libraries are imported.
    """
    devnull_fd = os.open(os.devnull, os.O_WRONLY)
    libc = ctypes.CDLL(None)
    libc.dup2(devnull_fd, 2)          # fd-2 is STDERR


