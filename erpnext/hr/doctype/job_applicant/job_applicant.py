# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
from frappe.model.document import Document
import frappe
from frappe import _
from frappe.utils import comma_and

class JobApplicant(Document):
	def autoname(self):
		keys = filter(None, (self.applicant_name, self.email_id))
		if not keys:
			frappe.throw(_("Name or Email is mandatory"), frappe.NameError)
		self.name = " - ".join(keys)

	def validate(self):
		self.check_email_id_is_unique()

	def check_email_id_is_unique(self):
		if self.email_id:
			names = frappe.db.sql_list("""select name from `tabJob Application`
				where email_id=%s and name!=%s""", (self.email_id, self.name))

			if names:
				frappe.throw(_("Email id must be unique, already exists for {0}").format(comma_and(names)), frappe.DuplicateEntryError)

	def set_sender(self, sender):
		self.email_id = sender
