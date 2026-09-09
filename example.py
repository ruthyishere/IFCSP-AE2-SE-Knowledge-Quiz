"""
Mock, MagicMock, and patch learning sheet
=========================================

This file is deliberately unrelated to the quiz app. It uses a tiny online shop
example so you can practise the same testing ideas without copying an answer.

Useful documentation links found with fetch_webpage:
- unittest.mock: https://docs.python.org/3/library/unittest.mock.html
- where to patch: https://docs.python.org/3/library/unittest.mock.html#where-to-patch
- patch: https://docs.python.org/3/library/unittest.mock.html#patch
- MagicMock: https://docs.python.org/3/library/unittest.mock.html#magicmock-and-magic-method-support
- unittest basics: https://docs.python.org/3/library/unittest.html

Run this file as tests with either:
	python -m unittest -v example

or:
	python example.py
"""

import unittest
from unittest.mock import MagicMock, Mock, call, patch


# ---------------------------------------------------------------------------
# 1. Some tiny "production" code to test
# ---------------------------------------------------------------------------


class PaymentGateway:
	"""Pretend this talks to a real payment provider over the internet."""

	def charge(self, amount):
		# In real code this might call Stripe, PayPal, etc.
		# Unit tests should not call real payment systems.
		return f"receipt-for-{amount}"


class EmailClient:
	"""Pretend this sends real email."""

	def send(self, recipient, subject, body):
		# In real code this might call an SMTP server or email API.
		return True


def calculate_checkout_total(prices, tax_service):
	"""
	Function under test.

	It owns the subtotal calculation, but it asks another object for tax.
	That other object is a good candidate for Mock because this function only
	cares that it can call tax_service.calculate_tax(subtotal).
	"""
	subtotal = sum(prices)
	tax = tax_service.calculate_tax(subtotal)
	return subtotal + tax


def complete_purchase(email_address, amount):
	"""
	Function under test.

	It creates its own helper objects. Because the helpers are created inside
	the function, a test cannot pass in fake helpers directly. That is where
	patch() becomes useful.
	"""
	gateway = PaymentGateway()
	emailer = EmailClient()

	receipt_id = gateway.charge(amount)
	emailer.send(
		email_address,
		"Your receipt",
		f"Thank you for your purchase. Receipt: {receipt_id}",
	)

	return receipt_id


def build_summary(items, formatter):
	"""
	Function under test.

	The formatter is used repeatedly. This lets us practise side_effect,
	call_count, and call_args_list.
	"""
	lines = []
	for item in items:
		lines.append(formatter.format_line(item))
	return "\n".join(lines)


# This lets patch targets work both when the file is imported by unittest and
# when the file is run directly with python example.py.
MODULE_UNDER_TEST = __name__


# ---------------------------------------------------------------------------
# 2. Tests showing Mock
# ---------------------------------------------------------------------------


class MockBasicsTest(unittest.TestCase):
	def test_mock_return_value_and_assertion(self):
		"""
		A Mock is useful when your code needs to call another object.

		Here, calculate_checkout_total does not need a real tax website or tax
		calculator. It only needs an object with a calculate_tax method.
		"""
		tax_service = Mock()
		tax_service.calculate_tax.return_value = 2.50

		result = calculate_checkout_total([10.00, 15.00], tax_service)

		self.assertEqual(result, 27.50)

		# This checks the conversation between your function and the fake
		# dependency. The subtotal should have been passed to calculate_tax.
		tax_service.calculate_tax.assert_called_once_with(25.00)

	def test_mock_side_effect_as_list(self):
		"""
		side_effect can return a different value each time the mock is called.

		This is useful when the code under test loops and calls the same helper
		repeatedly. The first call gets the first side_effect value, and so on.
		"""
		formatter = Mock()
		formatter.format_line.side_effect = ["1. notebook", "2. pencil"]

		result = build_summary(["notebook", "pencil"], formatter)

		self.assertEqual(result, "1. notebook\n2. pencil")
		self.assertEqual(formatter.format_line.call_count, 2)

		# call_args_list records every call in order.
		self.assertEqual(
			formatter.format_line.call_args_list,
			[call("notebook"), call("pencil")],
		)

	def test_mock_side_effect_as_function(self):
		"""
		side_effect can also be a function.

		The side_effect function receives the same arguments that the mock
		received. Its return value becomes the mock's return value.
		"""
		formatter = Mock()

		def number_the_item(item):
			return f"Item: {item.upper()}"

		formatter.format_line.side_effect = number_the_item

		result = build_summary(["paper", "pen"], formatter)

		self.assertEqual(result, "Item: PAPER\nItem: PEN")


# ---------------------------------------------------------------------------
# 3. Tests showing MagicMock
# ---------------------------------------------------------------------------


