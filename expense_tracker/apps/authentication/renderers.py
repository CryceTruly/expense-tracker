import json

from rest_framework.renderers import JSONRenderer


class UserJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        # If the view throws an error (such as the user can't be authenticated
        # or something similar), `data` will contain an `errors` key. We want
        # the default JSONRenderer to handle rendering errors, so we need to
        # check for this case.
        response=''
        if "Err" in str(data):
            response = json.dumps({'errors': data})
        else:
            response = json.dumps({'user': data})

        # Finally, we can render our data under the "user" namespace.
        return response
