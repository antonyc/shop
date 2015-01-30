__author__ = 'chapson'

def api_v1():
    import v1
    return v1.api

api = {'1': api_v1()}