import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import sys
import os
import subprocess
from pathlib import Path

class MyIntegrationAppService(win32serviceutil.ServiceFramework):
    _svc_name_ = 'MyIntegrationApp'
    _svc_display_name_ = 'My Integration App'
    _svc_description_ = 'A service for integrating Google Calendar, Gmail, and LinkedIn'

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.is_alive = True
        self.process = None

    def SvcStop(self):
        """Handle service stop event"""
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.is_alive = False
        if self.process:
            self.process.terminate()
            self.process.wait()
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)

    def SvcDoRun(self):
        """Run the service"""
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, '')
        )
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        self.main()

    def main(self):
        """Start the Flask server"""
        # Get the directory where this script is located
        script_dir = Path(__file__).parent
        
        # Start the Flask server
        try:
            env = os.environ.copy()
            self.process = subprocess.Popen(
                [sys.executable, str(script_dir / 'server.py')],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=str(script_dir)
            )
            
            # Wait for the process to complete
            while self.is_alive:
                if self.process.poll() is not None:
                    # Process terminated unexpectedly
                    break
                win32event.WaitForMultipleObjects(
                    (self.hWaitStop,), False, 5000
                )
                
        except Exception as e:
            servicemanager.LogErrorMsg(f'Failed to start server: {str(e)}')
            self.is_alive = False


if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.StartServiceCtrlDispatcher(
            [(MyIntegrationAppService._svc_name_, MyIntegrationAppService)]
        )
    else:
        win32serviceutil.HandleCommandLine(MyIntegrationAppService)
