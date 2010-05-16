# Generated by the windmill services transformer
from windmill.authoring import WindmillTestClient
from datetime import datetime

def test_recordingSuite0():
    client = WindmillTestClient(__name__)
    now = unicode(datetime.today())

    client.click(link=u'Igor Bestuzhev')
    client.waits.forPageLoad(timeout=u'20000')
    client.waits.forElement(link=u'Login here', timeout=u'8000')
    client.click(link=u'Login here')
    client.waits.forPageLoad(timeout=u'20000')
    client.type(text=u'igor', id=u'id_username')
    client.type(text=u'wrong', id=u'id_password')
    client.click(value=u'login')
    client.waits.forPageLoad(timeout=u'20000')
    client.type(text=u'123', id=u'id_password')
    client.click(value=u'Login')
    client.waits.forPageLoad(timeout=u'20000')
    client.waits.forElement(link=u'Edit profile for Igor Bestuzhev', timeout=u'8000')
    client.click(link=u'Edit profile for Igor Bestuzhev')
    client.waits.forPageLoad(timeout=u'20000')
    client.waits.forElement(timeout=u'8000', id=u'id_biography')
    client.click(id=u'id_biography')
    client.type(text=u'Some text about me\nLast edit %s'%now, id=u'id_biography')
    client.click(value=u'Save')
    client.waits.forPageLoad(timeout=u'20000')
    client.asserts.assertTextIn(validator=now, tagname=u'table')
    client.click(link=u'logout from igor')