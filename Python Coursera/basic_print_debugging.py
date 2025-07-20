"""
Basic Print Debugging Examples
==============================

This file demonstrates the five common ways to use print statements for debugging,
as described in the text about print debugging techniques.
"""

def example_1_variable_tracking():
    """
    Number 1: Variable Tracking
    Shows the current value of a variable to track its changes
    """
    print("=== Example 1: Variable Tracking ===")
    
    x = 10
    print(x)  # Simple print statement to show current value
    
    x = x * 2
    print(x)  # Track changes
    
    x = x + 5
    print(x)  # Final value

def example_2_function_entry():
    """
    Number 2: Function Entry
    Marks the beginning of a function's execution
    """
    print("=== Example 2: Function Entry ===")
    
    def calculate_area(length, width):
        print("Entering calculate_area function")  # Function entry marker
        area = length * width
        return area
    
    result = calculate_area(5, 3)
    print(f"Result: {result}")

def example_3_function_exit():
    """
    Number 3: Function Exit
    Marks the end of a function's execution
    """
    print("=== Example 3: Function Exit ===")
    
    def calculate_perimeter(length, width):
        perimeter = 2 * (length + width)
        print("Exiting calculate_perimeter function")  # Function exit marker
        return perimeter
    
    result = calculate_perimeter(4, 6)
    print(f"Result: {result}")

def example_4_loop_iteration():
    """
    Number 4: Loop Iteration
    Shows the current iteration number within a loop
    """
    print("=== Example 4: Loop Iteration ===")
    
    for i in range(5):
        print(i)  # Shows current iteration number
    
    print("\nWith more context:")
    for i in range(3):
        print(f"Loop iteration {i + 1}/3")  # More informative iteration tracking

def example_5_conditional_checks():
    """
    Number 5: Conditional Checks
    Provides feedback about whether a condition has been met
    """
    print("=== Example 5: Conditional Checks ===")
    
    age = 25
    income = 60000
    
    if age >= 18:
        print("Age requirement met")  # Conditional check feedback
    else:
        print("Age requirement not met")
    
    if income >= 50000:
        print("Income requirement met")  # Conditional check feedback
    else:
        print("Income requirement not met")

def example_advanced_formatting():
    """
    Advanced Technique 1: Formatting Output
    Uses f-strings for more informative and structured output
    """
    print("=== Advanced: Formatting Output ===")
    
    user_data = {"name": "Alice", "age": 28, "email": "alice@example.com"}
    
    # Using f-strings for better formatting
    print(f"Name: {user_data['name']}")
    print(f"Age: {user_data['age']}")
    print(f"Email: {user_data['email']}")

def example_conditional_printing():
    """
    Advanced Technique 2: Conditional Printing
    Uses if statements to control when debug messages are displayed
    """
    print("=== Advanced: Conditional Printing ===")
    
    DEBUG_MODE = True  # Control debug output
    
    def process_data(data):
        if DEBUG_MODE:
            print(f"Processing data: {data}")  # Only prints if DEBUG_MODE is True
        
        result = data * 2
        
        if DEBUG_MODE:
            print(f"Result: {result}")  # Only prints if DEBUG_MODE is True
        
        return result
    
    process_data(10)

def example_logging():
    """
    Advanced Technique 3: Logging
    Uses Python's logging module for structured logs
    """
    print("=== Advanced: Logging ===")
    
    import logging
    
    # Set up basic logging
    logging.basicConfig(level=logging.DEBUG)
    
    def complex_function():
        logging.debug("Starting complex_function")  # Debug level message
        logging.info("Processing data")  # Info level message
        logging.warning("This is a warning")  # Warning level message
        logging.error("This is an error")  # Error level message
    
    complex_function()

def complete_debugging_process():
    """
    Demonstrates the complete debugging process step by step
    """
    print("=== Complete Debugging Process ===")
    
    def buggy_function(numbers):
        """
        Step 1: Identify suspicious code sections
        This function has a potential bug with empty lists
        """
        print("Function called with:", numbers)  # Step 2: Insert print statements
        
        total = 0
        print(f"Initial total: {total}")
        
        for i in range(len(numbers)):
            print(f"Processing index {i}: value = {numbers[i]}")  # Track loop progress
            total += numbers[i]
            print(f"Running total: {total}")
        
        print(f"Final total: {total}")  # Step 3: Check final result
        return total
    
    # Step 4: Run code and analyze output
    print("Test case 1: Normal list")
    result1 = buggy_function([1, 2, 3])
    print(f"Result: {result1}")
    
    print("\nTest case 2: Empty list")
    result2 = buggy_function([])
    print(f"Result: {result2}")
    
    # Step 5: Pinpoint the error
    # The function works with normal lists but shows no output for empty lists
    # This helps identify the issue
    
    # Step 6: Iterate and refine (fix the bug)
    def fixed_function(numbers):
        print("Function called with:", numbers)
        
        if len(numbers) == 0:
            print("Empty list detected")
            return 0
        
        total = 0
        print(f"Initial total: {total}")
        
        for i in range(len(numbers)):
            print(f"Processing index {i}: value = {numbers[i]}")
            total += numbers[i]
            print(f"Running total: {total}")
        
        print(f"Final total: {total}")
        return total
    
    print("\nFixed function test:")
    fixed_result = fixed_function([])
    print(f"Fixed result: {fixed_result}")

def main():
    """
    Run all the basic print debugging examples
    """
    print("Basic Print Debugging Examples")
    print("=" * 40)
    
    # Run the five basic examples
    example_1_variable_tracking()
    example_2_function_entry()
    example_3_function_exit()
    example_4_loop_iteration()
    example_5_conditional_checks()
    
    print("\n" + "=" * 40)
    print("Advanced Techniques:")
    
    # Run advanced examples
    example_advanced_formatting()
    example_conditional_printing()
    example_logging()
    
    print("\n" + "=" * 40)
    print("Complete Debugging Process:")
    
    # Run complete process example
    complete_debugging_process()
    
    print("\n" + "=" * 40)
    print("All examples completed!")

if __name__ == "__main__":
    main() 