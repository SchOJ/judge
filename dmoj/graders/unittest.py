import gc
import logging
import platform
import subprocess
import os

from dmoj.error import OutputLimitExceeded
from dmoj.executors import executors
from dmoj.graders.base import BaseGrader
from dmoj.result import Result
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
        
        if result.result_flag & Result.IR:
            result.result_flag = Result.WA
        if result.result_flag == Result.AC:
            result.points = case.points
        else:
            result.points = case.points
        result.feedback = result.feedback
        result.extended_feedback = result.extended_feedback

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
