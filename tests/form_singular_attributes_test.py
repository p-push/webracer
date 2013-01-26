import webracer
from tests import utils
from tests import form_app

def setup_module():
    utils.start_bottle_server(form_app.app, 8050)

@webracer.config(host='localhost', port=8050)
class FormSingularAttributesTest(webracer.WebTestCase):
    def test_attributes_explicit(self):
        self.get('/one_form')
        self.assert_status(200)
        
        # call
        form = self.response.form()
        self._check(form)
    
    def test_attributes_on_proxy(self):
        self.get('/one_form')
        self.assert_status(200)
        
        # do not call
        form = self.response.form
        self._check(form)
    
    def _check(self, form):
        self.assertEqual('/there', form.action)
        self.assertEqual('http://localhost:8050/there', form.computed_action)
        self.assertEqual('post', form.method)
        self.assertEqual('POST', form.computed_method)
        self.assertEqual('formname', form.name)
        self.assertEqual('formid', form.id)
        
        # internal
        self.assertEqual(3, len(form.elements.elements))
        
        self.assertEqual([['textf', 'textv']], utils.listit(form.elements.params.list))
        self.assertEqual([['textf', 'textv']], utils.listit(form.params.list))

if __name__ == '__main__':
    import unittest
    unittest.main()
