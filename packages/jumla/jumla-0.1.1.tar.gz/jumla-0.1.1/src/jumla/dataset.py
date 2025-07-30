import json
import os
from typing import Dict, List
from dataclasses import dataclass
from .files import Files
from .parser import Parser
from .log import logger


@dataclass
class Dataset(Files, Parser):
    DESCRIPTION_TITLE = "-----Description-----"
    INPUT_TITLE = "-----Input-----"
    OUTPUT_TITLE = "-----Output-----"
    DESCRIPTION_FILENAME = "description.txt"
    SIGNATURE_FILENAME = "signature.json"
    LEAN_TASK_FILENAME = "task.lean"
    TEST_FILENAME = "test.json"
    LEAN_TEST_FILENAME = "tests.lean"
    CODE_START = "  -- << CODE START >>"
    CODE_BODY = "  -- {{code}}\n  sorry"
    CODE_END = "  -- << CODE END >>"
    SPEC_START = "  -- << SPEC START >>"
    SPEC_BODY = "  -- {{spec}}\n  sorry"
    SPEC_END = "  -- << SPEC END >>"
    PROOF_START = "  -- << PROOF START >>"
    PROOF_BODY = "  -- {{proof}}\n  sorry"
    PROOF_END = "  -- << PROOF END >>"

    def __init__(
        self,
        function: str,
        description_doc: str,
        input_doc: str,
        output_doc: str,
        test_cases: List[Dict[str, str]],
        dir="task_id_0",
    ):
        self.function = function
        self.description_doc = description_doc
        self.input_doc = input_doc
        self.output_doc = output_doc
        function_name, params, lean_return_type = self.extract_function_signature()
        self.function_name = function_name
        self.params = params
        self.lean_return_type = lean_return_type
        self.lean_arguments = self.build_lean_args()
        self.signature = self.build_signature()
        self.lean_task = self.build_lean_task()
        self.test_cases = test_cases

        if not os.path.exists("dataset"):
            os.makedirs("dataset")
        if not os.path.exists(f"dataset/{dir}"):
            os.makedirs(f"dataset/{dir}")
        self.dir = f"dataset/{dir}/"

    def build_description(self, log=False):
        description = (
            f"{self.DESCRIPTION_TITLE}\n{self.description_doc}\n\n"
            f"{self.INPUT_TITLE}\n{self.input_doc}\n\n"
            f"{self.OUTPUT_TITLE}\n{self.output_doc}"
        )

        if log:
            logger.bullet(f"[build] {self.DESCRIPTION_FILENAME} ready")

        return description

    def write_description(self, log=False):
        data = self.build_description(log=log)
        path = self.dir + self.DESCRIPTION_FILENAME
        self.write_to_file(path, data, log=log)

    def write_signature(self, log=False):
        signature = self.build_signature(log=log)
        signature_str = json.dumps(signature, indent=2)
        path = self.dir + self.SIGNATURE_FILENAME
        self.write_to_file(path, signature_str, log=log)

    def write_lean_task(self, log=False):
        lean_sig = self.build_lean_task(log=log)
        path = self.dir + self.LEAN_TASK_FILENAME
        self.write_to_file(path, lean_sig, log=log)

    def write_tests(self, log=False):
        tests = self.build_tests(log=log)
        tests_str = json.dumps(tests, indent=2)
        path = self.dir + self.TEST_FILENAME
        self.write_to_file(path, tests_str, log=log)

    def write_lean_tests(self, log=False):
        tests = self.build_lean_tests(log=log)
        path = self.dir + self.LEAN_TEST_FILENAME
        self.write_to_file(path, tests, log=log)

    def write_all(self, log=False):
        logger.step(f"Writing dataset to `{self.dir}`")

        self.write_description(log=log)
        logger.bullet(f"📄 {self.DESCRIPTION_FILENAME}")

        self.write_signature(log=log)
        logger.bullet(f"🧾 {self.SIGNATURE_FILENAME}")

        self.write_lean_task(log=log)
        logger.bullet(f"📘 {self.LEAN_TASK_FILENAME}")

        self.write_tests(log=log)
        logger.bullet(f"🧪 {self.TEST_FILENAME}")

        self.write_lean_tests(log=log)
        logger.bullet(f"🔍 {self.LEAN_TEST_FILENAME}")

        logger.success(f"[✓] Dataset generated: {self.dir}")

    def build_signature(self, log=False) -> Dict[str, str]:
        signature = {
            "name": self.function_name,
            "parameters": self.params,
            "return_type": self.lean_return_type,
        }
        if log:
            logger.bullet(f"[build] {self.SIGNATURE_FILENAME} signature ready")
        return signature

    def build_lean_task(self, log=False) -> str:
        imports = "import Mathlib\nimport Aesop\n"
        function = self.build_lean_function()
        spec = self.build_lean_spec(log=log)
        theorem = self.build_lean_theorem(log=log)
        lean_task = f"{imports}\n{function}\n\n{spec}\n\n{theorem}"

        if log:
            logger.info(f"  [build] {self.LEAN_TASK_FILENAME} task ready")

        return lean_task

    def build_lean_function(self) -> str:
        body = f"{self.CODE_START}\n{self.CODE_BODY}\n{self.CODE_END}"
        return f"def {self.function_name} {self.lean_arguments} : {self.lean_return_type} :=\n{body}"

    def build_lean_spec(self, log=False) -> str:
        function_definition = (
            f"def {self.function_name}_spec "
            f"{self.lean_arguments} "
            f"(_ : {self.lean_return_type}) : Prop :="
        )
        spec = (
            f"{function_definition}\n"
            f"{self.SPEC_START}\n{self.SPEC_BODY}\n{self.SPEC_END}"
        )
        if log:
            logger.info(f"  [build] {self.LEAN_TASK_FILENAME} spec ready")
        return spec

    def build_lean_theorem(self, log=False):
        theorem_definition = (
            f"theorem {self.function_name}_spec_satisfied {self.lean_arguments} :"
        )
        args = " ".join(param["param_name"] for param in self.params)
        spec_prop = (
            f"{self.function_name}_spec {args} ({self.function_name} {args}) := by"
        )
        proof_unfold = f"  unfold {self.function_name} {self.function_name}_spec"
        theorem = (
            f"{theorem_definition} {spec_prop}\n"
            f"{self.PROOF_START}\n"
            f"{proof_unfold}\n"
            f"{self.PROOF_BODY}"
            f"\n{self.PROOF_END}"
        )

        if log:
            logger.info(f"  [build] {self.LEAN_TASK_FILENAME} theorem ready")

        return theorem

    def build_lean_args(self):
        params = [
            f"({param['param_name']} : {param['param_type']})" for param in self.params
        ]
        parameters = " ".join(params)
        return parameters

    def build_test(self, test_case: Dict[str, str], log=False) -> Dict[str, str]:
        test = {
            "input": test_case.get("input", {}),
            "expected": test_case.get("expected", ""),
            "unexpected": test_case.get("unexpected", [{}]),
        }
        if log:
            logger.info(f"  [build] {self.TEST_FILENAME} ready")

        return test

    def build_lean_tests(self, log=False) -> str:
        tests = []
        for test_case in self.test_cases:
            expected_guard = self.build_lean_test(test_case, log=log)
            tests.append(expected_guard)

            # Optional: negative test cases
            for un in test_case.get("unexpected", []):
                unexpected_guard = self.build_lean_test(
                    {"input": test_case["input"], "expected": un}, equal=False, log=log
                )
                tests.append(unexpected_guard)

        return "\n".join(tests)

    def build_lean_test(self, test_case: Dict, equal: bool = True, log=False) -> str:
        inputs = test_case.get("input", {})
        expected = test_case.get("expected")

        # Ensure argument order matches function definition
        args = " ".join([f"({inputs[p['param_name']]})" for p in self.params])

        # Use ≠ for negative cases
        operator = "=" if equal else "≠"
        guard = f"#guard {self.function_name} {args} {operator} ({expected})"

        if log:
            logger.info(f"  [build] {self.LEAN_TEST_FILENAME} ready")
        return guard

    def build_tests(self, log=False) -> List[Dict[str, str]]:
        tests = []
        for test in self.test_cases:
            test = self.build_test(test, log=log)
            tests.append(test)
        return tests
