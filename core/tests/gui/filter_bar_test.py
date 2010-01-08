# Created By: Virgil Dupras
# Created On: 2008-08-02
# Copyright 2010 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "HS" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/hs_license

from nose.tools import eq_

from ..base import TestCase
from ..reconciliation_test import CommonSetup
from ...document import FilterType
from ...model.account import AccountType

class Pristine(TestCase):
    def setUp(self):
        self.create_instances()
    
    def test_attributes(self):
        """the filter bars start out as unfiltered, and both etable and ttable have one"""
        self.assertTrue(self.tfbar.filter_type is None)
        self.assertTrue(self.efbar.filter_type is None)
    

class TransactionsOfEachType(TestCase):
    def setUp(self):
        self.create_instances()
        self.add_account_legacy('asset 1')
        self.add_account_legacy('asset 2')
        self.add_entry(description='first', transfer='Income', increase='1')
        self.add_entry(description='second', increase='2')
        self.add_entry(description='third', transfer='Expense', decrease='3')
        self.add_entry(description='fourth', transfer='asset 1', decrease='4')
        self.clear_gui_calls()
    
    def test_efbar_filter_expenses(self):
        #The etable's expense filter makes it only show entries with a decrease
        self.efbar.filter_type = FilterType.Expense # decrease
        self.check_gui_calls(self.etable_gui, ['refresh'])
        eq_(len(self.etable), 2)
        eq_(self.etable[0].description, 'third')
        eq_(self.etable[1].description, 'fourth')
        #The ttable's expense filter makes it only show entries with a transfer to an expense.
        self.mainwindow.select_transaction_table()
        self.check_gui_calls(self.tfbar_gui, ['refresh']) # refreshes on connect()
        assert self.tfbar.filter_type is FilterType.Expense
        eq_(len(self.ttable), 1)
        eq_(self.ttable[0].description, 'third')
    
    def test_efbar_filter_income(self):
        #The etable's income filter makes it only show entries with an increase.
        self.efbar.filter_type = FilterType.Income
        self.check_gui_calls(self.etable_gui, ['refresh'])
        eq_(len(self.etable), 2)
        eq_(self.etable[0].description, 'first')
        eq_(self.etable[1].description, 'second')
        #The etable's income filter makes it only show entries with a transfer to an income.
        self.mainwindow.select_transaction_table()
        self.check_gui_calls(self.tfbar_gui, ['refresh']) # refreshes on connect()
        assert self.tfbar.filter_type is FilterType.Income
        eq_(len(self.ttable), 1)
        eq_(self.ttable[0].description, 'first')
    
    def test_efbar_filter_transfer(self):
        #The etable's transfer filter makes it only show entries with a transfer to an asset/liability.
        self.efbar.filter_type = FilterType.Transfer
        self.check_gui_calls(self.etable_gui, ['refresh'])
        eq_(len(self.etable), 1)
        eq_(self.etable[0].description, 'fourth')
        self.mainwindow.select_transaction_table()
        self.check_gui_calls(self.tfbar_gui, ['refresh']) # refreshes on connect()
        assert self.tfbar.filter_type is FilterType.Transfer
        eq_(len(self.ttable), 1)
        eq_(self.ttable[0].description, 'fourth')
    
    def test_efbar_filter_unassigned(self):
        # The etable's unassigned filter makes it only show unassigned entries. going to ttable keeps
        # the filter on.
        self.efbar.filter_type = FilterType.Unassigned
        self.check_gui_calls(self.etable_gui, ['refresh'])
        eq_(len(self.etable), 1)
        eq_(self.etable[0].description, 'second')
        self.mainwindow.select_transaction_table()
        self.check_gui_calls(self.tfbar_gui, ['refresh']) # refreshes on connect()
        assert self.tfbar.filter_type is FilterType.Unassigned
        eq_(len(self.ttable), 1)
    
    def test_enable_disable_buttons(self):
        # The enable disable mechanism of the income, expense and transfer buttons work as expected
        self.efbar.filter_type = FilterType.Income
        self.mainwindow.select_income_statement()
        self.istatement.selected = self.istatement.income[0]
        self.clear_gui_calls()
        self.istatement.show_selected_account()
        assert self.efbar.filter_type is None
        self.check_gui_calls(self.efbar_gui, ['refresh', 'disable_transfers'])
        self.mainwindow.select_transaction_table()
        self.check_gui_calls(self.tfbar_gui, ['refresh']) # no disable
        self.mainwindow.select_balance_sheet()
        self.bsheet.selected = self.bsheet.assets[0]
        self.bsheet.show_selected_account()
        self.check_gui_calls(self.efbar_gui, ['refresh', 'enable_transfers'])
    
    def test_multiple_filters_at_the_same_time(self):
        # Having an unassigned filter at the same time as a search filter works as expected.
        self.mainwindow.select_transaction_table()
        self.tfbar.filter_type = FilterType.Unassigned
        self.sfield.query = 'first'
        eq_(len(self.ttable), 0)
    

class ThreeEntriesOneReconciled(TestCase, CommonSetup):
    def setUp(self):
        self.create_instances()
        self.setup_three_entries_reconciliation_mode()
        self.setup_reconcile_second_entry()
        self.document.toggle_reconciliation_mode() # commit reonciliation
    
    def test_efbar_not_reconciled(self):
        self.efbar.filter_type = FilterType.NotReconciled
        eq_(len(self.etable), 2)
        eq_(self.etable[0].description, 'one')
        self.mainwindow.select_transaction_table()
        eq_(len(self.ttable), 2)
        eq_(self.ttable[1].description, 'three')
    
    def test_efbar_reconciled(self):
        self.efbar.filter_type = FilterType.Reconciled
        eq_(len(self.etable), 1)
        eq_(self.etable[0].description, 'two')
        self.mainwindow.select_transaction_table()
        eq_(len(self.ttable), 1)
        eq_(self.ttable[0].description, 'two')
    

class SplitExpenseFromAssetAndLiability(TestCase):
    # A transaction going to an expense, half coming from an asset, the other half coming from a
    # liability
    def setUp(self):
        self.create_instances()
        self.add_account_legacy('liability', account_type=AccountType.Liability)
        self.add_account_legacy('asset')
        self.add_entry(transfer='expense', decrease='100')
        self.tpanel.load()
        self.stable.select([0]) # the liability split
        self.stable[0].credit = '50' # lower it to 50, creating an unassigned 50.
        self.stable.save_edits()
        self.stable.select([2])
        self.stable[2].account = 'liability'
        self.stable.save_edits()
        self.tpanel.save()
        self.clear_gui_calls()
        # we're now on etable, looking at 'asset'
    
    def test_efbar_increase_decrease(self):
        self.efbar.filter_type = FilterType.Income # increase
        eq_(len(self.etable), 0)
        self.efbar.filter_type = FilterType.Expense # decrease
        eq_(len(self.etable), 1)
        # now, let's go to the liability side
        self.mainwindow.select_balance_sheet()
        self.bsheet.selected = self.bsheet.liabilities[0]
        self.bsheet.show_selected_account()
        # we're still on FilterType.Expense (decrease)
        eq_(len(self.etable), 0)
        self.efbar.filter_type = FilterType.Income # increase
        eq_(len(self.etable), 1)
    
