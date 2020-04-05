# Orders 
[![Build Status](https://travis-ci.org/NYU-Devops-orders/orders.svg?branch=master)](https://travis-ci.org/NYU-Devops-orders/orders)

This repository contains sample code for Customer orders for an e-commerce web site. This shows how to create a REST API with subordinate resources like orders that have products:

Note: This repo has a Vagrantfile so the easiest way to play with it is to:

vagrant up
vagrant ssh
cd /vagrant
nosetests
flask run -h 0.0.0.0
These are the RESTful routes for orders and products

Endpoint          Methods  Rule
----------------  -------  -----------------------------------------------------
index             GET      /

list_orders     GET      /orders
create_orders   POST     /orders
get_orders      GET      /orders/<order_id>
update_orders   PUT      /orders/<order_id>
delete_orders   DELETE   /orders/<order_id>

list_products    GET      /orders/<int:order_id>/products
create_products  POST     /orders/<order_id>/products
get_products     GET      /orders/<order_id>/products/<product_id>
update_products  PUT      /orders/<order_id>/products/<product_id>
delete_products  DELETE   /orders/<order_id>/products/<product_id>
The test cases have 95% test coverage and can be run with nosetests
