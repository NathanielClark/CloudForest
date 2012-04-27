#!/usr/bin/env python
# encoding: utf-8
"""
File: test_cloudforest.py
Author: Brant Faircloth

Created by Brant Faircloth on 26 April 2012 16:04 PDT (-0700)
Copyright (c) 2012 Brant C. Faircloth. All rights reserved.

"""

import os
import cPickle
import unittest
import numpy as np
from context import cloudforest

import pdb

class TestCloudForestFunctions(unittest.TestCase):

    def setUp(self):
        self.p = cloudforest.Process()
        self.one = open('alignments/3.oneliners', 'rU').readline()

    def test_oneliner_to_phylip(self):
        expected = cPickle.load(open('pickles/expected_phylip.pickle'))
        observed = self.p.oneliner2phylip(self.one)
        assert observed == expected

    def test_bootstrap(self):
        # we are assuming sampling with replacement works as advertised
        # and just checking to make sure we re-order according to sample
        # here.
        expected = self.prep_oneliner_array()
        taxa, align = self.p.onelinerAlignment2Array(expected)
        bs, choices = self.p.bootstrap(align, 1, 0, True)
        for k, aln in enumerate(bs):
            assert (bs[0][k] == align[choices[k]]).all()

    def prep_oneliner_array(self):
        locus = self.one.strip().split(';')
        locus = locus[0].split(':')[1]
        return locus

    def test_oneliner_to_array(self):
        exp_taxa = ['MusMuscu', 'GorGoril', 'PanTrogl']
        exp_align = cPickle.load(open('pickles/expected_align_to_array.pickle'))
        locus = self.prep_oneliner_array()
        obs_taxa, obs_align = self.p.onelinerAlignment2Array(locus)
        assert obs_taxa == exp_taxa
        # comparing arrays
        assert (obs_align == exp_align).all()

    def test_array_to_oneliner(self):
        expected = self.prep_oneliner_array()
        taxa, align = self.p.onelinerAlignment2Array(expected)
        observed = self.p.array2OnelinerAlignment(taxa, align)
        assert observed == expected

    def test_make_tree_name(self):
        d = {'chrm': 'chr1_1036'}
        observed = self.p.makeTreeName(d)
        expected = 'chrm=chr1_1036'
        assert observed == expected

    def test_process_oneliner_data(self):
        # send single oneliner
        expected = {'chrm': 'chr1_1036'}
        observed = self.p.processOnelinerData(self.one, {})
        assert observed == expected

    def test_duplicate_oneliners(self):
        locus = self.prep_oneliner_array()
        d = {'chrm': 'chr1_1036'}
        tree_name = self.p.makeTreeName(d)
        oneliner = "%s:%s" % (tree_name, locus)
        expected = [(r, oneliner) for r in range(1, 7)[::-1]]
        dupes = self.p.duplicateOneliners(1, oneliner, 5)
        observed = [d for d in dupes]
        assert observed == expected

    def test_process_stats_file(self):
        pass

    def test_lines_to_oneliner(self):
        # I'm not entirely sure what this does
        pass

    def test_phyml(self):
        pass

    def test_mraic(self):
        try:
            os.makedirs('tmp')
        except OSError:
            pass
        observed = self.p.mrAIC(1, self.one, '../binaries')
        #pdb.set_trace()
        #os.remove('tmp')


if __name__ == '__main__':
    unittest.main()
