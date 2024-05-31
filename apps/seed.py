import uuid
from datetime import datetime, timezone

from apps.authentication.models import CustomUser
from apps.customer.models import Customer
from apps.customer.services import CustomerService
from apps.loans.services import LoanService

from faker import Faker

fake = Faker()


def create_admin_users():
	CustomUser.objects.create_user('test_drive', 'gabriel@wearemo.com', 'password', id="1", is_staff=True)


def create_customer():
	score = fake.random_number(digits=9)
	return Customer.objects.create(status=1, external_id=uuid.uuid4(), score=float(score))


def create_payment(customer):
	number_of_payments = fake.random_int(min=1, max=10)
	for _ in range(number_of_payments):
		CustomerService.make_payment(customer.external_id, fake.random_number(digits=7))


def create_loans(customer):
	number_of_loans = fake.random_int(min=2, max=5)
	for _ in range(number_of_loans):
		loan_amount = fake.random_number(digits=7)
		loan = LoanService.create_loan(user_id=customer.external_id, loan_amount=loan_amount, loan_details={
			'external_id': uuid.uuid4(),
			'maximum_payment_date': datetime.now(timezone.utc)
		})
		LoanService.change_load_status(loan_id=loan.external_id, status=2)


def main():
	create_admin_users()
	number_of_customers = fake.random_int(min=10, max=20)
	for _ in range(number_of_customers):
		customer = create_customer()
		create_loans(customer)
		create_payment(customer)


if __name__ == "__main__":
	main()


