# Copyright 2016, 2019 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Test Factory to make fake objects for testing
"""
#from datetime import datetime
import factory
from factory.fuzzy import FuzzyChoice
from service.models import Order, Product

class ProductFactory(factory.Factory):
    """ Creates fake Products """

    class Meta:
        """ Creates fake Products """
        model = Product

    id = factory.Sequence(lambda n: n)
#	order_id = ???
    name = factory.Faker("name")
    price = factory.fuzzy.FuzzyInteger(0, 100)
    quantity = factory.fuzzy.FuzzyInteger(0, 10)


class OrderFactory(factory.Factory):
    """ Creates fake Orders """

    class Meta:
        """ Creates fake Orders """
        model = Order

    id = factory.Sequence(lambda n: n)
    name = factory.Faker("name")
    status = FuzzyChoice(choices=["Delivered", "In Progress", "Cancelled"])
