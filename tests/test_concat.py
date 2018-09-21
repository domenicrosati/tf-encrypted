import unittest

import numpy as np
import tensorflow as tf
import tensorflow_encrypted as tfe


class Testconcat(unittest.TestCase):
    def setUp(self):
        tf.reset_default_graph()

    def test_concat(self):
        config = tfe.LocalConfig([
            'server0',
            'server1',
            'crypto_producer'
        ])

        with tf.Session() as sess:
            t1 = [[1, 2, 3], [4, 5, 6]]
            t2 = [[7, 8, 9], [10, 11, 12]]
            out = tf.concat([t1, t2], 0)
            actual = sess.run(out)

        tf.reset_default_graph()

        with tfe.protocol.Pond(*config.get_players('server0, server1, crypto_producer')) as prot:
            x = prot.define_private_variable(np.array(t1))
            y = prot.define_private_variable(np.array(t2))

            out = prot.concat([x, y], 0)

            with config.session() as sess:
                sess.run(tf.global_variables_initializer())
                final = out.reveal().eval(sess)

        np.testing.assert_array_equal(final, actual)

    def test_masked_concat(self):
        config = tfe.LocalConfig([
            'server0',
            'server1',
            'crypto_producer'
        ])

        with tf.Session() as sess:
            t1 = [[1, 2, 3], [4, 5, 6]]
            t2 = [[7, 8, 9], [10, 11, 12]]
            out = tf.concat([t1, t2], 0)
            actual = sess.run(out)

        tf.reset_default_graph()

        with tfe.protocol.Pond(*config.get_players('server0, server1, crypto_producer')) as prot:
            x = prot.mask(prot.define_private_variable(np.array(t1)))
            y = prot.mask(prot.define_private_variable(np.array(t2)))

            out = prot.concat([x, y], 0)

            with config.session() as sess:
                sess.run(tf.global_variables_initializer())
                final = out.unmasked.reveal().eval(sess)

        np.testing.assert_array_equal(final, actual)


if __name__ == '__main__':
    unittest.main()