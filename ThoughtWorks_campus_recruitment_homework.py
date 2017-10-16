#!/usr/bin/env python
# -*- coding: utf-8 -*-


import time
from datetime import datetime,timedelta,date

NO_MAINTENANCE = 0
TIME_RELATED_MAINTENANCE = 1
DISTANCE_RELATED_MAINTENANCE = 2
WRITE_OFF_MAINTENANCE = 3

def main():
	submit_date, cars = get_input()
	write_off_cars = dict()
	distance_related_maintenance_cars = dict()
	time_related_maintenance_cars = dict()
	for car in cars:
		notify_type = car.notify_maintenance(submit_date)
		if notify_type == NO_MAINTENANCE:
			continue
		elif notify_type == WRITE_OFF_MAINTENANCE:
			if write_off_cars.has_key(car.brand_name):
				write_off_cars[car.brand_name].append(car)
			else:
				write_off_cars[car.brand_name] = [car]
		elif notify_type == DISTANCE_RELATED_MAINTENANCE:
			if  distance_related_maintenance_cars.has_key(car.brand_name):
				distance_related_maintenance_cars[car.brand_name].append(car)
			else:
				distance_related_maintenance_cars[car.brand_name] = [car]
		elif notify_type == TIME_RELATED_MAINTENANCE:
			if time_related_maintenance_cars.has_key(car.brand_name):
				time_related_maintenance_cars[car.brand_name].append(car)
			else:
				time_related_maintenance_cars[car.brand_name] = [car]
		else:
			print "error: unknown notify type!"
	output(write_off_cars, distance_related_maintenance_cars, time_related_maintenance_cars)

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
	
	print '* Time-related maintenance coming soon...'
	for brand_name in sorted(time_related_maintenance_cars.keys()):
		license_plate_number_list = []
		for car in time_related_maintenance_cars[brand_name]:
			license_plate_number_list.append(car.license_plate_number)
		print "%s: %d (%s)" % (brand_name, len(time_related_maintenance_cars[brand_name]), ", ".join(license_plate_number_list))

	print '\n'
	print '* Distance-related maintenance coming soon...'
	for brand_name in sorted(distance_related_maintenance_cars.keys()):
		license_plate_number_list = []
		for car in distance_related_maintenance_cars[brand_name]:
			license_plate_number_list.append(car.license_plate_number)
		print "%s: %d (%s)" % (brand_name, len(distance_related_maintenance_cars[brand_name]), ", ".join(license_plate_number_list))

	print '\n'
	print '*Write-off coming soon...'
	for brand_name in sorted(write_off_cars.keys()):
		license_plate_number_list = []
		for car in write_off_cars[brand_name]:
			license_plate_number_list.append(car.license_plate_number)
		print "%s: %d (%s)" % (brand_name, len(write_off_cars[brand_name]), ", ".join(license_plate_number_list))

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
		if self.had_been_maintained:
			# assume the maintain time is the purchasing time
			maintenance_interval = 3
		elif submit_date.year - self.purchasing_date.year >= 3:
			maintenance_interval = 6
		else:
			maintenance_interval = 12
		month_interval = submit_date.year * 12 + submit_date.month - self.purchasing_date.year * 12 - self.purchasing_date.month
		# the reason of add 1 is that we need notify it before 1 month
		if (month_interval + 1) % maintenance_interval == 0:
			return True
		else:
			return False

	def is_notify_distance_related_maintenance(self):
		return self.running_distance >= 10000 - 500

	def is_notify_write_off(self, submit_date):
		if self.had_been_maintained:
			time_add = timedelta(days = 365 * 3)
		else:
			time_add = timedelta(days = 365 * 6)
		write_off_date = self.purchasing_date + time_add

		if write_off_date.month == 1:
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