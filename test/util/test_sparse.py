import torch
import unittest
from gpytorch.utils import sparse_eye, sparse_getitem, sparse_repeat, to_sparse


class TestSparse(unittest.TestCase):
    def setUp(self):
        self.indices = torch.LongTensor([[0, 1, 2, 3, 4], [2, 1, 0, 0, 1]])
        self.values = torch.FloatTensor([3, 4, 5, 2, 6])
        self.sparse = torch.sparse.FloatTensor(
            self.indices,
            self.values,
            torch.Size((5, 3)),
        )
        self.dense = self.sparse.to_dense()

    def test_sparse_eye(self):
        res = sparse_eye(5)
        actual = torch.eye(5)
        self.assertTrue(torch.equal(res.to_dense(), actual))

    def test_sparse_getitem_one_dim_int(self):
        actual = self.dense[3]
        res = sparse_getitem(self.sparse, 3)
        self.assertTrue(torch.equal(actual, res.to_dense()))

    def test_sparse_getitem_one_dim_slice(self):
        actual = self.dense[2:4]
        res = sparse_getitem(self.sparse, slice(2, 4))
        self.assertTrue(torch.equal(actual, res.to_dense()))

    def test_sparse_getitem_two_dim_int(self):
        actual = self.dense[2, 1]
        res = sparse_getitem(self.sparse, (2, 1))
        self.assertEqual(actual, res)

    def test_sparse_getitem_two_dim_int_slice(self):
        actual = self.dense[:, 1]
        res = sparse_getitem(self.sparse, (slice(None, None, None), 1))
        self.assertTrue(torch.equal(actual, res.to_dense()))

        actual = self.dense[1, :]
        res = sparse_getitem(self.sparse, (1, slice(None, None, None)))
        self.assertTrue(torch.equal(actual, res.to_dense()))

    def test_sparse_getitem_two_dim_slice(self):
        actual = self.dense[2:4, 1:3]
        res = sparse_getitem(self.sparse, (slice(2, 4), slice(1, 3)))
        self.assertTrue(torch.equal(actual, res.to_dense()))

    def test_sparse_repeat_1d(self):
        sparse_1d = sparse_getitem(self.sparse, 1)
        actual = sparse_1d.to_dense().repeat(3, 1)
        res = sparse_repeat(sparse_1d, 3, 1)
        self.assertTrue(torch.equal(actual, res.to_dense()))

        actual = sparse_1d.to_dense().repeat(2, 3)
        res = sparse_repeat(sparse_1d, 2, 3)
        self.assertTrue(torch.equal(actual, res.to_dense()))

    def test_sparse_repeat_2d(self):
        actual = self.sparse.to_dense().repeat(3, 2)
        res = sparse_repeat(self.sparse, 3, 2)
        self.assertTrue(torch.equal(actual, res.to_dense()))

        actual = self.sparse.to_dense().repeat(1, 2)
        res = sparse_repeat(self.sparse, 1, 2)
        self.assertTrue(torch.equal(actual, res.to_dense()))

        actual = self.sparse.to_dense().repeat(3, 1)
        res = sparse_repeat(self.sparse, 3, 1)
        self.assertTrue(torch.equal(actual, res.to_dense()))

    def test_to_sparse(self):
        actual = self.sparse
        res = to_sparse(self.sparse.to_dense())
        self.assertTrue(torch.equal(actual.to_dense(), res.to_dense()))


if __name__ == '__main__':
    unittest.main()
