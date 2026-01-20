"""
Example usage of the Workflow Registry

This script demonstrates how to use the WorkflowRegistry class to:
- Create a registry
- Publish multiple versions of workflows
- Retrieve latest configurations
- Compare configurations between versions
"""

from workflow_registry import WorkflowRegistry
import json


def print_section(title: str):
    """Helper to print section headers."""
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print('=' * 60)


def main():
    # Create a registry instance
    registry = WorkflowRegistry()

    print_section("1. Publishing Workflow Versions")

    # Publish version 1.0.0 of "member_eligibility" workflow
    print("\nPublishing member_eligibility v1.0.0...")
    registry.publish(
        name="member_eligibility",
        version="1.0.0",
        env_config={
            "API_URL": "https://qa.example.com",
            "TIMEOUT_SECONDS": 10,
            "MAX_RETRIES": 3,
            "DEBUG_MODE": False
        }
    )
    print("✓ Published successfully")

    # Publish version 1.1.0 with updated configuration
    print("\nPublishing member_eligibility v1.1.0...")
    registry.publish(
        name="member_eligibility",
        version="1.1.0",
        env_config={
            "API_URL": "https://qa.example.com",
            "TIMEOUT_SECONDS": 15,  # Changed
            "MAX_RETRIES": 5,       # Changed
            "DEBUG_MODE": False,
            "CACHE_ENABLED": True   # Added
        }
    )
    print("✓ Published successfully")

    # Publish version 2.0.0 with more changes
    print("\nPublishing member_eligibility v2.0.0...")
    registry.publish(
        name="member_eligibility",
        version="2.0.0",
        env_config={
            "API_URL": "https://prod.example.com",  # Changed
            "TIMEOUT_SECONDS": 20,                   # Changed
            "MAX_RETRIES": 5,
            "CACHE_ENABLED": True,
            "FEATURE_FLAG_NEW_UI": True              # Added
            # Removed DEBUG_MODE
        }
    )
    print("✓ Published successfully")

    print_section("2. Getting Latest Version")

    # Get the latest version configuration
    latest_config = registry.get_latest("member_eligibility")
    print("\nLatest configuration for 'member_eligibility':")
    print(json.dumps(latest_config, indent=2))

    print_section("3. Comparing Version Configurations")

    # Compare v1.0.0 to v1.1.0
    print("\n📊 Diff from v1.0.0 to v1.1.0:")
    diff_1_to_1_1 = registry.diff_env("member_eligibility", "1.0.0", "1.1.0")
    print(json.dumps(diff_1_to_1_1, indent=2))

    # Compare v1.1.0 to v2.0.0
    print("\n📊 Diff from v1.1.0 to v2.0.0:")
    diff_1_1_to_2 = registry.diff_env("member_eligibility", "1.1.0", "2.0.0")
    print(json.dumps(diff_1_1_to_2, indent=2))

    # Compare v1.0.0 to v2.0.0 (skipping intermediate version)
    print("\n📊 Diff from v1.0.0 to v2.0.0:")
    diff_1_to_2 = registry.diff_env("member_eligibility", "1.0.0", "2.0.0")
    print(json.dumps(diff_1_to_2, indent=2))

    print_section("4. Publishing Another Workflow")

    # Demonstrate with a different workflow
    print("\nPublishing payment_processor v1.0.0...")
    registry.publish(
        name="payment_processor",
        version="1.0.0",
        env_config={
            "PAYMENT_API": "https://api.stripe.com",
            "WEBHOOK_SECRET": "whsec_test123",
            "CURRENCY": "USD"
        }
    )
    print("✓ Published successfully")

    print("\nPublishing payment_processor v1.0.1...")
    registry.publish(
        name="payment_processor",
        version="1.0.1",
        env_config={
            "PAYMENT_API": "https://api.stripe.com",
            "WEBHOOK_SECRET": "whsec_prod456",  # Changed
            "CURRENCY": "USD",
            "TAX_CALCULATION": True              # Added
        }
    )
    print("✓ Published successfully")

    print("\n📊 Diff for payment_processor from v1.0.0 to v1.0.1:")
    payment_diff = registry.diff_env("payment_processor", "1.0.0", "1.0.1")
    print(json.dumps(payment_diff, indent=2))

    print_section("5. Error Handling Examples")

    # Try to publish a version that's not greater than the latest
    print("\n❌ Attempting to publish v1.0.0 (should fail)...")
    try:
        registry.publish(
            name="member_eligibility",
            version="1.0.0",
            env_config={"TEST": "value"}
        )
    except ValueError as e:
        print(f"✓ Correctly rejected: {e}")

    # Try to get latest for non-existent workflow
    print("\n❌ Attempting to get latest for non-existent workflow...")
    result = registry.get_latest("non_existent")
    print(f"✓ Correctly returned: {result}")

    # Try to diff with non-existent version
    print("\n❌ Attempting to diff with non-existent version...")
    try:
        registry.diff_env("member_eligibility", "1.0.0", "99.99.99")
    except ValueError as e:
        print(f"✓ Correctly rejected: {e}")

    print_section("Summary")
    print("\n✅ All operations completed successfully!")
    print("\nWorkflows in registry:")
    print("  - member_eligibility: 3 versions (1.0.0, 1.1.0, 2.0.0)")
    print("  - payment_processor: 2 versions (1.0.0, 1.0.1)")
    print()


if __name__ == "__main__":
    main()
