from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import time

import numpy as np
import tensorflow as tf

from beholder.beholder import Beholder
from beholder.shared_config import DEFAULT_CONFIG
from beholder.file_system_tools import write_pickle



class BeholderTest(tf.test.TestCase):
  def _write_config(self):
    write_pickle(self.config, '/tmp/beholder-test/plugins/beholder/config.pkl')

  def _dummy_frame(self):
    frame = np.random.randint(0, 255, (100, 100))
    return frame

  def setUp(self):
    conv_weights = tf.Variable(tf.truncated_normal([3, 3, 1, 32],
                                                   dtype=tf.float32,
                                                   stddev=1e-1))
    self.sess = tf.Session()
    self.sess.run(tf.global_variables_initializer())

    self.beholder = Beholder(self.sess, '/tmp/beholder-test')
    self.config = dict(DEFAULT_CONFIG)
    self.config['FPS'] = 100000000000
    self._write_config()


  def test_update_trainable_variables(self):
    self.config['values'] = 'trainable_variables'
    self._write_config()
    self.beholder.update()


  def test_update_arrays(self):
    self.config['values'] = 'arrays'
    self._write_config()
    self.beholder.update(arrays=None)
    self.beholder.update(arrays=[np.random.randint(0, 100, (10, 10))])


  def test_update_frame(self):
    self.config['values'] = 'frames'
    self._write_config()
    self.beholder.update(frame=None)
    self.beholder.update(frame=self._dummy_frame())


  def test_update_recording(self):
    self.config['is_recording'] = False
    self.beholder._update_recording(self._dummy_frame(), self.config)
    self.beholder._update_recording(self._dummy_frame(), self.config)
    self.config['is_recording'] = True
    self.beholder._update_recording(self._dummy_frame(), self.config)
    self.beholder._update_recording(self._dummy_frame(), self.config)
    self.config['is_recording'] = False
    self.beholder._update_recording(self._dummy_frame(), self.config)


  def test_enough_time_has_passed(self):
    self.assertFalse(self.beholder._enough_time_has_passed(0))

    self.beholder.update()
    time.sleep(1)
    self.assertTrue(self.beholder._enough_time_has_passed(30))

    self.beholder.update()
    self.assertFalse(self.beholder._enough_time_has_passed(1))



if __name__ == '__main__':
  tf.test.main()
