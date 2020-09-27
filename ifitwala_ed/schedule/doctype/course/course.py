# -*- coding: utf-8 -*-
# Copyright (c) 2020, ifitwala and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe 
import json 
from frappe import _
from frappe.model.document import Document

class Course(Document):
	pass

@frappe.whitelist()
def add_course_to_programs(course, programs, mandatory=False):
	programs = json.loads(programs)
	for entry in programs:
		program = frappe.get_doc('Program', entry)
		program.append('courses', {
			'course': course,
			'course_name': course,
			'mandatory': mandatory
		})
		program.flags.ignore_mandatory = True
		program.save()
	frappe.db.commit()
	frappe.msgprint(_('Course {0} has been added to all the selected programs successfully.').format(frappe.bold(course)),
		title=_('Programs updated'), indicator='green')

@frappe.whitelist()
def get_programs_without_course(course):
	data = []
	for entry in frappe.db.get_all('Program'):
		program = frappe.get_doc('Program', entry.name)
		courses = [c.course for c in program.courses]
		if not courses or course not in courses:
			data.append(program.name)
	return data