class MagicMockBasicsTest(unittest.TestCase):
	def test_magicmock_supports_len_and_iteration(self):
		"""
		MagicMock is like Mock, but it already understands many Python special
		methods such as __len__, __iter__, __getitem__, and context managers.

		Use MagicMock when the fake object must behave like a list, dict, file,
		context manager, or other protocol-based object.
		"""
		fake_basket = MagicMock()
		fake_basket.__len__.return_value = 3
		fake_basket.__iter__.return_value = iter(["book", "lamp", "mug"])

		self.assertEqual(len(fake_basket), 3)
		self.assertEqual(list(fake_basket), ["book", "lamp", "mug"])

		# list(fake_basket) may also ask for len(fake_basket) as a length hint,
		# so checking "it was called" is more accurate than "called once" here.
		fake_basket.__len__.assert_called()

		# Magic method calls are stored in mock_calls.
		self.assertIn(call.__iter__(), fake_basket.mock_calls)

	def test_magicmock_can_fake_context_manager(self):
		"""
		A with-statement calls __enter__ and __exit__.

		MagicMock already has these methods, so it is convenient for replacing
		objects used in with blocks.
		"""
		fake_resource = MagicMock()
		fake_resource.__enter__.return_value = "connected"

		with fake_resource as connection:
			self.assertEqual(connection, "connected")

		fake_resource.__enter__.assert_called_once_with()
		fake_resource.__exit__.assert_called_once_with(None, None, None)


# ---------------------------------------------------------------------------
# 4. Tests showing patch
# ---------------------------------------------------------------------------


class PatchBasicsTest(unittest.TestCase):
	@patch(f"{MODULE_UNDER_TEST}.EmailClient", autospec=True)
	@patch(f"{MODULE_UNDER_TEST}.PaymentGateway", autospec=True)
	def test_patch_replaces_classes_temporarily(
		self,
		mock_payment_gateway_class,
		mock_email_client_class,
	):
		"""
		patch() temporarily replaces a name while this test runs.

			# list(fake_basket) may also ask for len(fake_basket) as a length hint,
			# so checking "it was called" is more accurate than "called once" here.
			fake_basket.__len__.assert_called()
		complete_purchase looks up PaymentGateway and EmailClient in this module,
		so this test patches those names in this module.

		With stacked decorators, mocks are passed into the test from the bottom
		decorator upward. PaymentGateway is the bottom patch, so its mock is the
		first extra parameter.
		"""
		fake_gateway_instance = mock_payment_gateway_class.return_value
		fake_email_instance = mock_email_client_class.return_value

		fake_gateway_instance.charge.return_value = "fake-receipt-123"

		result = complete_purchase("alex@example.com", 42.00)

		self.assertEqual(result, "fake-receipt-123")

		mock_payment_gateway_class.assert_called_once_with()
		mock_email_client_class.assert_called_once_with()

		fake_gateway_instance.charge.assert_called_once_with(42.00)
		fake_email_instance.send.assert_called_once_with(
			"alex@example.com",
			"Your receipt",
			"Thank you for your purchase. Receipt: fake-receipt-123",
		)

	def test_patch_as_context_manager(self):
		"""
		patch() can also be used with a with block.

		This is nice when the patch only matters for a few lines or when you do
		not want extra mock parameters in the test method signature.
		"""
		with patch(f"{MODULE_UNDER_TEST}.PaymentGateway", autospec=True) as mock_gateway_class:
			with patch(f"{MODULE_UNDER_TEST}.EmailClient", autospec=True) as mock_email_class:
				mock_gateway_class.return_value.charge.return_value = "context-receipt"

				result = complete_purchase("sam@example.com", 9.99)

		self.assertEqual(result, "context-receipt")
		mock_gateway_class.return_value.charge.assert_called_once_with(9.99)
		mock_email_class.return_value.send.assert_called_once()

	def test_patch_side_effect_for_multiple_instances(self):
		"""
		If patched code creates several instances, side_effect can provide a
		different fake instance each time the patched class is called.

		This example is intentionally small: calling PaymentGateway() twice will
		return first_gateway, then second_gateway.
		"""
		first_gateway = Mock()
		second_gateway = Mock()

		with patch(
			f"{MODULE_UNDER_TEST}.PaymentGateway",
			side_effect=[first_gateway, second_gateway],
		) as mock_gateway_class:
			first = PaymentGateway()
			second = PaymentGateway()

		self.assertIs(first, first_gateway)
		self.assertIs(second, second_gateway)
		self.assertEqual(mock_gateway_class.call_count, 2)


# ---------------------------------------------------------------------------
# 5. Common mental model
# ---------------------------------------------------------------------------


"""
Quick mental model
------------------

Mock:
	"I need a fake object or fake method, and I want to check how it was used."

MagicMock:
	"I need a fake object that also behaves like a Python protocol object:
	len(x), for x in y, x[0], with x as y, etc."

patch:
	"The code under test creates or imports the dependency itself, so I need to
	temporarily replace that dependency's name during the test."

return_value:
	"When this mock is called, always return this value."

side_effect as a list:
	"Return these values one at a time across repeated calls."

side_effect as a function:
	"Run this function whenever the mock is called."

assert_called_once_with(...):
	"The mock should have been called exactly once with these arguments."

call_args_list:
	"Show me every call that happened, in order."

The big patch rule:
	Patch the name where the code under test looks it up, not necessarily where
	that object was originally defined.
"""


if __name__ == "__main__":
	unittest.main(verbosity=2)
