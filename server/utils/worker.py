from PySide6.QtCore import QRunnable, QThreadPool, QObject, Signal, Slot
import time
import sys

class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data, just emit when the processing is done
    
    error
        tuple (exctype, value, traceback.format_exc() )
    
    result
        object data returned from processing, anything
    
    progress
        int indicating % progress 
    '''
    finished = Signal()
    error = Signal(tuple)
    result = Signal(object)
    progress = Signal(int)
    canceled = Signal()

class Worker(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.
    '''

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        self._cancelled = False
    
    def cancel(self):
        self._cancelled = True

    def is_cancelled(self):
        return self._cancelled
    
    @Slot()
    def run(self):
        """
        Run the task with cancellation support.
        """
        try:
            # Inject cancellation and progress function if accepted
            if 'check_cancelled' in self.fn.__code__.co_varnames:
                self.kwargs['check_cancelled'] = self.is_cancelled
            if 'progress_callback' in self.fn.__code__.co_varnames:
                self.kwargs['progress_callback'] = self.signals.progress.emit

            result = self.fn(*self.args, **self.kwargs)

            if self._cancelled:
                self.signals.canceled.emit()
                return

            self.signals.result.emit(result)

        except:
            self.signals.error.emit(sys.exc_info())
        finally:
            self.signals.finished.emit()