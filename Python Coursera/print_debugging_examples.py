"""
Print Debugging Examples in Python
==================================

This file demonstrates various print debugging techniques to help you
track variable values, monitor program flow, and isolate errors in your code.
"""

import logging
import time
from datetime import datetime

# Set up logging for advanced debugging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('debug.log'),
        logging.StreamHandler()
    ]
)

def example_1_variable_tracking():
    """
    Example 1: Variable Tracking
    Shows how to track variable values throughout your program
    """
    print("\n=== Example 1: Variable Tracking ===")
    
    # Initial value
    x = 10
    print(f"Initial value of x: {x}")
    
    # After modification
    x = x * 2
    print(f"After multiplication: x = {x}")
    
    # After another operation
    x = x + 5
    print(f"After addition: x = {x}")
    
    # Final value
    print(f"Final value of x: {x}")

def example_2_function_entry_exit():
    """
    Example 2: Function Entry and Exit
    Shows how to mark the beginning and end of function execution
    """
    print("\n=== Example 2: Function Entry and Exit ===")
    
    def calculate_area(length, width):
        print(f"Entering calculate_area function with length={length}, width={width}")
        
        area = length * width
        print(f"Calculated area: {area}")
        
        print("Exiting calculate_area function")
        return area
    
    # Test the function
    result = calculate_area(5, 3)
    print(f"Function returned: {result}")

def example_3_loop_iteration():
    """
    Example 3: Loop Iteration
    Shows how to track loop progress and iterations
    """
    print("\n=== Example 3: Loop Iteration ===")
    
    # Simple loop tracking
    print("Starting loop iteration tracking:")
    for i in range(5):
        print(f"Loop iteration {i + 1}/5: i = {i}")
    
    # More complex loop with calculations
    print("\nComplex loop with calculations:")
    numbers = [1, 2, 3, 4, 5]
    total = 0
    
    for index, number in enumerate(numbers):
        print(f"Processing item {index + 1}/{len(numbers)}: {number}")
        total += number
        print(f"Running total: {total}")
    
    print(f"Final total: {total}")

def example_4_conditional_checks():
    """
    Example 4: Conditional Checks
    Shows how to debug decision-making flow in your code
    """
    print("\n=== Example 4: Conditional Checks ===")
    
    def check_eligibility(age, income):
        print(f"Checking eligibility for age={age}, income=${income}")
        
        if age >= 18:
            print("✓ Age requirement met (>= 18)")
        else:
            print("✗ Age requirement not met (< 18)")
            return False
        
        if income >= 50000:
            print("✓ Income requirement met (>= $50,000)")
        else:
            print("✗ Income requirement not met (< $50,000)")
            return False
        
        print("✓ All requirements met - eligible!")
        return True
    
    # Test cases
    print("Test case 1:")
    check_eligibility(25, 60000)
    
    print("\nTest case 2:")
    check_eligibility(16, 70000)
    
    print("\nTest case 3:")
    check_eligibility(30, 30000)

def example_5_formatting_output():
    """
    Example 5: Formatting Output
    Shows advanced formatting techniques for better debugging output
    """
    print("\n=== Example 5: Formatting Output ===")
    
    # Complex data structure
    user_data = {
        "name": "Alice Johnson",
        "age": 28,
        "email": "alice@example.com",
        "scores": [85, 92, 78, 96]
    }
    
    print("=== User Data Debug Info ===")
    print(f"Name: {user_data['name']}")
    print(f"Age: {user_data['age']}")
    print(f"Email: {user_data['email']}")
    print(f"Test Scores: {user_data['scores']}")
    print(f"Average Score: {sum(user_data['scores']) / len(user_data['scores']):.2f}")
    
    # Table-like formatting
    print("\n=== Score Analysis ===")
    for i, score in enumerate(user_data['scores'], 1):
        status = "PASS" if score >= 80 else "FAIL"
        print(f"Test {i:2d}: {score:3d} points - {status}")

def example_6_conditional_printing():
    """
    Example 6: Conditional Printing
    Shows how to control when debug messages are displayed
    """
    print("\n=== Example 6: Conditional Printing ===")
    
    # Debug flag to control output
    DEBUG_MODE = True
    
    def process_data(data, debug=False):
        if debug:
            print(f"Processing data: {data}")
        
        result = data * 2
        
        if debug:
            print(f"Result: {result}")
        
        return result
    
    # With debug enabled
    print("With debug enabled:")
    process_data(10, debug=True)
    
    # With debug disabled
    print("\nWith debug disabled:")
    process_data(10, debug=False)

