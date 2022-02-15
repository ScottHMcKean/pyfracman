import time
import subprocess

class FracmanRunner:
    """Class to run FracMan with a macro file and monitor it
    Initial design credit due to Thomas Bym & SKB
    """
    def __init__(self):

        self.fracman_exe_path = None
        self.non_responded_time = 0.0 #first time the process was not responding
        self.maxnon_responded_time = 6000.0 #max time for not responding process
        self.time_out = 50000.0 #max total time for the process
        self.start_time = 0 #simulation start time
        self.show_window = False #should we show the fracman window?
        self.check_interval_s = 5 #check the process after t seconds

    def Run(self, macro_filepath):
        """run FracMan with the macro"""
        if self.fracman_exe_path is None:
            system_command = "fracman " + macro_filepath
        else:
            assert isinstance(self.fracman_exe_path, str)
            system_command = self.fracman_exe_path + "\" \"" + macro_filepath + "\""
        
        print("RUNNING: {0}".format(macro_filepath))
        info = subprocess.STARTUPINFO()
        info.dwFlags = 1
        info.wShowWindow = self.show_window

        #start the process
        p = subprocess.Popen(system_command, stdin=subprocess.PIPE, startupinfo=info)
        self.start_time = time.time()
        
        while True:
            time.sleep(self.check_interval_s)
            t = time.time()

            #terminate if the program times out due to lack of convergence
            if (t - self.start_time) > self.time_out:
                p.terminate()
                print("TIME_OUT: {0}".format(macro_filepath))
                break

            # continue if program is responding
            if self.check_pid_response(p.pid):
                self.non_responded_time = 0
                continue
            
            #check if the process finished
            if p.poll() != None:
                print("NORMAL_FINISH: {0}".format(macro_filepath))
                break

            #process is not responding or finished already
            if self.non_responded_time == 0: #first time the process was not responding
                self.non_responded_time = t
                continue
            
            #terminate if program stalls
            if t - self.non_responded_time > self.maxnon_responded_time:
                p.terminate()
                print("NOT_RESPONDING: {0}".format(macro_filepath))
                break

    def check_pid_response(self, pid: int) -> bool:
        """Check if a program is responding based on its Process ID

        Args:
            pid (int): Process ID (PID) for subprocess

        Returns:
            bool: True if responding
        """
        cmd = 'tasklist /FI "PID eq %d" /FI "STATUS eq running"' % pid
        status = subprocess.Popen(cmd, stdout=subprocess.PIPE).stdout.read()
        return str(pid) in str(status)