# coding=utf-8
import unittest


class JavaTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(JavaTestCase, cls).setUpClass()

    def runAnalysis(self):
        super(JavaTestCase, self).setUp()
        from main import CCMetric

        metric = CCMetric('tests/Complicated.java')
        res = metric.run(showoutput=True)
        self.assertEqual(res['data'], 12)

        metric = CCMetric('tests/ooo.java')
        res = metric.run(showoutput=True)
        self.assertEqual(res['error'], 'Incorrect input file')

        metric = CCMetric('tests/ooo1.java')
        res = metric.run(showoutput=True)
        self.assertEqual(res['error'], 'File tests/ooo1.java does not exist')

        metric = CCMetric('tests/OtherClass.java')
        res = metric.run(showoutput=True)
        self.assertEqual(res['data'], 3)
