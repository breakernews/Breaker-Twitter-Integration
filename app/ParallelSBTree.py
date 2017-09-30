#!/usr/bin/env python

import sys
import signal
from threading import Thread, Semaphore

from bintrees import AVLTree

class ParallelSBTree(object):

    """
    Parallel threading structure as a Self-balancing Tree.  Used to implement
    the Reduce Parallel Computation algorithm.  For operations over the whole
    tree forming threads
    """

    def __init__(self, entries,shared = None):
        self.sem_lock = Semaphore(value = 1)
        self.psbt = AVLTree(entries)
        self.shared = shared


    def foreach(self, function, root):
        if root == None:
            return

        value = root.value
        # change value to args
        worker_thread = Thread(target = function, args=(self.shared, value,))
        worker_thread.start()

        # exponential spawning
        if root.left != None:
            worker_thread_l = Thread(target = self.foreach, args=(function, root.left))
            worker_thread_l.start()

        if root.right != None:
            worker_thread_r = Thread(target = self.foreach, args=(function, root.right))
            worker_thread_r.start()

    def update_node(self, key, value):
        print self.psbt
        self.remove(key)
        self.insert(key, value)

    def new_node(self, key, value):
        return self.psbt._new_node(key, value)

    def insert(self, key, value):
        self.psbt.insert(key, value)

    def remove(self, key):
        self.psbt.remove(key)

    def merge_result(self, shared_result):
        pass
