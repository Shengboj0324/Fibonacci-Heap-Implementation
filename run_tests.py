#!/usr/bin/env python3

import unittest
import sys
import os
import time
from typing import List, Dict

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import test modules
from tests.test_fibonacci_node import TestFibonacciNode
from tests.test_fibonacci_heap import TestFibonacciHeap
from tests.test_analysis import TestFibonacciHeapAnalyzer

def run_test_suite(test_class, class_name: str) -> Dict[str, any]:

    print(f"\n{'='*60}")
    print(f"Running {class_name} Tests")
    print(f"{'='*60}")

    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(test_class)

    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)

    start_time = time.time()
    result = runner.run(suite)
    end_time = time.time()

    # Calculate results
    total_tests = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    skipped = len(result.skipped) if hasattr(result, 'skipped') else 0
    passed = total_tests - failures - errors - skipped

    results = {
        'class_name': class_name,
        'total': total_tests,
        'passed': passed,
        'failed': failures,
        'errors': errors,
        'skipped': skipped,
        'time': end_time - start_time,
        'success': failures == 0 and errors == 0
    }

    # Print summary
    print(f"\n{class_name} Summary:")
    print(f"  Total tests: {total_tests}")
    print(f"  Passed: {passed}")
    print(f"  Failed: {failures}")
    print(f"  Errors: {errors}")
    print(f"  Skipped: {skipped}")
    print(f"  Time: {end_time - start_time:.3f} seconds")
    print(f"  Status: {'PASS' if results['success'] else 'FAIL'}")

    # Print failure details if any
    if failures > 0:
        print(f"\nFailures in {class_name}:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback.split('AssertionError:')[-1].strip()}")

    if errors > 0:
        print(f"\nErrors in {class_name}:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback.split('Error:')[-1].strip()}")

    return results

def run_all_tests() -> List[Dict[str, any]]:

    print("Fibonacci Heap Implementation - Test Suite")
    print("=" * 60)
    print("Running comprehensive tests for all components...")

    # Define test suites
    test_suites = [
        (TestFibonacciNode, "FibonacciNode"),
        (TestFibonacciHeap, "FibonacciHeap"),
        (TestFibonacciHeapAnalyzer, "FibonacciHeapAnalyzer")
    ]

    results = []

    # Run each test suite
    for test_class, class_name in test_suites:
        try:
            result = run_test_suite(test_class, class_name)
            results.append(result)
        except Exception as e:
            print(f"\nError running {class_name} tests: {e}")
            results.append({
                'class_name': class_name,
                'total': 0,
                'passed': 0,
                'failed': 0,
                'errors': 1,
                'skipped': 0,
                'time': 0,
                'success': False
            })

    return results

def print_overall_summary(results: List[Dict[str, any]]) -> None:

    print(f"\n{'='*60}")
    print("OVERALL TEST SUMMARY")
    print(f"{'='*60}")

    total_tests = sum(r['total'] for r in results)
    total_passed = sum(r['passed'] for r in results)
    total_failed = sum(r['failed'] for r in results)
    total_errors = sum(r['errors'] for r in results)
    total_skipped = sum(r['skipped'] for r in results)
    total_time = sum(r['time'] for r in results)

    all_success = all(r['success'] for r in results)

    print(f"Test Suites Run: {len(results)}")
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {total_passed}")
    print(f"Failed: {total_failed}")
    print(f"Errors: {total_errors}")
    print(f"Skipped: {total_skipped}")
    print(f"Total Time: {total_time:.3f} seconds")
    print(f"Success Rate: {(total_passed/total_tests*100):.1f}%" if total_tests > 0 else "N/A")

    print(f"\nOverall Status: {'PASS' if all_success else 'FAIL'}")

    # Print per-suite breakdown
    print(f"\nPer-Suite Breakdown:")
    for result in results:
        status = "PASS" if result['success'] else "FAIL"
        print(f"  {result['class_name']:<25} {result['passed']:>3}/{result['total']:<3} {status}")

    if not all_success:
        print(f"\n⚠️  Some tests failed. Please review the output above.")
        return False
    else:
        print(f"\n✅ All tests passed successfully!")
        return True

def run_integration_tests() -> bool:

    print(f"\n{'='*60}")
    print("Running Integration Tests")
    print(f"{'='*60}")

    try:
        from fibonacci_heap import FibonacciHeap, FibonacciHeapAnalyzer, FibonacciHeapVisualizer

        print("Testing component integration...")

        # Test 1: Heap with analyzer
        heap = FibonacciHeap()
        analyzer = FibonacciHeapAnalyzer()

        # Insert elements
        for i in range(10):
            heap.insert(i)

        # Analyze
        analysis = analyzer.theoretical_vs_actual_analysis(heap)
        assert analysis['fibonacci_property_satisfied'], "Fibonacci property not satisfied"
        assert analysis['degree_bound_satisfied'], "Degree bound not satisfied"

        print("✓ Heap + Analyzer integration test passed")

        # Test 2: Heap with visualizer
        visualizer = FibonacciHeapVisualizer()

        # Log operations
        for i in range(5):
            heap.insert(i + 10)
            visualizer.log_operation("insert", heap, key=i+10)

        # Generate visualization
        structure = visualizer.print_heap_structure(heap)
        assert len(structure) > 0, "Visualization failed"

        print("✓ Heap + Visualizer integration test passed")

        # Test 3: Complex operations
        for _ in range(3):
            heap.delete_min()

        # Verify heap is still valid
        assert not heap.is_empty(), "Heap should not be empty"
        assert heap.find_min() is not None, "Should have minimum element"

        print("✓ Complex operations integration test passed")

        print("\nAll integration tests passed!")
        return True

    except Exception as e:
        print(f"Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():

    start_time = time.time()

    # Run unit tests
    results = run_all_tests()

    # Run integration tests
    integration_success = run_integration_tests()

    # Print overall summary
    unit_test_success = print_overall_summary(results)

    end_time = time.time()

    print(f"\n{'='*60}")
    print(f"TEST EXECUTION COMPLETE")
    print(f"{'='*60}")
    print(f"Total execution time: {end_time - start_time:.3f} seconds")

    overall_success = unit_test_success and integration_success

    if overall_success:
        print("🎉 All tests completed successfully!")
        sys.exit(0)
    else:
        print("❌ Some tests failed. Please review the output above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
