import webracer
import nose.plugins.attrib
from . import utils
from .apps import kitchen_sink_app

utils.app_runner_setup(__name__, kitchen_sink_app.app, 8051)

@nose.plugins.attrib.attr('client')
@webracer.config(host='localhost', port=8051)
class HeaderTest(webracer.WebTestCase):
    def test_raw_headers(self):
        self.get('/ok')
        self.assert_status(200)
        self.assertEqual('ok', self.response.body)
        
        actual = utils.listit(self.response.raw_headers)
        lowercased = [[key.lower(), value] for key, value in actual]
        self.assertTrue(['content-length', '2'] in lowercased)
        
        # in python 2.7 header names are lowercased.
        # in python 3.3 they are camelcased.
        # in any event, bogus casing should not be allowed.
        self.assertTrue(['content-LENGTH', '2'] not in actual)
    
    def test_headers(self):
        self.get('/ok')
        self.assert_status(200)
        
        actual = self.response.headers
        lowercased_keys = [key.lower() for key in actual.keys()]
        
        assert 'content-length' in lowercased_keys
        
        # all cases should be accepted by the dict itself
        assert 'content-length' in actual
        assert 'Content-Length' in actual
        assert 'content-LENGTH' in actual
        
        self.assertEqual('2', actual['content-LENGTH'])
