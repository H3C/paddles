from pecan import expose, abort, request
from paddles.models import Run
from paddles.controllers.jobs import JobController
from paddles.controllers import error


class RunController(object):

    def __init__(self, name):
        self.name = name
        try:
            self.run = Run.filter_by(name=name).first()
        except ValueError:
            self.run = None
        request.context['run'] = self.run

    @expose('json')
    def index(self):
        if not self.run:
            error('/errors/not_found/', 'requested job resource does not exist')
        return self.run

    @expose('json')
    def _lookup(self, job_id, *remainder):
        return JobController(job_id), remainder


class RunsController(object):

    @expose(generic=True, template='json')
    def index(self):
        return Run.query.limit(10).all()

    @index.when(method='POST', template='json')
    def index_post(self):
        # save to DB here
        try:
            name = request.json.get('name')
        except ValueError:
            error('/errors/invalid/', 'could not decode JSON body')
        if not name:
            error('/errors/invalid/', "could not find required key: 'name'")
        new_run = Run(name)
        return dict()

    @expose('json')
    def _lookup(self, name, *remainder):
        return RunController(name), remainder
