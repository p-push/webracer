import webracer
import nose.plugins.attrib
from . import utils
from .apps import kitchen_sink_app

utils.app_runner_setup(__name__, kitchen_sink_app.app, 8053)

@nose.plugins.attrib.attr('client')
@webracer.config(host='localhost', port=8053)
class ResponseUrljoinTest(webracer.WebTestCase):
    def test_request_uri(self):
        self.get('/json/empty')
        self.assert_status(200)
        # XXX should this be an absolute uri?
        #self.assertEqual('http://localhost:8053/json/empty', self.response.request_uri)
        self.assertEqual('http://localhost:8053/json/empty', self.response.request_url)
    
    def test_urljoin(self):
        self.get('/json/empty')
        self.assert_status(200)
        
        url = self.response.urljoin('bar/quux')
        # XXX should this be an absolute uri?
        self.assertEqual('http://localhost:8053/json/bar/quux', url)
