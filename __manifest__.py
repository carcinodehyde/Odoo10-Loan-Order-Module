# -*- coding: utf-8 -*-
##############################################################################
#
# This module is developed by Deddy Setiawan
# Copyright (C) 2017 Deddy Setiawan (<http://dedset.xyz>).
# All Rights Reserved
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name' : 'Engineers Learning Task 16',
    'version' : '1.0.0',
    'summary': 'Engineers Learning Task 16',
    'author' : 'PCI, Deddy Setiawan',
    'category': 'Purchases',
    'description': """
    - add loan order module
    """,
    'license':'LGPL-3',
    'depends' : ['base', 'purchase',],
    'data': [
    'views/loan_order_menu_view.xml',
    'views/loan_order_list_view.xml',
    'views/loan_order_form_view.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
