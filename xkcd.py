__author__ = 'christophertaormina'
import json
import sys
import random
import urllib2


def lambda_handler(event, context):
    req = _formparams_to_dict(event['formparams'])
    comicresp = {}
    if req['text']:
        num = int(req['text'])
        comicresp = getComicById(num)
    else:
        comicresp = getRandomComic()

    slackresp = formatResponse(comicresp, req)

    return slackresp



def getComicById(id):
    xkcdapi = "http://xkcd.com/{comicid}/info.0.json".format(comicid=id)
    resp = getResp(xkcdapi)
    if 'err' not in resp:
        comic = {"img":resp['img'], "alt":resp['alt'], "num":resp['num']}
        return comic
    else:
        return resp


def getRandomComic():
    xkcdapi =  "http://xkcd.com/info.0.json"
    resp = getResp(xkcdapi)
    if 'err' not in resp:
        rand_max = resp['num']
        rand = random.randrange(1,rand_max)
        return getComicById(rand)
    else:
        return resp


def getResp(api):
    try:
        resp = urllib2.urlopen(api)
    except urllib2.HTTPError as e:
        return {"err":e}
    except urllib2.URLError as e:
        return {"err":e}
    except:
        return {"err":sys.exc_info()[0]}
    else:
        str_resp = resp.read().decode('utf-8')
        return json.loads(str_resp)


def _formparams_to_dict(s1):
    """ Converts the incoming formparams from Slack into a dictionary. Ex: 'text=votebot+ping' """
    retval = {}
    for val in s1.split('&'):
        k, v = val.split('=')
        retval[k] = v
    return retval


def formatResponse(resp, req):
    if 'err' in resp:
        return formatFailedResponse(resp)
    else:
        return formatSuccessfulResponse(resp, req)


def formatSuccessfulResponse(resp, req):
    slackresp = {}
    slackresp['response_type'] = 'in_channel'
    slackresp['user_name'] = req['user_name']
    slackresp['attachments'] = [
        {
            "text":str(resp['num']) + ' - ' + resp['alt'],
            "image_url":resp['img']
        }
    ]
    return slackresp



def formatFailedResponse(resp):
    slackresp = {}
    slackresp['text'] = resp['err']
    return slackresp