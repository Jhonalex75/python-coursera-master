"""
Simple Debugging Examples
=========================

Practical examples of debugging techniques for Python developers.
"""

import logging

# Set up basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ============================================================================
# 1. PRINT STATEMENTS - Quick debugging
# ============================================================================

def print_debugging_example():
    """Demonstrates print statements for quick debugging"""
    print("\n=== PRINT STATEMENTS ===")
    
    def calculate_average(numbers):
        # Add print statements to track execution
        print(f"Input: {numbers}")
        
        total = sum(numbers)
        print(f"Total: {total}")
        
        count = len(numbers)
        print(f"Count: {count}")
        
        if count == 0:
            print("Warning: Empty list!")
            return 0
        
        average = total / count
        print(f"Average: {average}")
        
        return average
    
    # Test the function
    print("Test 1: Normal data")
    result1 = calculate_average([10, 20, 30])
    print(f"Result: {result1}")
    
    print("\nTest 2: Empty list")
    result2 = calculate_average([])
    print(f"Result: {result2}")

# ============================================================================
# 2. LOGGING - Detailed tracking
# ============================================================================

def logging_example():
    """Demonstrates logging for detailed event tracking"""
    print("\n=== LOGGING ===")
    
    def process_user(user_data):
        logging.info(f"Processing user: {user_data.get('name', 'Unknown')}")
        
        # Check required fields
        if 'age' not in user_data:
            logging.warning("Missing age field")
            return False
        
        if 'email' not in user_data:
            logging.warning("Missing email field")
            return False
        
        # Validate age
        age = user_data['age']
        if age < 0 or age > 120:
            logging.error(f"Invalid age: {age}")
            return False
        
        # Validate email
        email = user_data['email']
        if '@' not in email:
            logging.error(f"Invalid email: {email}")
            return False
        
        logging.info("User processed successfully")
        return True
    
    # Test cases
    users = [
        {'name': 'Alice', 'age': 25, 'email': 'alice@example.com'},
        {'name': 'Bob', 'age': -5, 'email': 'bob@example.com'},
        {'name': 'Charlie', 'age': 30, 'email': 'invalid-email'},
        {'name': 'Diana', 'age': 35}  # Missing email
    ]
    
    for user in users:
        success = process_user(user)
        print(f"{user.get('name', 'Unknown')}: {'SUCCESS' if success else 'FAILED'}")

# ============================================================================
# 3. ASSERTIONS - Validation
# ============================================================================

def assertion_example():
    """Demonstrates assertions for input validation"""
    print("\n=== ASSERTIONS ===")
    
    def calculate_area(length, width):
        # Assertions to validate inputs
        assert length > 0, f"Length must be positive, got {length}"
        assert width > 0, f"Width must be positive, got {width}"
        assert isinstance(length, (int, float)), f"Length must be numeric, got {type(length)}"
        assert isinstance(width, (int, float)), f"Width must be numeric, got {type(width)}"
        
        area = length * width
        return area
    
    # Test valid cases
    print("Valid cases:")
    try:
        area1 = calculate_area(5, 3)
        print(f"Area: {area1}")
    except AssertionError as e:
        print(f"Assertion failed: {e}")
    
    # Test invalid cases
    print("\nInvalid cases:")
    test_cases = [
        ("Negative length", lambda: calculate_area(-5, 3)),
        ("Zero width", lambda: calculate_area(5, 0)),
        ("String input", lambda: calculate_area("5", 3))
    ]
    
    for description, test_func in test_cases:
        try:
            result = test_func()
            print(f"{description}: {result}")
        except AssertionError as e:
            print(f"{description}: {e}")

# ============================================================================
# 4. DEBUGGER CONCEPTS
# ============================================================================

def debugger_example():
    """Demonstrates debugger concepts"""
    print("\n=== DEBUGGER CONCEPTS ===")
    
    def complex_function(data):
        print("Starting complex function...")
        
        # This is where you would set a breakpoint in your IDE
        # breakpoint()  # Uncomment to use Python's built-in breakpoint
        
        result = 0
        for i, value in enumerate(data):
            print(f"Processing item {i}: {value}")
            
            if value > 0:
                result += value * 2
            else:
                result += abs(value)
            
            print(f"Running total: {result}")
        
        print(f"Final result: {result}")
        return result
    
    # Test the function
    test_data = [10, -5, 20, -3, 15]
    result = complex_function(test_data)
    
    print(f"\nTo use a debugger:")
    print("1. Set breakpoints in your IDE")
    print("2. Run in debug mode")
    print("3. Step through code line by line")
    print("4. Inspect variables at each step")

