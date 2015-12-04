# -*- coding: utf-8 -*-
#
#    Author: Yannick Vaucher, ported by Denis Leemann
#    Copyright 2015 Camptocamp SA
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from openerp.osv import orm, fields

class ProjetctTask(orm.Model):
    _inherit = 'project.task'

    # TOTEST
    def _get_invoiced_hours(self, cr, uid, ids, context=None):
        import pdb; pdb.set_trace()
        """ Sum timesheet line invoiced hours """
        res = {}
        for task in self.browse(cr, uid, ids, context=context):
            res[task.id] = sum(l.invoiced_hours for l in task.work_ids)
        return res

    ## TODO Check fieldnames parameter
    def _get_analytic_line(self, cr, uid, ids, arg, context=None):
        import pdb; pdb.set_trace()
        result = []
        for aal in self.pool['account.analytic.line'].browse(cr, uid, ids, context=context):
            if aal.task_id:
                result.append(aal.taks_id.id)
        return result

    #TOTEST
    def _get_remaining_hours(self, cr ,uid , ids, context=None):
        import pdb; pdb.set_trace()
        res = {}
        for task in self.browse(cr, uid, ids, context=context):
            remaining_hours = task.planned_hours - task.invoiced_hours
            res[task.id] = remaining_hours
        return res

    _columns ={
        'invoiced_hours': fields.function(
            _get_invoiced_hours,
            type='float',
            store={'project.task': (lambda self, cr, uid, ids, c=None: ids,
                                    ['work_ids'], 20),
                    'account.analytic.line': (_get_analytic_line,
                                                ['task_id', 'invoiced_hours'],20)
                }
            ),
        'remaining_hours': fields.function(
            _get_remaining_hours,
            type='float',
            store={'project.task': (lambda self, cr, uid, ids, c=None: ids,
                                    ['planned_hours', 'invoiced_hours'],20),
                }
            ),
    }
    
