#!/usr/bin/env python
# -*- coding: utf-8 -*-


import time
from datetime import datetime

NO_MAINTENANCE = 0
TIME_RELATED_MAINTENANCE = 1
DISTANCE_RELATED_MAINTENANCE = 2
WRITE_OFF_MAINTENANCE = 3

def main():
	submit_date, cars = get_input()
	no_maintenance_cars = []
	write_off_cars = []
	distance_related_maintenance_cars = []
	time_related_maintenance_cars = []
	for car in cars:
		notify_type = car.notify_maintenance(submit_date)
		if notify_type == NO_MAINTENANCE:
			continue
		elif notify_type == WRITE_OFF_MAINTENANCE:
			write_off_cars.append(car)
		elif notify_type == DISTANCE_RELATED_MAINTENANCE:
			distance_related_maintenance_cars.append(car)
		elif notify_type == TIME_RELATED_MAINTENANCE:
			time_related_maintenance_cars.append(car)
		else:
			print "error: unknown notify type!"


def get_input():
	with open('./ThoughtWorks_campus_recruitment_homework.input') as f:
		lines = f.readlines()
	cars = []
	for line in lines:
		# print line
		if line.startswith('SubmitDate'):
			submit_date = datetime.strptime(line.split(':')[1].strip(), '%Y/%m/%d').date()
			# print 'SubmitDate: ', submit_date_str
		else :
			t_car = line.split('|')
			car = Car(t_car[0].strip(), t_car[1].strip(), t_car[2].strip(), t_car[3].strip(), t_car[4].strip())
			cars.append(car)
	return submit_date, cars

def output(write_off_cars, distance_related_maintenance_cars, time_related_maintenance_cars):
	print 'Reminder'
	print '=================='
	print '\n'
	print '* Time-related maintenance coming soon...'
	for car in time_related_maintenance_cars:
		pass

class Car(object):
	def __init__(self, license_plate_number, purchasing_date, brand_name, running_distance, had_been_maintained):
		super(Car, self).__init__()
		self.license_plate_number = license_plate_number
		self.purchasing_date = datetime.strptime(purchasing_date, '%Y/%m/%d').date()
		self.brand_name = brand_name
		self.running_distance = int(running_distance)
		if had_been_maintained == 'T':
			self.had_been_maintained = True
		elif had_been_maintained == 'F':
			self.had_been_maintained = False
		else :
			print "error input:", had_been_maintained

	def is_notify_time_related_maintenance(self, submit_date):

		return False

	def is_notify_distance_related_maintenance(self):
		return self.running_distance >= 10000 - 500

	def is_notify_write_off(self, submit_date):
		if self.had_been_maintained:
			time_add = timedelta(days = 365 * 3)
		else:
			time_add = timedelta(days = 365 * 6)
		write_off_date = self.purchasing_date + time_del

		if write_off_date.month > 1:
			notify_date = date(write_off_date.year - 1, 12, 1)
		else:
			notify_date = date(write_off_date.year, write_off_date.month - 1, 1)

		if submit_date > notify_date:
			return True
		else:
			return False

	def  notify_maintenance(self, submit_date):
		if self.is_notify_write_off(submit_date):
			return WRITE_OFF_MAINTENANCE
		elif self.is_notify_distance_related_maintenance():
			return DISTANCE_RELATED_MAINTENANCE
		elif self.is_notify_time_related_maintenance(submit_date):
			return TIME_RELATED_MAINTENANCE
		else:
			return NO_MAINTENANCE

	def to_string(self):
		return 'Car[' + self.license_plate_number + ' ' + self.purchasing_date.strftime("%Y/%m/%d") + ' ' + self.brand_name + ' ' + str(self.running_distance) + ' ' + str(self.had_been_maintained) + ']'
		
if __name__ == '__main__':
	main()