# ============================================================================
# 5. MEMORY LEAK SIMULATION
# ============================================================================

def memory_leak_simulation():
    """Simulates the memory leak case study"""
    print("\n=== MEMORY LEAK SIMULATION ===")
    
    class ImageProcessor:
        def __init__(self):
            self.processed_images = []
            self.memory_usage = 0
        
        def process_without_cleanup(self, image_data):
            """Buggy version - causes memory leak"""
            processed = f"processed_{image_data}"
            self.processed_images.append(processed)  # BUG: Never removed
            self.memory_usage += len(processed)
            return processed
        
        def process_with_cleanup(self, image_data):
            """Fixed version - proper cleanup"""
            processed = f"processed_{image_data}"
            self.memory_usage += len(processed)
            return processed  # No accumulation
    
    # Test both versions
    buggy = ImageProcessor()
    fixed = ImageProcessor()
    
    test_images = [f"image_{i}" for i in range(5)]
    
    print("Buggy version (memory leak):")
    for image in test_images:
        buggy.process_without_cleanup(image)
        print(f"Memory usage: {buggy.memory_usage}, Images in memory: {len(buggy.processed_images)}")
    
    print("\nFixed version (proper cleanup):")
    for image in test_images:
        fixed.process_with_cleanup(image)
        print(f"Memory usage: {fixed.memory_usage}")
    
    print(f"\nFinal comparison:")
    print(f"Buggy version: {len(buggy.processed_images)} images accumulated")
    print(f"Fixed version: No accumulation")

# ============================================================================
# 6. COMPLETE DEBUGGING WORKFLOW
# ============================================================================

def complete_workflow_example():
    """Demonstrates a complete debugging workflow"""
    print("\n=== COMPLETE DEBUGGING WORKFLOW ===")
    
    def buggy_function(data_list):
        """Function with potential bugs"""
        print(f"Processing {len(data_list)} items")
        
        total = 0
        valid_count = 0
        errors = []
        
        for i, item in enumerate(data_list):
            print(f"Processing item {i + 1}: {item}")
            
            try:
                # Add assertions for validation
                assert isinstance(item, dict), f"Item {i} is not a dictionary"
                assert 'value' in item, f"Item {i} missing 'value'"
                
                value = item['value']
                assert isinstance(value, (int, float)), f"Value must be numeric"
                assert value >= 0, f"Value must be non-negative"
                
                total += value
                valid_count += 1
                print(f"  Valid item. Running total: {total}")
                
            except AssertionError as e:
                error_msg = f"Item {i}: {e}"
                print(f"  Error: {error_msg}")
                errors.append(error_msg)
            
            except Exception as e:
                error_msg = f"Item {i}: Unexpected error - {e}"
                print(f"  Error: {error_msg}")
                errors.append(error_msg)
        
        result = {
            'total': total,
            'valid_count': valid_count,
            'error_count': len(errors),
            'errors': errors
        }
        
        print(f"Final result: {result}")
        return result
    
    # Test with problematic data
    test_data = [
        {'value': 100},
        {'value': -50},  # Negative value
        {'name': 'test'},  # Missing value
        'not_a_dict',  # Wrong type
        {'value': 200}
    ]
    
    result = buggy_function(test_data)
    
    print(f"\nSummary:")
    print(f"Total value: {result['total']}")
    print(f"Valid items: {result['valid_count']}")
    print(f"Errors: {result['error_count']}")

def main():
    """Run all debugging examples"""
    print("Simple Debugging Examples")
    print("=" * 40)
    
    print_debugging_example()
    logging_example()
    assertion_example()
    debugger_example()
    memory_leak_simulation()
    complete_workflow_example()
    
    print("\n" + "=" * 40)
    print("All examples completed!")
    print("\nKey Points:")
    print("• Print statements: Quick, immediate feedback")
    print("• Logging: Structured, persistent tracking")
    print("• Assertions: Early error detection")
    print("• Debuggers: Deep inspection capabilities")
    print("• Combine techniques for comprehensive debugging")

if __name__ == "__main__":
    main() 