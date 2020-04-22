import multiprocessing

bind = "unix:api.sock"
workers = multiprocessing.cpu_count() * 2 + 1
accesslog = '-'
loglevel = 'info'
timeout = 30
user = 0
spew = False


def log_traceback(worker):
    ## get traceback info
    import threading, sys, traceback
    id2name = {th.ident: th.name for th in threading.enumerate()}
    code = []
    for threadId, stack in sys._current_frames().items():
        code.append("\n# Thread: %s(%d)" % (id2name.get(threadId, ""),
                                            threadId))
        for filename, lineno, name, line in traceback.extract_stack(stack):
            code.append('File: "%s", line %d, in %s' % (filename,
                                                        lineno, name))
            if line:
                code.append("  %s" % (line.strip()))
    worker.log.info("\n".join(code))


def worker_int(worker):
    worker.log.info("worker received INT or QUIT signal")
    log_traceback(worker=worker)


def worker_abort(worker):
    worker.log.info("worker received SIGABRT signal")
    log_traceback(worker=worker)
