import gc
import logging
import platform
import subprocess
import os

from dmoj.error import OutputLimitExceeded
from dmoj.executors import executors
from dmoj.graders.base import BaseGrader
from dmoj.result import CheckerResult, Result
from dmoj.judgeenv import get_problem_root

log = logging.getLogger('dmoj.graders')


class UnitTestGrader(BaseGrader):
    def grade(self, case):
        result = Result(case)

        if self.language != "PY3":
            # If not python 3, give a runtime error.
            result.result_flag = Result.RTE
            result.points = 0
            result.feedback = "Unittest only works on Python 3."
            return result

        input = case.input_data()  # cache generator data

        self._launch_process(case)

        error = self._interact_with_process(case, result, input)

        process = self._current_proc

        self.populate_result(error, result, process)

        check = self.check_result(case, result)

        # checkers must either return a boolean (True: full points, False: 0 points)
        # or a CheckerResult, so convert to CheckerResult if it returned bool
        if not isinstance(check, CheckerResult):
            check = CheckerResult(check, case.points if check else 0.0)

        if result.result_flag & Result.IR:
            result.result_flag = Result.WA
        result.points = check.points
        result.feedback = check.feedback or result.feedback
        result.extended_feedback = check.extended_feedback or result.extended_feedback

        case.free_data()

        # Where CPython has reference counting and a GC, PyPy only has a GC. This means that while CPython
        # will have freed any (usually massive) generated data from the line above by reference counting, it might
        # - and probably still is - in memory by now. We need to be able to fork() immediately, which has a good chance
        # of failing if there's not a lot of swap space available.
        #
        # We don't really have a way to force the generated data to disappear, so calling a gc here is the best
        # chance we have.
        if platform.python_implementation() == 'PyPy':
            gc.collect()

        return result

    def populate_result(self, error, result, process):
        self.binary.populate_result(error, result, process)

    def check_result(self, case, result):
        # If the submission didn't crash and didn't time out, there's a chance it might be AC
        # We shouldn't run checkers if the submission is already known to be incorrect, because some checkers
        # might be very computationally expensive.
        # See https://github.com/DMOJ/judge/issues/170
        checker = case.checker()
        # checker is a `partial` object, NOT a `function` object
        if not result.result_flag or getattr(checker.func, 'run_on_error', False):
            try:
                check = checker(result.proc_output,
                                case.output_data(),
                                submission_source=self.source,
                                judge_input=case.input_data(),
                                point_value=case.points,
                                case_position=case.position,
                                batch=case.batch,
                                submission_language=self.language,
                                binary_data=case.has_binary_data,
                                execution_time=result.execution_time,
                                problem_id=self.problem.id)
            except UnicodeDecodeError:
                # Don't rely on problemsetters to do sane things when it comes to Unicode handling, so
                # just proactively swallow all Unicode-related checker errors.
                return CheckerResult(False, 0, feedback='invalid unicode')
        else:
            # Solution is guaranteed to receive 0 points
            check = False

        return check

    def _launch_process(self, case):
        self._current_proc = self.binary.launch(
            time=self.problem.time_limit, memory=self.problem.memory_limit, symlinks=case.config.symlinks,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            wall_time=case.config.wall_time_factor * self.problem.time_limit,
        )

    def _interact_with_process(self, case, result, input):
        process = self._current_proc
        try:
            result.proc_output, error = process.communicate(input, outlimit=case.config.output_limit_length,
                                                            errlimit=1048576)
        except OutputLimitExceeded:
            error = b''
            try:
                process.kill()
            except RuntimeError as e:
                if e.args[0] != 'TerminateProcess: 5':
                    raise
            # Otherwise it's a race between this kill and the shocker,
            # and failed kill means nothing.
            process.wait()
        return error

    def _generate_binary(self):
        unitTestFile = open(os.path.join(get_problem_root(self.problem.id), self.problem.config['unit_test']),'r')
        unitTestCode = unitTestFile.read()
        unitTestFile.close()
        finalCode = self.source.decode() + '\n\n' + unitTestCode
        return executors[self.language].Executor(self.problem.id, finalCode.encode(),
                                                 hints=self.problem.config.hints or [],
                                                 unbuffered=self.problem.config.unbuffered)
