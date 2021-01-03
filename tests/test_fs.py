import unittest
import gym_vim
from gym_vim.envs.fs import *
from pynvim import attach

class TestVim(unittest.TestCase):
    def setUp(self):
        self.nvim = attach('child', argv=["/bin/env", "nvim", "--embed", "--headless"])

    def tearDown(self):
        self.nvim.close()

    def test_sh(self):
        self.assertEqual(["a"], sh("echo a"))
        self.assertRaises(Exception, sh, "blah")

    def test_get_mode(self):
        self.assertEqual("n", get_mode(self.nvim))
        self.nvim.feedkeys("iham")
        self.assertEqual("i", get_mode(self.nvim))
        self.nvim.feedkeys("\x1b") # i.e <Esc> key, see replace_termcodes()
        self.assertEqual("n", get_mode(self.nvim))
        self.nvim.feedkeys("v")
        self.assertEqual("v", get_mode(self.nvim))

    def test_get_curpos(self):
        self.assertEqual([0, 1, 1, 0, 1], get_curpos(self.nvim))

    def test_get_state(self):
        self.nvim.feedkeys("iham")
        state = get_state(self.nvim)
        self.assertEqual("i", state.mode)
        self.assertEqual([0, 1, 4, 0, 4], state.curpos)
        self.assertEqual(["ham"], state.strings)

if __name__ == '__main__':
    unittest.main()
