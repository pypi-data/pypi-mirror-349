from eopf.exceptions.errors import CriticalException, ExceptionWithExitCode


class ErrorPolicy:
    def __init__(self) -> None:
        self._errors: list[Exception] = []

    def handle(self, exc: Exception) -> None:
        raise NotImplementedError

    def finalize(self) -> None:
        """Optionally raise if needed at end"""
        pass

    @property
    def errors(self) -> list[Exception]:
        return self._errors


class FailFastPolicy(ErrorPolicy):
    def handle(self, exc: Exception) -> None:
        # All exceptions
        raise exc


class BestEffortPolicy(ErrorPolicy):
    def handle(self, exc: Exception) -> None:
        # Only our exception get a bypass, all the other ones are re raised
        if not isinstance(exc, ExceptionWithExitCode):
            raise exc
        self._errors.append(exc)

    def finalize(self) -> None:
        if len(self.errors) == 0:
            return
        # Create a synthetic exception at the end
        exit_code = 1
        message = ""
        for f in self.errors:
            if isinstance(f, ExceptionWithExitCode):
                exit_code = f.exit_code if f.exit_code > exit_code else exit_code
            message += f"{str(f)};"
        raise ExceptionWithExitCode(message, exit_code=exit_code)


class FailOnCriticalPolicy(BestEffortPolicy):
    def handle(self, exc: Exception) -> None:
        if isinstance(exc, CriticalException) or not isinstance(exc, ExceptionWithExitCode):
            raise exc
        self.errors.append(exc)


ERROR_POLICY_MAPPING = {
    "FAIL_FAST": FailFastPolicy,
    "FAIL_ON_CRITICAL": FailOnCriticalPolicy,
    "BEST_EFFORT": BestEffortPolicy,
}
