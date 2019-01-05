# SchOJ Judge [![Linux Build Status](https://img.shields.io/travis/SchOJ/judge.svg?logo=linux)](https://travis-ci.org/SchOJ/judge)

**A fork of [DMOJ/judge](https://github.com/DMOJ/judge)**

Python [AGPLv3](https://github.com/SchOJ/judge/blob/master/LICENSE) contest judge backend for the [SchOJ](http://github.com/SchOJ/site) / [DMOJ](http://github.com/DMOJ/site) site interface.

## What is added?

* New language support (like Julia)
* `unittest` capability

## Supported Platforms and Runtimes

Our instance runs on Linux x64. DMOJ/judge supports more architectures. Since we also update from upstream, SchOJ/judge may also work on these architectures.

The judge does **not** need a root user to run on Linux machines: it will run just fine under a normal user. However, to run it in Docker, a [privileged](https://docs.docker.com/engine/reference/run/#runtime-privilege-and-linux-capabilities) permission is needed.

Supported languages include:
* C++ 11/14/17 (GCC and Clang)
* C 99/11
* Java 8/9/10/11
* Python 2/3
* PyPy 2/3
* Pascal
* Perl
* Mono C#/F#/VB
* Julia

The judge can also grade in the languages listed below. These languages are less tested and more likely to be buggy.
* Ada
* AWK
* COBOL
* D
* Dart
* Fortran
* Forth
* Go
* Groovy
* Haskell
* INTERCAL
* Kotlin
* Lua
* NASM
* Objective-C
* OCaml
* PHP
* Pike
* Prolog
* Racket
* Ruby
* Rust
* Scala
* Chicken Scheme
* sed
* Steel Bank Common Lisp
* Swift
* Tcl
* Turing
* V8 JavaScript
* Brain\*\*\*\*

## Installation

We don't publish the package to Pypi while DMOJ/judge [does](https://pypi.python.org/pypi/dmoj).

The [Linux Installation](https://docs.dmoj.ca/en/latest/judge/linux_installation/) instructions of DMOJ/judge also works on SchOJ/judge.

Several environment variables can be specified to control the compilation of the sandbox:

* `DMOJ_USE_SECCOMP`; set it to `no` if you're building on a pre-Linux 3.5 kernel to disable `seccomp` filtering in favour of pure `ptrace` (slower).
   This flag has no effect when building outside of Linux.
* `DMOJ_TARGET_ARCH`; use it to override the default architecture specified for compiling the sandbox (via `-march`).
   Usually this is `native`, but will not be specified on ARM unless `DMOJ_TARGET_ARCH` is set (a generic, slow build will be compiled instead).

## Usage
### Running a Judge Server
```
$ dmoj --help
usage: dmoj [-h] [-p SERVER_PORT] -c CONFIG [-l LOG_FILE] [--no-watchdog]
            [-a API_PORT] [-A API_HOST] [-s] [-k] [-T TRUSTED_CERTIFICATES]
            [-e ONLY_EXECUTORS | -x EXCLUDE_EXECUTORS] [--no-ansi]
            server_host [judge_name] [judge_key]

Spawns a judge for a submission server.

positional arguments:
  server_host           host to connect for the server
  judge_name            judge name (overrides configuration)
  judge_key             judge key (overrides configuration)

optional arguments:
  -h, --help            show this help message and exit
  -p SERVER_PORT, --server-port SERVER_PORT
                        port to connect for the server
  -c CONFIG, --config CONFIG
                        file to load judge configurations from
  -l LOG_FILE, --log-file LOG_FILE
                        log file to use
  --no-watchdog         disable use of watchdog on problem directories
  -a API_PORT, --api-port API_PORT
                        port to listen for the judge API (do not expose to
                        public, security is left as an exercise for the
                        reverse proxy)
  -A API_HOST, --api-host API_HOST
                        IPv4 address to listen for judge API
  -s, --secure          connect to server via TLS
  -k, --no-certificate-check
                        do not check TLS certificate
  -T TRUSTED_CERTIFICATES, --trusted-certificates TRUSTED_CERTIFICATES
                        use trusted certificate file instead of system
  -e ONLY_EXECUTORS, --only-executors ONLY_EXECUTORS
                        only listed executors will be loaded (comma-separated)
  -x EXCLUDE_EXECUTORS, --exclude-executors EXCLUDE_EXECUTORS
                        prevent listed executors from loading (comma-
                        separated)
  --no-ansi             disable ANSI output
```

### Running a CLI Judge
```
$ dmoj-cli --help
usage: dmoj-cli [-h] -c CONFIG
                [-e ONLY_EXECUTORS | -x EXCLUDE_EXECUTORS]
                [--no-ansi]

Spawns a judge for a submission server.

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        file to load judge configurations from
  -e ONLY_EXECUTORS, --only-executors ONLY_EXECUTORS
                        only listed executors will be loaded (comma-separated)
  -x EXCLUDE_EXECUTORS, --exclude-executors EXCLUDE_EXECUTORS
                        prevent listed executors from loading (comma-
                        separated)
  --no-ansi             disable ANSI output
```

## Documentation
For info on the problem file format and more, [read the documentation.](https://docs.dmoj.ca)
