# super simple program which calculates the area of any rectangle given any base and height as input

def area (w, h):
    if isinstance(w, (float, int)) == False or isinstance(h, (float, int)) == False or w < 0 or h < 0:
        raise ValueError('w and h must both be numbers and greater than 0')
    return w * h
