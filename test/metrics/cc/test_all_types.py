# coding=utf-8
import unittest


class JavaTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(JavaTestCase, cls).setUpClass()

    def runAnalysis(self):
        super(JavaTestCase, self).setUp()
        from aibolit.metrics.cc.main import CCMetric

        metric = CCMetric('test/metrics/cc/javafiles/')
        res = metric.value(True)
        data = list(filter(lambda x: x['file'] == 'test/metrics/cc/javafiles/Complicated.java', res['data']))
        self.assertEqual(data[0]['complexity'], 12)

        data = list(filter(lambda x: x['file'] == 'test/metrics/cc/javafiles/OtherClass.java', res['data']))
        self.assertEqual(data[0]['complexity'], 3)

        errors = list(filter(lambda x: x['file'] == 'test/metrics/cc/javafiles/ooo.java', res['errors']))
        self.assertEqual(errors[0]['message'][0:12], 'PMDException')

        file = 'test/metrics/cc/javafiles/Complicated.java'
        metric = CCMetric(file)
        res = metric.value(True)
        self.assertEqual(res['data'][0]['complexity'], 12)
        self.assertEqual(res['data'][0]['file'], file)

        file = 'test/metrics/cc/javafiles/ooo.java'
        metric = CCMetric(file)
        res = metric.value(True)
        self.assertEqual(res['errors'][0]['message'][0:12], 'PMDException')
        self.assertEqual(res['errors'][0]['file'], file)

        with self.assertRaises(Exception) as context:
            file = 'test/metrics/cc/javafiles/ooo1.java'
            metric = CCMetric(file)
            res = metric.value(True)
        self.assertTrue('File test/metrics/cc/javafiles/ooo1.java does not exist' == str(context.exception))

        file = 'test/metrics/cc/javafiles/OtherClass.java'
        metric = CCMetric(file)
        res = metric.value(True)
        self.assertEqual(res['data'][0]['complexity'], 3)
