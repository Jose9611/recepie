from rest_framework.response import Response

class ResponseInfo(object):
    def __init__(self, **args):
        self.response = {
            "msg": args.get('msg', ""),
            "data": args.get('data', {}),
            "status": args.get('status', True),
            "error": args.get('error', ""),
        }

class ShopBaseView:

    def response(self, msg="",status=False, data={},  error=""):
        out ={}
        response = ResponseInfo(msg=msg,status=status, data=data,  error=error).response
        out['msg'] = response['msg']
        out['status'] = response['status']
        out['data'] = response['data']
        out['error'] = response['error']
        return Response(out)

    def audit_trail(self, **kwargs):
        pass

    def log(self, **kwargs):
        pass

