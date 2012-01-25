import re


class StripWhitespaceMiddleware(object):
    """
    Strips leading and trailing whitespace from response content.
    """

    def __init__(self):
        self.whitespace = re.compile('^\s+', re.MULTILINE)
        self.whitespace_trail = re.compile('\s+$', re.MULTILINE)


    def process_response(self, request, response):
        if "text/html" in response['Content-Type']:
            new_content = self.whitespace.sub('', response.content)
            new_content = self.whitespace_trail.sub('\n', new_content)
            response.content = new_content
            return response
        else:
            return response