def example_7_logging():
    """
    Example 7: Logging
    Shows how to use Python's logging module for structured debugging
    """
    print("\n=== Example 7: Logging ===")
    
    def complex_calculation(a, b, c):
        logging.debug(f"Starting calculation with a={a}, b={b}, c={c}")
        
        try:
            # Step 1: Validate inputs
            logging.info("Validating input parameters")
            if a <= 0 or b <= 0 or c <= 0:
                logging.warning("Negative or zero values detected")
                raise ValueError("All values must be positive")
            
            # Step 2: Perform calculation
            logging.debug("Performing intermediate calculations")
            intermediate = a * b
            logging.debug(f"Intermediate result: {intermediate}")
            
            result = intermediate / c
            logging.info(f"Calculation completed successfully: {result}")
            
            return result
            
        except Exception as e:
            logging.error(f"Error in calculation: {e}")
            raise
    
    # Test the logging function
    try:
        result = complex_calculation(10, 5, 2)
        print(f"Calculation result: {result}")
    except Exception as e:
        print(f"Error: {e}")

def example_8_complete_debugging_process():
    """
    Example 8: Complete Debugging Process
    Demonstrates the step-by-step debugging process
    """
    print("\n=== Example 8: Complete Debugging Process ===")
    
    def buggy_function(numbers):
        """
        This function has a bug - let's debug it step by step
        """
        print("=== Step 1: Identify suspicious code ===")
        print("Function called with:", numbers)
        
        total = 0
        print(f"Initial total: {total}")
        
        # Step 2: Insert print statements around suspicious code
        for i in range(len(numbers)):
            print(f"Processing index {i}: value = {numbers[i]}")
            total += numbers[i]
            print(f"Running total: {total}")
        
        # Step 3: Check final result
        print(f"Final total: {total}")
        
        # Step 4: Analyze output - what's wrong?
        # The bug: we're using range(len(numbers)) but numbers might be empty
        # or contain non-numeric values
        
        return total
    
    # Test cases to demonstrate the debugging process
    print("Test case 1: Normal list")
    result1 = buggy_function([1, 2, 3, 4, 5])
    print(f"Result: {result1}")
    
    print("\nTest case 2: Empty list")
    result2 = buggy_function([])
    print(f"Result: {result2}")
    
    print("\nTest case 3: List with non-numeric values")
    try:
        result3 = buggy_function([1, "two", 3])
        print(f"Result: {result3}")
    except Exception as e:
        print(f"Error caught: {e}")

def example_9_real_world_scenario():
    """
    Example 9: Real-World Debugging Scenario
    A practical example of debugging a data processing function
    """
    print("\n=== Example 9: Real-World Debugging Scenario ===")
    
    def process_user_orders(orders):
        """
        Process a list of user orders and calculate totals
        """
        print("=== Processing User Orders ===")
        print(f"Received {len(orders)} orders")
        
        total_revenue = 0
        processed_orders = 0
        errors = []
        
        for i, order in enumerate(orders, 1):
            print(f"\n--- Processing Order {i} ---")
            print(f"Order data: {order}")
            
            try:
                # Extract order details
                if isinstance(order, dict):
                    amount = order.get('amount', 0)
                    customer = order.get('customer', 'Unknown')
                else:
                    print(f"Warning: Order {i} is not a dictionary")
                    amount = 0
                    customer = 'Unknown'
                
                print(f"Customer: {customer}")
                print(f"Amount: ${amount}")
                
                # Validate amount
                if amount <= 0:
                    print(f"Warning: Invalid amount ${amount} for order {i}")
                    errors.append(f"Order {i}: Invalid amount ${amount}")
                    continue
                
                # Add to total
                total_revenue += amount
                processed_orders += 1
                print(f"Order {i} processed successfully")
                print(f"Running total: ${total_revenue}")
                
            except Exception as e:
                print(f"Error processing order {i}: {e}")
                errors.append(f"Order {i}: {e}")
        
        print(f"\n=== Processing Complete ===")
        print(f"Total orders processed: {processed_orders}")
        print(f"Total revenue: ${total_revenue}")
        print(f"Errors encountered: {len(errors)}")
        
        if errors:
            print("Errors:")
            for error in errors:
                print(f"  - {error}")
        
        return {
            'total_revenue': total_revenue,
            'processed_orders': processed_orders,
            'errors': errors
        }
    
    # Test with various scenarios
    test_orders = [
        {'customer': 'Alice', 'amount': 100},
        {'customer': 'Bob', 'amount': 50},
        {'customer': 'Charlie', 'amount': -10},  # Invalid amount
        {'customer': 'Diana', 'amount': 75},
        'invalid_order',  # Not a dictionary
        {'customer': 'Eve', 'amount': 200}
    ]
    
    result = process_user_orders(test_orders)
    print(f"\nFinal result: {result}")

def main():
    """
    Main function to run all debugging examples
    """
    print("Print Debugging Examples in Python")
    print("=" * 50)
    
    # Run all examples
    example_1_variable_tracking()
    example_2_function_entry_exit()
    example_3_loop_iteration()
    example_4_conditional_checks()
    example_5_formatting_output()
    example_6_conditional_printing()
    example_7_logging()
    example_8_complete_debugging_process()
    example_9_real_world_scenario()
    
    print("\n" + "=" * 50)
    print("All debugging examples completed!")
    print("Check the debug.log file for logging output.")

if __name__ == "__main__":
    main() 