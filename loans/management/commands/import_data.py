from django.core.management.base import BaseCommand
from django.db import connection
from loans.models import Customer, Loan
import pandas as pd
from datetime import datetime
from decimal import Decimal


class Command(BaseCommand):
    help = 'Import customer and loan data from Excel files'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Starting data import...'))
        
        # Clear existing data
        self.stdout.write('Clearing existing data...')
        Loan.objects.all().delete()
        Customer.objects.all().delete()
        
        # Import customers
        self.import_customers()
        
        # Import loans
        self.import_loans()
        
        # Reset PostgreSQL sequences
        self.reset_sequences()
        
        self.stdout.write(self.style.SUCCESS('Data import completed successfully!'))
    
    def import_customers(self):
        self.stdout.write('Importing customers...')
        
        try:
            # Read customer data
            df = pd.read_excel('customer_data.xlsx')
            
            customers_created = 0
            for index, row in df.iterrows():
                customer = Customer.objects.create(
                    customer_id=int(row['Customer ID']),
                    first_name=str(row['First Name']),
                    last_name=str(row['Last Name']),
                    age=int(row['Age']) if pd.notna(row.get('Age')) else 25,
                    phone_number=int(row['Phone Number']),
                    monthly_salary=Decimal(str(row['Monthly Salary'])),
                    approved_limit=Decimal(str(row['Approved Limit'])),
                    current_debt=Decimal(str(row.get('Current Debt', 0)))
                )
                customers_created += 1
            
            self.stdout.write(self.style.SUCCESS(f'✓ Imported {customers_created} customers'))
        
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('Error: customer_data.xlsx not found!'))
            self.stdout.write('Please place customer_data.xlsx in the project root directory')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing customers: {str(e)}'))
    
    def import_loans(self):
        self.stdout.write('Importing loans...')
        
        try:
            # Read loan data
            df = pd.read_excel('loan_data.xlsx')
            
            loans_created = 0
            loans_skipped = 0
            
            for index, row in df.iterrows():
                try:
                    # Get the customer
                    customer = Customer.objects.get(customer_id=int(row['Customer ID']))
                    
                    # Parse dates
                    start_date = pd.to_datetime(row['Date of Approval']).date()
                    end_date = pd.to_datetime(row['End Date']).date()
                    
                    # Create loan with explicit loan_id
                    loan = Loan.objects.create(
                        loan_id=int(row['Loan ID']),
                        customer=customer,
                        loan_amount=Decimal(str(row['Loan Amount'])),
                        tenure=int(row['Tenure']),
                        interest_rate=Decimal(str(row['Interest Rate'])),
                        monthly_repayment=Decimal(str(row['Monthly payment'])),
                        emis_paid_on_time=int(row['EMIs paid on Time']),
                        start_date=start_date,
                        end_date=end_date
                    )
                    loans_created += 1
                
                except Customer.DoesNotExist:
                    self.stdout.write(self.style.WARNING(
                        f'Warning: Customer ID {int(row["Customer ID"])} not found. Skipping loan.'
                    ))
                    loans_skipped += 1
                except Exception as e:
                    self.stdout.write(self.style.WARNING(
                        f'Warning: Error creating loan: {str(e)}'
                    ))
                    loans_skipped += 1
            
            self.stdout.write(self.style.SUCCESS(f'✓ Imported {loans_created} loans'))
            if loans_skipped > 0:
                self.stdout.write(self.style.WARNING(f'⚠ Skipped {loans_skipped} loans'))
        
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('Error: loan_data.xlsx not found!'))
            self.stdout.write('Please place loan_data.xlsx in the project root directory')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing loans: {str(e)}'))
    
    def reset_sequences(self):
        """Reset PostgreSQL sequences after importing data with explicit IDs"""
        self.stdout.write('Resetting database sequences...')
        
        try:
            with connection.cursor() as cursor:
                # Reset customer_id sequence
                cursor.execute("""
                    SELECT setval(pg_get_serial_sequence('customers', 'customer_id'), 
                           COALESCE((SELECT MAX(customer_id) FROM customers), 1), 
                           true);
                """)
                
                # Reset loan_id sequence
                cursor.execute("""
                    SELECT setval(pg_get_serial_sequence('loans', 'loan_id'), 
                           COALESCE((SELECT MAX(loan_id) FROM loans), 1), 
                           true);
                """)
            
            self.stdout.write(self.style.SUCCESS('✓ Database sequences reset'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error resetting sequences: {str(e)}'))