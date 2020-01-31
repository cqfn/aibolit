# coding=utf-8
import unittest


class JavaTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(JavaTestCase, cls).setUpClass()

    def runAnalysis(self):
        super(JavaTestCase, self).setUp()
        from main import CCMetric

        file = 'tests/javafiles/Complicated.java'
        metric = CCMetric(file)
        res = metric.run(showoutput=True)
        self.assertEqual(res['data'][0]['complexity'], 12)
        self.assertEqual(res['data'][0]['file'], file)

        file = 'tests/javafiles/ooo.java'
        metric = CCMetric(file)
        res = metric.run(showoutput=True)
        self.assertEqual(res['errors'][0]['message'][0:12], 'PMDException')
        self.assertEqual(res['errors'][0]['file'], file)

        file = 'tests/javafiles/ooo1.java'
        metric = CCMetric(file)
        res = metric.run(showoutput=True)
        self.assertEqual(res['errors'][0]['message'], 'File does not exist')
        self.assertEqual(res['errors'][0]['file'], file)

        metric = CCMetric('tests/javafiles/OtherClass.java')
        res = metric.run(showoutput=True)
        self.assertEqual(res['data'][0]['complexity'], 3)
