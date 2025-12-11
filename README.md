# Problem Statement

 **Title: Simple Workflow Release Registry**

 You are designing a small part of a *Workflow Release Management* service.
 Implement a minimal in-memory “workflow registry” in Python with the semantics below.

 A **workflow** has:

* a `name` (string, e.g. `"member_eligibility"`)
* one or more **versions** (semantic version string e.g. `"1.0.0"`, `"1.0.1"`)
* each version has an `env_config` dictionary of environment variables, e.g.:

 ```python
 {
   "API_URL": "https://qa.example.com",
   "TIMEOUT_SECONDS": 10,
   "MAX_RETRIES": 3,
 }
 ```

### Requirements

 1. Implement a function:

    ```python
    def compare_versions(v1: str, v2: str) -> int:
        """
        Returns:
          -1 if v1 < v2
           0 if v1 == v2
           1 if v1 > v2
        """
    ```

    * Versions are in the form `"major.minor.patch"` (all integers).

 2. Implement a `WorkflowRegistry` class with at least these methods:

    ```python
    class WorkflowRegistry:
        def publish(self, name: str, version: str, env_config: dict) -> None:
            """
            Registers a new workflow version.
            Rules:
            - If this is the first version for `name`, accept it.
            - Otherwise, `version` must be strictly greater than the latest version
              for this workflow. If not, raise a ValueError.
            """

        def get_latest(self, name: str) -> dict | None:
            """
            Returns the env_config of the latest version for this workflow name,
            or None if it does not exist.
            """

        def diff_env(self, name: str, from_version: str, to_version: str) -> dict:
            """
            Compares the env_config of two versions of the same workflow.
            Returns a dict with the structure:

            {
              "added":   [list of keys present only in to_version],
              "removed": [list of keys present only in from_version],
              "changed": {
                key: {"from": old_value, "to": new_value},
                ...
              }
            }

            If either version does not exist, raise a ValueError.
            """
    ```

 3. Show how you would use this in code by:

    * Creating a registry.
    * Publishing at least two versions of a workflow with different `env_config`.
    * Printing the result of `get_latest` and `diff_env` between versions.

### Notes

* You do **not** need to implement any persistence or web API; in-memory is enough.
* Focus on clarity, correctness, and handling edge cases.
* If you have time, you may add simple tests (e.g. using plain asserts or a small `pytest` style function), but that’s optional.

---
