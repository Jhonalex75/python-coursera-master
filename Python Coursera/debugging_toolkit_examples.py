"""
Debugging Toolkit: Essential Techniques for Python Developers
============================================================

This file demonstrates various debugging techniques including:
1. Print statements for quick debugging
2. Logging for detailed event tracking
3. Assertions for validation
4. Debugger usage examples
5. Real-world debugging scenarios
"""

import logging
import time
import sys
from datetime import datetime
from typing import List, Dict, Any
import traceback

# Set up comprehensive logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(funcName)s - %(message)s',
    handlers=[
        logging.FileHandler('debug_toolkit.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

# ============================================================================
# 1. PRINT STATEMENTS: Your code's narrator
# ============================================================================

def example_print_statements():
    """
    Demonstrates how print statements can be used for quick debugging
    """
    print("\n" + "="*60)
    print("1. PRINT STATEMENTS: Your code's narrator")
    print("="*60)
    
    def calculate_average_basic(numbers):
        """Basic function without debugging"""
        total = sum(numbers)
        count = len(numbers)
        return total / count
    
    def calculate_average_with_prints(numbers):
        """Same function with print statements for debugging"""
        print("Input numbers:", numbers)
        total = sum(numbers)
        print("Total:", total)
        count = len(numbers)
        print("Count:", count)
        average = total / count
        print("Average:", average)
        return average
    
    # Test with normal data
    print("Testing with normal data:")
    result1 = calculate_average_basic([10, 20, 30, 40])
    print(f"Basic result: {result1}")
    
    print("\nTesting with debugging prints:")
    result2 = calculate_average_with_prints([10, 20, 30, 40])
    print(f"Debugged result: {result2}")
    
    # Test with problematic data
    print("\nTesting with empty list (will cause error):")
    try:
        result3 = calculate_average_with_prints([])
    except ZeroDivisionError as e:
        print(f"Error caught: {e}")
        print("The print statements helped us see that count was 0!")

# ============================================================================
# 2. LOGGING: A detailed chronicle of events
# ============================================================================

def example_logging():
    """
    Demonstrates logging for tracking issues in larger programs
    """
    print("\n" + "="*60)
    print("2. LOGGING: A detailed chronicle of events")
    print("="*60)
    
    def process_user_data(user_data: Dict[str, Any]) -> bool:
        """
        Process user data with comprehensive logging
        """
        logging.info(f"Starting to process user data for user: {user_data.get('name', 'Unknown')}")
        
        try:
            # Validate user data
            logging.debug("Validating user data structure")
            required_fields = ['name', 'age', 'email']
            
            for field in required_fields:
                if field not in user_data:
                    logging.warning(f"Missing required field: {field}")
                    return False
            
            # Process age
            age = user_data['age']
            logging.debug(f"Processing age: {age}")
            
            if age < 0 or age > 120:
                logging.error(f"Invalid age value: {age}")
                return False
            
            # Process email
            email = user_data['email']
            logging.debug(f"Processing email: {email}")
            
            if '@' not in email:
                logging.error(f"Invalid email format: {email}")
                return False
            
            logging.info("User data processed successfully")
            return True
            
        except Exception as e:
            logging.error(f"Unexpected error processing user data: {e}")
            logging.debug(f"Full traceback: {traceback.format_exc()}")
            return False
    
    # Test cases
    test_users = [
        {'name': 'Alice', 'age': 25, 'email': 'alice@example.com'},
        {'name': 'Bob', 'age': -5, 'email': 'bob@example.com'},
        {'name': 'Charlie', 'age': 30, 'email': 'invalid-email'},
        {'name': 'Diana', 'age': 35}  # Missing email
    ]
    
    for i, user in enumerate(test_users, 1):
        print(f"\nProcessing user {i}: {user.get('name', 'Unknown')}")
        success = process_user_data(user)
        print(f"Result: {'SUCCESS' if success else 'FAILED'}")

# ============================================================================
# 3. ASSERTIONS: Guardians of expectations
# ============================================================================

def example_assertions():
    """
    Demonstrates assertions as safety nets within code
    """
    print("\n" + "="*60)
    print("3. ASSERTIONS: Guardians of expectations")
    print("="*60)
    
    def calculate_area(length: float, width: float) -> float:
        """
        Calculate area with assertions to catch invalid inputs
        """
        assert length > 0, f"Length must be positive, got {length}"
        assert width > 0, f"Width must be positive, got {width}"
        assert isinstance(length, (int, float)), f"Length must be numeric, got {type(length)}"
        assert isinstance(width, (int, float)), f"Width must be numeric, got {type(width)}"
        
        area = length * width
        assert area > 0, f"Calculated area should be positive, got {area}"
        
        return area
    
    def calculate_percentage(total: float, part: float) -> float:
        """
        Calculate percentage with assertions
        """
        assert total > 0, f"Total must be positive, got {total}"
        assert part >= 0, f"Part must be non-negative, got {part}"
        assert part <= total, f"Part ({part}) cannot be greater than total ({total})"
        
        percentage = (part / total) * 100
        assert 0 <= percentage <= 100, f"Percentage should be between 0-100, got {percentage}"
        
        return percentage
    
    # Test valid cases
    print("Testing valid cases:")
    try:
        area1 = calculate_area(5, 3)
        print(f"Area calculation: {area1}")
        
        percentage1 = calculate_percentage(100, 25)
        print(f"Percentage calculation: {percentage1}%")
    except AssertionError as e:
        print(f"Assertion failed: {e}")
    
    # Test invalid cases
    print("\nTesting invalid cases:")
    test_cases = [
        ("Negative length", lambda: calculate_area(-5, 3)),
        ("Zero width", lambda: calculate_area(5, 0)),
        ("String input", lambda: calculate_area("5", 3)),
        ("Invalid percentage", lambda: calculate_percentage(100, 150))
    ]
    
    for description, test_func in test_cases:
        try:
            result = test_func()
            print(f"{description}: {result}")
        except AssertionError as e:
            print(f"{description}: AssertionError - {e}")

# ============================================================================
# 4. DEBUGGER: Your code's time machine
# ============================================================================

def example_debugger_usage():
    """
    Demonstrates debugger concepts and breakpoint usage
    """
    print("\n" + "="*60)
    print("4. DEBUGGER: Your code's time machine")
    print("="*60)
    
    def complex_calculation(data: List[int]) -> Dict[str, Any]:
        """
        A complex function that would benefit from debugger inspection
        """
        print("Starting complex calculation...")
        
        # This is where you would set a breakpoint in your IDE
        # breakpoint()  # Python 3.7+ built-in breakpoint
        
        result = {
            'sum': 0,
            'average': 0,
            'max': None,
            'min': None,
            'count': len(data)
        }
        
        if not data:
            print("No data to process")
            return result
        
        # Process each number
        for i, num in enumerate(data):
            print(f"Processing number {i + 1}/{len(data)}: {num}")
            
            # Update running calculations
            result['sum'] += num
            
            if result['max'] is None or num > result['max']:
                result['max'] = num
            
            if result['min'] is None or num < result['min']:
                result['min'] = num
        
        # Calculate final results
        result['average'] = result['sum'] / result['count']
        
        print(f"Final results: {result}")
        return result
    
    # Test the function
    test_data = [10, 25, 5, 30, 15]
    print("Testing complex calculation:")
    result = complex_calculation(test_data)
    
    print("\nTo use a debugger:")
    print("1. Set breakpoints in your IDE (PyCharm, VS Code, etc.)")
    print("2. Run the code in debug mode")
    print("3. Inspect variables at each breakpoint")
    print("4. Step through code line by line")
    print("5. Examine the call stack and variable values")

# ============================================================================
# 5. REAL-WORLD CASE STUDY: Memory Leak Simulation
# ============================================================================

class ImageProcessor:
    """
    Simulates the memory leak case study from the text
    """
    
    def __init__(self):
        self.processed_images = []
        self.memory_usage = 0
        logging.info("ImageProcessor initialized")
    
    def process_image_without_cleanup(self, image_data: str) -> str:
        """
        Simulates the buggy image processing (causes memory leak)
        """
        logging.debug(f"Processing image: {image_data[:20]}...")
        
        # Simulate image processing
        processed_image = f"processed_{image_data}"
        
        # BUG: Not cleaning up - adding to list without removing
        self.processed_images.append(processed_image)
        self.memory_usage += len(processed_image)
        
        logging.info(f"Image processed. Memory usage: {self.memory_usage}")
        return processed_image
    
    def process_image_with_cleanup(self, image_data: str) -> str:
        """
        Simulates the fixed image processing (proper cleanup)
        """
        logging.debug(f"Processing image: {image_data[:20]}...")
        
        # Simulate image processing
        processed_image = f"processed_{image_data}"
        
        # FIXED: Clean up after processing
        self.memory_usage += len(processed_image)
        
        logging.info(f"Image processed and cleaned up. Memory usage: {self.memory_usage}")
        return processed_image
    
    def get_memory_usage(self) -> int:
        """Get current memory usage"""
        return self.memory_usage

def memory_leak_case_study():
    """
    Demonstrates the memory leak case study from the text
    """
    print("\n" + "="*60)
    print("5. REAL-WORLD CASE STUDY: Memory Leak Simulation")
    print("="*60)
    
    print("Simulating the Facebook-like memory leak scenario...")
    
    # Create processor instances
    buggy_processor = ImageProcessor()
    fixed_processor = ImageProcessor()
    
    # Simulate multiple image uploads
    test_images = [f"image_{i}_data" * 100 for i in range(10)]
    
    print("\n=== BUGGY VERSION (Memory Leak) ===")
    for i, image in enumerate(test_images, 1):
        print(f"Processing image {i}/10...")
        buggy_processor.process_image_without_cleanup(image)
        print(f"Memory usage: {buggy_processor.get_memory_usage()}")
    
    print(f"\nFinal memory usage (buggy): {buggy_processor.get_memory_usage()}")
    print(f"Number of images in memory: {len(buggy_processor.processed_images)}")
    
    print("\n=== FIXED VERSION (Proper Cleanup) ===")
    for i, image in enumerate(test_images, 1):
        print(f"Processing image {i}/10...")
        fixed_processor.process_image_with_cleanup(image)
        print(f"Memory usage: {fixed_processor.get_memory_usage()}")
    
    print(f"\nFinal memory usage (fixed): {fixed_processor.get_memory_usage()}")
    
    print("\n=== ANALYSIS ===")
    print("The buggy version accumulates images in memory, causing a memory leak.")
    print("The fixed version processes images and cleans up properly.")
    print("This demonstrates how debugging tools help identify and fix memory issues.")

# ============================================================================
# 6. ONLINE RESOURCES: Debugging with community help
# ============================================================================

def example_online_resources():
    """
    Demonstrates how to prepare for seeking online help
    """
    print("\n" + "="*60)
    print("6. ONLINE RESOURCES: Tapping into collective wisdom")
    print("="*60)
    
    def create_debug_report(error: Exception, code_snippet: str, context: str) -> str:
        """
        Creates a well-structured debug report for online communities
        """
        report = f"""
=== DEBUG REPORT ===

ERROR:
{type(error).__name__}: {error}

CODE SNIPPET:
{code_snippet}

CONTEXT:
{context}

ENVIRONMENT:
Python version: {sys.version}
Platform: {sys.platform}

WHAT I'VE TRIED:
- Added print statements to track variable values
- Checked input data types and values
- Verified function parameters

MINIMAL REPRODUCIBLE EXAMPLE:
{code_snippet}

EXPECTED BEHAVIOR:
[Describe what you expected to happen]

ACTUAL BEHAVIOR:
[Describe what actually happened]

QUESTION:
[Ask specific question about the issue]
"""
        return report
    
    # Example of a problematic function
    def problematic_function(data):
        """Function with a potential bug"""
        try:
            result = sum(data) / len(data)
            return result
        except Exception as e:
            # This is how you might prepare for online help
            code_snippet = """
def problematic_function(data):
    result = sum(data) / len(data)
    return result
"""
            context = "Calculating average of numeric data"
            
            report = create_debug_report(e, code_snippet, context)
            print("Example debug report for online communities:")
            print(report)
            raise
    
    # Test the problematic function
    print("Testing problematic function:")
    try:
        problematic_function([])  # This will cause an error
    except Exception as e:
        print(f"Error occurred: {e}")

# ============================================================================
# 7. COMPREHENSIVE DEBUGGING WORKFLOW
# ============================================================================

def comprehensive_debugging_workflow():
    """
    Demonstrates a complete debugging workflow using all techniques
    """
    print("\n" + "="*60)
    print("7. COMPREHENSIVE DEBUGGING WORKFLOW")
    print("="*60)
    
    def buggy_data_processor(data_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        A function with multiple potential bugs for debugging practice
        """
        logging.info("Starting data processing")
        logging.debug(f"Input data: {data_list}")
        
        # Initialize results
        results = {
            'total_items': 0,
            'valid_items': 0,
            'total_value': 0,
            'errors': []
        }
        
        # Process each item
        for i, item in enumerate(data_list):
            print(f"Processing item {i + 1}/{len(data_list)}: {item}")
            
            try:
                # Assertions for validation
                assert isinstance(item, dict), f"Item {i} is not a dictionary"
                assert 'value' in item, f"Item {i} missing 'value' key"
                assert 'name' in item, f"Item {i} missing 'name' key"
                
                # Process the item
                value = item['value']
                name = item['name']
                
                print(f"  Name: {name}, Value: {value}")
                
                # More assertions
                assert isinstance(value, (int, float)), f"Value must be numeric, got {type(value)}"
                assert value >= 0, f"Value must be non-negative, got {value}"
                
                # Update results
                results['total_items'] += 1
                results['valid_items'] += 1
                results['total_value'] += value
                
                print(f"  Item processed successfully. Running total: {results['total_value']}")
                
            except AssertionError as e:
                error_msg = f"Item {i}: {e}"
                logging.warning(error_msg)
                results['errors'].append(error_msg)
                results['total_items'] += 1
                
            except Exception as e:
                error_msg = f"Item {i}: Unexpected error - {e}"
                logging.error(error_msg)
                results['errors'].append(error_msg)
                results['total_items'] += 1
        
        logging.info(f"Processing complete. Results: {results}")
        return results
    
    # Test data with various issues
    test_data = [
        {'name': 'Item 1', 'value': 100},
        {'name': 'Item 2', 'value': -50},  # Negative value
        {'name': 'Item 3'},  # Missing value
        {'value': 75},  # Missing name
        'not_a_dict',  # Wrong type
        {'name': 'Item 4', 'value': 200},
        {'name': 'Item 5', 'value': 'invalid'}  # Non-numeric value
    ]
    
    print("Testing comprehensive debugging workflow:")
    results = buggy_data_processor(test_data)
    
    print(f"\nFinal Results:")
    print(f"Total items processed: {results['total_items']}")
    print(f"Valid items: {results['valid_items']}")
    print(f"Total value: {results['total_value']}")
    print(f"Errors: {len(results['errors'])}")
    
    if results['errors']:
        print("\nErrors encountered:")
        for error in results['errors']:
            print(f"  - {error}")

def main():
    """
    Run all debugging toolkit examples
    """
    print("Debugging Toolkit: Essential Techniques for Python Developers")
    print("=" * 80)
    
    # Run all examples
    example_print_statements()
    example_logging()
    example_assertions()
    example_debugger_usage()
    memory_leak_case_study()
    example_online_resources()
    comprehensive_debugging_workflow()
    
    print("\n" + "=" * 80)
    print("All debugging toolkit examples completed!")
    print("Check 'debug_toolkit.log' for detailed logging output.")
    print("\nKey Takeaways:")
    print("1. Print statements: Quick, immediate feedback for simple issues")
    print("2. Logging: Structured, persistent tracking for complex systems")
    print("3. Assertions: Early error detection and code validation")
    print("4. Debuggers: Deep inspection and step-by-step analysis")
    print("5. Online resources: Leverage community knowledge and experience")
    print("6. Combine techniques: Use multiple approaches for comprehensive debugging")

if __name__ == "__main__":
    main() 