from flask import current_app, _app_ctx_stack
import tasktiger


class TaskTiger(object):

    def __init__(self, redis, app=None):
        self.redis = redis
        if app:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault('TASKTIGER_ALWAYS_EAGER', app.debug)

    def _create(self):
        return tasktiger.TaskTiger(self.redis, self._config)

    @property
    def _config(self):
        return dict([(key[10:], value) for key, value in current_app.config.items() if key.startswith('TASKTIGER_')])

    def delay(self, *args, **kwargs):
        ctx = _app_ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, 'TaskTiger'):
                ctx.TaskTiger = self._create()
            return ctx.TaskTiger.delay(*args, **kwargs)
        else:
           raise RuntimeError("You need to use this from a flask app context")

    def task(self, queue=None, hard_timeout=None, unique=None, lock=None, lock_key=None, retry=None, retry_on=None, retry_method=None, batch=False):
        def _delay(func):
            def _delay_inner(*args, **kwargs):
                self.delay(func, args=args, kwargs=kwargs)
            return _delay_inner

        def _wrap(func):
            if hard_timeout is not None:
                func._task_hard_timeout = hard_timeout
            if queue is not None:
                func._task_queue = queue
            if unique is not None:
                func._task_unique = unique
            if lock is not None:
                func._task_lock = lock
            if lock_key is not None:
                func._task_lock_key = lock_key
            if retry is not None:
                func._task_retry = retry
            if retry_on is not None:
                func._task_retry_on = retry_on
            if retry_method is not None:
                func._task_retry_method = retry_method
            if batch is not None:
                func._task_batch = batch

            func.delay = _delay(func)

            return func

        return _wrap
