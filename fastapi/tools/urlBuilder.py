from constants import IMAGE_DIR, URL


def urlFor(filename):
    return URL + "/" + IMAGE_DIR + "/" + filename


def staticURL(filename):
    return URL + "/static/" + filename
