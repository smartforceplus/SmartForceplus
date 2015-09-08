
from openerp.osv import fields, osv
from openerp.tools.translate import _
import re
import logging
_logger = logging.getLogger(__name__)

class opportunity_customer(osv.osv_memory):
    _name = 'opportunity.customer'
    _description = 'Opportunity'

    _columns = {
        'name': fields.selection([
                ('exist', 'Link to an existing customer'),
                ('create', 'Create a new customer'),
                
            ], 'Conversion Action', required=True),
        'partner_id': fields.many2one('res.partner', 'Customer'),
    }

    def view_init(self, cr, uid, fields, context=None):
        """
        Check some preconditions before the wizard executes.
        """
        if context is None:
            context = {}
        lead_obj = self.pool.get('crm.lead')
        return False

    def onchange_action(self, cr, uid, ids, name, context=None):
        return {'value': {'partner_id': False if name != 'exist' else self._find_matching_partner(cr, uid, context=context)}}

    def _find_matching_partner(self, cr, uid, context=None):
        """
        Try to find a matching partner regarding the active model data, like
        the customer's name, email, phone number, etc.

        :return int partner_id if any, False otherwise
        """
        if context is None:
            context = {}
        partner_id = False
        partner_obj = self.pool.get('res.partner')
        _logger.info('\n\n\n context %s',context)
        # The active model has to be a lead or a phonecall
        if (context.get('active_model') == 'crm.lead') and context.get('active_id'):
            active_model = self.pool.get('crm.lead').browse(cr, uid, context.get('active_id'), context=context)
        elif (context.get('active_model') == 'crm.phonecall') and context.get('active_id'):
            active_model = self.pool.get('crm.phonecall').browse(cr, uid, context.get('active_id'), context=context)

        # Find the best matching partner for the active model
        if (active_model):
            partner_obj = self.pool.get('res.partner')

            # A partner is set already
            if active_model.partner_id:
                partner_id = active_model.partner_id.id
            # Search through the existing partners based on the lead's email
            elif active_model.email_from:
                partner_ids = partner_obj.search(cr, uid, [('email', '=', active_model.email_from)], context=context)
                if partner_ids:
                    partner_id = partner_ids[0]
            # Search through the existing partners based on the lead's partner or contact name
            elif active_model.partner_name:
                partner_ids = partner_obj.search(cr, uid, [('name', 'ilike', '%'+active_model.partner_name+'%')], context=context)
                if partner_ids:
                    partner_id = partner_ids[0]
            elif active_model.contact_name:
                partner_ids = partner_obj.search(cr, uid, [
                        ('name', 'ilike', '%'+active_model.contact_name+'%')], context=context)
                if partner_ids:
                    partner_id = partner_ids[0]

        return partner_id

    def action_apply(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        lead = self.pool.get('crm.lead')
        res = False
        lead_ids = context.get('active_id')
        data = self.browse(cr, uid, ids, context=context)[0]
        partner_id = data.partner_id.id
        leads = lead.browse(cr, uid, lead_ids, context=context)
        _logger.info('oppppppppppppppppporrrrrrrrrrrr')
        for lead_id in self.browse(cr, uid, ids, context=context):
            _logger.info('\n\n\n leads %s',leads.id)
            partner_id = self._create_partner(cr, uid, leads.id, data.name, partner_id or leads.partner_id.id, context=context)
        return True

    def _create_partner(self, cr, uid, lead_id, name, partner_id, context=None):
        """
        Create partner based on action.
        :return dict: dictionary organized as followed: {lead_id: partner_assigned_id}
        """
        #TODO this method in only called by crm_lead2opportunity_partner
        #wizard and would probably diserve to be refactored or at least
        #moved to a better place
        if context is None:
            context = {}
        lead = self.pool.get('crm.lead')
        if name == 'create' or name == 'exist':
            ctx = dict(context)
            ctx['active_id'] = lead_id
            _logger.info('\n\n\ _create_partner ctx %s',ctx)
            partner_id = self._find_matching_partner(cr, uid, context=ctx)
            name = 'create'
        res = lead.handle_partner_assignation(cr, uid, [lead_id], name, partner_id, context=context)
        _logger.info('resssssssssssssssssssssssssssss')
        return res.get(lead_id)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
