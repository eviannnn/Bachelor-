from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig


class ProjectAnonymizer:
    def __init__(self):
        self.analyzer = AnalyzerEngine()
        self.anonymizer = AnonymizerEngine()
        self._add_custom_recognizers()

    def _add_custom_recognizers(self):
        latvian_phone_pattern = Pattern(
            name="latvian_phone_pattern",
            regex=r"(\+371\s?)?\d{8}",
            score=0.85,
        )

        latvian_phone_recognizer = PatternRecognizer(
            supported_entity="PHONE_NUMBER",
            patterns=[latvian_phone_pattern],
        )

        email_pattern = Pattern(
            name="email_pattern",
            regex=r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
            score=0.9,
        )

        email_recognizer = PatternRecognizer(
            supported_entity="EMAIL_ADDRESS",
            patterns=[email_pattern],
        )

        self.analyzer.registry.add_recognizer(latvian_phone_recognizer)
        self.analyzer.registry.add_recognizer(email_recognizer)

    def anonymize(self, text: str) -> str:
        results = self.analyzer.analyze(
            text=text,
            language="en",
            entities=[
                "PERSON",
                "PHONE_NUMBER",
                "EMAIL_ADDRESS",
                "LOCATION",
                "ORGANIZATION",
            ],
        )

        anonymized_result = self.anonymizer.anonymize(
            text=text,
            analyzer_results=results,
            operators={
                "PERSON": OperatorConfig("replace", {"new_value": "[PERSON]"}),
                "PHONE_NUMBER": OperatorConfig("replace", {"new_value": "[PHONE]"}),
                "EMAIL_ADDRESS": OperatorConfig("replace", {"new_value": "[EMAIL]"}),
                "LOCATION": OperatorConfig("replace", {"new_value": "[LOCATION]"}),
                "ORGANIZATION": OperatorConfig("replace", {"new_value": "[ORGANIZATION]"}),
            },
        )

        return anonymized_result.text
