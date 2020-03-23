from dmoj.executors.script_executor import ScriptExecutor

                                                                                                                                                                                            
class Executor(ScriptExecutor):                                                                                                                                                             
    ext = '.jl'                                                                                                                                                                             
    name = 'JULIA'                                                                                                                                                                          
    command = 'julia'                                                                                                                                                                       
    command_paths = ['julia']                                                                                                                                                               
    syscalls = ['epoll_ctl', 'epoll_create', 'epoll_wait', 'poll',                                                                                                                          
                'epoll_create1', 'pipe2', 'eventfd2', 'rt_sigtimedwait',                                                                                                                    
                'sched_getaffinity', 'sched_setaffinity', 'mbind',                                                                                                                          
                'mincore', 'memfd_create', 'pwrite64', 'msync']                                                                                                                                                                  
    fs = ['/opt/julia-1\.0\.1/.*', '/home/judge/\.julia/.*', '']                                                                                                                                                                                            
    address_grace = 131072 << 2                                                                                                                                                             
    nproc = -1                                                                                                                                                                            
    test_memory = 65536 << 3                                                                                                                                                                
    test_program = "print(read(stdin, String))"                                                                                                                                             
                                                                                                                                                                                            
    @classmethod                                                                                                                                                                            
    def get_version_flags(cls, command):                                                                                                                                                    
        return ['-v'] 
